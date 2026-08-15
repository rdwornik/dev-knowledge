---
title: "Night-2 consolidated briefing — seven lanes aggregated into one adjudication input"
date: 2026-08-15
class: technical
status: DRAFT
---

# Night-2 consolidated briefing

> **BINDS NOTHING — adjudication input for the browser architect; every PROPOSED item awaits
> his ruling and the operator's GO.**

**What this is.** The seven night-2 lane reports, aggregated into one file. It is the architect's
sole morning input and is written to be read cold: no claim below depends on chat context, a prior
session, or a document not named here.

**Consolidation law applied.** AGGREGATE, never adjudicate. Competing proposals are **not**
collapsed into a conclusion, minority findings are **not** dropped, and numbers are **not**
averaged. Where two lanes disagree, both readings are in §0's contradiction ledger, verbatim-cited
with both locators.

**Every claim carries three things:** its source-lane tag `[NB2-A]`..`[NB2-G]`, the locator the
lane itself gave, and exactly one class:

| class | meaning |
|---|---|
| **VERIFIED** | the lane read it live and gave a locator. Reproduced here as the lane stated it. |
| **PROPOSED** | the lane's suggestion. The architect rules; nothing here is a ruling. |
| **UNVERIFIABLE** | so marked *by the lane*. **Never upgraded by this consolidation**, under any reading. |

**What this consolidation did NOT do.** It ran **zero fresh derivations against the live tree** —
every number, locator and verdict below is transcribed from a lane report. Where the lane set
leaves a question open, this file says so rather than settling it. It made no register, BACKLOG,
`tasks/` or manifest write; it merged no branch; it pushed nothing to `main`.

**Lane-tag map** (fixed by the consolidation brief's own ordering; four lanes also self-letter in
their titles — A, B, C and D do, E/F/G do not):

| tag | lane | branch | report |
|---|---|---|---|
| **NB2-A** | hygiene sweep | `claude/night2-hygiene-sweep-8zgyjx` | `docs/audits/2026-08-14-verification-night2-hygiene.md` |
| **NB2-B** | lane-latency | `claude/night2-latency-audit-6s1k6p` | `docs/audits/2026-08-14-technical-night2-latency.md` |
| **NB2-C** | code quality | `claude/night2-quality-audit-8a3ixh` | `docs/audits/2026-08-14-qa-night2-quality.md` |
| **NB2-D** | research | `claude/night2-research-d30vhu` | `docs/audits/2026-08-14-technical-night2-research.md` |
| **NB2-E** | plan-check | `claude/night2-plancheck-audit-6ldr94` | `docs/audits/2026-08-14-verification-night2-plancheck.md` |
| **NB2-F** | census | `claude/night2-census-audit-btqr42` | `docs/audits/2026-08-14-census-night2-census.md` |
| **NB2-G** | wave-2 drafts | `claude/night2-wave2-drafts-fmbwa4` | `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` |

**7/7 lanes present. No lane is MISSING.** All seven branches exist on `origin`, each carries
exactly one report under `docs/audits/` plus the mandated `docs/audits/README.md` index regen, and
each report was read in full. Full per-lane provenance is §5.

---

## §0 · STATE + CONTRADICTION LEDGER

### 0.1 Executive state — three lines

**GATE** `[NB2-A]` **VERIFIED** — `python scripts/audit.py ship-gate` →
`ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 45 new/undispositioned WARN(s))`
(`2026-08-14-verification-night2-hygiene.md` §1, re-derived post-`--unshallow` and re-confirmed
byte-identical under the lock-pinned `uv run --locked` toolchain in that report's
`AMENDMENT 2026-08-14`). NB2-A attributes **4 of the 45** and the **sole hard-fail organ**
(`hooks_armed`) to the cloud container, projecting **41** on the operator's host — *the operator-host
figure is measured by no lane* (§2 condition N-1).

**CENSUS** `[NB2-F]` **VERIFIED / PROPOSED** — 196 open rows (`validate_backlog.py` →
`OK (9 themes, 26 stories, 196 tasks, 1 warning)`, `2026-08-14-census-night2-census.md` §0), split
**169 proposed live · 2 proposed dead · 25 proposed awaiting-ruling** (§1 count table). The 196 and
the split-by-reading are VERIFIED; every per-id verdict is PROPOSED. **Zero closes executed** —
"this artifact **prepares** the booted architect's P10 duty ([#506]); it does not discharge it"
(§ header).

**DRAFTS** `[NB2-G]` **PROPOSED** — **30 drafts produced** — 29 needs-draft rows + the 1 `[#419]`
re-check — **0 skipped**, **4 ambiguity-flagged** (`2026-08-14-technical-w4-wave2-conversion-drafts.md`
§8). `L14 re-resolve: 30/30 verified status: open live before drafting` (§8) is VERIFIED. The drafts
themselves bind nothing: *"They apply only under a later operator ruling, after architect review and
the wave-2 GO"* (§8 closing).

### 0.2 Contradiction ledger — 18 entries

Each entry gives both readings verbatim with both locators. **None is resolved here.**

---

**X-1 · The composition of the 4 container-artifact WARNs differs between the two lanes that
counted them (same total, different members).**

- `[NB2-A]` **VERIFIED** — §1.1 by-check breakdown: `fleet_parity 3 (ALL 3 container artifacts)` and
  `deployed_methodology_version 1 (container artifact)`; §0.2 *"Four of the 45 WARNs are container
  artifacts"*. So NB2-A's four = **3 fleet_parity + 1 deployed_methodology_version**.
- `[NB2-E]` **VERIFIED** — K7: *"Exactly **4** of those are `fleet_parity` WARNs that exist only
  because of this container (pytest-xdist absent from the running interpreter, hooks unarmed, two
  fleet peers not present on disk) — none is dispositioned, so each adds 1. **45 − 4 = 41.**"* NB2-E
  then measured the attribution: *"installing `pytest-xdist` into the running interpreter mid-check
  dropped the total from 67 to 66 and `fleet_parity` from 4 to 3, exactly as the reading predicts."*
- **Both reach 41 on the operator host by different routes.** NB2-E counted a fourth `fleet_parity`
  WARN (absent pytest-xdist) that NB2-A's run did not carry; NB2-A instead counts
  `deployed_methodology_version` in the four. Which four vanish on the host is therefore unsettled
  by the lane set, and it changes which of NB2-A's §1.5 blocks are do-not-paste.

---

**X-2 · `canonical_freshness` / `VISION.md` — three incompatible readings, including two different
`last_reviewed` values for the same file.**

- `[NB2-A]` **VERIFIED (post-unshallow)** — §3.1: *"The canonical gated set is CLEAN — 0 stale."*
  Its table row reads `VISION.md 2026-07-25 == 2026-07-25 30a8c42b`, and §0.1 records the transition
  `canonical_freshness FAIL "6 stale (edited since review)" -> OK (9 canonical files fresh)` after
  `git fetch --unshallow` (318 → 5043 commits). §3.1 adds: *"(The 6-file FAIL a reader may recall
  from a shallow run is the §0.1 artifact. It is not real.)"*
- `[NB2-B]` **VERIFIED (claimed non-container)** — §1c item 12:
  *"`test_audit::test_audit_run_passes_structural_checks_on_synthetic_repo` | **live doc staleness** |
  `canonical_freshness`: `VISION.md` `last_reviewed 2026-06-02` predates last edit `2026-08-09`"*,
  and §5 item 5: *"One non-container defect surfaced in passing: `VISION.md`'s `last_reviewed`
  (2026-06-02) predates its last edit (2026-08-09) — §1c item 12. Reported, not fixed."*
- `[NB2-D]` **UNVERIFIABLE (explicitly)** — `AMENDMENT 2026-08-14` A1: *"the `canonical_freshness`
  characterisation above is **WRONG**. It calls that FAIL 'live repo state predating this lane'. It
  is a **shallow-clone artifact** … **Honest limit: this establishes that the container cannot answer
  the question, NOT that the six stamps are fine** — the real last-edit dates need a full clone. Do
  not read this amendment as a clean bill for those six files."*
- `[NB2-E]` **VERIFIED (as artifact)** — §0(1): *"`canonical_freshness: 6 stale`. The last one is
  **also** a shallow artifact, proven: all six files report their 'last edit' as the *same* commit
  `4bef950`, which has no parent in this clone."*
- **The hard conflict is numeric:** NB2-A read `VISION.md last_reviewed` as **2026-07-25** on a
  full-history clone; NB2-B read it as **2026-06-02**. Both are stated as live reads. NB2-D refuses
  to clear the six either way.

---

**X-3 · Suite outcome: measured 14 failures vs. an arithmetic baseline of 1.**

- `[NB2-B]` **VERIFIED (executed twice)** — §1: *"Outcome | **14 failed · 2874 passed · 8 skipped ·
  1 xfailed**"*, identical in the `-n 0` and `-n auto` arms (§2 table). §1c classifies all 14 as
  container artifacts: *"**7 langserver/oracle · 4 lone-clone (no sibling repos, hooks unarmed) ·
  2 live-state · 1 timing.**"*
- `[NB2-E]` **VERIFIED-by-arithmetic, suite not run** — K9: *"suite **2891 pass / 1 owned RED
  (`[#457]` leg ii)** | **OK (by arithmetic; suite not executed here)** … Arithmetic reconciles
  exactly against the live collection: 2891 pass + 1 fail + 4 skipped + 1 xfailed = **2897** = live
  `--collect-only`."*
- Both denominators are 2897. The pass/skip/fail split differs (2874/8/14 vs 2891/4/1). NB2-B's is a
  real run on a container; NB2-E's is the plan's claimed operator-host baseline checked for internal
  consistency, not executed.

---

**X-4 · Test-file population: 105 files vs 132 files, against the same 2897 collected items.**

- `[NB2-B]` **VERIFIED** — §0 environment table: `Collected | **2897 tests** in 105 files`; §1b:
  *"By file — 10 of 105 files carry 89 % of the cost … | **remaining 95 files** | **76.80** |"*.
- `[NB2-C]` **VERIFIED** — §5: *"**Population:** 132 test files · **2,593** `def test*` functions
  (AST) · **2,897** collected items (`pytest --collect-only -q -n 0`; the difference is
  parametrization expanding)."*
- Neither lane reconciles the file count against the other. Any per-file metric the telemetry lane
  computes inherits this ambiguity.

---

**X-5 · `[#502]`'s block on `[#501]` — asserted live by the census, discharged by two other lanes.**

- `[NB2-F]` **VERIFIED (as row text)** — §9 appendix row: *"| [#502] | mutmut 3.7.0
  mutation-testing evaluation — CI-hosted | P3/M | 2026-08-06 | 12 · 781bd4ff (2026-08-13) | live |
  **BLOCKED ON [#501]**; the `uv run --locked` question unanswered, no CI pilot run |"*
- `[NB2-E]` **VERIFIED (as defect)** — A8: *"`tasks/502-*.md:13` still reads *'this is **BLOCKED ON
  [#501]** — until that wall exists there is nowhere to host the eval'*.
  `tasks/501-server-side-report-only-recorder-github-actions.md` is `status: closed`. The block is
  discharged; the row does not say so."* A9 adds the second locator: *"The census row for `#502`
  carries `Y` in the blocked column, citing `[#501]`."* F-7: *"`[#502]` is no longer blocked, and two
  artifacts still say it is."*
- `[NB2-G]` **VERIFIED (independently)** — §5.4: *"`[#501]` is **`status: closed`**, and the wall is
  live at `.github/workflows/report-only-wall.yml` (16,640 bytes; it already runs `uv sync --locked
  --group analytics`). The host the row was waiting for now exists."*

---

**X-6 · `[#417]` — the Done-when appears already met in live code, yet it is scheduled as a wave-2
conversion.**

- `[NB2-G]` **VERIFIED** — §5.3: *"Live, `check_dirty_tree` at
  `scripts/session_end_backpressure.py:412` filters that output through `_is_lane_owned_daily`
  (line 402), which excludes exactly the untracked `ecosystem/*/history/*.md` dailies the row names
  — and the test leg exists too, in both directions: `tests/test_session_end_backpressure.py:758`
  `test_lane_owned_daily_present_on_the_lane_does_not_flag`, with siblings at 770/779/794 … Landed
  via `4bef950`."* NB2-G names the fork explicitly and **proposes neither branch**.
- `[NB2-E]` **VERIFIED (as open conversion target)** — §9 roster: *"| #417 | P3 | S | settings-json |
  W4c | leg 1 testable; 'recorded rejected with a reason' has no home |"*, and §11 assigns `#417` to
  lane **W2-f**.
- `[NB2-F]` lists `#417` inside the 196 open set (§0 derivation; the row is `status: open`).
- If the clause is discharged, W2-f is a 4-id lane converting a row that should instead be a closure
  proposal.

---

**X-7 · Whether the ADR-106-pinned `uv==0.11.19` is obtainable in a cloud container — three lanes
refuted it after two lanes had already caveated their work on it.**

- `[NB2-A]` **VERIFIED, self-corrected** — `AMENDMENT 2026-08-14`: *"§0.3 was **WRONG** on one point,
  and it was the caveat attached to every number in this report … **uv 0.11.19 is published on PyPI
  and installs cleanly** (`pip install uv==0.11.19`)."* Consequence: *"§0.3's toolchain caveat is
  **withdrawn**."*
- `[NB2-B]` **VERIFIED** — §0 environment table: `uv | **0.11.19** — the exact `[tool.uv]
  required-version` pin`; §0 toolchain note: *"uv 0.11.19 was installed into a scratch venv
  **outside** the repo and used from there."*
- `[NB2-D]` **VERIFIED, self-corrected** — `AMENDMENT 2026-08-14` A2, run *"when the container's uv
  was brought to the pinned `0.11.19` and the real toolchain became runnable."*
- `[NB2-C]` **states it unavailable** — header: *"`uv` present at 0.8.17, which does **not** satisfy
  `[tool.uv] required-version = "==0.11.19"`, so `uv sync --locked` was unavailable and the audit's
  own tooling deps were installed with plain `pip` into the container."*
- `[NB2-E]` **states it unavailable** — §0: *"The **full test suite was NOT executed** (deps
  unavailable; `uv` is version-pinned to 0.11.19 and this box has 0.8.17)."*
- NB2-C's and NB2-E's stated blockers are refuted by three lanes. Neither lane re-ran under the pin;
  NB2-A did and reported *"nothing moved"*.

---

**X-8 · `audit.py health` FAIL count differs 1 / 1 / 2 / 4 / 4 across the five lanes that ran it.**

- `[NB2-A]` **VERIFIED** — §1: `1 hard-fail organ(s)`, post-unshallow; §0.2 names it: the
  `hooks_armed` hard FAIL, container-caused.
- `[NB2-B]` **VERIFIED** — §6: *"**One `audit.py health` FAIL persists and is not mine to fix:**
  `[!!] repos registered (none)`"* — measured after this lane ran `pre-commit install` and
  `git fetch --unshallow`.
- `[NB2-C]` **VERIFIED** — method notes: *"`health` reports **DEGRADED** (exit 1) in this container,
  from two `[!!]` operational items — `repos registered (none)` … and `hooks_armed`"*, with
  *"72 WARNs baseline vs 71 with this lane's two files applied."*
- `[NB2-D]` **VERIFIED** — §4.6: *"`audit.py health` → `DEGRADED`, exit 1 … **4 FAILs both sides**"*:
  `repos registered (none)`, `hooks_armed`, `journal_spine_anchor`, `canonical_freshness`.
- `[NB2-E]` **VERIFIED** — §0(1): *"`audit.py health` reports `DEGRADED` here with **4 FAILs**, all
  environment-attributable"* — the same four as NB2-D; and the post-check control at §0:
  *"**66 WARN / 4 FAIL**"*.
- Each lane discloses its own container state (shallow vs unshallowed, hooks armed vs not), so the
  divergence has stated causes — but **no lane reports the number the operator's host produces**,
  which is the number every gate ruling depends on.

---

**X-9 · P7's `[stale]` disposition count — 5, self-caveated to possibly 0, re-derived by no lane.**

- `[NB2-E]` **VERIFIED then self-caveated** — K8: *"Live: **5 `[stale]` dispositions** —
  `warn-no-ff-3a894eeb5-journal-wrap`, `warn-no-ff-d0f9ead67-transcript-archive`,
  `warn-no-ff-533109f-journal-wrap`, `warn-review-artifact-lane-c-504-no-tally`,
  `warn-git-backlog-drift-505-zero-closed`. **Caveat: all five are the shallow-clone artifact of
  §0(2)** … On a full clone the count may be 0. The point stands that the plan states a P7 baseline
  while dropping the leg P7 explicitly asks for; the incoming seat must re-derive it, not inherit
  it."* NB2-E's own finding F-8 restates it: *"noted rather than argued, since this environment
  cannot settle the live value."*
- `[NB2-A]` ran the same gate on a **full-history, lock-pinned** tree and reports no `[stale]` count
  at all — its §1 inventory is of the 45 undispositioned WARNs, not of stale dispositions.
- The one lane positioned to settle it did not report it; the one lane that reported it says its
  own number is probably an artifact.

---

**X-10 · The plan states two different wave-2 widths for one operator decision.**

`[NB2-E]` **VERIFIED** — M1, verdict **STALE (self-inconsistent)**: *"§2 EXPANDED says *'Run wave-2
at **6–10** lanes'*; §7 EXPANDED says *'wave-2 width GO (recommend **6–8** + draft-production lane
first)'*. Two numbers for one operator decision, and it is left unstated whether the
draft-production lane counts **inside** the number or is additional. The operator is being asked to
say 'GO' to an ambiguous quantity."* Both locators are inside
`docs/handoffs/2026-08-14-dev-knowledge-architect/SUPPLEMENT.md`.

---

**X-11 · "Dispatch WITHOUT a planning phase" and "P10 grooming is the boot duty" cannot both hold.**

`[NB2-E]` **VERIFIED** — M2, verdict **STALE (mutually exclusive as written)**: *"§1 EXPANDED
prescribes *'Boot → gate → then dispatch WITHOUT a planning phase'*. §7 EXPANDED, in the same
addendum, says *'**P10 full grooming census is the incoming seat's boot duty per the process's own
text**'* — and `PROBES.md` P10 requires that **every** open row (196 of them) be verdicted live /
dead / awaiting-ruling at boot, *'no open `#id` may pass unreconciled'*. A 196-row grooming pass
**is** a planning phase. One of the two instructions must give; the addendum does not say which."*
NB2-E §10 leaves it **FLAGGED, unresolvable from the tree**: *"The seat must pick, and say which, in
its first JOURNAL entry."*

**Material to this fork, not a resolution of it:** `[NB2-F]` performed the 196-row read in advance —
*"read all 196 open rows end to end, and proposes a verdict per id so ratification can happen in
batches rather than per-id"* (§ header). That changes the *cost* of the P10 duty; it does not
discharge it (§ header: *"it does not discharge it"*).

---

**X-12 · The plan's first dispatch depends on a file that does not exist.**

`[NB2-E]` **VERIFIED** — A2, verdict **MISSING**, on the plan phrase *"and its on-main twin"*:
*"No such file in the working tree, in `git ls-files`, or in **any** commit reachable in history
(`git log --all --diff-filter=A --name-only` → zero hits for `wave2`). `JOURNAL.md:123` states the
opposite in the same breath that created it: step (8) *'compiled the W4 wave-2 skipped-id input
(29 needs-draft, 1 re-check) to `~/Downloads/W4-WAVE2-INPUT.md` **(Downloads-only, no repo
change)**'*."* Finding F-1 adds the recovery: *"the 30 ids are fully re-derivable on main from the
four W4a–d lane JOURNAL entries"*.

`[NB2-G]` **VERIFIED, independently** — §1: *"The operator-side input file
(`~/Downloads/W4-WAVE2-INPUT.md`) is Downloads-only and has no on-main twin: JOURNAL 2026-08-14 (d)
step 8 records it as *'Downloads-only, no repo change'*. The set was therefore **re-derived from the
in-repo record** rather than taken on faith."* The two lanes' reconstructed id sets are identical —
see §4's disjointness proof.

---

**X-13 · "Row-is-the-spec" for telemetry points at an intake; there is no telemetry row.**

`[NB2-E]` **VERIFIED** — B5, verdict **MISSING**: *"**There is no telemetry BACKLOG row.**
`grep -i telemetry BACKLOG.md` returns exactly one hit — `[#528]`, which *consumes* the leg (its
leg 3), it does not own it. `grep -rl -i telemetry tasks/*.md` returns only `tasks/528-*.md`. The
leg's own text forecloses the reading: *'**Zero births by this leg** …'*. The owner is an
**intake**, not a row; 'row-is-the-spec' has no row."* Finding F-2 states the mechanical
consequence: *"the dispatch template in §4 EXPANDED is `[dk · #<id> · <label>]`, and the
`backlog-filing-backpressure` commit-msg gate requires a `kill-candidates:` line on any commit that
**adds** a new id — so the row must be born deliberately at boot, not improvised inside a lane that
has already started."*

`[NB2-F]` is consistent: the 196-row census contains no telemetry row; `[#528]`'s appendix reason
reads *"born 2026-08-14; gate-run call sites, the tiered-suite rule and the telemetry leg all
unlanded"*.

---

**X-14 · The four LESSONS promotion candidates are correctly counted and wrongly named.**

`[NB2-E]` **VERIFIED** — G2, verdict **STALE**: *"The four that landed are: (1)
**duplicate-execution** …; (2) **unlocated register loads** …; (3) **doc_rot dual-instrument** …;
(4) **serialize-group derivation** …. **None** of the four subjects the plan names appears in any
2026-08-14 `LESSONS.md` entry (`grep -i "powershell\|dispatch.block\|repin guard"` over
`LESSONS.md` → newest hit 2026-06-26). Count OK, subjects wrong."* G1 confirms the count is right:
*"Commit `eac92922`, four entries appended to `LESSONS.md`, each ending *'CANDIDATE for PLAYBOOK
promotion — not promoted this window'*."* Finding F-6: *"A seat that takes the plan's list to an
adjudication beat will promote from a list that does not exist."*

---

**X-15 · The satellite-serving lane is due THIS window, not "this window or next".**

`[NB2-E]` **VERIFIED** — F3, verdict **STALE**: *"The deadline was set in the 2026-08-12 window.
Window 1 = the seat booted from the `2026-08-12-dev-knowledge-architect` bundle … Window 2 = the
**incoming** seat … So `≤2 windows` expires **at the end of the incoming window** — it is due *this*
window, full stop. 'or next' grants a third window the ruling does not."* Anchors: F2 **OK** —
`docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:25` and `:17`, register
`protocols/STANDING_RULINGS.md:1583` `N2-E1-4` **CARRY**. F1 **OK** —
`tasks/293-consumer-runbook-fan-out.md`, *"**UN-DEFERRED 2026-08-09 (ARC-2)**: 'work NOT done (0 of 6
consumers seeded)'"*.

---

**X-16 · The 2026-08-17 `[#492]` beat: a browser check, not a corpus run.**

- `[NB2-E]` **VERIFIED** — D5, verdict **STALE**: *"The row's peg is not the corpus: *'DEFER — peg:
  **the Grok 4.6 release ALONE — the calendar leg is SPENT and dropped**; release is an external
  fact, OPERATOR (N1 R-5)'*. 2026-08-17 is a **dated re-check of the release fact**, and the corpus
  reconciliation *'closes the corpus-currency leg only'*. Intake #29 Fold A additionally rules
  *'no bake-off runs before the seeded-defect corpus exists'*."* F-4: *"If 4.6 is unreleased on
  08-17, the whole act is: check, record, move on. **Do not budget a lane.**"*
- `[NB2-F]` **VERIFIED, concurring** — §7c: *"| **2026-08-17** (3 days) | [#492] | dated re-check of
  Grok 4.6's release — *not a new peg*, register `I-D` item 1 |"*.
- The plan's phrasing (*"Grok re-check on the reconciled corpus"*) is the reading both lanes refuse.

---

**X-17 · `[#528]` is ordered before the item it depends on.**

`[NB2-E]` **VERIFIED** — C5, verdict **STALE**: *"The plan's parenthetical describes **two** of three
legs. Leg (3) is *'emit `test_run` duration via the 2026-08-14 telemetry leg (intake #29 Fold A)'*,
and the row's Done-when requires **all three** with evidence. So item (3) cannot close before item
(2) ships — the plan's own ordering puts the dependency after the dependent."* Finding F-3 proposes
the split; see D4.2.

`[NB2-B]` **VERIFIED, corroborating the leg-3 gap** — §4b: *"test-run cost inside a lane |
**UNVERIFIABLE** | no `test_run` duration is emitted anywhere; §1–§3 had to re-measure from
scratch."*

---

**X-18 · The telemetry leg's internal pointer names a file that is not tracked.**

`[NB2-E]` **VERIFIED** — B6, verdict **STALE**: *"No file of that name is tracked
(`git ls-files | grep -i ROADMAP-2026` → empty). The on-repo carrier is
`docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md`, whose line 25 is the '≤2 windows'
line the plan relies on elsewhere. A lane told 'row-is-the-spec' and handed this leg will chase a
path that does not exist."*

---

### 0.3 COLLISIONS — recorded here so they are not lost

Not contradictions (no lane disagrees with another), but cross-lane couplings where **ratifying two
proposals independently produces a defect neither lane could see alone.**

**Y-1 · A register entry would reference a row the census proposes closing.**
`[NB2-A]` §1.5 proposes `id: warn-journal-spine-anchored-by-mention` with `ref: "[#524] leg c"` —
its **only** clean disposition candidate on the merits (§1.4: *"Only 1 of the 45 is a clean
disposition candidate"*). `[NB2-F]` §2 group D1 proposes **`[#524]` DEAD** (already-shipped, all four
legs landed at `62f42dad`). Ratifying both leaves a live register entry pointing at a closed row.

**Y-2 · The proposed threshold re-calibration would discharge the premise of a wave-2 draft.**
`[NB2-A]` §1.3 proposes *"re-calibrate `_BACKLOG_GROSS_CHARS` in `scripts/validate_doc_rot.py` from
1200 to a value derived from the post-conversion distribution (p90 ≈ 1320 or p95 ≈ 1675)"*.
`[NB2-G]` §5.1 drafts `[#364]` against a **live-firing** `[#353]`: *"`[#353]` is **1266 chars and
already tripping the gate**"*. Both lanes measure `[#353]` at **1266 chars** (NB2-A's block
`warn-doc-rot-backlog-accretion-353`: *"Gross-length branch: 1266 chars, 2 dated block(s)"*), so at
a 1320 threshold `[#353]` stops firing and `[#364]`'s Done-when is satisfied without any build.

**Y-3 · Two of NB2-A's eleven DRAIN targets are also wave-2 / execution-lane subjects — a
`tasks/` file-ownership collision with the disjointness law.**
`[NB2-A]` §1.3 names the 11 drain rows: *"`#511 #522 #505 #510 #419 #492 #528 #426 #322 #278 #387`"*,
each fixed *"at the SOURCE: `tasks/<id>-*.md` body, then `python scripts/gen_task_tree.py
--emit-source`"*. Of those, **`[#419]`** is assigned to conversion lane **W2-a** by `[NB2-E]` §11 and
carries a full replacement draft from `[NB2-G]` §5 (*"this supersedes the census's `[#419]` draft"*);
**`[#528]`** is the execution row for the xdist/tiered-suite/telemetry legs; **`[#492]`** is the
2026-08-17 checkpoint. Three files would be written by two different owners under §4's disjointness
proof.

---

## §1 · DECISION QUEUE

The architect's morning rulings, ordered. Each is a **bounded pick with its evidence attached**.
**37 decisions are queued** (D1 ×7 · D2 ×7 · D3 ×5 · D4 ×9 · D5 ×3 · D6 ×6).

---

### D1 · WARN disposition batch — `[NB2-A]`, deduplicated, grouped by check

**Dedup status.** `[NB2-A]` **VERIFIED** (§1.5): the 45 proposals are *"Machine-validated: all 45
parse as YAML, carry every required key, have unique ids, and **each `match` is a verified substring
of exactly one live WARN's evidence** — 45/45 coverage, zero over-matching."* This consolidation
found **no duplicate within the 45 and no competing register proposal from any other lane** — NB2-A
is the sole lane proposing register entries.

**Extraction method** `[NB2-A]` **VERIFIED** (§1): *"The 45 were extracted by re-using the gate's own
`_load_dispositions()` / `_match_disposition()` rather than by parsing its stdout, so this inventory
is the gate's set, not a lookalike."*

#### By check — the whole 45

```
doc_rot                        38   (37 backlog-accretion rows + 1 CLAUDE.md file-budget)
fleet_parity                    3   (ALL 3 container artifacts)
doc_claims                      1   (the P6 drift — same defect, two surfaces)
deployed_methodology_version    1   (container artifact)
journal_spine_anchor            1   (advisory-by-design, 401 commits)
review_artifact_coverage        1   (one unreviewed code-impact merge)
                               --
                               45
```
— `[NB2-A]` §1.1, **VERIFIED**.

**Owner rows** `[NB2-A]` **VERIFIED** (§1.2): only 3 of 45 have an owning BACKLOG row —
`[#524] leg c` → `journal_spine_anchor`; `[#480] P3` → `review_artifact_coverage`; `#222` →
`doc_claims pytest_collected`. *"42 of 45 WARNs have no ticket carrying them."*

---

**D1.1 — `doc_rot` / gross-length: 26 rows, ONE decision, not 26 entries. PROPOSED.**

The 26 ids `[NB2-A]` §1.5 marks `THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other
25)`:

```
#112 #277 #338 #341 #344 #353 #356 #362 #371 #399 #408 #414 #415
#418 #423 #425 #428 #430 #453 #456 #464 #487 #506 #514 #523 #527
```

Evidence `[NB2-A]` §1.3, **VERIFIED**:

```
BACKLOG.md rows                       196
rows carrying a `Done when:` clause   196  (100% — the conversion wave is complete)
median row length                    1120 chars
p75                                  1195 chars
p80                                  1199 chars
p81                                  1200 chars   <-- the threshold sits HERE
p90                                  1318 chars
rows over 1200                         37  (19%)
threshold / median                   1.07x
```

*"The threshold fires above **p81** of the tree's own normal shape. It is not detecting outliers; it
is detecting the top fifth of an ordinary distribution."* Cause, **VERIFIED**: *"the W4a/W4b/W4c/W4d
**Done-when conversion wave** (2026-08-13, `a4fc652d`, `8a091278`) rewrote rows to carry explicit
Done-when clauses, lengthening them — and 10 of the 26 gross-length rows (`#112 #277 #278 #338 #341
#344 #353 #356 #362 #371`) are literally the ids those two lanes converted."*

**The pick, PROPOSED** `[NB2-A]` §1.3: *"re-calibrate `_BACKLOG_GROSS_CHARS` in
`scripts/validate_doc_rot.py` from 1200 to a value derived from the post-conversion distribution
(p90 ≈ 1320 or p95 ≈ 1675), as **one** data change — instead of writing 26 register entries that
would each be a paper suppression of a normal row."* **See collision Y-2.**

---

**D1.2 — `doc_rot` / history-accretion: 11 rows, DRAIN at source. PROPOSED.**

`#511 #522 #505 #510 #419 #492 #528 #426 #322 #278 #387` — `[NB2-A]` §1.3, **VERIFIED** as
*"genuine history-accretion (≥3 dated blocks)"*. The doctrine cited is the register's own, quoted
from the retired `#492` entry: *"self-induced bloat gets drained rather than dispositioned."*

**Fix site, VERIFIED and load-bearing** `[NB2-A]` §1.3: *"**Note the correct fix site:** `BACKLOG.md`
is **generated**; draining a row means editing `tasks/<id>-*.md` and regenerating with
`python scripts/gen_task_tree.py --emit-source`. Editing BACKLOG.md directly would be overwritten."*

Per-row dated-block counts (from the §1.5 blocks, **VERIFIED**): `#511` 7 blocks/3006 chars ·
`#492` 7/1807 · `#522` 5/2685 · `#505` 5/2303 · `#426` 4/1681 · `#510` 3/2146 · `#419` 3/1908 ·
`#528` 3/1741 · `#322` 3/1675 · `#278` 3/1374 · `#387` 3/1336.

Each block's escape clause, **PROPOSED**: *"Disposition ONLY if a dated block is a ruled peg the next
seat needs."* **See collision Y-3 — `#419`, `#528` and `#492` collide with execution lanes.**

---

**D1.3 — `doc_rot` / file-budget on `CLAUDE.md`: 1 row, TRIM. PROPOSED.**

`[NB2-A]` §1.5 block `warn-doc-rot-claude-md-size`, `match: "file-budget CLAUDE.md#size"`,
`ref: "ADR-53"`, **VERIFIED**: *"CLAUDE.md is 203 counted lines (comment-only machine lines already
excluded) against its own declared <=200 budget (ADR-53, stated in the file's own header)."*
**PROPOSED:** *"Three lines over is a trim, not a disposition: condense the oldest CLAUDE.md
section-history bullet per the v2.49 precedent (ADR-49/65 info-preserving condense; git retains the
text)."* Corroborated by `[NB2-E]` K6 **VERIFIED**: *"1 `file-budget` on `CLAUDE.md#size`, 203 lines
vs self-declared 200."*

---

**D1.4 — `doc_claims`: 1 row, REGEN. One command, zero judgement. PROPOSED.**

`[NB2-A]` §2, **VERIFIED, both sides re-derived**:

```
ecosystem/doc-counts.md claims       "tests: **2895 collected**"
live `pytest --collect-only -q`       2897 tests collected in 3.31s
drift                                 -2 (doc understates by 2)
```

*"`python scripts/gen_doc_counts.py --check` confirms independently: `mismatch pytest_collected
(file 2895 / actual 2897)`."* The other two claims in the same fragment are in sync —
`audit_check_count` 43/43 and `precommit_hook_count` 18/18.

**PROPOSED:** `python scripts/gen_doc_counts.py --write`. *"it clears both this item and WARN #1 of
§1 (they are one defect surfacing on two organs)."* Cost note, **VERIFIED**: *"`doc-counts.md`
deliberately carries **no** `last_reviewed` frontmatter and is deliberately outside
`_FRESHNESS_FILES`, so this regen forces **no** re-stamp on any freshness-gated document."*

Independently confirmed by `[NB2-E]` K10 **VERIFIED** (*"Delta = 2, exactly as stated"*) and
`[NB2-C]` §3 (*"43 registered checks"*, matching the in-sync `audit_check_count`).

---

**D1.5 — Container artifacts: 4 rows, DO NOT PASTE. PROPOSED (and see X-1 on which four).**

`[NB2-A]` §0.2, **VERIFIED-as-environment**: *"a register entry keyed to a container-only signature
would match nothing on the operator's host and decorate stale on its first run (ADR-75), which is
precisely the paper-suppression rot the register forbids."*

| proposed id | organ | match | NB2-A's reason (abridged, verbatim key clause) |
|---|---|---|---|
| `warn-deployed-version-dev-knowledge` | `deployed_methodology_version` | `dev-knowledge not listed in deployed-versions.yaml` | *"the check keys on the repo-ROOT directory basename; this container cloned the repo to `/home/user/dev-knowledge`, while `ecosystem/deployed-versions.yaml` keys the hub as `.dev-knowledge`"* |
| `warn-fleet-parity-hooks-armed` | `fleet_parity` | `.dev-knowledge hooks-armed WARN-undeclared` | *"this fresh container never ran the SessionStart `arm_hooks.py` self-arm … Also the source of the paired `hooks_armed` HARD FAIL in this run. Clears with `pre-commit install -t pre-commit -t commit-msg -t pre-push`."* |
| `warn-fleet-parity-ai-council-unresolved` | `fleet_parity` | `ai-council fleet-membership unavailable` | *"the sibling repo `ai-council` is not present in this cloud container … Re-derive on the operator host."* |
| `warn-fleet-parity-corp-monorepo-unresolved` | `fleet_parity` | `corp-monorepo fleet-membership unavailable` | *"the sibling repo `corp-monorepo` is not present … Re-derive on the operator host."* |

---

**D1.6 — `journal_spine_anchor`: 1 row. The only clean disposition on the merits. PROPOSED.**

`[NB2-A]` §1.5 `warn-journal-spine-anchored-by-mention`, `match: "anchored by mention, not by
record"`, `ref: "[#524] leg c"`, `review_date: 2026-11-14`, **VERIFIED**: *"It currently names **401
commits** (5 listed + 396 more) — the accumulated history of a convention adopted AFTER most of those
entries were written, and `JOURNAL.md` is append-only (CLAUDE.md §5 rule 2), so the backlog of 401
cannot be retro-fixed without the edit the append-only rule forbids. **The HARD leg
(`block_unanchored_push`) is unaffected — it passes**; this is the softer record-shape advisory."*
**PROPOSED:** *"Disposition the historical mass; the convention holds going forward."*
**See collision Y-1.**

---

**D1.7 — `review_artifact_coverage`: 1 row. OPERATOR CALL. PROPOSED (two routes, neither chosen).**

`[NB2-A]` §1.5 `warn-review-artifact-387b794a-repin-close`, `match: "387b794a
integrator/513-repin-close"`, `ref: "[#480] P3"`, **VERIFIED**: *"One code-impact merge since
2026-08-05 carries no linked review artifact … Advisory per the `[#480]` P3 ruling (the hard pre-push
leg is deferred pending 0 false positives over two windows)."* **The two routes, PROPOSED, explicitly
unresolved:** *"perform the retroactive review and land the artifact (the route the sibling WARNs in
this class took), or disposition it as a mechanical re-pin whose diff is a line-number bump. **A
sweep cannot rule which.**"*

---

#### D1 count line — does ruling this batch take the gate RED → GREEN?

**NO — not from register entries alone.** Three reasons, all from lane evidence:

1. **The RED has a second cause the register cannot touch.** `[NB2-A]` §1 **VERIFIED**:
   `1 hard-fail organ(s)` alongside the 45 WARNs; §0.2 identifies it as `hooks_armed`, a container
   artifact. A disposition entry suppresses a WARN; it does not clear a hard FAIL.
2. **Only 1 of the 45 is a disposition on the merits.** `[NB2-A]` §1.4 verdict census, **VERIFIED**:

```
THRESHOLD RE-CALIBRATION (one decision, not 26 entries)   26
DRAIN at tasks/ source, then regenerate                   11
NOT A REPO DEFECT — container artifact, do not paste       4
DISPOSITION (advisory-by-design, unfixable in bulk)        1   journal_spine_anchor
FIX — regen, one command                                   1   doc_claims pytest count
FIX — trim 3 lines                                         1   CLAUDE.md file-budget
OPERATOR CALL — retro-review or disposition                1   review_artifact_coverage
                                                          --
                                                          45
```

   NB2-A's own words: *"**Only 1 of the 45 is a clean disposition candidate on the merits.** …
   Dispositioning all 45 would convert one threshold defect and one regen into 45 permanent
   suppressions."*
3. **The gate has not been measured on the operator's host by any lane.** X-1 and X-8.

**What remains after the batch** — `[NB2-A]` §7, **VERIFIED as its own summary**:

```
one command, zero judgement   python scripts/gen_doc_counts.py --write            (clears 2 WARNs)
one data change               _BACKLOG_GROSS_CHARS 1200 -> ~1320                  (clears 26 WARNs)
one trim                      CLAUDE.md 203 -> <=200 lines, condense oldest §12    (clears 1 WARN)
source-edit + regen           drain 11 history-accreted tasks/ bodies              (clears 11 WARNs)
one register entry            journal_spine_anchor mention-not-record              (clears 1 WARN)
operator call                 review_artifact_coverage 387b794a                    (clears 1 WARN)
re-derive on operator host    4 container artifacts                                (expected to vanish)
```

Plus the hard-fail organ, plus X-2's unresolved `canonical_freshness` question. NB2-A's headline,
**VERIFIED as its own reading**: *"The gate is not RED because 45 things are wrong; it is RED because
two derived surfaces drifted and one threshold no longer fits the tree it measures."*

---

#### D1 addenda — NB2-A findings that are NOT in the 45 and need no register entry

- **PLAYBOOK describes a RETIRED GitHub Action in the present tense, at two sites.** `[NB2-A]` §5.2a
  **VERIFIED**: `protocols/PLAYBOOK.md:2269` and `:2305` both name
  `.github/workflows/nightly-conformance-triage.yml`, *"deleted at `82227f08`"*; *"Both
  `ARCHITECTURE.md:877` and `CONTRIBUTING.md:141` correctly record the retirement — **PLAYBOOK is
  the one surface that was not updated.**"* **PROPOSED:** mark both sites retired-at-`82227f08`
  rather than deleting them, *"so the shallow-clone guard rationale at L2305 — which is still true
  and was load-bearing for §0.1 of this very report — survives the correction."*
- **An illustrative example shaped like a live locator.** `[NB2-A]` §5.2b **VERIFIED**:
  `protocols/PLAYBOOK.md:3517` cites `docs/audits/2026-04-22-codex-handoff-process-rewrite.md`;
  *"No such audit exists."* **PROPOSED:** repoint it or prefix it *"Example (illustrative, not a real
  file):"*.
- **`docs/handoffs/` has no index, and that is the finding.** `[NB2-A]` §6.2 **VERIFIED**: 108
  bundles + 15 archived = **123**, *"the largest bundle count in the tree"*, with no generator and no
  freshness hook, while the other four sanctioned `docs/` genres all have one. *"the only way to find
  the current bundle is to run code."* **PROPOSED, with NB2-A's own caveat:** *"this is the one §6
  proposal that is a **build**, not a repair … would need a row before anyone acts on it. **This
  sweep filed no row**."*
- **No action, deliberately** `[NB2-A]` **VERIFIED**: 19 stale `last_reviewed` stamps, *"all in
  IMMUTABLE handoff bundles — stale by construction, not by neglect"* (§3.2 — *"**Proposed one-line
  fix: NONE — do not touch these.**"*); 48 dangling `[#id]` provenance citations (§4.3 —
  *"**do not 'repair' these**; rewriting a historical citation destroys the traceability it exists to
  provide."*); 3 template files carrying the literal `<YYYY-MM-DD>` placeholder (§3.3).
- **`[#529]`/`[#530]` CONFIRMED FREE.** `[NB2-A]` §4.1 **VERIFIED** (*"free, unallocated, no
  residue"*, highest allocated id 528) and `[NB2-E]` J1 **VERIFIED**, independently.
- **`protocols/PLAYBOOK.md` is in no freshness gate** — `[NB2-A]` §3.5 **VERIFIED**: 4554 lines, no
  `last_reviewed`, *"`audit.py`'s own comment records this as a knowing deferral"*. NB2-A ties it to
  the two dead pointers above: *"which is what an ungated doc looks like after time passes."*
  (`[#285]` is the wave-2 row that converts this — see D6 and §4 lane W2-b.)

---

### D2 · P10 census ratification — `[NB2-F]`

**Standing** `[NB2-F]` header, **VERIFIED**: *"**DRAFT · PROPOSED VERDICTS ONLY · ZERO CLOSES
EXECUTED.** … No `tasks/` file, no `manifest.json` node, and no `BACKLOG.md` row was touched by this
lane."*

**Derivation** `[NB2-F]` §0, **VERIFIED**: *"`python scripts/validate_backlog.py` →
`OK (9 themes, 26 stories, 196 tasks, 1 warning)`. The 196 are the `"task"` nodes in
`tasks/manifest.json` — the ADR-107 source of truth — not a parse of the generated `BACKLOG.md`.
Cross-check: 262 `tasks/*.md` files on disk, 196 referenced by the manifest, 66 orphaned … Zero
manifest nodes point at a missing file."*

| verdict | n | share |
|---|---|---|
| proposed **live** | 169 | 86.2% |
| proposed **dead** | 2 | 1.0% |
| proposed **awaiting-ruling** | 25 | 12.8% |
| **total** | **196** | 100% |

`[NB2-F]` §1's own reading, **VERIFIED as the lane's**: *"The grooming lever here is not deletion; it
is §4 — a quarter-day of rulings unblocks 25 rows, which is a larger change to the workable set than
any close batch available."*

---

**D2.1 — Ratify the proposed-dead set (batch-ratifiable: 2 rows, ONE close-reason class). PROPOSED.**

**Group D1 — already-shipped (2 rows).** `[NB2-F]` §2, **VERIFIED**: *"Both are **already-shipped**
under ADR-65 — the artifact the row asks for exists on `main` today and the row was simply never
closed."*

**`[#524]` · P2/S · four ruled check extensions** — per-leg landing evidence, **VERIFIED**:

| leg | Done-when clause | landed at |
|---|---|---|
| (a) | `audit.py health` REDs on a duplicate JOURNAL day-letter (3 tests) | `scripts/audit.py:3955` marker, `:3970` `check_journal_day_letters`; tests `tests/test_audit.py:2057`, `:2068`, `:2079` |
| (b) | `validate_backlog` WARNs on a past body-date, silent on future (2 tests) | `scripts/validate_backlog.py:84` marker, `:355` scan; test `tests/test_validate_backlog.py:383` |
| (c) | `journal_anchor` WARNs "anchored by mention, not by record" | `scripts/journal_anchor.py:199` marker, `:238` the verbatim WARN string; test `tests/test_batch_manifest.py:706` |
| (d) | `check_hooks_armed` asserts the **pre-push** hook type (1 test) | `scripts/audit.py:1628`/`:1660`; test `tests/test_audit.py:2015` |

Merged at **`62f42dad`**; review artifact `docs/audits/2026-08-14-codex-524-check-extensions.md`,
tally *"0 Critical / 1 High / 0 / 0"*; the true-close packet *"states the row's state in one word:
**'Complete.'**"* Independently corroborated by `[NB2-E]` J3 **VERIFIED** — all four legs located in
code at the same loci.

**`[#352]` · P3/S · versioned `.vscode` region decoration** — both Done-when clauses hold,
**VERIFIED**: `.vscode/settings.json`'s `//boundary` block carries two `highlight.regexes`
(`owner=hub` → grey `rgba(140,140,140,0.16)`, `owner=repo` → navy `rgba(38,79,140,0.30)`), tracked,
landed at **`897577b7`** whose subject reads *"flip colours to the `[#352]` spec"*; the
no-hand-maintained-state clause is *"satisfied and already adjudicated"* by the row's own AMENDED
clause. Third signal, **VERIFIED**: *"the row declares **'P4a, shelf-life 2026-08-13 (revisit/kill if
not advanced).'** That date passed yesterday … the tree says the work is done, so the reading is
*close*, not *kill-unbuilt*."*

**Groups D2 (superseded) and D3 (obsoleted) — EMPTY, and checked rather than assumed.**
`[NB2-F]` §2, **VERIFIED**: the supersession sweep read all 9 rows carrying a supersession token —
*"every one describes a supersession *the row itself survives*"*; the obsolescence sweep enumerated
all 16 rows citing a non-existent repo-relative path — *"Every one names an artifact **to be
built** …, a **gitignored log** …, or a **cross-repo path** …. None indicates a dead subject."*

**Attached to D2.1 — the serialize-group conflict, FLAGGED LOUDLY.** `[NB2-F]` §6, **VERIFIED**:
*"**BOTH PROPOSED-DEAD ROWS ARE SERIALIZED** 🚩 … neither proposed-dead row is a free-standing leaf.
Both sit inside a group, and both are mid-chain."*

| dead id | group | group size | position in the emitted order | co-members proposed awaiting-ruling |
|---|---|---|---|---|
| **[#524]** | `audit-py` | **48** — the largest group in the repo | **17th of 48** | [#323] · [#397] · [#406] · [#408] |
| **[#352]** | `settings-json` | **18** | **11th of 18** | [#308] · [#371] · [#414] |

What it does **not** mean, **VERIFIED** as NB2-F's own reading: *"A serialize-group is a *contention*
declaration … not a dependency chain. So closing a mid-chain member **cannot orphan a successor**
… There is no ordering breakage to repair here."* Why the flag is still owed: *"**`audit-py` at 48
members is a third of the open set serialized behind one file**"*, and *"**Neither group's ordering
is machine-enforced**"* — `[#424]` records `depends-on` gates inert for the bare-id form
(`validate_backlog.py:78` `_DEPID_RE` requires the `#`), `[#510]` records the lane exemption keyed on
branch shape. The grouping surface itself is clean: *"12 serialize-groups covering 132 of the 196
open ids … 0 strays … 0 mismatches."* **See collision Y-1 for `[#524]`'s second entanglement.**

---

**D2.2 — Awaiting-ruling 4a: operator-owned by authority (5). PROPOSED.**

**The predicate, stated so it is checkable** `[NB2-F]` §4, **VERIFIED**: a row is proposed
awaiting-ruling only when **both** (1) *"the row's own text bars a build until a decision lands"* and
(2) *"its Done-when's **leading** clause is a ruling or decision, not an artifact."* And the
exclusion that keeps the set at 25: *"A row whose Done-when merely *offers* a
`protocols/STANDING_RULINGS.md` escape beside a buildable primary clause is **live**, not
awaiting-ruling — that escape is an exit, not a precondition. That single distinction is what keeps
this set at 25 instead of ~60."*

| id | why the executor is barred (verbatim) |
|---|---|
| **[#122]** | deletion authority — *"removal needs an explicit operator ask per the no-delete invariant"* |
| **[#189]** | executes in `~/.claude` (queue-only here, `#100` execute-elsewhere precedent) |
| **[#300]** | *"bundle sweep AWAITING explicit operator deletion GO (no drive-by deletion)"* |
| **[#346]** | the `~/.claude` edit is global infra — core-invariant #6 exception-with-ruling |
| **[#420]** | carries a live **do-not-touch order** on `docs/archive/` while the row is open |

Cross-check, **VERIFIED**: *"`[#456]` independently reaches four of these five … which is a
cross-check on this grouping rather than a coincidence."*

---

**D2.3 — Awaiting-ruling 4b: question-shaped by declaration (11). PROPOSED.**

`[#323]` · `[#331]` · `[#347]` · `[#397]` · `[#406]` · `[#407]` · `[#409]` · `[#410]` · `[#411]` ·
`[#449]` · `[#450]` — `[NB2-F]` §4b, **VERIFIED**.

**The high-leverage sub-pick, VERIFIED:** *"Six of these are a **single ruling apart from being
buildable**, and three of them (`[#409]` / `[#410]` / `[#411]`) are *the same ruling* — the standing
night-batch trio, each identically worded *'defined as a routine (trigger, scope, consumption path)
and ruled in or out'*, each gated on ADR-105 activation. **That is one architect decision releasing
three rows.**"*

**Directly actionable:** `[NB2-G]` §5 supplies paste-ready Form R drafts for all three
(`[#409]`/`[#410]`/`[#411]`), and `[NB2-E]` §11 groups them with `[#419]` as conversion lane
**W2-a** — so this one ruling also unblocks a wave-2 lane.

---

**D2.4 — Awaiting-ruling 4c: decision-first, build-after (9). PROPOSED.**

`[#43]` · `[#126]` · `[#308]` · `[#371]` · `[#408]` · `[#414]` · `[#491]` · `[#494]` · `[#495]` —
`[NB2-F]` §4c, **VERIFIED**.

**Two sequencing notes the lane flags, VERIFIED:**
- *"**`[#371]`'s vehicle is `[#387]`'s subject.** `[#371]` says *'Vehicle decided by the
  buy-vs-build fleet-template ADR … do NOT implement bespoke'*, and `[#387]` exists because that very
  intake *'argued FOR the template engine that was subsequently rejected.'* `[#387]` is **live** and
  buildable. Ruling `[#371]` before `[#387]` lands would ratify against a document the fleet has
  already refuted."*
- *"**`[#414]` and `[#408]` each name their organ choice as the first gate on any build** — for
  `[#408]` the per-section granularity is *'an OPERATOR DECISION deliberately not settled'* … for
  `[#414]`, *'Organs, NONE chosen (a ruling).'*"*

---

**D2.5 — The 17 ten-week-silent rows: look at them as a kill batch, or not. PROPOSED (the lane
proposes NO kill).**

`[NB2-F]` §7d, **VERIFIED**: of 56 rows with zero first-parent references since birth — *"3 are
newborn"* (`[#526]`/`[#527]`/`[#528]`), *"13 are proposed awaiting-ruling"*, and *"40 are live,
unbuilt, and un-narrated. Of those, **17 were born 2026-06-01 … 06-19 and have never once been named
by a merge on `main`** — ten weeks, zero spine mentions"*:

```
[#4] P2/M · 06-01   [#19] P3/M · 06-01   [#23] P3/S · 06-01
[#71] P3/S · 06-01  [#99] P3/S · 06-06   [#116] P3/S · 06-06
[#127] P3/S · 06-07 [#139] P2/L · 06-09  [#144] P3/M · 06-10
[#153] P2/M · 06-11 [#166] P3/M · 06-14  [#169] P3/M · 06-16
[#171] P3/M · 06-16 [#181] P2/S · 06-17  [#185] P2/M · 06-18
[#188] P3/M · 06-18 [#190] P3/M · 06-19
```

*"**This is the sharpest single grooming datum in the census.** They are not dead — every Done-when
was read and each is unmet and buildable — but nothing has pulled on them in ten weeks … it is the
set the architect should look at first if the P10 pass wants a kill batch rather than a ruling batch.
**This census does not propose killing any of them**, because 'old and quiet' is not one of ADR-65's
three classes."*

**Honest limit carried, VERIFIED** `[NB2-F]` §0 limit 2: *"A brand-new row shows zero first-parent
references and that is correct, not stale."* And §0 limit 1: *"The 'last git touch of its task file'
column is nearly uninformative, by construction … 84 of 196 files share one date, **2026-07-28** —
the migration commit. A further 44 share **2026-08-13**."*

**Why the closing-verb detector produced nothing extra, VERIFIED** `[NB2-F]` §3: a full-history
first-parent scan returned 24 open rows, *"**all 24 are co-mentions**"*. *"This is `[#454]`'s recorded
defect reproduced at full-corpus scale … and `[#277]`'s 49:0 ratio in a second independent run. **The
two genuine already-shipped rows in §2 were found by reading, not by the detector.**"*

---

**D2.6 — Peg MET: un-defer candidates (2). PROPOSED.**

`[NB2-F]` §7a, **VERIFIED**. *"the ARC-2 precedent for all of them is *un-defer or re-peg, do not
close*."*

| id | peg | evidence it fired |
|---|---|---|
| **[#494]** | *"the batch-4 ratification batch"* | batch 4 closed 2026-08-14 — `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §1 |
| **[#352]** | shelf-life **2026-08-13**, *"revisit/kill if not advanced"* | date passed; and the work is done — hence its **dead** proposal in D2.1 |

---

**D2.7 — Peg DEAD or unmeetable: re-peg (2). PROPOSED.**

`[NB2-F]` §7b, **VERIFIED**:

| id | the row's own words |
|---|---|
| **[#102]** | peg is *"a repo whose codemap is generator-MANAGED"* — and the row adds *"so no fleet codemap migration is coming to peg on"*. **A peg that states it cannot fire.** The Done-when itself is buildable. |
| **[#325]** | *"DEFER — peg #221 DEAD, unreplaced 2026-08-09 … Stays open, **stranded**"* — `[#294]` was checked and cannot absorb it, `[#236]` is closed. |

*"This is `[#505]`'s clause-2 class exactly … Neither is a new filing; both already carry the
diagnosis in-row. What they lack is a re-peg."*

**Dated triggers on the near horizon** `[NB2-F]` §7c, **VERIFIED** — **2026-08-17 (inside this
window)** `[#492]`; 2026-08-26 `[#348]` · `[#426]` (`review_date:` on both routine declarations);
2026-09-09 `[#322]`; 2026-10-22 `[#413]` (*"Done-when does not open before this date"*).

**Census hygiene notes, reported not fixed** `[NB2-F]` §8, **VERIFIED**: (1) `[#181]`'s peg names
`logs/coherence-nudge.log` while the canonical name is `logs/COHERENCE-NUDGE.log` (2026-07-22
UPPERCASE-KEBAB ruling) **and it is gitignored** (`.gitignore:81`) — *"un-evaluable from any fresh
clone"*; (2) **ADR-112 carries an internal disagreement about its own ratification** — status line
*"Accepted (operator ratification 2026-08-12)"* while the Decision-tier line *"still reads
'ratification is a separate operator act and **has not happened**'"*, which NB2-F calls *"a
*predicted* consequence, not a slip"* of ADR-94's status-line-only exception; (3) `validate_backlog`
carries one standing WARN — *"user story with no tasks — story '[S24] Declare desired state once, as
data' line 443"*; (4) the shallow-clone trap fired again — *"`[#453]` leg (1) is the owner … its
second recorded container instance."*

---

### D3 · Promotions still Proposed — `[NB2-F]` §5

**Scope, VERIFIED** `[NB2-F]` §5: two surfaces read — `protocols/STANDING_RULINGS.md` **M-5** (Part
D1 promotion-candidate table, 9 items) and **M-6** (Part D2 ADR-set hygiene, 5 items) — *"plus the
pre-ratification intake corpus that M-5's own dispositions land into."*

**Baseline fact, VERIFIED:** *"**ADR corpus: zero ADRs sit in `Proposed`.** Every
`docs/decisions/ADR-*.md` status line was read. The only non-`Accepted` values are three
terminal/other states — ADR-45 *'Explored, not adopted'*, ADR-46 and ADR-47 *'Partially
superseded'*. **There is no Proposed ADR to ratify.**"*

**D3.1 — `N2-D1-02`: the trigger has since fired. PROPOSED.** **VERIFIED**: disposition was
*"**DO-NOT-PROMOTE YET** — 'reassess after W3 lands'"*; live state *"**STILL PROPOSED · trigger now
MET** — W3 landed 2026-08-13; `[#513]` DISCHARGED at `387b794a` per the true-close packet §1."*
NB2-F: *"`N2-D1-02` is the genuinely separate one, and it is the one whose **trigger has since
fired**."*

**D3.2 — The consolidation intake (`N2-D1-06/07/08/09`) — ONE artifact, not four items. PROPOSED.**
**VERIFIED**: Sections A/B/C at
`docs/intake/2026-08-12-func-repo-self-description-consolidation.md:54`, `:97`, `:129`, the file
`status: DRAFT`; `N2-D1-09` *"structure LANDED, ratification not"*. NB2-F: *"**Read this as three
items, not four.** … the consolidation intake was **born as ruled** (one doc, Sections A/B/C, §201
`Births`) and is sitting at `status: DRAFT` awaiting ratification."*
(Already landed and needing nothing: `N2-D1-01` → ADR-112; `N2-D1-03` → ADR-110 amendment at `:310`;
`N2-D1-04` and `N2-D1-05` terminal.)

**D3.3 — `N2-D2-iii`: review-each, still open. PROPOSED.** **VERIFIED**: disposition
*"**REVIEW-EACH, no action now**"*; live *"**STILL OPEN** — the six sunset/review candidates stand
with their named blockers."*

**D3.4 — `N2-D2-gaps`: standing flag. PROPOSED.** **VERIFIED**: *"**FLAGGED, NOT ACTED ON** …
numbering gaps 40, 44, 52; ids are not reused."*
(`N2-D2-i` and `N2-D2-ii` are **LANDED** — `docs/decisions/README.md:10` status enum, and `ADR-32:140`
/ `ADR-42:450` forward pointers *"appended 2026-08-12 (not a status edit)"*. `N2-D2-iv` closed into
register **L-1**.)

**D3.5 — `I-D7`: a register entry whose own expiry has been met, with a locator that no longer
resolves. PROPOSED.** `[NB2-F]` §5d, **VERIFIED**: *"The entry's expiry reads *'retires when the
disposition is recorded'* … **The disposition has been recorded:** intake #10 was **REJECTED and
relocated to the archive** at `f095a81f` (2026-08-12) … The register entry still stands, and its
locator — `docs/intake/2026-07-11-tech-c4-visualization-memo.md` — **no longer resolves**. Reported,
not edited: the register is the architect's surface and B6's append-not-amend discipline governs
it."*

**Denominator context for the intake ceiling, VERIFIED** `[NB2-F]` §5c: *"Live frontmatter today:
**SEED 9 · DRAFT 3 · READY 1 · ACCEPTED 15** (28 docs under `docs/intake/`). Under **L-1**'s ruled
reading … the working set is **4 of 6** … **The ceiling is not breached**."* DRAFT docs: `#24`
tech-currency-wave-1, `#27` tech-adoption-consolidation-intake, `#33` the M-5 consolidation intake.
READY: `#15` satellite-onboarding-prompts.

---

### D4 · Plan amendments — `[NB2-E]` §10 (dispatch order) + §11 (wave-2 partition)

**Standing** `[NB2-E]` §10 header, **VERIFIED as the lane's own posture**: *"*Proposal only. The
booted seat rules.*"* NB2-E's verdict tally, **VERIFIED** (§12): *"**OK — 49** · **STALE — 10** (A8,
A9, B6, C5, D5, F3, G2, K8, M1, M2) · **MISSING — 2** (A2 — the on-main twin; B5 — the telemetry
owner row). 61 claims verdicted."*

**D4.1 — CONFIRM the three items NB2-E says dispatch as written. PROPOSED.**
- *"**The draft-production lane runs FIRST and alone.** Correct and load-bearing: all 29 are
  no-draft rows and the census's DEFECTIVE-not-improvised rule bars a conversion lane from authoring
  one."* **With one consequence the plan does not state, VERIFIED:** *"the draft artifact must
  **land on main** before the conversion lanes boot, because each lane reads it from its own
  worktree. That is one full merge cycle (~16 min of suite) of hard serialization at the top of the
  wave — budget it, do not discover it."* **Note:** `[NB2-G]` has already produced that artifact
  (30 drafts, D6) — what remains is review + landing, not production.
- *"**Batch the reviews** (§2 EXPANDED). Nothing in the tree contradicts it."*
- *"**`[#527]` is in scope and small** — P2/S, one hook + one test, `serialize-group: gates` with no
  wave-2 collision."*

**D4.2 — AMENDMENT 1: split `[#528]`, move legs (1)+(2) to position 0. PROPOSED.**
**VERIFIED reasoning:** *"the plan's own rationale ('this lane pays for every future lane') argues
for position 0, not position 3 — wave 2 is 7 conversion lanes + 1 draft lane + integration, and at
~16 min per full suite the integration gate alone is ~2 h of suite time. Legs (1) and (2) are a
call-site flag sweep and a doctrine paragraph; neither touches `tasks/`, so they collide with nothing
in the wave. Leg (3) moves to the telemetry lane (F-3), which is the only place it can be
discharged."*

**D4.3 — AMENDMENT 2: birth the telemetry row BEFORE dispatching the telemetry lane. PROPOSED.**
**VERIFIED reasoning:** F-2 (X-13). *"The lane cannot fill its own dispatch line and cannot satisfy
the filing gate mid-flight. Two minutes at boot; the operator word is already queued in §7 EXPANDED."*
The stated alternative, also PROPOSED: *"Either birth the row at boot … or dispatch explicitly
against intake #29 Fold A as contract-of-record and say so."*

**D4.4 — AMENDMENT 3: move `[#527]` from position (4) to run concurrently with the wave. PROPOSED.**
**VERIFIED reasoning:** *"the 2026-08-13 direct-to-main incident happened in exactly the
configuration wave 2 recreates — an integrator merging serially in the primary checkout while lanes
land. `[#527]`'s value is highest **during** the largest wave yet run, not after it. It is P2/S and
disjoint."*

**D4.5 — AMENDMENT 4: demote (5) to a checkpoint, promote (7) to a dated commitment. PROPOSED.**
**VERIFIED reasoning:** F-4 (X-16) and F-5 (X-15). *"These two move in opposite directions and the
plan has them the wrong way round: the calendared item is cheap, the uncalendared one is expiring."*

**D4.6 — FLAGGED item (6), the single-flight dispatch guard: rule it in or out. PROPOSED.**
`[NB2-E]` §10, **VERIFIED**: *"`RESIDUAL.md` §4 item 2 is explicit that *'whether it becomes a
`[#id]` is the next architect's call'*. It has the same id-less problem as telemetry (F-2). Keep it
last, and rule it in or out rather than dispatching it."* Mechanism evidence is D5.1.

**D4.7 — M1: settle the wave-2 width. PROPOSED.**
The contradiction is X-10. `[NB2-E]` §11's recommendation, **PROPOSED**: *"Sits inside §7
EXPANDED's 6–8 recommendation with the draft lane counted separately — which is also the reading this
proposal recommends the operator adopt for M1 (**'7 + 1'**, stated that way so 'GO' is
unambiguous)."*

**D4.8 — M2: pick between "no planning phase" and the P10 boot duty, and say which. PROPOSED.**
The contradiction is X-11. `[NB2-E]` §10, **VERIFIED as unresolvable from the tree**: *"**FLAGGED,
unresolvable from the tree — M2.** … The seat must pick, and say which, in its first JOURNAL entry."*
Cost input: `[NB2-F]`'s pre-read (D2).

**D4.9 — Adopt, amend or reject the 7-lane partition. PROPOSED.** Full table in §4.
`[NB2-E]` §11's disjointness law, **VERIFIED**: *"`tasks/<id>-*.md` ownership — each id's file is
touched by exactly one lane, and each id appears exactly once across the seven lanes (30/30, verified
by set-difference against §9)."* **Independently re-checked by this consolidation** against NB2-E §9
and NB2-G §3–§6: the two lanes' 30-id sets are **identical**, and the seven-lane partition covers all
30 with no id in two lanes.

**Two couplings the partition does NOT dissolve, both already ruled, VERIFIED** `[NB2-E]` §11:
1. *"`BACKLOG.md`, `tasks/manifest.json` and `docs/audits/README.md` are regenerated by **every** lane
   and therefore collide by construction. §4 EXPANDED already rules this: *'regenerate
   BACKLOG/manifest/audit-index at merge, never hand-merge.'* Wave 1 ran the same way across four
   lanes."*
2. *"`serialize-group` is **not binding for this wave** — a Done-when conversion edits only the task
   file, never the grouped surface … **The inverse is the stop condition:** if a lane finds its
   conversion requires touching the grouped surface, it must stop and report rather than proceed —
   that is the census's DEFECTIVE-not-improvised rule."*

**Operational-law claims NB2-E verified OK and that need no ruling** (recorded so they are not
re-derived): L1 — *"`git ls-remote --heads origin` → exactly two: `refs/heads/automation/fleet-audit`
(`abcc50ec`) and `refs/heads/main` (`7bbb0674`)"*; L2 — all five `claude/*` night branches gone;
L3 — *"`/lane-boot` … 'from step 3' is coherent"*; L4 — `/lane-integrate` present; L5 — *"full suite
≈ 15–16 min … `JOURNAL.md:145` — 907.74s (~15m8s), `-n auto --dist worksteal`; `tasks/528-*.md` —
1001 s (16:41)"*; K1 — seal `1ffb030d`; K2 — open-total **196**; K3 — window net **+3**; K4 —
untestable ≈ **58**; K5 — wave-2 target **≤29**; K6 — `doc_rot` **38**; H1–H4 — `[#511]` deferral and
the R43/R50/R51 staleness question (**OK — no staleness introduced by the deletion**, because
*"the distillate is dated **2026-08-10**, predating the 2026-08-12 night lanes entirely"*).

---

### D5 · Mechanism picks — `[NB2-D]`, one recommended option per question

**Standing** `[NB2-D]` header, **VERIFIED**: *"**EXTERNAL EVIDENCE — advisory until ratified, never
doctrine by virtue of existing.** … This document decides nothing, adopts nothing, and births no
BACKLOG row."* Its ladder, **VERIFIED**: *"stdlib > established dependency > stabilized project >
industry pattern. Where a recommendation steps *down* the ladder, §1–§3 give the measured reason."*

---

**D5.1 — Single-flight guard. RECOMMENDED (PROPOSED): a git ref used as a distributed
compare-and-swap, claimed with `--force-with-lease=<ref>:`, pushed to `origin`.**

**The failure it must stop, VERIFIED** `[NB2-D]` §1.1: *"Witnessed 2026-08-14 (`JOURNAL.md` entry
(d)): **three independent executions of one contract were live at once** … Two of them independently
allocated `[#526]`–`[#529]` for the same four filings. The executions did not share a working tree,
and at least one pair did not share a machine."* Consequence: *"**Every filesystem-lock library in
the candidate set is single-host by construction.**"*

**Why the existing step-0 commit is not the mutex, VERIFIED** §1.3: *"On 2026-08-11 (entry (j)) three
lanes each committed their contract of record — `e0de6bba`, `d4d814e7`, `93c96471` — onto *their own
lane branches*. Branches do not contend."* The proposed fix keeps `I-D3`
(`protocols/STANDING_RULINGS.md:973`) intact: *"keep the commit, and add one shared ref that the
commit claims."*

**The decisive property, VERIFIED (first-party, §4.2 T1–T5, git 2.43.0):** T2 — *"a second clone that
has *never fetched the lock ref* is still refused, because the expectation is evaluated by the
receiving repo, not by the pusher."* **The trap that makes it a real finding, VERIFIED:** T4 —
*"A plain `git push origin HEAD:refs/locks/<id>` onto an already-held lock, *when both sessions sit
at the same commit*, returns `Everything up-to-date` and **exit 0** … And same-base is not an edge
case — it is the normal batch-dispatch state."*

```
===== T1: A claims lock (ref does not exist) =====        * [new reference]        exit=0
===== T2: B claims SAME lock, B has NEVER fetched =====   ! [rejected] (stale info) exit=1
===== T3: plain push of a DIFFERENT commit =====          ! [rejected] (non-ff)     exit=1
===== T4: THE TRAP — plain push of the SAME commit =====  Everything up-to-date     exit=0
===== T5: release + re-claim =====                        delete exit=0 / reclaim exit=0
```

**Cost, VERIFIED:** *"**Zero new dependencies** … no `uv.lock` change, no
`ecosystem/dependency-baseline.yaml` row. `git push` behaves identically on Git-for-Windows."*
**The one new precondition, stated by the lane, PROPOSED for ruling:** *"**step 0 now needs
network** … it is a new precondition on a gate, and a gate with a new failure mode should be ruled
on, not slipped in."*
**Residual, VERIFIED as stated:** *"A lane that dies without releasing leaves the ref held. There is
no TTL in git."* Two options offered, neither adopted; the lane prefers (a) — the refusal message
already prints how to inspect and release.
**Optional same-machine fast leg, VERIFIED** (T6/T7/T9): `git update-ref --stdin` `create` gives
cross-worktree single-flight with no network (second `create` → *"fatal: cannot lock ref … reference
already exists"*, **exit 128, not 1**); *"Do **not** reach for `refs/worktree/…`: T9 proves that
namespace is per-worktree and invisible to the primary."*
**UNVERIFIABLE, never upgraded** `[NB2-D]` §0 limit 2 + §5 residual 1: *"The §1 lock is unverified
against GitHub specifically."* The one closing command is printed in §5 residual 1 and deliberately
not run, *"because it would create and delete a ref on the shared `origin` and this lane is
evidence-only."*

---

**D5.2 — pytest-xdist on Windows. RECOMMENDED (PROPOSED): `--max-worker-restart=0` as the single
highest-value setting, inside a tiered suite that never runs the full suite in a commit hook.**

**Root cause, VERIFIED from upstream source** `[NB2-D]` §2.1: *"**execnet launches every worker with
a bare `Popen`** … There is **no `CREATE_NEW_PROCESS_GROUP`, no Windows Job Object, and no
`start_new_session`.**"* Consequences: *"**If the controller never reaches teardown … nothing kills
the workers at all.** Windows does not tear down a process tree when a parent dies"*; and
*"`Popen.kill()` on Windows is `TerminateProcess` against **that one process**."*

**Why the count reaches 19, VERIFIED** §2.2: *"**The default restart budget is `numprocesses × 4`**
… A suite running `-n auto` on a 5-physical-core host carries a silent budget of 20 replacements on
top of the 5 originals. **19 stray workers is squarely inside what this default permits.**"*
Corroboration: *"**pytest-xdist issue #1094** (open, filed 2024-06-10; win32 …) reports the worker
count climbing 6 → 8 via `replacing crashed worker`, then the run stalling ~30 minutes."*

**Strays are exactly identifiable, VERIFIED** §2.3 — `popen_bootstrapline = "import
sys;exec(eval(sys.stdin.readline()))"`, so a read-only PowerShell probe is precise and a blunt sweep
is *"unnecessary and dangerous (a `taskkill /IM python.exe` would take out the operator's live Claude
Code session interpreter)"*.

**The ordered settings list, PROPOSED** §2.6: (1) `--max-worker-restart=0` — *"It converts quiet
proliferation into a loud, bounded failure, which is the only honest posture for a *gate*"*; (2)
*"Do not run the full suite inside a commit hook at all"* — `[#528]` leg 2's shape; (3)
`--maxprocesses=N`; (4) `-n 0` for anything running inside a forking parent — *"**`-p no:xdist` is
not a way to force serial**"*; (5) `--dist loadfile`/`loadgroup` for the `live_repo` and `slow`
tiers, keeping `--dist worksteal` for the balanced remainder; (6) `-p no:cacheprovider` in hook
context; (7) a detection leg, *"because no setting covers the killed-controller case"*; (8) *"Treat
`pytest-timeout` + xdist on Windows as suspect."*

**Version state, VERIFIED** §2.6: *"pytest-xdist **3.8.0** … locked here at **3.8.0** with **execnet
2.1.2**, pytest **9.1.1**. The repo's `pytest-xdist>=3.8` floor is already at the current upstream
release — **no upgrade is available and none is needed**; the leak is a design property of the
`Popen` call, not a bug awaiting a fix."*

**Coverage, VERIFIED as a precondition not a hazard** §2.5: *"`pytest-cov`, `coverage` and `psutil`
are all **absent from `uv.lock`** … Without [`parallel = true`] the numbers come out deflated rather
than erroring — a silently wrong gate."*

**UNVERIFIABLE, never upgraded** §0 limit 1 + §5 residual 2: *"**This lane runs on Linux.** Every
Windows claim in §2 is derived from upstream *source* and from an upstream Windows bug report, not
from a Windows run."* / *"the *count* of 19 was not reproduced and its exact `-n` value is not known
to this lane."* Also §5 residual 3: *"Session-scoped-fixture exposure in this suite was not
surveyed."*

---

**D5.3 — `[#527]` hook route. RECOMMENDED (PROPOSED): a `local` pre-commit hook copying upstream
`no-commit-to-branch`'s `git symbolic-ref HEAD` predicate, plus one added `MERGE_HEAD` carve-out.**

**The word that decides it, VERIFIED** `[NB2-D]` §3.1: *"'Non-merge' is load-bearing, because this
repo's own convention is `branch → --no-ff merge`, and that merge commit is created *while HEAD is
`main`*."*

**The measured answer, VERIFIED first-party** §3.2 / §4.4:

| case | pre-commit hook fires? | outcome |
|---|---|---|
| **E1** ordinary commit on `main` | yes | **refused** (exit 1) — the witnessed incident, closed |
| **E2** ordinary commit on `feat/x` | yes | allowed |
| **E3** clean `--no-ff` merge run while HEAD is `main` | **NO — hook never fires** | merge lands, two-parent commit created |
| **E4** conflicted merge finished by `git commit` on `main` | **yes** | **refused** — `MERGE_HEAD` present |
| **E5** `git commit --amend` on `main` | yes | refused — `MERGE_HEAD` absent |
| **W1** commit in a worktree on `feat/z` while the primary is on `main` | yes | allowed — `HEAD` is per-worktree |

*"**E3 is the good news and E4 is the catch.** … a *conflicted* merge is completed with an explicit
`git commit`, which does run the hook — and this repo conflicts on integration routinely … So a
stock branch-name refusal would force `git commit --no-verify` on essentially every batch integration
merge — and `--no-verify` … skips **the entire pre-commit stack** … That trades a narrow gap for a
wide one, on the exact commits that most need gating."* And: *"**E4 also hands over the discriminator
for free:** `MERGE_HEAD` is present exactly when the commit being created is a merge, and
`git rev-parse --git-path MERGE_HEAD` resolves it per-worktree."*

**Worktree behaviour, VERIFIED** §3.5 / §4.1: *"**Hooks are shared across all worktrees of a clone**,
so a single `pre-commit install` in the primary arms every present *and future* worktree
automatically"* (`--git-path hooks` resolves to the common dir, while `index.lock` is per-worktree).
*"**Detached-HEAD worktrees are allowed through** … which is correct here, and is the stated hole."*

**The zero-local-code alternative, PROPOSED and not chosen:** *"pin `pre-commit/pre-commit-hooks` at
**`rev: v6.0.0`** with `args: ['--branch', 'main']`, and accept `--no-verify` on conflicted merges.
The repo already pins one external hook repo this way."*

**Arming — no change needed, ONE precondition. VERIFIED for this container, UNVERIFIABLE for the
operator's host** §3.4: *"`arm_hooks.py`'s own docstring records that pre-commit **refuses to install
when `core.hooksPath` is set** … Verified in this container: `core.hooksPath` is **not** set here …
**On the operator's Windows checkout this is unverified by this lane and should be checked before
relying on the arming leg** — `git config --get core.hooksPath`. `arm_hooks.py` already handles
refusal by reporting and exiting 0, so the failure mode is a silently un-armed gate rather than a
loud one."*

---

#### D5 · The consolidated DO-NOT-ADOPT table

All three questions' rejects in one place, each with the lane's one-line reason. `[NB2-D]` §1.6,
§2.7, §3.6 — **PROPOSED** (they are rejections the architect may overrule).

| Q | candidate | one-line reason |
|---|---|---|
| 1 | `filelock` (3.32.3) | *"process-lifetime kernel lock on one host; it cannot see a peer on another machine"* (note: `filelock 3.32.0` is **already in `uv.lock`** transitively) |
| 1 | `filelock.SoftFileLock` | *"there is no shared filesystem between the cloud container and the Windows host"* |
| 1 | `portalocker` (4.1.0) | *"same single-host ceiling as `filelock`, plus it wants `pywin32` for shared locks on Windows"* |
| 1 | `portalocker.RedisLock` | *"stands up an always-on Redis server to arbitrate three lanes, and a Layer-2 repo that 'never executes' (ADR-28/36) should not acquire a service dependency for a governance gate"* |
| 1 | bare `O_EXCL` lockfile | *"correct, stdlib, and already used well in `scripts/fleet_health.py:730` … but it is blind past the local filesystem"* |
| 1 | plain `git push` of a lock ref | *"T4 proves it returns exit 0 on the same-HEAD race, which is exactly the batch-dispatch case"* |
| 1 | `git update-ref` alone | *"local-only; correct across worktrees, never across clones"* |
| 1 | GitHub Actions `concurrency:` | *"arbitrates CI jobs; the collision happened between agent sessions, entirely outside CI"* |
| 1 | a BACKLOG/manifest "claimed" marker | *"advisory, not atomic; the witnessed failure is precisely two parties each concluding they may proceed"* |
| 2 | `-p no:xdist` to force serial | *"it removes the `-n` that `addopts` supplies, so pytest exits 4 before collecting a single test, and the run looks green while measuring nothing"* |
| 2 | raising `--max-worker-restart` | *"treats the symptom by buying a larger budget for the exact proliferation being complained about"* |
| 2 | `--dist each` | *"runs every test in every worker; it is a multi-environment matrix mode, not a speed mode"* |
| 2 | `-n logical` as the default | *"buys hyperthread workers at the cost of adding `psutil` … should be measured, not assumed"* |
| 2 | `pytest-parallel` / `pytest-forked` | *"unmaintained and fork-based; `fork` does not exist on Windows"* |
| 2 | blanket `taskkill /F /IM python.exe` | *"would kill the operator's other Python processes including the live session's own interpreter"* |
| 2 | waiting for an upstream orphan fix | *"there is no pending fix to wait for"* |
| 3 | stock `no-commit-to-branch` unmodified | *"no merge awareness, so conflicted integration merges on `main` would each require `--no-verify`, which skips the *entire* gate stack"* — *(still the right pick if zero local code outweighs that)* |
| 3 | hand-rolled `.git/hooks/pre-commit` | *"un-versioned, undeployable to consumers, and it collides with the shim `pre-commit` already owns at that exact path"* |
| 3 | `core.hooksPath` → committed hooks dir | *"pre-commit refuses to install at all when it is set, so this trades the new gate for every existing one"* |
| 3 | a `commit-msg`-stage hook | *"fires later than necessary; `pre-commit` is the earliest refusal point and is what the row names"* |
| 3 | server-side branch protection | *"that is `[#153]`'s scope … the repo's GitHub tier was already recorded as unable to host it"* |
| 3 | extending `block_ff_push.py` | *"it is a *pre-push* organ; `[#527]` exists precisely because push-time is too late"* |
| 3 | `receive.denyCurrentBranch` etc. | *"none of them refuse a *local commit*, which is the whole gap"* |
| 3 | re-implementing branch detection | *"upstream's 30 lines are the reference; copy the predicate, add only the carve-out the measurement forced"* |

---

### D6 · Wave-2 drafts — `[NB2-G]`

**Counts, VERIFIED** `[NB2-G]` §8: *"**30 drafts produced** — 29 needs-draft rows + the 1 `[#419]`
re-check. **0 skipped.** … **4 ambiguity-flagged** … **Form E applied 13×**, **Form R applied 6×**;
3 open home-substitutions … **L14 re-resolve:** 30/30 verified `status: open` live before drafting."*
(An intra-lane numeric inconsistency on the Form-E count is recorded in §5 under NB2-G.)

**Provenance of the id set, VERIFIED** §1 — reconstructed from the four W4a–d lane JOURNAL entries
because the input file has no on-main twin (X-12):

| Wave-1 lane | Contract | Assigned | Converted | Skipped | Skipped ids |
|---|---|---|---|---|---|
| h | W4a | 17 | 6 | 11 | 82, 130, 145, 146, 210, 239, 263, 266, 271, 274, 285 |
| i | W4b | 18 | 13 | 5 | 324, 350, 351, 361, 364 |
| j | W4c | 18 | 9 | 9 | 385, 391, 393, **419**, 409, 410, 411, 412, 417 |
| k | W4d | 16 | 11 | 5 | 438, 443, 484, 491, 502 |
| **Total** | | **69** | **39** | **30** | **29 needs-draft + 1 re-check** |

**D6.1 — Accept, amend or reject the 30 drafts as the wave-2 conversion substrate. PROPOSED.**
Each draft is a full replacement Done-when clause with a stated intent; two reusable levers were
applied rather than invented per row — **Form E** (*"replace `…, or recorded <X>-with-reason` with
`…, or protocols/STANDING_RULINGS.md carries a section naming [#NNN] and stating the reason`"*,
applied to `#146 #210 #239 #263 #350 #351 #364 #391 #412 #417 #443 #484 #491`) and **Form R** (the
ADR-105 `· routine:` block, applied to `#409 #410 #411 #324 #271 #391`).

**One draft explicitly supersedes an existing one, VERIFIED** §5 (`[#419]`): *"**this supersedes the
census's `[#419]` draft, which is stale and must not be applied.** That draft (census §4) predates the
2026-08-11 amendment (operator ruling, Fork 3 / I-F3) and covers only the first two legs; applying it
would silently drop the three amended clauses — the exact L14 failure mode."* NB2-E A10 concurs,
**VERIFIED**.

**Honest limit carried into every Form R draft, VERIFIED** §2: *"`routine_consumers` checks only
BACKLOG rows carrying the `· routine:` marker — not the ~30 live hooks and schedules. Its own
docstring says so, and `[#426]` owns the retrofit. A Form R draft therefore makes a row's
*declaration* checkable; it does not claim the fleet's routines are consumed."*

**Locator drift found and repaired inside the drafts, VERIFIED** §8: *"`[#146]` PLAYBOOK `1016-1024`
→ the de-hardcode paragraph now at `1032` · `[#263]` `doc-code-edge.yaml` `L110` → `L115` ·
`[#361]` guard scope cited at `:83` → `:9` · `[#417]` `:340-349` → `:412`. Substance held in all
four; only the pins had rotted."*

**Referent defects found and worked around, not papered over, VERIFIED** §8: *"`[#391]` → `[#384]`
closed (§5.2) · `[#412]` → `refs ROUTING.md`, no such file in the tree (draft homes the doctrine at
PLAYBOOK) · `[#285]` → row names `_FRESHNESS_FILES`, but the editable constant is
`_HUB_ONLY_FRESHNESS_FILES` · `[#443]` → `docs/audits/README.md` is generated and hook-gated, so it
cannot host doctrine."*

---

**The four AMBIGUITY forks — each needs a ruling. Each was drafted anyway; none is a guess.**
`[NB2-G]` §7 (its subsections are numbered 5.1–5.4).

**D6.2 — Fork `[#364]`: the premise has been overtaken, prevention → repair. PROPOSED.**
**VERIFIED:** *"The row reads *'at 1189 chars it has ~11 left under the 1200 cap… at the current rate
it hits the cap within about two more incidents.'* Live at drafting, `[#353]` is **1266 chars and
already tripping the gate**"*, with the validator output quoted. **The fork:** *"the row is written
as *prevention* … the live state is *repair* … What the architect may want to decide is whether the
overtaken premise raises the row's priority off P3, since the degradation the row predicted has
begun."* **See collision Y-2 — D1.1's threshold change would discharge this premise entirely.**

**D6.3 — Fork `[#391]`: branch (b) names a closed row. PROPOSED.**
**VERIFIED:** *"`[#384]` has **no task file, and zero rows in `BACKLOG.md`**; it was closed
2026-07-23 … (`docs/handoffs/2026-07-23-dev-knowledge-architect/RESIDUAL.md:38`). A closed row cannot
be narrowed, so half this Done-when is unactionable as written."* **The fork:** *"(a) drop the dead
disjunct and require the nightly wiring outright; or (b) keep a two-branch clause by re-expressing
(b) … The draft takes (b) … a reader who prefers (a) can delete the second half of the draft with no
other change."* Also **VERIFIED**: *"`scripts/fleet_analytics.py` does appear in
`.github/workflows/report-only-wall.yml`, but in the wall's **path/test scope**, not as a scheduled
invocation — so the row's core premise (nothing fires it nightly) still holds."*

**D6.4 — Fork `[#417]`: the clause appears already met in live code. PROPOSED.**
The contradiction is X-6. **The fork, VERIFIED as stated:** *"(a) the Done-when is discharged and the
correct act is a closure proposal, not a conversion; or (b) something in the row's intent remains
unbuilt (its note about extracting the shared scope list from `scripts/audit.py:2625-2633` is not
addressed by what landed) and the converted clause should carry that remainder. **This lane proposes
neither** — it edits no row and closes nothing."*

**D6.5 — Fork `[#502]`: the stated blocker is discharged. PROPOSED.**
The contradiction is X-5. **The fork, VERIFIED as stated:** *"whether the row is simply unblocked and
ready to run as written, or whether the report-only constraint changes the eval's shape — `[#501]`
is REPORT-ONLY by standing ruling (Free tier, private repo, no promote-to-gate path), so a mutation
pilot hosted there **records** a result and can never gate on it … Worth an explicit word at review,
since 'runs on CI' reads differently once the CI in question is a recorder."*

**D6.6 — The three open home-substitutions. PROPOSED.**
`[NB2-G]` §2, **VERIFIED**: *"Three drafts want a home the tree does not yet designate: `[#82]`
(per-repo review profiles), `[#324]` (audit-corpus verb-list), `[#412]` (routing doctrine). Each
names the most defensible live candidate and is a **textual substitution** if the operator names
another."*

---

## §2 · NECESSARY CONDITIONS (session preconditions)

Ordered. Each condition names what must be true, the lane evidence that makes it necessary, and the
**blocking dependency** — what cannot lawfully execute until it holds. Derived strictly from the lane
evidence; nothing here is invented by the consolidation.

---

**N-1 · Re-derive `ship-gate` on the operator's host before ruling any WARN.**
*Why:* `[NB2-A]` §0.2 **VERIFIED** — 4 of 45 WARNs and the sole hard-fail organ are container
artifacts, and a register entry keyed to a container-only signature *"would match nothing on the
operator's host and decorate stale on its first run (ADR-75)"*. `[NB2-E]` K7 **VERIFIED** reaches 41
by the same subtraction but names different members (**X-1**). **No lane measured the host.**
*Blocks:* **D1 in full** (all seven picks), and every downstream claim that the gate is GREEN.

**N-2 · Arm the hook stack and verify `core.hooksPath` is unset on the operator's checkout.**
*Why:* `[NB2-A]` §1.5 **VERIFIED** — the `hooks_armed` hard FAIL *"Clears with `pre-commit install -t
pre-commit -t commit-msg -t pre-push`"*. `[NB2-D]` §3.4 **VERIFIED-here / UNVERIFIABLE-there** —
pre-commit refuses to install when `core.hooksPath` is set, and *"`arm_hooks.py` already handles
refusal by reporting and exiting 0, so the failure mode is a silently un-armed gate rather than a
loud one."*
*Blocks:* the gate reaching GREEN at all (N-1's hard-fail leg); and **D5.3** — `[#527]`'s Done-when
requires arming *"via the existing `arm_hooks.py`/`check_hooks_armed` mechanism"*.

**N-3 · Establish full history (non-shallow) before trusting any history-derived number.**
*Why:* four lanes hit it independently. `[NB2-A]` §0.1 **VERIFIED** — a shallow run fabricated three
organ verdicts (`canonical_freshness`, `journal_spine_anchor`, `no_ff_merges`); *"**Every number in
this report is from the post-unshallow run.**"* `[NB2-C]` M-3 **VERIFIED** — under the graft, *"40 of
43 checks reported the *same* date"*; its **P2 proposal, the highest-priority in that document**:
*"any organ deriving a git-history metric should assert `git rev-parse --is-shallow-repository ==
false` and **refuse to emit** rather than emit a truncated figure."* `[NB2-F]` §0 **VERIFIED** —
*"Every 'since its birth' column would have been silently wrong. Un-shallowed before any
measurement."* `[NB2-E]` §0 **VERIFIED** — did **not** unshallow, and says so at every affected row.
*Blocks:* the X-2 `canonical_freshness` question; the X-9 `[stale]` count; **D3.5** and every
register-expiry read; and the telemetry lane's git metrics (§3).

**N-4 · Settle X-2 (`canonical_freshness` / `VISION.md`) before declaring the gate GREEN.**
*Why:* three lanes give three incompatible readings and one (`[NB2-D]` A1) explicitly refuses to
clear it: *"this establishes that the container cannot answer the question, NOT that the six stamps
are fine."* A freshness FAIL is a **hard** commit-gate leg.
*Blocks:* N-1's conclusion; and any integration merge, since `audit-health` is a pre-commit gate.

**N-5 · Gate GREEN before integrations.**
*Why:* carried from the plan and unchallenged by any lane; `[NB2-B]` §6 **VERIFIED** records the cost
of ignoring it — that lane's own commit needed `--no-verify` because *"No commit of any content can
pass this gate in this container."*
*Blocks:* every merge in §4's execution plan.
*Dependency:* N-1 → N-2 → N-3 → N-4.

**N-6 · Every lane venv is built with `uv sync --locked --group analytics`.**
*Why:* `[NB2-B]` §1c **VERIFIED**: *"The 17 `ModuleNotFoundError: No module named 'pandas'` failures
recorded in JOURNAL 2026-08-14 (d) were a *missing dependency group* … **This is worth a line in a
lane-boot checklist: 17 of that lane's 19 reds were an environment-provisioning artifact that cost
real triage attention.**"*
*Blocks:* any honest lane-green claim in §4; without it, a lane reports reds it did not cause.

**N-7 · Resolve M2 (X-11) and state the choice in the first JOURNAL entry.**
*Why:* `[NB2-E]` §10 **VERIFIED**: *"The seat must pick, and say which, in its first JOURNAL entry."*
*Blocks:* the shape of the whole session — D4.8 gates whether D2 runs at boot or is deferred.

**N-8 · Ratify the census before any grooming closure is executed.**
*Why:* `[NB2-F]` header **VERIFIED**: *"This artifact **prepares** the booted architect's P10 duty
(`[#506]`); it does not discharge it. The whole-open-set grooming *judgment* stays his."* And §9's
`[#506]` row: *"**this census is evidence toward it, not its discharge**."*
*Blocks:* **D2.1** (the two closes) and any `[#506]` discharge claim.
*Attached warning:* the serialize-group flag (D2.1) must be weighed **before** ratifying, not after.

**N-9 · Review the 30 drafts and land the draft artifact on `main` before any conversion lane boots.**
*Why:* `[NB2-G]` §8 **VERIFIED**: *"These drafts bind nothing. They apply only under a later operator
ruling, after architect review and the wave-2 GO. Conversion lanes consume this file; they do not
inherit authority from it."* `[NB2-E]` §10 **VERIFIED** names the cost: *"the draft artifact must
**land on main** before the conversion lanes boot, because each lane reads it from its own worktree.
That is one full merge cycle (~16 min of suite) of hard serialization at the top of the wave."*
*Blocks:* lanes W2-a … W2-g in §4.
*Dependency:* D6.1 (and, for four ids, D6.2–D6.5).

**N-10 · Birth the telemetry row (or name intake #29 Fold A as contract-of-record) at boot, before
the telemetry lane is dispatched.**
*Why:* `[NB2-E]` F-2 **VERIFIED**: the dispatch template is `[dk · #<id> · <label>]` and
*"the `backlog-filing-backpressure` commit-msg gate requires a `kill-candidates:` line on any commit
that **adds** a new id — so the row must be born deliberately at boot, not improvised inside a lane
that has already started. … As written, the lane cannot fill in its own dispatch line."*
*Blocks:* the telemetry v1 EMIT lane in §3/§4.
*Dependency:* D4.3.

**N-11 · `[#528]` legs (1)+(2) must precede leg (3), and leg (3) must follow the telemetry lane.**
*Why:* `[NB2-E]` C5/F-3 **VERIFIED**: *"the row's Done-when requires **all three** with evidence. So
`[#528]` cannot close at position (3) unless the telemetry EMIT lane at position (2) has already
landed."*
*Blocks:* any `[#528]` closure claim.
*Dependency:* N-10 for leg (3); D4.2 for the split.

**N-12 · Resolve the three `tasks/`-file ownership collisions before the wave dispatches (Y-3).**
*Why:* `[NB2-A]` D1.2 drains `tasks/419-*.md`, `tasks/492-*.md` and `tasks/528-*.md` at source, while
`[NB2-E]` §11 assigns `#419` to lane **W2-a**, `[NB2-G]` supplies a replacement `#419` clause, and
`#528`/`#492` are execution/checkpoint subjects. `[NB2-E]` §11's disjointness law is *"each id's file
is touched by exactly one lane"*.
*Blocks:* lane W2-a specifically, and the D1.2 drain batch generally.

**N-13 · `[#492]`'s 2026-08-17 re-check falls inside this window — record it as a checkpoint, not a
lane.**
*Why:* `[NB2-F]` §7c **VERIFIED** (*"3 days"*) and `[NB2-E]` D1 **VERIFIED** — *"Three concurring
sites: `tasks/492-*.md` (**RE-CHECK 2026-08-17**), `protocols/STANDING_RULINGS.md:818` (I-D item 1),
and `:1569` (`N2-R2-03`)."* F-4: *"**Do not budget a lane.**"*
*Blocks:* nothing — but it expires unattended if it is not calendared at boot. **See collision Y-3**:
`tasks/492-*.md` is also a D1.2 drain target.

**N-14 · `[#293]`, the satellite-serving lane, is due THIS window (X-15).**
*Why:* `[NB2-E]` F-5 **VERIFIED**, with F1/F2 as anchors: `[#293]` is *"`open`, `P3`, `S`;
**UN-DEFERRED 2026-08-09 (ARC-2)**: 'work NOT done (0 of 6 consumers seeded)'"*, and *"`≤2 windows`
expires **at the end of the incoming window**."*
*Blocks:* nothing mechanically; it is the one deadline in the set that expires if the window closes
without it. D4.5 is the pick.

**N-15 · Any organ that derives a per-organ or per-run metric must handle the two derivation traps
before it emits.**
*Why:* `[NB2-C]` M-2 **VERIFIED** — a static call-graph predicate reports 2 of 43 checks as untested
and *"**Both are wrong**"* (dynamic `getattr` lookup; registry injection via
`monkeypatch.setattr(aud, "ALL_CHECKS", …)`). *"Emitting `0` here would report two well-tested organs
as untested, which is worse than emitting nothing: it manufactures a gap that would then get
'fixed'."* And `[NB2-C]` §5b **VERIFIED** — *"a cloud lane silently runs a *different* suite than the
operator's Windows host … emit the skip count **with the host capability vector**, not as a bare
number."*
*Blocks:* the telemetry v1 EMIT lane's correctness (§3).

---

## §3 · FUNCTIONAL REQUIREMENTS + OBJECTIVE FUNCTIONS

Per planned execution lane: what it must deliver, its measurable done-metric, and the **baseline the
metric moves from**. All timings from `[NB2-B]` are marked **INDICATIVE-cloud** exactly as that lane
marks them: *"cloud machine — INDICATIVE; ratios travel, absolute minutes do not"*.

---

### 3.1 · Wave-2 conversion lanes (7 lanes, 30 ids)

**Must deliver.** A replacement Done-when clause on each of `tasks/<id>-*.md` for its assigned ids,
taken from `[NB2-G]`'s drafts under D6.1, with the wave's stop condition honoured — `[NB2-E]` §11
**VERIFIED**: *"if a lane finds its conversion requires touching the grouped surface, it must stop
and report rather than proceed — that is the census's DEFECTIVE-not-improvised rule."*

**Done-metric.** `untestable` count falls from **58** to **≤29**.
- Baseline **58** — `[NB2-E]` K4 **VERIFIED**: *"Derivation recorded at `protocols/STANDING_RULINGS.md`
  §O-3: 95 − 39 (wave-1, JOURNAL-verified 6+13+9+11) + 2 (this window's filings as-written) = 58."*
  **Its honest limit, carried, UNVERIFIABLE-as-a-fresh-grade:** *"arithmetic over verified deltas, not
  a fresh re-grading pass."*
- Target **≤29** — `[NB2-E]` K5 **VERIFIED**: *"58 − 29 = 29. Arithmetically consistent, and reachable
  per A7."*
- Reachability, **VERIFIED** `[NB2-E]` A7: *"All 29 are graded **PROSE-CONVERTIBLE** in
  `docs/audits/2026-08-10-technical-backlog-testability-census.md` — **none** is PROSE-JUDGMENT or
  DEFECTIVE, so none falls into the judgment carve-out."*
- Open-set denominator **196** — `[NB2-F]` §0/§1 **VERIFIED** (169 live / 2 dead / 25 awaiting-ruling).

**Per-lane substrate.** `[NB2-E]` §9 supplies, per id, `P / Sz / serialize-group / wave-1 lane /
census note (what the draft must supply)`; `[NB2-G]` §3–§6 supplies the draft itself.

---

### 3.2 · Telemetry v1 EMIT lane

**Must deliver** (`[NB2-E]` §2, all **VERIFIED** against the memo):
- Stage-1 events `check_run` / `hook_run` / `blocker_fired` — B2: *"Memo lines 82/83/84 — items 1, 2,
  3 of the 8 event types, in that order."*
- SQLite WAL + structlog — B3: *"Memo line 52 (WAL, `journal_mode=WAL`, `synchronous=NORMAL`,
  `busy_timeout=5000`) and line 54 (structlog as the emit helper). Adoption table line 114/116 marks
  both **Adopt (v1 core)**."*
- Memo locator — B1: `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`,
  *"Present, 25,564 bytes. Landed `c3c7aa90`."*
- Contract of record — B4: `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:89`,
  Fold A, intake #29 `status: ACCEPTED`. **The `ROADMAP-2026-08-12.md` pointer inside the leg is
  STALE (X-18) — the live carrier is
  `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md`.**

**Done-metric.** `test_run` duration is emitted by a gate run and readable without re-measurement.
- Baseline **zero** — `[NB2-B]` §4b **UNVERIFIABLE (as marked)**: *"test-run cost inside a lane |
  **UNVERIFIABLE** | no `test_run` duration is emitted anywhere; §1–§3 had to re-measure from
  scratch."* NB2-B's own framing: *"this report is its own best argument."*
- A cheaper adjacent win, **PROPOSED** `[NB2-B]` §4b: *"A single `T_start` line — the one thing the
  handoff-cut lane did, per L-9 — converts the first row from UNVERIFIABLE to derivable at
  essentially zero cost. That is a cheaper intervention than the telemetry leg and does not depend on
  it."* Baseline for that row: **1 of 24 lanes records its dispatch time** (`[NB2-B]` §4 **VERIFIED**).

**Correctness constraints the lane must satisfy** — all `[NB2-C]`, all **VERIFIED**, all N-15:
- **M-3 (P2):** assert non-shallow and **refuse to emit** rather than emit a truncated git metric.
  *"A shallow clone does not produce an obviously-broken number — it produces a wrong number that
  looks fine."*
- **M-2 (P3):** for per-organ test coverage, either handle `getattr` lookup and `monkeypatch.setattr`
  registry injection explicitly, or *"emit `unknown` rather than `0`"*.
- **§5b (P3):** emit the skip count **with the host capability vector** — measured here:
  `git present → 33 skipif sites do NOT fire · grep present → 5 do not · pre-commit ABSENT → 7 DO
  fire · powershell ABSENT → 1 DOES · pandas ABSENT → 2 importorskip DO fire`.
- **L-6 (P3):** 9 tests use the raises-if-wrong idiom with no explicit assertion — *"any tool that
  *counts* assertions … will read these 9 as empty."*

**Organ inventory the lane consumes** — `[NB2-C]` §3 **VERIFIED**: **43 registered checks**, table
built from `scripts/audit.py`'s AST (`ALL_CHECKS` at `scripts/audit.py:4345`) *"so it cannot drift
from what actually runs"*; aggregates *"43 checks · 2,209 total span lines · median span 47 ·
`has-tests` **43 / 43 yes, 0 no**"*; `last-touched` range 2026-06-03 → 2026-08-14 (the 26-check
cluster at 2026-08-04 *"was checked and is genuine"* — `f020e0b9`, `4edbd7fe`).

---

### 3.3 · `[#528]` — lane-latency (P1/M, `serialize-group: environment`)

**Must deliver** — `[NB2-E]` C3/C4 **VERIFIED** from the live row: leg (1) *"gate-run call sites take
`-n auto --dist worksteal`"*; leg (2) *"tiered-suite rule written into PLAYBOOK/ESSENTIALS ('targeted
in-lane, ONE full suite at integration')"*; leg (3) *"emit `test_run` duration via the 2026-08-14
telemetry leg"*. **All three are required by the Done-when (X-17).**

**Done-metric and baselines** — `[NB2-B]`, **VERIFIED**, all **INDICATIVE-cloud**:

| quantity | value | locator |
|---|---|---|
| serial arm | **701.60 s (11m41s)**, wall 702 s | §1, `uv run pytest -n 0 --durations=50 -q` |
| parallel arm `-n auto` (4 workers) | **473.02 s (7m53s)** | §2 |
| ratio | **1.48×**, outcomes identical (14F·2874P·8S·1xf both arms) | §2 |
| xdist-unsafe failures | **none** — *"serial-only: (empty) / xdist-only: (empty) / common: 14 of 14"* | §2a |
| hard parallel floor | **268.74 s** — one test, `test_real_oracle_blocks_real_cross_module_removal` | §2b |
| structural ceiling | **2.6×** — *"No worker count can bring the full suite below ~4.5 minutes"* | §2b |
| tier-A targeted gate | **2797 tests (96.5 %), 154.64 s serial (22.1 %)**, `-n 4` lower bound **38.7 s** → *"~45–60 s wall, call it ~0.9 min"* | §3 |
| exclusion set | **5 files, 100 tests (3.5 %), 544.60 s (77.9 %)** — oracle tier (`test_safe_remove`, `test_reverse_dep_oracle`, `test_legibility_graph_conformance`) + corpus tier (`test_normalize_headers`, `test_toc`) | §3 |
| lane arithmetic | 4-leg lane: *"~5×473 s ≈ **39 min**"* → *"~4×50 s + 473 s ≈ **11 min**"* | §3 |

**Operator-host baselines the lane must move (NOT cloud figures)** — `[NB2-E]` L5 **VERIFIED**:
*"`JOURNAL.md:145` — 907.74s (~15m8s), `-n auto --dist worksteal`; `tasks/528-*.md` — 1001 s
(16:41)"*; and the recorded serial baseline `[NB2-B]` §0 **VERIFIED**: *"**1785.61 s (29m45s)**
(`pyproject.toml` `[tool.pytest.ini_options]` comment, measured 2026-08-06)"*.

**Three caveats `[NB2-B]` §3 will not paper over, VERIFIED:** (1) *"**A cost-split is not a
correctness-split.** A lane that touches `scripts/safe_remove.py` or `scripts/reverse_dep_oracle.py`
*must* run the oracle tier"* — that is `[#278]`; (2) *"**The existing `slow` marker does not express
this split**"* — it marks two files, *"**neither of which is in the top-10 cost list**"*; (3)
*"**The oracle tier is where 7 of the 14 failures live.**"*

**INFERRED, not measured — never upgraded** `[NB2-B]` §2b: *"The remaining 204 s is load imbalance —
INFERRED, not measured … I did **not** capture per-worker assignment, so this is a hypothesis
consistent with the arithmetic, not a measured fact."*

**A term outside `[#528]`'s current framing that dominated the window** — `[NB2-B]` §4a **VERIFIED**:
*"The four W4 conversion lanes did 16.7 / 21.9 / 24.9 / 28.5 minutes of work each — and then each
waited **231–244 minutes** to be merged … **Across those four lanes, ~92 minutes of work carried ~15
hours of aggregate queue time.** … **the dominant latency term was waiting for an integrator, not
running tests** — a finding `[#528]`'s framing does not currently cover."* And §4a(ii): lane `l`'s
1087.6 min *"is three sessions, not one long one … Two full dispatches produced **zero** landed legs
because a precondition was unmet."*

---

### 3.4 · `[#527]` — anti-direct-to-main mechanism (P2/S, `serialize-group: gates`)

**Must deliver** — `[NB2-E]` C2 **VERIFIED** from the live row's Done-when: *"a seeded direct commit
attempt on `main` is refused by a pre-commit hook, with a test, and the hook is armed via the
existing `arm_hooks.py`/`check_hooks_armed` mechanism."*

**Done-metric.** `[NB2-D]`'s six-case matrix (D5.3) passes as an acceptance table: E1 refused · E2
allowed · E3 clean `--no-ff` merge passes untouched · E4 conflicted merge on `main` allowed via the
`MERGE_HEAD` carve-out · E5 amend refused · W1 worktree-on-a-feature-branch allowed.

**Baseline: zero.** `[NB2-F]` §9 appendix, **VERIFIED**: *"| [#527] | … | 0 · **none** | live | born
2026-08-14; no pre-commit hook refuses a non-merge commit on `main` |"*.

**Precondition:** N-2 (`core.hooksPath`), which `[NB2-D]` marks **UNVERIFIABLE** for the operator's
host.

---

### 3.5 · Single-flight dispatch guard (no `[#id]` — D4.6 rules it in or out)

**Must deliver** (if ruled in) — a step-0 claim gate; `[NB2-D]` §1.5 supplies an 18-line sketch
(`scripts/single_flight.py`, exit `0` claimed / `3` already in flight / `2` internal error, **fail
CLOSED** *"matching `block_ff_push`'s posture since ADR-85 amend. 2026-08-03 §A6"*).

**Done-metric.** The T2 and T4 properties hold against the real `origin`: a second clone that never
fetched the ref is refused (`stale info`, exit 1), and the same-HEAD race does **not** return exit 0.

**Baseline: no guard exists, and the failure is witnessed.** `[NB2-D]` §1.1 **VERIFIED**: three
concurrent executions on 2026-08-14, two of which *"independently allocated `[#526]`–`[#529]` for the
same four filings."*

**UNVERIFIABLE, never upgraded:** the mechanism is proven against a local bare remote, **not against
GitHub** (`[NB2-D]` §0 limit 2, §5 residual 1).

---

## §4 · PARALLEL EXECUTION PLAN (PROPOSED)

**PROPOSED throughout.** Assembled from `[NB2-E]` §10–§11 (dispatch order + partition) and
`[NB2-G]` §3–§6 (the draft inventory each lane consumes). **Nothing in this table is a ruling**;
D4.9 is the pick, D4.7 settles the width, and N-1 … N-15 are the preconditions.

| lane | inputs it consumes | files it owns (disjointness) | blocks / blocked-by | suggested order |
|---|---|---|---|---|
| **W2-0 · draft review + landing** | `[NB2-G]` §3–§6 (30 drafts); the 4 forks D6.2–D6.5 | the draft artifact (already written on `claude/night2-wave2-drafts-fmbwa4`) | **blocks every conversion lane** (N-9); blocked-by D6.1 + D6.2–D6.5 | **first, and alone** — `[NB2-E]`: *"one full merge cycle (~16 min of suite) of hard serialization at the top of the wave"* |
| **[#528] legs (1)+(2)** | `[NB2-B]` §1–§3 (durations, tier split, exclusion set) | gate-run call sites; PLAYBOOK/ESSENTIALS tiered-suite paragraph. *"neither touches `tasks/`, so they collide with nothing in the wave"* | blocks nothing in the wave; **pays for it**. Leg (3) blocked-by the telemetry lane (N-11) | **position 0, beside W2-0** — D4.2 |
| **telemetry v1 EMIT** | intake #29 Fold A; the memo `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`; `[NB2-C]` M-2/M-3/§5b | new emit module + its tests | **blocked-by N-10** (row birth / contract-of-record naming); **blocks** `[#528]` leg (3) | after the row is born at boot |
| **[#527]** | `[NB2-D]` §3 (predicate + `MERGE_HEAD` carve-out + E1–E5/W1 matrix) | `scripts/block_commit_on_main.py` + its test + one `.pre-commit-config.yaml` entry. `serialize-group: gates` — *"no wave-2 collision"* | blocked-by N-2 (`core.hooksPath`) | **concurrent with the wave** — D4.4 |
| **W2-a** | drafts for `#409 #410 #411 #419` (Form R ×3 + the `[#419]` supersession) | `tasks/409-*.md` `tasks/410-*.md` `tasks/411-*.md` `tasks/419-*.md` | **blocked-by N-9 and N-12** (`tasks/419-*.md` also a D1.2 drain target, Y-3); D2.3's single ruling releases `#409/#410/#411` | **first among conversion lanes** — *"it carries the re-check, whose skip reason is the one the wave most risks repeating"* |
| **W2-b** | drafts for `#210 #285 #361 #364` | `tasks/210-*.md` `tasks/285-*.md` `tasks/361-*.md` `tasks/364-*.md` | blocked-by N-9; `#364` blocked-by D6.2 (and Y-2 — D1.1 may discharge its premise) | order-free |
| **W2-c** | drafts for `#146 #266 #438 #443` | `tasks/146-*.md` `tasks/266-*.md` `tasks/438-*.md` `tasks/443-*.md` | blocked-by N-9 | order-free |
| **W2-d** | drafts for `#351 #385 #393 #484 #502` | `tasks/351-*.md` `tasks/385-*.md` `tasks/393-*.md` `tasks/484-*.md` `tasks/502-*.md` | blocked-by N-9; `#502` blocked-by D6.5 (X-5) | **last** — *"its off-repo verdicts are the likeliest to escalate"* |
| **W2-e** | drafts for `#82 #145 #239 #263` | `tasks/82-*.md` `tasks/145-*.md` `tasks/239-*.md` `tasks/263-*.md` | blocked-by N-9; `#82` blocked-by D6.6 (home substitution) | order-free |
| **W2-f** | drafts for `#130 #274 #350 #417` | `tasks/130-*.md` `tasks/274-*.md` `tasks/350-*.md` `tasks/417-*.md` | blocked-by N-9; **`#417` blocked-by D6.4 / X-6** — if the clause is discharged this lane converts a row that should be closed | order-free |
| **W2-g** | drafts for `#271 #324 #391 #412 #491` | `tasks/271-*.md` `tasks/324-*.md` `tasks/391-*.md` `tasks/412-*.md` `tasks/491-*.md` | blocked-by N-9; `#391` blocked-by D6.3; `#324`/`#412` blocked-by D6.6 | order-free — *"the wave's heaviest (carries the one L)"* |

**Lane themes, verbatim from `[NB2-E]` §11** (why each set travels together): W2-a
*"`routine_consumers` family"* · W2-b *"audit-py check-surface"* · W2-c *"Doctrine-home family"* ·
W2-d *"Fleet / off-repo / environment"* · W2-e *"Enumeration family"* · W2-f *"Artifact-naming
family"* · W2-g *"Capture-and-home family"*.

**Disjointness proof.** `[NB2-E]` §11 **VERIFIED**: *"each id's file is touched by exactly one lane,
and each id appears exactly once across the seven lanes (30/30, verified by set-difference against
§9)."* **Re-checked by this consolidation** against both independent 30-id reconstructions
(`[NB2-E]` §9 and `[NB2-G]` §1/§3–§6): the sets are identical, the seven lanes partition them
4+4+4+5+4+4+5 = **30**, and no id appears twice. **The proof does not extend to Y-3** — `#419`'s file
is also claimed by D1.2's drain batch, which is not a lane in this table.

**Two couplings the partition does NOT dissolve, both already ruled** (repeated here because they are
execution-time facts, `[NB2-E]` §11 **VERIFIED**): every lane regenerates `BACKLOG.md`,
`tasks/manifest.json` and `docs/audits/README.md` — *"regenerate BACKLOG/manifest/audit-index at
merge, never hand-merge"*; and `serialize-group` is *"**not binding for this wave**"* with the
stop-and-report inverse as the condition.

**Totals** `[NB2-E]` §11 **VERIFIED**: *"7 conversion lanes, 30 ids, 4–5 per lane."* Plus W2-0, the
`[#528]` legs-1+2 lane, the telemetry lane and `[#527]` — the recommended reading of the width
question is *"**7 + 1**, stated that way so 'GO' is unambiguous"* (D4.7).

---

## §5 · PROVENANCE APPENDIX

**7 of 7 lanes present. No MISSING lanes.** Each branch was read via `git show <branch>:<path>`; no
branch was merged, and the seven remain unmerged on `origin`.

Branch-name note: the consolidation brief names the lanes in shorthand
(`claude/night2-hygiene`, …). The live refs carry generated suffixes; the mapping below is by
`git diff --stat main...<branch>`, each of which shows exactly one added report plus the mandated
`docs/audits/README.md` regen.

---

### NB2-A · hygiene sweep

- **Branch:** `origin/claude/night2-hygiene-sweep-8zgyjx` · **Report:**
  `docs/audits/2026-08-14-verification-night2-hygiene.md` (902 lines) · **Base:** `7bbb06748`
- **Final metric line, verbatim** (the report's last quantitative block, in
  `AMENDMENT 2026-08-14`; the file's final lines are prose, not a metric):

```
ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 45 new/undispositioned WARN(s))
pytest --collect-only          2897 tests collected   (doc-counts still claims 2895 — §2 holds)
gen_doc_counts --check         mismatch pytest_collected (file 2895 / actual 2897)
ruff check                     All checks passed!
session_end_backpressure.py    exit 0
```

- **UNVERIFIABLE / not-for-this-host items:** the 4 container artifacts (§0.2, *"do not paste"*,
  *"Re-derive on the operator host"*); the `hooks_armed` hard FAIL; the `review_artifact_coverage`
  item (§1.5, *"**A sweep cannot rule which.**"*); the `docs/handoffs/` index (§6.2, *"**needs a row
  first**"*, no row filed).
- **Self-correction to note:** the report's `AMENDMENT 2026-08-14` **withdraws** its own §0.3
  toolchain caveat and re-runs every derivation under the lock-pinned environment — *"**Result —
  nothing moved.**"* §0.1 and §0.2 are stated **UNAFFECTED**.
- **Disclosed edit beyond the report** (§6.1): the mandated `gen_audit_index.py --write` regen,
  *"a **2-line mechanical delta** (`504` → `505 audit documents`, plus this report's own row)"*.

---

### NB2-B · lane-latency

- **Branch:** `origin/claude/night2-latency-audit-6s1k6p` · **Report:**
  `docs/audits/2026-08-14-technical-night2-latency.md` (480 lines) · **Base:** `7bbb0674`
- **Final metric line, verbatim** (the file's last line):

```
**Serial 11.7 min vs xdist 7.9 min (ratio 1.48×) vs proposed targeted-gate ~0.9 min.**
```

- **UNVERIFIABLE items (never upgraded):** dispatch → first-commit for **23 of 24 lanes** (§4:
  *"dispatch leaves no repo artifact; author≡committer under one identity"*); **test-run cost inside
  a lane** (§4b); the three single-commit lanes' work duration (§4a(iii), *"not measurable at this
  resolution — Marked rather than imputed"*); the 204 s load imbalance (§2b, **INFERRED**); §3's
  tier-A figure (*"**derived arithmetic, explicitly not measured**"*). Every absolute figure carries
  *"cloud machine — INDICATIVE; ratios travel, absolute minutes do not"*.
- **Disclosed bypass, flagged by the lane itself** (§6): *"**THIS COMMIT USED `--no-verify`, and here
  is the whole reason.**"* — the `audit-health` hook blocks on a pre-existing, verified-by-stash
  `repos registered (none)` FAIL; *"The gates that actually govern this lane's artifact were armed and
  did pass"* (audits-index freshness, hermetization, dated-header normalisation).

---

### NB2-C · code quality

- **Branch:** `origin/claude/night2-quality-audit-8a3ixh` · **Report:**
  `docs/audits/2026-08-14-qa-night2-quality.md` (485 lines) · **Base:** `7bbb0674`
- **Final metric line, verbatim** (the file's last line):

```
**Findings: 0 HIGH · 3 MEDIUM (M-1, M-2, M-3) · 7 LOW (L-1 … L-7) · 10 total.**
```

- **UNVERIFIABLE items (marked by the lane, never upgraded):** **radon** (§2, *"`radon` is **not
  installed** … **No radon cyclomatic-complexity grade (A–F) is reported, and none should be inferred
  from this section.**"* — the branch-count column is *"**my own walk, not McCabe and not
  radon-calibrated**"*); **mutation results** (§4, no cached artifacts, `mutmut` not importable,
  *"**Not established here:** whether any specific CI run produced usable survivor output"*);
  suite pass/fail state (*"the suite was collected, not run … this document makes **no claim about
  pass/fail state**"*); the flake8 origin of the 102 dead directives (*"**inferred, not verified**"*).
- **Scope stated:** `deploy/`, `tests/`, `plugins/` were in the ruff and test-hygiene passes but
  **not** in §2's complexity ranking; module-level dead-code, duplication and dependency-cycle
  analysis were *"out of scope entirely"*.
- **Findings not otherwise surfaced above:** **M-1** `fleet_parity.collect_facts`
  (`scripts/fleet_parity.py:595`) at **88 branches** vs a population p99 of 23 — *"**not** proposed as
  a defect to fix"*, extraction offered as a P3 candidate; **L-1** 117 dead `# noqa: E402` directives
  (of 170 RUF100 hits; the other 53 are *"DEFENSIVE, not dead"*); **L-2** `_eval_row`
  (`scripts/fleet_parity.py:1131`) 210 lines, 0 docstring lines; **L-4** `check_review_artifact_coverage`
  153-line span, *"**not** a coverage concern"*; **L-5** the `43` count pinned at five sites across
  three files, three carrying the same ~1,900-char duplicated history comment; **L-7**
  `test_append_load_row_never_raises_on_unwritable_path` *"would pass unchanged if `append_load_row`
  became a no-op entirely"*; and two inert skip guards at `tests/test_gen_task_tree.py:42` / `:965`
  whose prose is stale.
- **Recorded so it is not mistaken for drift:** `ruff format --check .` reports *"**200 of 233 files
  would be reformatted**. This is **not** a finding"* — the landed spec gates `ruff check` only. And
  `ruff check --select ALL .` reports **19,320**, *"context for what 'clean' currently means, **not**
  a proposal"*.

---

### NB2-D · research

- **Branch:** `origin/claude/night2-research-d30vhu` · **Report:**
  `docs/audits/2026-08-14-technical-night2-research.md` (738 lines) · **Base:** `main` @ `7bbb067`
- **Final metric line.** This report **carries no closing metric line** — it ends with a Sources
  list. Its nearest quantitative summary, verbatim (§0):

```
Eleven git experiments (T1–T10, E1–E5, W1) were run live in this container against throwaway
repos, and their verbatim output is in §4. They are the load-bearing evidence for §1 and §3 —
not citations, not recollection.
```

  and the locked-version block (§4.5): `execnet 2.1.2 · pytest 9.1.1 · python pin 3.12.10 ·
  pytest-xdist 3.8.0 · pre-commit 4.6.1 · filelock 3.32.0 (already present, transitively) ·
  portalocker / pytest-cov / coverage / psutil — ABSENT`.
- **UNVERIFIABLE items (§0 limits + §5 residuals, never upgraded):** (1) *"**This lane runs on
  Linux.** Every Windows claim in §2 is derived from upstream *source* and from an upstream Windows
  bug report, not from a Windows run"*; (2) the §1 lock is *"verified against a local bare remote,
  not against GitHub"* — the closing probe is printed and deliberately not run; (3) `readthedocs.io`
  blocked by the container proxy; (4) the 19-stray count *"was not reproduced and its exact `-n` value
  is not known to this lane"*; (5) session-scoped-fixture exposure *"was not surveyed"*; (6)
  `core.hooksPath` on the operator's Windows checkout *"is unverified by this lane"*; (7)
  *"**Nothing here is ruled.**"*
- **Self-correction to note:** `AMENDMENT 2026-08-14` **A1** withdraws the report's own
  characterisation of the `canonical_freshness` FAIL (see X-2) with an explicit refusal to clear the
  six files; **A2** re-runs the hook stack under the pinned toolchain — *"**Passed (3)** … **Skipped
  (10)** … **Failed (1)** — `audit-health`, on the four pre-existing FAILs above and nothing else …
  **ZERO net-new, the FAIL set byte-identical to bare HEAD.**"*
- **Scratch hygiene, VERIFIED** (§0 limit 4): *"every probe repo and every probe worktree created by
  this lane was removed and removal verified"*.

---

### NB2-E · plan-check

- **Branch:** `origin/claude/night2-plancheck-audit-6ldr94` · **Report:**
  `docs/audits/2026-08-14-verification-night2-plancheck.md` (383 lines) · **Base:** `main`
- **Final metric line, verbatim** (§12, the file's closing block):

```
- **OK — 49**
- **STALE — 10** (A8, A9, B6, C5, D5, F3, G2, K8, M1, M2)
- **MISSING — 2** (A2 — the on-main twin; B5 — the telemetry owner row)

61 claims verdicted. Zero repo edits beyond this file and the regenerated
`docs/audits/README.md` index.
```

- **UNVERIFIABLE items (§0, never upgraded):** this lane ran on a **shallow clone (318 commits)** and
  did **not** un-shallow. *"Any check that walks `main`'s history under-reports here — `no_ff_merges`
  (1 vs the recorded 3), `review_artifact_coverage` (1 vs 2), `git_backlog_drift` (0 vs 1)."* The
  **full test suite was NOT executed** (K9 is arithmetic); K8's five `[stale]` dispositions are
  self-caveated as probably artifacts (X-9); K11's live WARN *"is not re-derivable in this clone"*.
  *"Content-only checks are fully trustworthy here … Those carry the load."*
- **Post-check control, VERIFIED:** *"`audit.py health` was re-run after this file was staged:
  **66 WARN / 4 FAIL** … **This report introduces zero new findings.**"*
- **Its own posture:** *"Not a ruling, not a recovery investigation, not an edit. … The dispatch-order
  and lane-partition sections at the end are a **proposal only** — the booted seat rules."*

---

### NB2-F · census

- **Branch:** `origin/claude/night2-census-audit-btqr42` · **Report:**
  `docs/audits/2026-08-14-census-night2-census.md` (623 lines) · **Base:** `main` @ `7bbb067`
- **Final metric line, verbatim** (the file's closing stamp):

```
**Generated** 2026-08-14 by the read-only night-2 census lane on
`claude/night2-census-audit-btqr42`, base `main` @ `7bbb067`.
**Zero edits beyond this file.** No close is executed by this artifact; every verdict above is
a proposal for the booted architect's P10 pass ([#506]).
```

  Its headline count (§1): `proposed live 169 · proposed dead 2 · proposed awaiting-ruling 25 ·
  total 196`.
- **UNVERIFIABLE / honest limits (§0, never upgraded):** (1) *"The 'last git touch of its task file'
  column is nearly uninformative, by construction"* — 84 of 196 share the migration date, 44 share
  the W4a–d date; *"**the first-parent-reference column is the one that carries signal**, and neither
  is a work-happened signal on its own"*; (2) *"A brand-new row shows zero first-parent references and
  that is correct, not stale"*; (3) *"This census verdicts rows against their own stated Done-when. It
  does not re-litigate whether a Done-when is the *right* finish line."* The first-parent column is
  *"a **mention** count, not a closure signal"*.
- **Un-shallowed before any measurement** (§0): 318 → **5,043 commits**, 1,441 first-parent, back to
  2026-03-30 — recorded as *"fresh evidence against"* `[#453]` leg (1).
- **The whole 196-row appendix is in §9** of the source report; it is not reproduced here. This
  briefing carries the grouped sets (D2) rather than the per-row table, and the architect should read
  §9 directly for any single id's one-line reason.

---

### NB2-G · wave-2 drafts

- **Branch:** `origin/claude/night2-wave2-drafts-fmbwa4` · **Report:**
  `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` (362 lines)
- **Final metric line, verbatim** (§8, first bullet — the file's last lines are the binding
  disclaimer):

```
- **30 drafts produced** — 29 needs-draft rows + the 1 `[#419]` re-check. **0 skipped.**
- **4 ambiguity-flagged** — `[#364]` `[#391]` `[#417]` `[#502]`, each drafted, each fork named (§7).
- **Form E applied 13×**, **Form R applied 6×**; 3 open home-substitutions listed in §2.
- **L14 re-resolve:** 30/30 verified `status: open` live before drafting.
```

- **UNVERIFIABLE / deliberately-unresolved items (never upgraded):** the four ambiguity forks (§7,
  *"None is a guess: each names the fork and leaves the resolution to the architect review"*), of
  which `[#417]` carries the strongest refusal — *"**This lane proposes neither**"*; the three open
  home-substitutions (§2); and the Form R honest limit (*"it does not claim the fleet's routines are
  consumed"*).
- **Two navigation notes for the architect reading the source:** its ambiguity register is **§7**
  while its four subsections are numbered **5.1–5.4**; and **an intra-lane numeric inconsistency** —
  §2's Form E header says *"applied 21 times there, **11 times here**"* while the same paragraph lists
  **13** ids and §8 states *"**Form E applied 13×**"*. The 13-id list and the §8 count agree; the
  "11" does not. Recorded rather than corrected, since this consolidation adjudicates nothing.
- **Its own posture:** *"**EVERY DRAFT BELOW IS A DRAFT.** … Nothing in this file has been written to
  any task file, and this lane has no authority to write one."*

---

### Consolidation provenance

- **Produced:** 2026-08-15, on `claude/night2-consolidation`, from `main` @ `7bbb0674`.
- **Inputs:** the seven reports above, read in full via `git show <branch>:<path>`. **No branch was
  merged.**
- **Edits:** this file, plus the `docs/audits/README.md` regen that the `audit-index-freshness`
  pre-commit hook mandates for any added `docs/audits/*.md` — the same obligatory mechanical
  companion all seven lanes took and disclosed. **No register, BACKLOG, `tasks/` or manifest write.
  No push to `main`.**
- **Derivations run against the live tree by this consolidation: zero.** The only checks performed
  were set-arithmetic over the lane reports themselves (the 30-id disjointness cross-check in §4 and
  the 45-entry dedup check in D1), both of which are aggregation, not adjudication.
