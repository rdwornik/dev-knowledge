# Backlog adjudication PREP — evidence sheets over the open set

**Date:** 2026-08-23 · **Class:** technical · **Lane:** CLOUD C3 (`backlog-adjudication-prep`) ·
**Branch:** `claude/backlog-adjudication-prep` · **Mode:** READ-ONLY, evidence only

> **This artifact issues NO verdicts.** Every disposition line below is a **lean**, labelled as
> such. The adjudication stays serial and stays with the architect. This lane assembled the
> evidence that makes 212 judgment calls cheap; it did not make them, and it closed nothing —
> no `status:` was flipped, no `tasks/manifest.json` node was removed, nothing under `tasks/`
> or `BACKLOG.md` was written.

---

## 1. Interpreter declaration

Probed, not assumed:

- `uv --version` → **`uv 0.8.17`**
- `pyproject.toml` `[tool.uv] required-version` → **`==0.11.19`**
- **MISMATCH.** The pinned `uv` is not present, so no `uv run --locked` mesh was available.
  Everything below was hand-run as `python3`.
- `python3 --version` → **`Python 3.11.15`**; `pyproject.toml` `requires-python` → **`>=3.12`**.
  The interpreter is also **below the declared floor**, a second divergence of the same
  ADR-106 class `[#484]` already names.

**Consequence, stated because it bounds the evidence:** `scripts/audit.py` does **not run** in
this container — `ModuleNotFoundError: No module named 'click'`. So no `audit.py` check was
executed here, and no row's lean rests on one. `scripts/validate_backlog.py` has no third-party
imports and **did** run; its output is the open-set authority used throughout.

## 2. The live open set

```
python3 scripts/validate_backlog.py
WARN  user story with no tasks — story "[S24] Declare desired state once, as data, inste" line 459
validate_backlog: OK (9 themes, 26 stories, 212 tasks, 1 warning(s))
```

`tasks/manifest.json` carries **486 nodes: 274 `prose`, 212 `{task, file}`** — the same 212, and
the membership-and-ordering authority the brief names. Theme and story on every row below are
read from the row's **manifest position** (the nearest preceding `## [E…]` and `### [S…]` prose
node), never guessed. 309 `.md` files sit under `tasks/`; the 97 with no manifest node render
into nothing and are **not** part of this sheet.

## 3. Method, and its honest limits

**Container repair performed first.** The repo arrived as a **shallow clone** — 321 commits,
history floor 2026-08-18. Under that clone, `git evidence` and `last touch` would have been
near-worthless for every row older than five days. `git fetch --unshallow` succeeded:
**5626 commits, full history**. Every sha below is from the recovered history.

**How `git evidence` was built.** One pass over `git log --all` with full bodies; every
`[#nnn]` occurrence in a subject or body indexed to its id; the result intersected with
`git log --first-parent main` so only merges that actually landed on main's spine are cited.
Merge subjects are reproduced **verbatim**, never paraphrased. Where a row has more than four
spine merges, the four most recent are shown and the remainder counted.

**How `acceptance` was extracted.** The `Done when:` clause of each `tasks/<id>-*.md` body, up
to the next top-level `·` separator, quoted in full. **All 212 rows have one** — there is no
`NONE` finding on this field, which is itself a measurement: the Done-when conversion waves
(W2/W4a–d, batch 6) reached the whole open set.

**Limits this sheet does not paper over:**

1. **Consumer repos are absent.** Only `rdwornik/dev-knowledge` is in scope. Any Done-when whose
   load-bearing clause is a *consumer-side* measurement (`[#244]`, `[#293]`, `[#332]`, `[#371]`,
   `[#463]`, `[#464]`, `[#82]`, …) cannot be discharged **or** refuted from here. Those rows
   lean `NEEDS-RULING` for that reason and the reason is stated on each.
2. **The gate mesh did not run** (§1). Rows whose acceptance is "check X reports zero …" were
   probed by reading the tree, not by running the check.
3. **Row-management classification is a regex, and regexes are approximations.** The split
   between a "row-management" merge (conversion / filing / drain / grooming / consolidation)
   and a substantive one drives cohort C4 vs C6. Where it misfires it misfires **toward** C6 —
   the cohort that gets per-row attention — so a row is never leaned `LIKELY-LIVE` on a
   mis-classified substantive merge without the merge subject being printed underneath it for
   the architect to read.
4. **Verbatim subjects, unverified content.** A merge subject is quoted as evidence *that the
   merge said this*, not as a claim that the merge did it. That distinction is the whole point
   of §5.

## 4. Coverage

- **Rows in the open set:** 212 (`validate_backlog`, live)
- **Rows carrying a full evidence line:** **212 of 212**
- **Rows marked `PREP-INCOMPLETE`:** **0** — every row's Done-when was specific enough that a
  deciding question follows from it without invention.
- **Boundary:** there is none inside the open set. The boundary is at the **edges** named in
  §3 — consumer-side clauses (no consumer repo) and check-output clauses (no runnable gate).
  Those rows are *prepped* (they carry every field) but their deciding question is answerable
  only with evidence this container cannot produce, and each says so.

## 5. The headline: **zero `LIKELY-DEAD` leans**, and that is a finding

| lean | count |
|---|---|
| `LIKELY-LIVE` | 114 |
| `NEEDS-RULING` | 98 |
| `LIKELY-DEAD` | **0** |
| `PREP-INCOMPLETE` | 0 |

**No row's quoted acceptance criteria were found discharged.** Not one. Under the bar the brief
sets — *a `LIKELY-DEAD` lean requires the merge's evidence to discharge the row's quoted
acceptance criteria, not merely to mention its id* — nothing cleared it.

This is not a null result; it **corroborates Phase 0's `banked = 0` from an independent
direction.** Phase 0 measured that no mechanical shortcut finds a closure. This lane measured
*why*: the ledger's mention-density is almost entirely **row-management traffic**.

Measured over the 212: **148 rows carry ≥1 spine merge naming their id.** Of those, **51 carry
row-management mentions ONLY** — conversion lanes, filing merges, drain passes, grooming arcs.
The single most-cited merge in the whole corpus is

```
a4fc652d 2026-08-13  Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane,
                     6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220]
                     [#277] [#278]
```

— a merge that **converted Done-when prose** on six rows and closed none of them. A detector
keyed on id-mention would read that subject as six closure signals. It is zero. This is the
same false-positive shape the brief warns about and that Phase 0's STRONG tier already failed
on twice, seen from the corpus side rather than the parser side.

**Twenty-one rows were probed live against the tree** rather than judged from merge subjects.
**Fourteen came back plainly unbuilt** — `[#227]` (still `protocols/AGENT_FRAMEWORK.md`),
`[#269]` (the audits index header *itself* says the count-tiered shape "is [#269] and is NOT
built"), `[#285]` (PLAYBOOK carries `reconciled_with:` only, no `last_reviewed`), `[#365]`,
`[#369]`, `[#470]`, `[#514]` (leg 1), `[#523]`, `[#537]`, `[#547]`, `[#551]`, `[#571]`,
`[#573]`, `[#577]`. **Seven came back partly-landed or blocked** — `[#244]`, `[#293]`,
`[#303]`, `[#324]`, `[#329]`, `[#332]`, `[#533]` — and each of those is leaned on the partial,
never on the whole. Each probe's command-level finding is written into that row's `lean` field
below rather than summarised here.

## 6. Cohort map

Rows are grouped by their **deciding question**, not by theme, so one architect answer applies
across a cohort. Sizes are exact and sum to 212.

| cohort | size | the question answered once |
|---|---|---|
| **C1** — ruling-dischargeable | **38** | May a new `protocols/STANDING_RULINGS.md` section be written **post-ratchet**? |
| **C2** — pegged / deferred | **34** | Is the peg live, met-and-spent, or dead — and does the row survive it? |
| **C6** — substantive merge present | **38** | Did the merge discharge the quoted criteria, or only one leg? |
| **C4** — row-management evidence only | **54** | Is there any evidence beyond conversion/filing traffic that this was built? |
| **C5** — no git evidence at all | **48** | Filed and forgotten, or still wanted? |

### C1 is the highest-leverage cohort in the set — and it is jammed on one unmade policy

38 rows — **18% of the whole open set** — carry a Done-when with an explicit OR-branch reading
*"…or `protocols/STANDING_RULINGS.md` carries a section naming `[#nnn]` and the reason."* Each
is dischargeable by **writing a ruling**, with no build at all.

That branch is currently unexercisable, and the repo says so in its own words. Both `[#344]`
and `[#491]` were deferred by the architect on **2026-08-22** with the identical annotation:

> DEFERRED 2026-08-22 (architect): held TOGETHER with its sibling on one unmade policy —
> **whether new `protocols/STANDING_RULINGS.md` sections may be written post-ratchet**

**One answer to that policy question changes the disposition of up to 38 rows.** If the branch
is open, a large fraction of C1 closes by ruling rather than by build — which is the single
largest lever this sheet found toward the sub-100 target. If it is closed, 38 Done-whens carry
a branch that can never be taken and need re-writing, which is a different and equally
actionable finding.

**Stated as a limit, not smuggled as a fact:** that annotation is recorded on `[#344]` and
`[#491]` only. Its extension to the other 36 C1 rows is **this lane's inference**, marked
`INFERRED` on every row it applies to.

### C2's pegs are visibly stale

Several C2 rows record their own peg as already met — `[#82]`, `[#145]`, `[#239]`, `[#297]` all
carry a variant of *"peg 'post-Wave-1' met 2026-07-07, one day BEFORE the peg was written"*, and
`[#117]` was un-deferred on a met peg. Those lean `LIKELY-LIVE`: the deferral no longer holds
them, and the work is simply unevidenced. Others point at referents that will not occur
(`[#325]`'s *"peg #221 DEAD, unreplaced"*, `[#322]`'s retired C4-research peg replaced by a dated
2026-09-09 review). **A peg census is a second cheap lever**, distinct from C1.

### C4 + C5 = 102 rows with no build evidence whatsoever

Nearly half the open set (48%) has **either no commit anywhere naming the id outside its own
task file, or nothing but row-management traffic**. These do not need investigation to
adjudicate — they need a want-it-or-not call. They are the cohort where the sub-100 target is
actually met or missed.

## 7. The trap, and what this lane refused to do

The brief names the failure mode: *do not lean `LIKELY-DEAD` because a row looks old or a merge
mentions its number.* Rows that would have tempted a mention-based detector, and were refused:

- **`[#332]`** — merge `2bc02196` reads *"merge: #328 fleet_parity checker + parity manifest +
  hub §9a declarations [#328] [#332]"*. `ecosystem/dependency-baseline.yaml` **does** exist and
  `scripts/fleet_parity.py` **does** read it. Two of three clauses look discharged. The third
  says *"with a test"* and `grep` over `tests/` returns **nothing**. → `NEEDS-RULING`, not DEAD.
- **`[#514]`** — exactly one `LANE_BRANCH_RE =` definition survives, which is precisely what leg
  3 asked for. Leg 1 (provisioning refusal) is unbuilt, and the row says so itself. →
  `LIKELY-LIVE`, not DEAD.
- **`[#533]`** — `scripts/audit_checks/` exists with 18 modules; the decomposition is genuinely
  under way. The byte-identical-`health` and preserved-order-**and**-count clauses are not
  verifiable without a runnable `audit.py`. → `NEEDS-RULING`.
- **`[#244]`** — three merge subjects say **SHIPPED** (`P2 remove leg`, `P3 … SHIPPED`,
  `P4 sync surfacing SHIPPED`). The Done-when's load-bearing clause is a *consumer-side*
  verified-ABSENT measurement. → `NEEDS-RULING`, with the reason named.
- **`[#324]`** — `65c9827e` reads *"#324 leg-c audit-corpus verb list"*. That is one leg of
  three. → `NEEDS-RULING`.
- **`[#293]` / `[#303]`** — the seeding merge `94f9307b` reads *"SEEDED THEN REVERTED on ADR-60
  conflict; row BLOCKED-ON-RULING"*. A mention-based reading would call `[#293]` shipped. It was
  reverted. → `NEEDS-RULING`, blocked on the ADR-60 ruling.

---

## 8. The evidence sheet

212 rows, one evidence line each, grouped by cohort. Within a cohort, rows appear in
`tasks/manifest.json` order (theme → story → position), so a cohort still reads down the
story map.

## Cohort C1 — Ruling-dischargeable — blocked on one unmade policy (38 rows)

**Shared deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#162] Vocab decision

- **id:** `[#162]`
- **title:** Vocab decision
- **theme / story:** [E1] Handoff continuity / [S1] Match the handoff payload to the work mode
- **status / size:** `open` · P2M · serialize-group `handoff`
- **acceptance (quoted):** "an ADR or a `protocols/STANDING_RULINGS.md` section lands the disambiguation, and each of `protocols/HANDOFF_BOOT.md`, `protocols/HANDOFF_PROCESS.md` §13, `ARCHITECTURE.md` Ch1 uses the ruled term with no surviving use of the superseded one"
- **last touch:** `449ad6b8` 2026-08-13 — "docs(tasks): W4a conversions — apply the 6 census P1/P2 drafts in the assigned set"
- **git evidence:** `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#344] Session-close gate for handoff generation + consumer hub-write guard

- **id:** `[#344]`
- **title:** Session-close gate for handoff generation + consumer hub-write guard
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `deferred` · P2M · serialize-group `handoff`
- **acceptance (quoted):** "Ask 1 and Ask 2 land as specified above (all preconditions met, each with a test); or protocols/STANDING_RULINGS.md carries a section naming [#344] and the reason for each Ask not built"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `7ef40567` 2026-07-31 — "Merge branch 'feat/382-desired-state-schema' — [#382] W1: ADR-109 accepted (fleet desired-state contract v1), sol independent derivation, intake #16/#22 NOTEs, [#344] fold-in"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
- **blocked on:** the unmade post-ratchet `STANDING_RULINGS.md` policy — RECORDED on this row: "DEFERRED 2026-08-22 (architect): held TOGETHER with its sibling on one unmade policy — whether new `protocols/STANDING_RULINGS.md` sections may be written post-ratchet"
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#350] Handoff-process refinements

- **id:** `[#350]`
- **title:** Handoff-process refinements
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P3S · serialize-group `handoff`
- **acceptance (quoted):** "(a) a non-CC browser can trigger a handoff and the path is documented in `protocols/HANDOFF_PROCESS.md`, (b) the handoff file-dependency class — a bundle citing a file that moved or was renamed — is detected by a check or recorded as accepted, and (c) each filed refinement carries a BACKLOG id; each of (a)/(b)/(c) landed, or `protocols/STANDING_RULINGS.md` carries a section naming `[#350]` and stating why it is deferred"
- **last touch:** `ce439780` 2026-08-16 — "docs(tasks): lane f — Done-when conversions for #130, #274, #350, #417 per W2 wave-2 drafts"
- **git evidence:** `8e8d55a2` 2026-08-16 — "Merge branch 'worktree-lane-f-130-conversions' -- batch 6 merge 5/11: [#130] [#274] [#350] [#417] Done-when conversions"
  - `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#346] Persist the two-tier new-path executor rule into `~/.claude`

- **id:** `[#346]`
- **title:** Persist the two-tier new-path executor rule into `~/.claude`
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `claude-md`
- **acceptance (quoted):** "`~/.claude/rules/` carries the two-tier new-path executor rule with a `verify:` line and the authorizing ruling cited in-file, or protocols/STANDING_RULINGS.md carries a section naming [#346] and the reason it stays hub-side"
- **last touch:** `8b04b6f1` 2026-08-13 — "docs(tasks): W4b batch 1/3 — mechanical Done-when for #338,#341,#344,#346,#347 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#349] Mechanize session-discipline inheritance

- **id:** `[#349]`
- **title:** Mechanize session-discipline inheritance
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a boot-injected + Stop-gated mechanism carries the test-then-close discipline with a test per leg, and one cold-session run is recorded in a docs/audits/ artifact; or this row is closed as folded into [#344] with the fold recorded in protocols/STANDING_RULINGS.md"
- **last touch:** `9ca3c8f3` 2026-08-13 — "docs(tasks): W4b batch 2/3 — mechanical Done-when for #349,#353,#356,#357,#358 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#353] Session-boot contract hardening

- **id:** `[#353]`
- **title:** Session-boot contract hardening
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a mechanism refuses a mid-session order whose side effects are not worktree-scoped while the tree is dirty or no worktree is declared, with a test seeding each of the two refusal conditions; or protocols/STANDING_RULINGS.md carries a section naming [#353] and the reason"
- **last touch:** `9ca3c8f3` 2026-08-13 — "docs(tasks): W4b batch 2/3 — mechanical Done-when for #349,#353,#356,#357,#358 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `ecc8b5aa` 2026-07-19 — "Merge feat/residual-completeness-gate — ARC-5's first enforcing mechanism @ 0a0d06de, 622baedb, e48e3e27, 2e444fa3, e2c2d9f7, cf17f6ad"
  - `8c913a6a` 2026-07-19 — "Merge docs/canon-inoculation — inoculate the four ARC-4 doctrine rulings into PLAYBOOK + ESSENTIALS (W6 seed 1)"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#484] ADR-106 system-Python divergence — named deferral, not an open build

- **id:** `[#484]`
- **title:** ADR-106 system-Python divergence — named deferral, not an open build
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P3M · serialize-group `environment`
- **acceptance (quoted):** "the system-vs-locked Python divergence is either closed on the operator's machines, evidenced by a recorded interpreter-version check on each, or `protocols/STANDING_RULINGS.md` carries a section naming `[#484]` stating the deferral reason; and the cp1252 console class is either fixed at the source — a stated encoding posture applied across `scripts/`, with a test asserting a non-ASCII glyph survives console output — or declared out of scope in that same section with its stated workaround"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `4ca67eed` 2026-08-16 — "Merge branch 'worktree-lane-d-351-conversions' -- batch 6 merge 7/11: [#351] [#385] [#393] [#484] [#502] Done-when conversions"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `4306a46a` 2026-08-04 — "Merge branch 'docs/file-484-485' — the two carried wrap items, filed not acted on"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#389] Prompt-lint — gate the five architect fields before a lane runs

- **id:** `[#389]`
- **title:** Prompt-lint — gate the five architect fields before a lane runs
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "a seeded prompt missing any one of the five ADR-87 §5 fields is refused or WARNed, with one test per field; and R6's disposition is recorded in ADR-87 or a `protocols/STANDING_RULINGS.md` section naming `[#389]`"
- **last touch:** `992891c4` 2026-08-13 — "docs(backlog): W4c batch 1/2 — Done-when conversions for #387, #389, #399, #408, #413"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `db878f4c` 2026-07-22 — "Merge docs/playbook-delivery-loop — [#386] delivery loop codified into PLAYBOOK (§21 spine + 4 in-place substances) + ride-along [#389] [#390] @ b4a373b3"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#425] The suite is green on a format the file does not use

- **id:** `[#425]`
- **title:** The suite is green on a format the file does not use
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "an artifact enumerates each parser-facing test corpus against the input forms its parser accepts, and every gap is closed with a negative-form fixture or listed there as justified; or `protocols/STANDING_RULINGS.md` carries a section naming `[#425]`"
- **last touch:** `cdbeb9a7` 2026-08-13 — "docs(tasks): W4d batch 1/2 -- Done-when conversions for [#425] [#428] [#430] [#453] [#456]"
- **git evidence:** `b5054945` 2026-08-16 — "Merge branch 'docs/batch6-wrap' -- batch-6 wrap acts (i)-(vii) + the ledger"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `09bce194` 2026-08-13 — "Merge branch 'docs/arc2b-ruled-micro-tail' — ARC2b executes the five ruled packet items, births [#524], and decides the dispatch shape [#508] [#524]"
  - `517e97ff` 2026-07-26 — "Merge docs/429-worktree-portability — file [#429] worktree provisioning portability [#429]"
  - (+1 further spine merges naming the id)
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#210] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule

- **id:** `[#210]`
- **title:** Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "the shape is recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#210]`, AND either (a) the `no_ff_merges` exemption ships with a test proving a JOURNAL-only direct commit passes while a same-commit code-path edit still WARNs, or (b) the wrap moves behind a `--no-ff` arc; and `ecosystem/disposition-register.yaml` carries none of the 3 journal-wrap per-instance entries"
- **last touch:** `18b2214c` 2026-08-16 — "docs(backlog): lane-b Done-when conversions for #210, #285, #361 (W2 wave-2 drafts, step 1)"
- **git evidence:** `40dd51d8` 2026-08-16 — "Merge branch 'worktree-lane-b-210-conversions' -- batch 6 merge 2/11: [#210] [#285] [#361] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `71c25d28` 2026-07-05 — "Merge docs/phase0-journal — Phase-0 integration JOURNAL entry (--no-ff wrap)"
  - `984ad66e` 2026-06-26 — "Merge chore/ratify-533109f-disposition -- ratify 3rd journal-wrap no-ff disposition + file [#210]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#408] Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOURNAL updates

- **id:** `[#408]`
- **title:** Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOURNAL updates
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a test seeds a close with no `ARCHITECTURE.md` and no `JOURNAL.md` edit and asserts the organ surfaces or blocks it, and a second test asserts a close carrying both passes clean; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#408]` and the reason"
- **last touch:** `992891c4` 2026-08-13 — "docs(backlog): W4c batch 1/2 — Done-when conversions for #387, #389, #399, #408, #413"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `b8957c98` 2026-08-06 — "Merge branch 'docs/supplement-fold-2026-08-06' — supplement folded, [#408] pointer filed, rider R-iii discharged"
  - `186efb5a` 2026-08-05 — "Merge branch 'chore/pre-seal-currency' — pre-seal doc-currency sweep + intake #24"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#418] `automation/fleet-audit` records 0–10 baselines a day, not one

- **id:** `[#418]`
- **title:** `automation/fleet-audit` records 0–10 baselines a day, not one
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "an audit artifact records a reproduction of the multiplicity with the observed per-day counts, and either a check FAILs on a second baseline for the same date (with a test) **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#418]` and why the multiplicity is acceptable"
- **last touch:** `6f06c8a5` 2026-08-13 — "docs(backlog): W4c batch 2/2 — Done-when conversions for #414, #415, #418, #423"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#417] `check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work

- **id:** `[#417]`
- **title:** `check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "the `history_specs`/`pathspecs` scope list at `_commit_routine_outputs` (`scripts/audit.py:4751-4760`) is extracted into a location shared with `check_dirty_tree`'s exclusion scope, narrowed to what the dirty-tree gate wants (not the wider `docs/audits/`-spanning branch-commit-helper scope), or `protocols/STANDING_RULINGS.md` carries a section naming `[#417]` and stating why the extraction was rejected"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** `8e8d55a2` 2026-08-16 — "Merge branch 'worktree-lane-f-130-conversions' -- batch 6 merge 5/11: [#130] [#274] [#350] [#417] Done-when conversions"
  - `bce5838a` 2026-08-15 — "Merge branch 'worktree-lane-s-w20-draft-landing'"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#414] Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored action (n=2 this week)

- **id:** `[#414]`
- **title:** Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored action (n=2 this week)
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2S · serialize-group `settings-json`
- **acceptance (quoted):** "a mechanism refuses or flags (a) a change to `main` with no recorded operator GO and (b) an unanchored change to `main`, with a test per case; and the organ choice is recorded in an ADR or a `protocols/STANDING_RULINGS.md` section naming `[#414]`"
- **last touch:** `6f06c8a5` 2026-08-13 — "docs(backlog): W4c batch 2/2 — Done-when conversions for #414, #415, #418, #423"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
  - `c74f918c` 2026-07-26 — "Merge docs/disposition-421-422 — dispositions for [#421]/[#422]/fleet_parity, [#430], and the SKIPPED-gate lesson"
  - `023520f0` 2026-07-24 — "Merge docs/lane-c-filings — Lane C filings [#406]-[#414] + self-acting-on-main incident repair (SHA-anchored, f3ead30b + c5910486) @ 438887e2"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#423] The integration sequence runs on prose every time, never mechanized

- **id:** `[#423]`
- **title:** The integration sequence runs on prose every time, never mechanized
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "the integration sequence's preconditions are enumerated in `plugins/tier1-lifecycle/commands/ship.md` and each is checked by `/ship` at run time with a test per precondition; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#423]` and which preconditions stay prose"
- **last touch:** `41c040b4` 2026-08-15 — "docs(backlog): step 1 -- drain 6 of 8 top-decile accretion rows (CONTRACT R)"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `c74f918c` 2026-07-26 — "Merge docs/disposition-421-422 — dispositions for [#421]/[#422]/fleet_parity, [#430], and the SKIPPED-gate lesson"
  - `ac798945` 2026-07-25 — "Merge docs/0726-cleanup — clear the orphaned #262 disposition; file [#423]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#239] Follow-up

- **id:** `[#239]`
- **title:** Follow-up
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "each of skills, commands (including `/codex-review`) and review-closure tooling either carries a `detect()` + versioned target-state that `scripts/enforcement_coverage.py` reports present-and-wired, or `protocols/STANDING_RULINGS.md` carries a section naming `[#239]` and stating that element's deferral reason"
- **last touch:** `4fb06a0d` 2026-08-16 — "docs(tasks): #82 conversions -- apply wave-2 census drafts to [#82] [#145] [#239] [#263]; regen BACKLOG+manifest"
- **git evidence:** `65cd26a0` 2026-08-16 — "Merge branch 'worktree-lane-e-82-conversions' -- batch 6 merge 4/11: [#82] [#145] [#239] [#263] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#443] Planning artifacts outside the three enforced classes carry no rent rule

- **id:** `[#443]`
- **title:** Planning artifacts outside the three enforced classes carry no rent rule
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `open` · P3S · serialize-group `playbook`
- **acceptance (quoted):** "each of handoff bundles, session plans and audit docs carries either a stated rent/binding rule at its canonical home — `protocols/HANDOFF_PROCESS.md` for bundles, `protocols/PLAYBOOK.md` for session plans and audit docs — or a section in `protocols/STANDING_RULINGS.md` naming `[#443]` that records it as deliberately-not-a-rule with its reason"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `b4862b9b` 2026-08-16 — "Merge branch 'worktree-lane-c-146-conversions' -- batch 6 merge 3/11: [#146] [#266] [#438] [#443] Done-when conversions"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `31fe0e01` 2026-07-28 — "Merge docs/intake-20-ratification — intake #20 ratified, #16 ACCEPTED/deferred, [#443] filed"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#456] Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR-108 §A

- **id:** `[#456]`
- **title:** Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR-108 §A
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "the cohort is enumerated as an explicit `[#id]` list in this row, and every member is either re-routed under ADR-108 §A, listed here as operator-owned with its reason, or named in a `protocols/STANDING_RULINGS.md` section citing `[#456]`"
- **last touch:** `cdbeb9a7` 2026-08-13 — "docs(tasks): W4d batch 1/2 -- Done-when conversions for [#425] [#428] [#430] [#453] [#456]"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#263] Protocols/edge-map reconciliation residuals

- **id:** `[#263]`
- **title:** Protocols/edge-map reconciliation residuals
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "`ecosystem/doc-code-edge.yaml` no longer carries the `mermaid_theme_directive` exempt entry or its stale comment word, the two `protocols/PLAYBOOK.md` 'per ESSENTIALS…English-only' refs and the `protocols/AI_COUNCIL_PROCESS.md` 'ESSENTIALS § Repo artifacts' ref each either resolve to live `protocols/ESSENTIALS.md` text or are recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#263]`, and `doc_code_coverage_drift` stays OK"
- **last touch:** `4fb06a0d` 2026-08-16 — "docs(tasks): #82 conversions -- apply wave-2 census drafts to [#82] [#145] [#239] [#263]; regen BACKLOG+manifest"
- **git evidence:** `65cd26a0` 2026-08-16 — "Merge branch 'worktree-lane-e-82-conversions' -- batch 6 merge 4/11: [#82] [#145] [#239] [#263] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#351] Fleet-Python-upgrade ticket

- **id:** `[#351]`
- **title:** Fleet-Python-upgrade ticket
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3M · serialize-group `pre-commit-config`
- **acceptance (quoted):** "a `docs/audits/<date>-technical-*` artifact defines the coordinated upgrade path across every member of the `adr104-fleet-members` declaration, and the newest-Python baseline is either raised for all of them in one arc — ruff `target-version` and the `pyproject.toml` required-version floor moving together — or `protocols/STANDING_RULINGS.md` carries a section naming `[#351]` with a stated next-review date"
- **last touch:** `0bacab02` 2026-08-16 — "docs(tasks): W2D lane -- Done-when conversions for [#351] [#385] [#393] [#484] [#502]"
- **git evidence:** `4ca67eed` 2026-08-16 — "Merge branch 'worktree-lane-d-351-conversions' -- batch 6 merge 7/11: [#351] [#385] [#393] [#484] [#502] Done-when conversions"
  - `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#338] codex-review drift consolidation

- **id:** `[#338]`
- **title:** codex-review drift consolidation
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `codex-review`
- **acceptance (quoted):** "each of (b), (c), (d), (e) as enumerated in this row is resolved with its evidence in the closing commit, or protocols/STANDING_RULINGS.md carries a section naming [#338] and that item's reason"
- **last touch:** `8b04b6f1` 2026-08-13 — "docs(tasks): W4b batch 1/3 — mechanical Done-when for #338,#341,#344,#346,#347 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
  - `a620d63e` 2026-07-16 — "merge: close [#333] doc-lane + file [#338] codex-review drift consolidation"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#341] Codex producer-lane activation mechanism

- **id:** `[#341]`
- **title:** Codex producer-lane activation mechanism
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `codex-review`
- **acceptance (quoted):** "(i)-(iv) as enumerated in this row are each resolved or named with their reason in a protocols/STANDING_RULINGS.md section citing [#341]; one activation run is recorded in a docs/audits/ artifact; and protocols/PLAYBOOK.md §16 describes the shipped mechanism"
- **last touch:** `8b04b6f1` 2026-08-13 — "docs(tasks): W4b batch 1/3 — mechanical Done-when for #338,#341,#344,#346,#347 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#412] Subagent / workflow routing + configured fan-out + online research into Anthropic's published commands/skills

- **id:** `[#412]`
- **title:** Subagent / workflow routing + configured fan-out + online research into Anthropic's published commands/skills
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "a `docs/audits/<date>-technical-*` artifact captures Anthropic's published command/skill set with a per-item fleet-adoption verdict, and a routing doctrine covering when to fan out, use a workflow, or use a subagent — configured fan-out included — is recorded in `protocols/PLAYBOOK.md`; or `protocols/STANDING_RULINGS.md` carries a section naming `[#412]` and stating why it is deferred"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `883618e5` 2026-08-17 — "Merge branch 'docs/window-close-final' -- window close: lane r, two births, priority order v2, the seat handoff"
  - `9997bc32` 2026-08-16 — "Merge branch 'worktree-lane-g-271-conversions' -- batch 6 merge 6/11: [#271] [#324] [#391] [#412] [#491] Done-when conversions"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#415] Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)

- **id:** `[#415]`
- **title:** Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "an audit artifact enumerates every test reading live repo content, and each enumerated test is either re-pointed to a committed fixture or listed in that artifact as an intentional integration smoke test with its reason; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#415]` and the blanket reason"
- **last touch:** `41c040b4` 2026-08-15 — "docs(backlog): step 1 -- drain 6 of 8 top-decile accretion rows (CONTRACT R)"
- **git evidence:** `b5054945` 2026-08-16 — "Merge branch 'docs/batch6-wrap' -- batch-6 wrap acts (i)-(vii) + the ledger"
  - `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `09bce194` 2026-08-13 — "Merge branch 'docs/arc2b-ruled-micro-tail' — ARC2b executes the five ruled packet items, births [#524], and decides the dispatch shape [#508] [#524]"
  - (+3 further spine merges naming the id)
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#453] Cloud night-run runbook — the container gaps that silently degrade an unattended session

- **id:** `[#453]`
- **title:** Cloud night-run runbook — the container gaps that silently degrade an unattended session
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `environment`
- **acceptance (quoted):** "`protocols/SESSION_SETUP.md` (or a named cloud runbook) records the three container gaps with a workaround each, and a session preflight performs the unshallow and asserts the `uv` pin with a test; or `protocols/STANDING_RULINGS.md` carries a section naming `[#453]` and which legs stay manual"
- **last touch:** `cdbeb9a7` 2026-08-13 — "docs(tasks): W4d batch 1/2 -- Done-when conversions for [#425] [#428] [#430] [#453] [#456]"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `b2329590` 2026-07-31 — "Merge branch 'docs/night-conformance-absorption' — audits index regen, ARCHITECTURE ADR-currency, [#462] filed, [#459] narrowed"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#347] Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern

- **id:** `[#347]`
- **title:** Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2M · serialize-group `playbook`
- **acceptance (quoted):** "the loop-harness is decomposed into filed `tasks/*.md` rows whose ids are listed in this row's closing commit, and the safe-deletion pattern is documented in protocols/PLAYBOOK.md or protocols/STANDING_RULINGS.md carries a section naming [#347] and the reason it stays unruled"
- **last touch:** `8b04b6f1` 2026-08-13 — "docs(tasks): W4b batch 1/3 — mechanical Done-when for #338,#341,#344,#346,#347 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#491] Gemini scanning lane — ruling R-G plus an acceptance contract

- **id:** `[#491]`
- **title:** Gemini scanning lane — ruling R-G plus an acceptance contract
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `deferred` · P3S · serialize-group `None`
- **acceptance (quoted):** "`protocols/STANDING_RULINGS.md` carries the R-G ruling in a section naming `[#491]`, and one acceptance run over real work — `[#487]`'s ranked sheet or the fleet dependency scan, read-only — is recorded in a `docs/audits/` artifact naming the load-bearing rows that were spot-verified and the outcome of that verification"
- **last touch:** `c4f888bc` 2026-08-23 — "docs(562): close [#562] REFUSED, land the admission verdict, annotate [#491]"
- **git evidence:** `9997bc32` 2026-08-16 — "Merge branch 'worktree-lane-g-271-conversions' -- batch 6 merge 6/11: [#271] [#324] [#391] [#412] [#491] Done-when conversions"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `1a4b11bb` 2026-08-08 — "Merge branch 'worktree-lane-seeded-defect-substrate' — Seeded-defect substrate inventory — 27 real instances, two gap lists [#491] [#492]"
- **blocked on:** the unmade post-ratchet `STANDING_RULINGS.md` policy — RECORDED on this row: "DEFERRED 2026-08-22 (architect): held TOGETHER with its sibling on one unmade policy — whether new `protocols/STANDING_RULINGS.md` sections may be written post-ratchet"
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#463] win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since admission

- **id:** `[#463]`
- **title:** win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since admission
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2S · serialize-group `environment`
- **acceptance (quoted):** "`python scripts/audit.py repo win-tooling` reports no FAIL and no WARN from `dot_prefix_discipline`, `canonical_freshness`, `workspace_settings` or `deployed_methodology_version`; or `protocols/STANDING_RULINGS.md` carries a section naming `[#463]` and the accepted reason per item"
- **last touch:** `ae531acf` 2026-08-13 — "docs(tasks): W4d batch 2/2 -- Done-when conversions for [#463] [#464] [#487] [#493] [#506] [#511]; 5 P3 skips recorded"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `13b98f22` 2026-07-31 — "Merge branch 'docs/fleet-audit-deep-review' — [#463][#464][#465] filed, [#460] recommendation recorded"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#464] corp-*/ai-council governance drift — five findings live 15–46 days, surfaced daily, zero consumption

- **id:** `[#464]`
- **title:** corp-*/ai-council governance drift — five findings live 15–46 days, surfaced daily, zero consumption
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2S · serialize-group `environment`
- **acceptance (quoted):** "each of the five findings enumerated in this row is absent from its repo's next fleet baseline, or `protocols/STANDING_RULINGS.md` carries a section naming `[#464]` and the accepted reason per finding"
- **last touch:** `ae531acf` 2026-08-13 — "docs(tasks): W4d batch 2/2 -- Done-when conversions for [#463] [#464] [#487] [#493] [#506] [#511]; 5 P3 skips recorded"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `13b98f22` 2026-07-31 — "Merge branch 'docs/fleet-audit-deep-review' — [#463][#464][#465] filed, [#460] recommendation recorded"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#409] Standing night batch — CODE review (formalize as routine)

- **id:** `[#409]`
- **title:** Standing night batch — CODE review (formalize as routine)
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the code-review night batch carries an ADR-105 `· routine:` block with all six fields populated (`trigger`/`scope`/`consumer`/`consumption_path`/`verified_by`/`review_date`) that `routine_consumers` passes — or it is ruled out in `protocols/STANDING_RULINGS.md` by a `###` section whose heading names `[#409]`, or by a line where `[#409]` carries a disposition token · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE)"
- **last touch:** `5c2c80e9` 2026-08-16 — "docs(tasks): wrap (vi) Form-E predicate repair + (v) [#533] leg 2"
- **git evidence:** `51d7fa08` 2026-08-16 — "Merge branch 'worktree-lane-a-409-conversions' -- batch 6 merge 1/11: [#409] [#410] [#411] [#419] Done-when conversions"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#410] Standing night batch — ARCHITECTURE review (formalize as routine)

- **id:** `[#410]`
- **title:** Standing night batch — ARCHITECTURE review (formalize as routine)
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the architecture-review night batch carries an ADR-105 `· routine:` block with all six fields populated (`trigger`/`scope`/`consumer`/`consumption_path`/`verified_by`/`review_date`) that `routine_consumers` passes — or it is ruled out in `protocols/STANDING_RULINGS.md` by a `###` section whose heading names `[#410]`, or by a line where `[#410]` carries a disposition token · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE)"
- **last touch:** `5c2c80e9` 2026-08-16 — "docs(tasks): wrap (vi) Form-E predicate repair + (v) [#533] leg 2"
- **git evidence:** `51d7fa08` 2026-08-16 — "Merge branch 'worktree-lane-a-409-conversions' -- batch 6 merge 1/11: [#409] [#410] [#411] [#419] Done-when conversions"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#411] Standing night batch — creative session, and the recurring Q&A cadence

- **id:** `[#411]`
- **title:** Standing night batch — creative session, and the recurring Q&A cadence
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the creative-session batch and the recurring Q&A cadence each carry an ADR-105 `· routine:` block with all six fields populated that `routine_consumers` passes — or each is ruled out in `protocols/STANDING_RULINGS.md` by a `###` section whose heading names `[#411]`, or by a line where `[#411]` carries a disposition token · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE)"
- **last touch:** `5c2c80e9` 2026-08-16 — "docs(tasks): wrap (vi) Form-E predicate repair + (v) [#533] leg 2"
- **git evidence:** `51d7fa08` 2026-08-16 — "Merge branch 'worktree-lane-a-409-conversions' -- batch 6 merge 1/11: [#409] [#410] [#411] [#419] Done-when conversions"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#537] `disposition token` is a Done-when branch nothing defines

- **id:** `[#537]`
- **title:** `disposition token` is a Done-when branch nothing defines
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the accepted tokens are enumerated where the predicate names them (or the branch is withdrawn), and a test asserts the `NIE` line at `STANDING_RULINGS.md:1353` does NOT satisfy the branch for `[#409]`"
- **last touch:** `b8bcae98` 2026-08-17 — "docs(tasks): birth [#537] -- `disposition token` is a Done-when branch nothing defines"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `LIKELY-LIVE` — live probe (this session) — "disposition token" occurs only in the three consuming rows and in [#537] itself — undefined at the predicate.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#356] RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declaration

- **id:** `[#356]`
- **title:** RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declaration
- **theme / story:** [E8] ARC-5 execution / [S21] Discharge the ARC-5 carried items that no wave has yet absorbed
- **status / size:** `open` · P2M · serialize-group `playbook`
- **acceptance (quoted):** "RULING-W and the merge-delegation composite each carry either a live mechanism with a test, or an entry in ecosystem/silent-rule-baseline.yaml with `owner:` and `review_date:` fields; and each carries a ratified ADR or a protocols/STANDING_RULINGS.md section naming [#356]"
- **last touch:** `9ca3c8f3` 2026-08-13 — "docs(tasks): W4b batch 2/3 — mechanical Done-when for #349,#353,#356,#357,#358 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `c0b40d37` 2026-07-28 — "Merge docs/recording-batch-2026-07-28 — recording batch: [E8] clause (b) AMENDED (D1), 7 conformance branches deleted (D2), North Star delta reviewed [#434] [#437] [#438]"
  - `9a3fb86b` 2026-07-19 — "Merge docs/arc5-census-filing — census declaration test + baseline into [E8], 6 tickets, [#355]/[#356] trimmed @ 45edaf07, 049aad7e, 00f86494"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#358] `ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD

- **id:** `[#358]`
- **title:** `ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "each of the three sites enumerated in this row states the post-[#337] blocking posture, or protocols/STANDING_RULINGS.md carries a section naming [#358] and the reason the divergence stands"
- **last touch:** `9ca3c8f3` 2026-08-13 — "docs(tasks): W4b batch 2/3 — mechanical Done-when for #349,#353,#356,#357,#358 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `c0b40d37` 2026-07-28 — "Merge docs/recording-batch-2026-07-28 — recording batch: [E8] clause (b) AMENDED (D1), 7 conformance branches deleted (D2), North Star delta reviewed [#434] [#437] [#438]"
  - `12ac9a48` 2026-07-27 — "Merge docs/session-prep-morning-loop — intake #19 verbatim, R12 ruled F1, [#436], next architect bundle"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#399] `templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)

- **id:** `[#399]`
- **title:** `templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `handoff`
- **acceptance (quoted):** "`templates/handoff/v5/README.md.tmpl`'s source claim matches what `scripts/seed_runbook.py` actually does — corrected, built, or recorded in a `protocols/STANDING_RULINGS.md` section naming `[#399]` — and the template's first line states whether it is live or superseded"
- **last touch:** `992891c4` 2026-08-13 — "docs(backlog): W4c batch 1/2 — Done-when conversions for #387, #389, #399, #408, #413"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#362] #242 carries a SUBSTANTIVE guard loss, not status hygiene

- **id:** `[#362]`
- **title:** #242 carries a SUBSTANTIVE guard loss, not status hygiene
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "the dropped-rule set is enumerated in this row or its closing commit, and each member is carried into a live surface, superseded by a named ADR, or recorded in a protocols/STANDING_RULINGS.md section naming [#362]; and [#242] does not reach a terminal status before this row does"
- **last touch:** `ca49020a` 2026-08-13 — "docs(tasks): W4b batch 3/3 — mechanical Done-when for #362,#366,#371 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `c0b40d37` 2026-07-28 — "Merge docs/recording-batch-2026-07-28 — recording batch: [E8] clause (b) AMENDED (D1), 7 conformance branches deleted (D2), North Star delta reviewed [#434] [#437] [#438]"
  - `12ac9a48` 2026-07-27 — "Merge docs/session-prep-morning-loop — intake #19 verbatim, R12 ruled F1, [#436], next architect bundle"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

### [#366] `residual_completeness` scans the WORKING TREE, not the staged blob

- **id:** `[#366]`
- **title:** `residual_completeness` scans the WORKING TREE, not the staged blob
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "`validate_residual_completeness` reads staged blob content at commit time, with a regression test seeding a staged-unfilled + working-filled pair that FAILs before the fix and passes after; or protocols/STANDING_RULINGS.md carries a section naming [#366] and the accepted limit"
- **last touch:** `ca49020a` 2026-08-13 — "docs(tasks): W4b batch 3/3 — mechanical Done-when for #362,#366,#371 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
- **blocked on:** the same unmade post-ratchet `STANDING_RULINGS.md` policy — INFERRED for this row (recorded explicitly only on `[#344]` and `[#491]`, 2026-08-22)
- **lean:** `NEEDS-RULING` — its Done-when carries an explicit `STANDING_RULINGS.md` OR-branch; whether that branch may be exercised is itself unruled.
- **deciding question:** May a new `protocols/STANDING_RULINGS.md` section be written post-ratchet — and if so, is this row's ruling OR-branch the intended discharge rather than the build?

## Cohort C2 — Pegged / deferred — peg liveness (34 rows)

**Shared deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#293] Consumer runbook fan-out

- **id:** `[#293]`
- **title:** Consumer runbook fan-out
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "each onboarded consumer carries the seeded runbook (per-repo tracked, n≥1 recorded)"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** `94f9307b` 2026-08-16 — "Merge branch 'worktree-lane-k-293-seeding' -- batch 6 merge 11/12: [#293] cross-repo seeding -- SEEDED THEN REVERTED on ADR-60 conflict; row BLOCKED-ON-RULING"
  - `dce393ec` 2026-08-15 — "Merge branch 'worktree-lane-q-293-satellite'"
  - `9e6ceb63` 2026-07-08 — "Merge feat/164-handoff-finish -- [#164] v5 /handoff generator FINISHED (7 legs): chat-title (leg e), v4-prose removal (leg g), hub-side runbook seeder (leg b)"
- **blocked on:** DEFERRED half of #164 leg b). UN-DEFERRED 2026-08-09 (ARC-2). **DENOMINATOR RULED at phase-1 integration (R6): 8, not 6** — ADR-104's declared non-hub members; ; the ADR-60 conflict ruling (its seeding merge records BLOCKED-ON-RULING)
- **lean:** `NEEDS-RULING` — live probe (this session) — its own seeding merge records "SEEDED THEN REVERTED on ADR-60 conflict; row BLOCKED-ON-RULING".
- **deciding question:** What is the ADR-60 ruling that the reverted seeding waits on?

### [#298] Handoff-generator polish

- **id:** `[#298]`
- **title:** Handoff-generator polish
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "(a) EPIC_BOOT renders an AUTO-PULLED BACKLOG-slice draft inside the FILL-IN, (b) a non-live `--epic-slug` leading id WARNs (not refuses), and (c) `--epic-slug` in an ignoring mode WARNs, each with a test"
- **last touch:** `cd38fb8a` 2026-08-09 — "docs(backlog): ARC-2 Phase A — the adjudication wave: closes [#213] [#215] [#441], 15 pegs ruled"
- **git evidence:** `71d3d7f7` 2026-07-08 — "Merge chore/consolidation-qa-intake-0708 -- consolidation + QA-intake (5 actions)"
- **blocked on:** DEFERRED 2026-08-09 (ARC-2): peg "next handoff-group pass" RAN this window and skipped this row; resolves N1 R-4
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#301] Session-plan artifact class

- **id:** `[#301]`
- **title:** Session-plan artifact class
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `deferred` · P2M · serialize-group `handoff`
- **acceptance (quoted):** "an architect bundle renders a PLAN.md skeleton, session-close fills the RETROSPECTIVE, and the v1→vN supersedes chain is exercised, each with a test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: #298 generator-polish arc
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#188] Deny-rule + hook completeness audit

- **id:** `[#188]`
- **title:** Deny-rule + hook completeness audit
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "a read-only pass emits a coverage matrix flagging any zone/path lacking a guard"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: #112 arc landed
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#499] Promote the review-artifact coverage leg to a hard pre-push gate

- **id:** `[#499]`
- **title:** Promote the review-artifact coverage leg to a hard pre-push gate
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "two consecutive windows are sealed with the leg's false-positive count reported and equal to 0, the hard leg lands with its own tests, **AND the coverage debt is discharged — the PLAYBOOK rule written, a `coverage_scope` entry replacing the TEMPORARY `ecosystem/doc-code-edge.yaml` exemption, and the `# rule: review-artifact-coverage` marker reinstated in `scripts/audit.py`** (rider R2 — this row owns the exemption's expiry so it cannot outlive its reason)"
- **last touch:** `23518240` 2026-08-05 — "docs(backlog): drain doc_rot accretion on four rows; disposition [#492] alone [#480]"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
  - `3a466bf7` 2026-08-06 — "Merge branch 'docs/handoff-2026-08-06-consolidation' — successor architect bundle cut; 2026-08-06 window closed"
  - `05450245` 2026-08-05 — "Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two declared routine rows are [#348] + [#426], the [#499]/[#500] cause refuted, and the 'exactly ONE row' boundary found stale at three sites; ruling — [#457] absorbs it, no new row"
  - `186efb5a` 2026-08-05 — "Merge branch 'chore/pre-seal-currency' — pre-seal doc-currency sweep + intake #24"
  - (+1 further spine merges naming the id)
- **blocked on:** peg: 0 false positives reported at two consecutive seals
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#139] merged-arc→record verifier

- **id:** `[#139]`
- **title:** merged-arc→record verifier
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `deferred` · P2L · serialize-group `audit-py`
- **acceptance (quoted):** "the verifier surfaces a seeded merged-arc lacking an item/closure/no-item-class, runs read-only (Layer-2), and is demonstrably NOT vacuous against real /ship merge subjects"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: #170
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#190] General intra-file duplication detector

- **id:** `[#190]`
- **title:** General intra-file duplication detector
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `deferred` · P3M · serialize-group `audit-py`
- **acceptance (quoted):** "a read-only check flags a seeded intra-file duplicated block (WARN, with tests), or it is explicitly closed as not-mechanizable"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: n=2 witnessed intra-file dup
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#169] Ungated-doc staleness detection

- **id:** `[#169]`
- **title:** Ungated-doc staleness detection
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "a deterministic staleness signal for the four ADR-85-ungated docs lands in the digest/dashboard"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: #171
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#171] Build the conformance dashboard at `ecosystem/conformance.md`

- **id:** `[#171]`
- **title:** Build the conformance dashboard at `ecosystem/conformance.md`
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "`ecosystem/conformance.md` is generated + committed by a read-only validator (Layer-2-safe) and ARCHITECTURE Ch2 carries the pointer"
- **last touch:** `cd38fb8a` 2026-08-09 — "docs(backlog): ARC-2 Phase A — the adjudication wave: closes [#213] [#215] [#441], 15 pegs ruled"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** DEFERRED 2026-08-09 (ARC-2): peg "post-Wave-1 n=2 consumers" met 2026-07-07; un-blocks the [#169]/[#322] chain
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#166] doctrine_enforcement_coherence check

- **id:** `[#166]`
- **title:** doctrine_enforcement_coherence check
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `deferred` · P3M · serialize-group `audit-py`
- **acceptance (quoted):** "the check ships read-only with fixtures + tests, folds into `audit.py health`, and flags a seeded enforcement-ahead-of-doctrine case"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: n=2 witnessed doctrine-mismatch
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#181] Coherence v2 nudge-response

- **id:** `[#181]`
- **title:** Coherence v2 nudge-response
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `deferred` · P2S · serialize-group `coherence`
- **acceptance (quoted):** "the nudge log shows real firing signal AND the response is decided + implemented, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: coherence-nudge.log has enough entries to adjudicate
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#218] Safe-removal gate M2+M3 boundary

- **id:** `[#218]`
- **title:** Safe-removal gate M2+M3 boundary
- **theme / story:** [E2] Enforced governance / [S6] Know what depends on code before removing it (ADR-89 computed edges)
- **status / size:** `deferred` · P1M · serialize-group `code-edge`
- **acceptance (quoted):** "the gate refuses a removal with an M2 referrer AND an M3 referrer on a fixture — non-destruction paths proven first and the destructive merge carrying its named operator authorization"
- **last touch:** `23518240` 2026-08-05 — "docs(backlog): drain doc_rot accretion on four rows; disposition [#492] alone [#480]"
- **git evidence:** `0bfa64b0` 2026-08-05 — "Merge branch 'chore/fr8-flip-batch' — FR-8 flip batch adjudicated [#498] [#489]"
  - `232dbe8c` 2026-06-26 — "Merge docs/file-195-successor — file [#218] safe-removal gate M2+M3 boundary (#195's deferred phases)"
- **blocked on:** peg: rides #487's first close batch (FR-8a)
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#117] Evaluate prompt/agent-based hooks

- **id:** `[#117]`
- **title:** Evaluate prompt/agent-based hooks
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "VF-1 passes and a go/no-go on a prompt-hook Tier-1 eval is recorded"
- **last touch:** `64ea92bb` 2026-08-11 — "docs(backlog): un-defer [#117] on its met peg, and record the two W2 register rulings"
- **git evidence:** `7f752a89` 2026-08-11 — "Merge branch 'docs/117-undefer-and-w2-rulings' — [#117] un-deferred on its met peg, and the two W2 register rulings recorded"
- **blocked on:** DEFERRED 2026-08-11 (operator ruling): peg `#270` MET at `7e4d503e` — the operator-load gauge landed and `[#270]` closed at `679d8eca`. Same treatment ARC-2 gav
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#310] Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold

- **id:** `[#310]`
- **title:** Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `deferred` · P3S · serialize-group `handoff`
- **acceptance (quoted):** "a sanctioned cold-annotation surface is defined AND the 07-05 architect bundle is recorded as-cold on it (no rendered bundle file edited, no retrospective fabricated)"
- **last touch:** `32445655` 2026-08-16 — "docs(ledger): finish-line acts for [#310] -- K1 declares, 14 permanent-defer re-annotations, kill-candidates + [#428] locator corrections"
- **git evidence:** `b150bfe4` 2026-08-16 — "Merge branch 'worktree-lane-h-310-ledger-docs' -- batch 6 merge 8/11: [#310] [#428] finish-line ledger acts -- K1 declares, 14 permanent-defer re-annotations"
  - `3b711e87` 2026-08-11 — "Merge branch 'docs/batch4-go-recording' — the batch-4 GO: intakes #28-#32 ratified as one act, [#513] amended as intake #30 §A's organ, [#521]/[#522] born"
  - `f91a4339` 2026-08-10 — "Merge branch 'docs/arc6-evidence-attachments' — ARC-6: two evidence attachments, and one unowned defect named rather than birthed"
  - `78ab77b4` 2026-08-09 — "Merge branch 'docs/arc3-hygiene-closeout' — ARC-3 hygiene close-out: closes verified real, seven carried writes landed, decision sheet cut [#519] [#520]"
  - (+1 further spine merges naming the id)
- **blocked on:** peg: post-Wave-1
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#240] Follow-up

- **id:** `[#240]`
- **title:** Follow-up
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `deferred` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "the leg WARNs when a consumer that showed `enforcing-local` for an organ regresses to `absent`, gated on a recorded baseline"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: mesh baseline n=2
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#267] Scope-exercising arc extension

- **id:** `[#267]`
- **title:** Scope-exercising arc extension
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "a consumer measurement shows both components FIRED under a scope-matching edit AND their `engages:` entries carry the scope condition"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `ffe4d875` 2026-07-06 — "Merge feat/267-scope-exercising-arc — #267 half-b (engages scope condition + observer tests); half-a DEGRADED (Block 5) [#267]"
  - `fb112667` 2026-07-06 — "Merge fix/g7-mirror-codex-highs -- Wave-3 close adjudication 4: G7 Codex 0 CRIT / 2 HIGH both fixed, suite 1323 green [#267] [#238] context"
  - `8e1dd571` 2026-07-06 — "Merge docs/2026-07-06-wave3-closure-declaration -- Wave-3 close: root declaration + 5 adjudications [#267] [#238] context"
  - `ff184e44` 2026-07-06 — "Merge docs/2026-07-06-wave3-step3-closure -- Wave-3 STEP-3 closure: FULL-COVERAGE measurement-3 audit, onboarding runbook template, [#267] filed, JOURNAL [#267] [#238] context"
- **blocked on:** DEFERRED — design decision, feasibility proven; measurement-4 memo.**
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#294] `validate_backlog` deploy-carrier + `--path` de-hardcode

- **id:** `[#294]`
- **title:** `validate_backlog` deploy-carrier + `--path` de-hardcode
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `deferred` · P3M · serialize-group `audit-py`
- **acceptance (quoted):** "`validate_backlog.py` takes a `--path`/`--repo` target AND either a carrier ships it to a consumer (validated green in-repo) or hub-only-by-design is recorded with a reason"
- **last touch:** `cd38fb8a` 2026-08-09 — "docs(backlog): ARC-2 Phase A — the adjudication wave: closes [#213] [#215] [#441], 15 pegs ruled"
- **git evidence:** `71d3d7f7` 2026-07-08 — "Merge chore/consolidation-qa-intake-0708 -- consolidation + QA-intake (5 actions)"
- **blocked on:** peg: the intake #25 W-wave carrier decision (W-2/W-3). Old peg named a "mesh-portability epic" existing nowhere but this row
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#297] Lightweight/dry `observe-arc` coverage mode

- **id:** `[#297]`
- **title:** Lightweight/dry `observe-arc` coverage mode
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "an `observe-arc` dry/coverage mode reports per-organ armed/fired state with no billed child spawn, with a test"
- **last touch:** `cd38fb8a` 2026-08-09 — "docs(backlog): ARC-2 Phase A — the adjudication wave: closes [#213] [#215] [#441], 15 pegs ruled"
- **git evidence:** `71d3d7f7` 2026-07-08 — "Merge chore/consolidation-qa-intake-0708 -- consolidation + QA-intake (5 actions)"
- **blocked on:** DEFERRED 2026-08-09 (ARC-2): peg "post-Wave-1" met 2026-07-07, one day BEFORE the peg was written
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#305] Add a verify-only / already-onboarded re-run mode to the onboarding runbook

- **id:** `[#305]`
- **title:** Add a verify-only / already-onboarded re-run mode to the onboarding runbook
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `deferred` · P3S · serialize-group `architecture`
- **acceptance (quoted):** "the runbook documents a verify-only re-run path AND assess runs on a dirty tree"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `e490275c` 2026-07-22 — "Merge docs/runbooks-collapse — genre collapse (docs/runbooks -> protocols/) + ADR-101 d.i reversal amendment [#304][#305][#300] repoints @ 9848a23b"
- **blocked on:** peg: a preflight split separating the assess gate from the execute gate
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#308] Decide the `verify` skill's canonical home

- **id:** `[#308]`
- **title:** Decide the `verify` skill's canonical home
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `deferred` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "the verify-skill home is decided (floor/plugin-distributed vs permanently hub-local) and recorded, at/along the P6 carrier step"
- **last touch:** `01410f94` 2026-08-09 — "chore(backlog): execute K-1/K-2/K-3 as ruled — zero closes, zero births"
- **git evidence:** `7e024317` 2026-08-09 — "Merge branch 'docs/arc2-consolidation' — ARC-2 Phases B–F: ADR-111 proposed, 229 items triaged, 3 rows born, net 0"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#325] Carry `/save` to consumers via a manifest command-artifact carrier

- **id:** `[#325]`
- **title:** Carry `/save` to consumers via a manifest command-artifact carrier
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `deferred` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "`/save` ships to a consumer via a manifest command-artifact carrier (verified present in-repo, n≥1) AND `/handoff`'s intentional absence is recorded with the ADR-42/ADR-36 reason"
- **last touch:** `01410f94` 2026-08-09 — "chore(backlog): execute K-1/K-2/K-3 as ruled — zero closes, zero births"
- **git evidence:** `7e024317` 2026-08-09 — "Merge branch 'docs/arc2-consolidation' — ARC-2 Phases B–F: ADR-111 proposed, 229 items triaged, 3 rows born, net 0"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#4] Build lessons-index.json + SessionStart retrieval + CLI query

- **id:** `[#4]`
- **title:** Build lessons-index.json + SessionStart retrieval + CLI query
- **theme / story:** [E3] Lessons feedback loop / [S9] Make lessons an active feedback loop, not a passive archive
- **status / size:** `deferred` · P2M · serialize-group `None`
- **acceptance (quoted):** "lessons are queryable + surfaced at session start"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: witnessed retrieval-miss after #185
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#144] Feature DoD = end-to-end / user-flow test

- **id:** `[#144]`
- **title:** Feature DoD = end-to-end / user-flow test
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "ADR-81 (d) carries an explicit E2E/user-flow clause (or deferral) AND the "in the cloud" target is resolved"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: first witnessed "deployed" dispute
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#145] Codification-completeness pass

- **id:** `[#145]`
- **title:** Codification-completeness pass
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "a `docs/audits/<date>-technical-*` artifact enumerates the fresh-session transmission gaps found across `protocols/PLAYBOOK.md` and the active handoff bundle, and every gap it enumerates carries either a BACKLOG id or a stated closure in that same artifact"
- **last touch:** `4fb06a0d` 2026-08-16 — "docs(tasks): #82 conversions -- apply wave-2 census drafts to [#82] [#145] [#239] [#263]; regen BACKLOG+manifest"
- **git evidence:** `65cd26a0` 2026-08-16 — "Merge branch 'worktree-lane-e-82-conversions' -- batch 6 merge 4/11: [#82] [#145] [#239] [#263] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `31fe0e01` 2026-07-28 — "Merge docs/intake-20-ratification — intake #20 ratified, #16 ACCEPTED/deferred, [#443] filed"
- **blocked on:** DEFERRED this window (ARC-2): peg "post-Wave-1" was met one day BEFORE the peg was written — dates deliberately omitted here, they push this row over the doc_ro
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#549] The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier

- **id:** `[#549]`
- **title:** The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `deferred` · P2S · serialize-group `None`
- **acceptance (quoted):** "intake #13 is either recorded SUPERSEDED with [E9]/ADR-109 named as the successor for the overlapping phases and any residue re-filed, or its `trigger:` is re-anchored onto a live id or a date — and if superseded, no living surface still cites it as the incoming sessions' comparison baseline"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** DEFERRED 2026-08-22 (architect): re-pegged to `[#572]` (intake-funnel completion) as its dated live trigger, replacing the spent peg; the SUPERSEDED-vs-re-ancho
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#19] Complete the ADR-39 register

- **id:** `[#19]`
- **title:** Complete the ADR-39 register
- **theme / story:** [E4] Decision management / [S12] Close the small ADR cross-reference + registry amendments
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "ADR-39 registry includes BACKLOG.md AND the templates/ class decision is recorded"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: first ADR-39 register lookup-miss
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#300] Hermetization residual d.ii

- **id:** `[#300]`
- **title:** Hermetization residual d.ii
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `deferred` · P1M · serialize-group `None`
- **acceptance (quoted):** "the mode-boot home is ruled AND the committed functional bundle's fate is landed (migrated or accepted, never drive-by-deleted)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `e490275c` 2026-07-22 — "Merge docs/runbooks-collapse — genre collapse (docs/runbooks -> protocols/) + ADR-101 d.i reversal amendment [#304][#305][#300] repoints @ 9848a23b"
  - `47f31b5c` 2026-07-10 — "Merge ship/lane-b-300 — #300 EPIC-I: ADR-101 hermetization draft (d.i/d.ii/d.iii), PROPOSED; rebased onto main, ratification + follow-up filing remain the operator's [#300]"
  - `1545c0d4` 2026-07-08 — "Merge chore/remediation-completion-0708 -- incident recovery + remediation completeness (5 actions): integrate stranded branch (408a9f8), file #299 G8 + #300 hermetization, QA-intake evidence [#299][#300]"
- **blocked on:** peg: BEFORE Wave-2
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#82] Define per-repository agentic-review profiles

- **id:** `[#82]`
- **title:** Define per-repository agentic-review profiles
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "every member of the `adr104-fleet-members` declaration carries a recorded agentic-review profile (which review runs, and on what cadence) at its stated home, and any member deliberately without one is named there with its reason"
- **last touch:** `4fb06a0d` 2026-08-16 — "docs(tasks): #82 conversions -- apply wave-2 census drafts to [#82] [#145] [#239] [#263]; regen BACKLOG+manifest"
- **git evidence:** `65cd26a0` 2026-08-16 — "Merge branch 'worktree-lane-e-82-conversions' -- batch 6 merge 4/11: [#82] [#145] [#239] [#263] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** DEFERRED 2026-08-09 (ARC-2): peg "per-repo at Wave-1 onboarding" met 2026-07-07 ([#221] closed), one day BEFORE the peg was written
- **lean:** `LIKELY-LIVE` — the row records its peg as met/spent/un-deferred, so the deferral no longer holds it — the work itself is unevidenced.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#231] Consumer → hub feedback report

- **id:** `[#231]`
- **title:** Consumer → hub feedback report
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `deferred` · P3M · serialize-group `None`
- **acceptance (quoted):** "a consumer that hits a methodology gap/ambiguity/broken-piece emits a structured hub-destined report (schema + destination defined) rather than guessing"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `7cc4b6a6` 2026-07-01 — "Merge docs/handoff-capture — pre-handoff capture: #226(a) floor-provisioning DECIDED (model A) + file #230 end-to-end conformance self-test + #231 consumer->hub feedback report + #221 sequencing (depends-on #226, #230 acceptance gate); doc-only [#226][#230][#231][#215][#221]"
- **blocked on:** peg: first witnessed consumer-gap report
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#102] Machine-readable repo index for agent consumption

- **id:** `[#102]`
- **title:** Machine-readable repo index for agent consumption
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `deferred` · P2M · serialize-group `None`
- **acceptance (quoted):** "a pilot index on one repo demonstrably replaces exploratory reads in a CC session"
- **last touch:** `01410f94` 2026-08-09 — "chore(backlog): execute K-1/K-2/K-3 as ruled — zero closes, zero births"
- **git evidence:** `7e024317` 2026-08-09 — "Merge branch 'docs/arc2-consolidation' — ARC-2 Phases B–F: ADR-111 proposed, 229 items triaged, 3 rows born, net 0"
- **blocked on:** peg: a repo whose codemap is generator-MANAGED (#262/#295 closed 2026-07-25 — flat / single-package layouts stay hand-authore
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#322] Fleet dashboard

- **id:** `[#322]`
- **title:** Fleet dashboard
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `deferred` · P2M · serialize-group `settings-json`
- **acceptance (quoted):** "the three legs are decided (data sources named, viz layer C4-ruled, surfacing habit chosen) AND a minimal dashboard renders from live fleet data with a surfacing hook"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#403] Extend `doc_claims` to ARCHITECTURE's machine-derivable claims

- **id:** `[#403]`
- **title:** Extend `doc_claims` to ARCHITECTURE's machine-derivable claims
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "carrier-set AND child-roster gated (doc_claims or a regen-and-diff sibling) with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `44e47b48` 2026-07-23 — "Merge docs/architecture-currency — ARCHITECTURE claim-drift verify-then-fix: carrier count 4->5 (5 sites) + Ch4 channel/carrier vocabulary split, child roster +win-tooling, ADR ceiling 80->103, Governing-ADRs +98/+101/+102-103 + ADR-43/ADR-92 annotations, #398 repoint, PLAYBOOK-Appendix-B qualifier; file [#403] [refs #403]"
  - `2802e401` 2026-07-23 — "Merge chore/consolidation-reconcile — BACKLOG next-free pointer [#403] + [#401] doc_rot trim (post-merge consolidation surface fixes) [refs #401]"
- **blocked on:** DEFERRED (a citation is not a governing relation).
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#492] Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs

- **id:** `[#492]`
- **title:** Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `deferred` · P3S · serialize-group `None`
- **acceptance (quoted):** "the comparison has run on ≥1 real diff set post-4.6 and the lane is admitted or refused on the measured result"
- **last touch:** `59df6478` 2026-08-18 — "docs(backlog): STEP 2 batch 2 -- trim 6 rows under the 1320 ceiling"
- **git evidence:** `d62796ad` 2026-08-15 — "merge boot-acts 2026-08-15: gate 41->11, closes #524 #352, births #529 #530, threshold 1320"
  - `5c6bc70d` 2026-08-13 — "Merge branch 'worktree-lane-e-492-corpus-reconciliation' — CORPUS-492: the seeded-defect corpus reconciles to the landed spec, 12/12 re-pinned, 0 flips [#492]"
  - `1a4b11bb` 2026-08-08 — "Merge branch 'worktree-lane-seeded-defect-substrate' — Seeded-defect substrate inventory — 27 real instances, two gap lists [#491] [#492]"
  - `e676cd3f` 2026-08-05 — "Merge branch 'feat/480-review-artifact-organ' — review-artifact coverage made checkable [#480] [#499] [#500]"
- **blocked on:** peg: the Grok 4.6 release ALONE — the calendar leg is SPENT and dropped; release is an external fact, OPERATOR (N1 R-5)
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

### [#495] Tech-currency cadence — give [#385] a recurring lane instead of a one-off

- **id:** `[#495]`
- **title:** Tech-currency cadence — give [#385] a recurring lane instead of a one-off
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S27] Make tech-currency a distributed rule, not a one-off
- **status / size:** `deferred` · P3S · serialize-group `None`
- **acceptance (quoted):** "the cadence is ruled (monthly vs event-driven vs rejected) and, if adopted, the lane has a declared consumer and consumption path per ADR-105"
- **last touch:** `4ca1ca23` 2026-08-05 — "docs(backlog): FR-8 flip batch — 8 rows opened, 3 re-pegged, [#489] retired into re-scoped [#218], [#498] filed"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** peg: rules with the #385 arc
- **lean:** `NEEDS-RULING` — the row is held by a peg whose liveness only the architect can call.
- **deciding question:** Is this row's peg live, met-and-spent, or dead — and does the row survive the answer?

## Cohort C6 — Substantive merge present — partial-discharge check (38 rows)

**Shared deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#511] The 30-minute handoff cut is ~99.8% session authoring, not machinery

- **id:** `[#511]`
- **title:** The 30-minute handoff cut is ~99.8% session authoring, not machinery
- **theme / story:** [E1] Handoff continuity / [S1] Match the handoff payload to the work mode
- **status / size:** `open` · P2M · serialize-group `handoff`
- **acceptance (quoted):** "`protocols/HANDOFF_PROCESS.md` carries the ruled cut of the NON-MECHANIZED loads with a version bump and dependents re-stamped (`reconciled_versions` green), and one post-change handoff records measured wall-clock and token cost against the recorded baseline in its bundle"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `4314782a` 2026-08-11 — "Merge branch 'docs/arc9-lane-ingest' — ARC-9 queue lane 5 (last): research corpus archived + distillate + [#511] commission-5 attachment"
  - `8c438220` 2026-08-07 — "Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: three fixed, one dispositioned, one filed [#505] [#511] [#512]"
  - `b669bd8f` 2026-08-07 — "Merge branch 'docs/handoff-engine-thinning' — the bundle carries pointers, the repo carries law; HANDOFF_PROCESS v6.1.0 [#505] [#511]"
  - (+1 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#390] Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template

- **id:** `[#390]`
- **title:** Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P2S · serialize-group `handoff`
- **acceptance (quoted):** "ADR-87 carries the resolution AND the template matches it"
- **last touch:** `52d230cc` 2026-08-13 — "docs(backlog): ARC2b step 1 — condense the four over-cap rows, then write the frozen ARC2 step-3 obligations in"
- **git evidence:** `bbacd6c0` 2026-08-11 — "Merge branch 'docs/arc9-qset-applications' — apply Q1-Q4: [#419]/[#426] organ amendment, [#241]/[#390] blocks, [#360] re-anchor, [#505] clause-2 re-peg + I-D3"
  - `db878f4c` 2026-07-22 — "Merge docs/playbook-delivery-loop — [#386] delivery loop codified into PLAYBOOK (§21 spine + 4 in-place substances) + ride-along [#389] [#390] @ b4a373b3"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#447] Self-referential gate family — the committing act cannot satisfy the gate's own precondition

- **id:** `[#447]`
- **title:** Self-referential gate family — the committing act cannot satisfy the gate's own precondition
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P3S · serialize-group `gates`
- **acceptance (quoted):** "one commit can raise a ratchet and be judged by the raised value, and a wrap commit can satisfy its own anchor gate, with tests"
- **last touch:** `645822ba` 2026-07-30 — "docs(protocols): transcribe the [#446] RESIDUAL §4 debts (a)(b)(c)(e)"
- **git evidence:** `a54994a3` 2026-07-30 — "Merge branch 'docs/handoff-2026-07-31-architect-2' — closing handoff + intake #22 SEED"
  - `ebda157e` 2026-07-29 — "Merge branch 'chore/447-row-trim' — [#447] row under the doc_rot cap + the 2nd instance absorbed"
  - `e69ad59b` 2026-07-29 — "Merge branch 'docs/vscode-w1-execution-record' ([#435] RULING-W .vscode W1 execution)"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#422] `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves

- **id:** `[#422]`
- **title:** `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P2S · serialize-group `handoff`
- **acceptance (quoted):** "a post-fold check FAILs on a bundle carrying cold-state framing prose after a FILLED flip (a `--check`-shaped leg wired where the fold runs), pinned by a test seeding a hand-authored cold claim in `PROBES.md`"
- **last touch:** `27ec8bc5` 2026-07-30 — "groom(backlog): arc 0731-g0-groom — 6 rows condensed, 5 dispositions retired, doc_rot clean [#426]"
- **git evidence:** `3b711e87` 2026-08-11 — "Merge branch 'docs/batch4-go-recording' — the batch-4 GO: intakes #28-#32 ratified as one act, [#513] amended as intake #30 §A's organ, [#521]/[#522] born"
  - `b4dd3e48` 2026-07-27 — "Merge docs/window-close-batch — ARCHITECTURE currency, MERGE IS ATOMIC codified, supplement folded"
  - `c74f918c` 2026-07-26 — "Merge docs/disposition-421-422 — dispositions for [#421]/[#422]/fleet_parity, [#430], and the SKIPPED-gate lesson"
  - `d5ef97d0` 2026-07-26 — "Merge docs/hub-defects-handoff-tooling — recover intake #17 + [#421] [#422] from the misfiled branch"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#401] ai-council routing still ARMED at the deleted hub landing zone

- **id:** `[#401]`
- **title:** ai-council routing still ARMED at the deleted hub landing zone
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "(a) shipped in ai-council AND (b) built per this ruling"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `19cf25dc` 2026-07-25 — "Merge docs/401b-anchor — JOURNAL merge-SHA anchor for the [#401] clause (b) ruling c5f65165 (refs #401)"
  - `c5f65165` 2026-07-25 — "Merge docs/401b-ruling — [#401] clause (b) ruled: routing.py PATH-REFUSAL (refs #401, does NOT close)"
  - `2802e401` 2026-07-23 — "Merge chore/consolidation-reconcile — BACKLOG next-free pointer [#403] + [#401] doc_rot trim (post-merge consolidation surface fixes) [refs #401]"
  - `eefb9f9c` 2026-07-23 — "Merge docs/adr43-rescope-transcripts-routing — ADR-43 amendment: routed-mirror clause retired (re-scope, not retirement); 8 PLAYBOOK + ESSENTIALS + AI_COUNCIL_PROCESS v2.1 + decisions-README/ARCHITECTURE repoints; file [#401] ai-council routing armed at deleted hub zone [refs #401]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#424] Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare

- **id:** `[#424]`
- **title:** Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "every `depends-on` clause parses, a regression test pins the bare-id form, and the `plugins/tier1-lifecycle` twin moves in lockstep"
- **last touch:** `808ef911` 2026-08-03 — "docs(backlog): ratify [#383] — caches-wave record, replacement Done-when, dangling-edge fix"
- **git evidence:** `09bce194` 2026-08-13 — "Merge branch 'docs/arc2b-ruled-micro-tail' — ARC2b executes the five ruled packet items, births [#524], and decides the dispatch shape [#508] [#524]"
  - `42ff1323` 2026-08-03 — "Merge branch 'docs/383-ratify-caches-wave' — ARC 0: [#383] ratified, caches wave named, [#424] trap cleared"
  - `153eae1a` 2026-07-27 — "Merge docs/lane-filings-uv-bakeoff-extraction — three lane tickets [#432][#433][#434] + the uv/rtk/pilot-precedes-contract rulings"
  - `903638c5` 2026-07-26 — "Merge docs/0726-brake-discharge — [E9] brake discharged, ADR-105 activation gate, [#419] given teeth"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#510] Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today

- **id:** `[#510]`
- **title:** Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `gates`
- **acceptance (quoted):** "the exemption resolves against a lane roster the open manifest declares, the no-roster posture is ruled and encoded, a test proves a lane branch OUTSIDE the roster is not exempt mid-batch, and Ch8 + the manifest template carry the field"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** `0136cec6` 2026-08-11 — "Merge branch 'worktree-lane-a-514-lane-regex' — batch-4 W1: one strict LANE_BRANCH_RE, defined once and imported [#514] [#510]"
  - `8c438220` 2026-08-07 — "Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: three fixed, one dispositioned, one filed [#505] [#511] [#512]"
  - `25ff8ec3` 2026-08-07 — "Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 rows filed, 0 closed [#505] [#430]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#514] Two rival `LANE_BRANCH_RE` constants ship in one repo

- **id:** `[#514]`
- **title:** Two rival `LANE_BRANCH_RE` constants ship in one repo
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P1M · serialize-group `None`
- **acceptance (quoted):** "provisioning refuses an off-enum lane name, one clean batch runs under it, and exactly ONE definition remains · **W1 DISCHARGE 2026-08-11 (batch-4 lane A) — leg 3 DONE:** exactly one binding survives, pinned by four tests; re-measured over main's first-parent spine **9 of 16 disagree**, not the row's stale 8-of-11. **Leg 1 NOT discharged** — a lane dispatched straight through `claude --worktree` never reaches `/lane-boot`'s check and the `KIND_UNKNOWN` BLOCK is unbuilt. **B1 2026-08-18: leg 1 unbuilt — 2 of 8 lanes off-grammar (F,G), renamed**"
- **last touch:** `fce8b5b0` 2026-08-18 — "docs(backlog,register,intake): batch-1 seat closure acts -- 6 rows banked, 0 births [#556] [#557] [#558] [#502] [#536]"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `0136cec6` 2026-08-11 — "Merge branch 'worktree-lane-a-514-lane-regex' — batch-4 W1: one strict LANE_BRANCH_RE, defined once and imported [#514] [#510]"
  - `7e024317` 2026-08-09 — "Merge branch 'docs/arc2-consolidation' — ARC-2 Phases B–F: ADR-111 proposed, 229 items triaged, 3 rows born, net 0"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — exactly ONE `LANE_BRANCH_RE =` definition survives (leg 3 discharged); leg 1 provisioning refusal still unbuilt, as the row itself records.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#531] Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it

- **id:** `[#531]`
- **title:** Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `gates`
- **acceptance (quoted):** "creating a `refs/heads/worktree-lane-*` branch whose name is off-grammar is REFUSED at creation with the reason, a conforming name is unaffected, non-lane ref updates are untouched, the escape is explicit and non-silent, and `/lane-boot` step 1 is stated as the friendly pre-check rather than the enforcement point"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** `43cd1cee` 2026-08-16 — "Merge branch 'chore/phase2-d1v2-amendment' — D-1v2: [#533] born, batch-6 roster 12 -> 11"
  - `d137cc6a` 2026-08-16 — "Merge branch 'chore/phase2-position0' — phase-2 Position 0, seven acts"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#533] Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry

- **id:** `[#533]`
- **title:** Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "every mechanically-extractable check lives in `scripts/audit_checks/<check_name>.py` with the module named for the check, an ordered registry preserves today's `ALL_CHECKS` order AND count, `audit.py` retains every public entrypoint and CLI verb byte-compatibly, `audit.py health` output on an unchanged tree is BYTE-IDENTICAL before and after, targeted tests for every touched surface are green, and any check that resists mechanical extraction is LEFT IN THE FACADE and REPORTED rather than redesigned mid-lane"
- **last touch:** `25102406` 2026-08-22 — "docs(audits,backlog): S3 -- the annotation-and-rulings ledger, and five rows pointer-ized"
- **git evidence:** `f4a01f0e` 2026-08-18 — "Merge branch 'worktree-lane-a-533-leg2' -- [#533] leg 2: journal_anchor memoization + opt-in parallel check runner"
  - `fe6200bf` 2026-08-17 — "Merge branch 'worktree-lane-a-534-audit-dispositions' -- batch 7a lane a: the audit disposition ledger + 9 births"
  - `e32093fd` 2026-08-16 — "Merge branch 'fix/533-oracle-pin-repoint' -- D-A: the three [#533] layout pins"
  - `b5054945` 2026-08-16 — "Merge branch 'docs/batch6-wrap' -- batch-6 wrap acts (i)-(vii) + the ledger"
  - (+3 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — live probe (this session) — `scripts/audit_checks/` exists with 18 modules — decomposition is under way; the byte-identical-health and order-AND-count clauses are unverified here.
- **deciding question:** Is a partially-landed decomposition (18 modules) closable, or does the row hold until `audit.py health` is proven byte-identical?

### [#241] Undeclared-edge groom

- **id:** `[#241]`
- **title:** Undeclared-edge groom
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2S · serialize-group `coherence`
- **acceptance (quoted):** "every id the `undeclared_edges` ship-gate leg surfaces is either declared (`reconciled_with`) or recorded permanent-defer-with-reason, and each such id's disposition entry retires or is re-annotated — the predicate reads the live surfaced set, never a fixed count"
- **last touch:** `6179ef17` 2026-08-11 — "docs(backlog+rules): apply the four Q-set rulings (Q1-Q4, 2026-08-11)"
- **git evidence:** `bbacd6c0` 2026-08-11 — "Merge branch 'docs/arc9-qset-applications' — apply Q1-Q4: [#419]/[#426] organ amendment, [#241]/[#390] blocks, [#360] re-anchor, [#505] clause-2 re-peg + I-D3"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#457] Two live-repo tests fail on main against green gates — test-vs-organ mismatch

- **id:** `[#457]`
- **title:** Two live-repo tests fail on main against green gates — test-vs-organ mismatch
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "both tests pass on main for verified reasons (filter-aware assertion; census-verified pin), verification recorded in the fixing commit"
- **last touch:** `fce8b5b0` 2026-08-18 — "docs(backlog,register,intake): batch-1 seat closure acts -- 6 rows banked, 0 births [#556] [#557] [#558] [#502] [#536]"
- **git evidence:** `d62796ad` 2026-08-15 — "merge boot-acts 2026-08-15: gate 41->11, closes #524 #352, births #529 #530, threshold 1320"
  - `5259b0f0` 2026-08-11 — "Merge branch 'worktree-am5-dispatch-visibility' — AM-5: a nested session carries no Agent View row, so the operator dispatches"
  - `461fa233` 2026-08-06 — "Merge branch 'docs/arc1-intake26-adr-doctrine' — ARC-1: intake #26 filed, ADR-110 cut, STANDING_RULINGS section D + B2 label landed, [#505] [#506] born"
  - `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
  - (+25 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#477] `deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-knowledge` cannot find `.dev-knowledge`

- **id:** `[#477]`
- **title:** `deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-knowledge` cannot find `.dev-knowledge`
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "the check resolves the hub's row from a checkout whose directory name differs from the registry key, with a test seeding a differently-named root"
- **last touch:** `d2ba06ca` 2026-08-03 — "docs(backlog): file the night batch's four defect rows [#477]-[#480] + annotate [#457]"
- **git evidence:** `8c0ed183` 2026-08-05 — "Merge branch 'claude/night-batch-review-prep-k1f2yr' -- night batch 2026-08-04 [night-batch]"
  - `0c64a76a` 2026-08-03 — "Merge branch 'docs/file-night-batch-defect-rows' — night-batch defect rows [#477]-[#480] filed, [#457] annotated"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#500] The Stop hook's BACKLOG advisory reads a correctly-closed task as \"nothing closed\

- **id:** `[#500]`
- **title:** The Stop hook's BACKLOG advisory reads a correctly-closed task as \"nothing closed\
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the advisory recognises row-DELETION plus the paired `tasks/*.md` terminal-status flip as a closure signal, pinned by a test that closes a row the sanctioned way and asserts the advisory stays silent"
- **last touch:** `23518240` 2026-08-05 — "docs(backlog): drain doc_rot accretion on four rows; disposition [#492] alone [#480]"
- **git evidence:** `78ab77b4` 2026-08-09 — "Merge branch 'docs/arc3-hygiene-closeout' — ARC-3 hygiene close-out: closes verified real, seven carried writes landed, decision sheet cut [#519] [#520]"
  - `05450245` 2026-08-05 — "Merge branch 'docs/457-routine-pin-census' — [#457] leg (ii) census discharged: the two declared routine rows are [#348] + [#426], the [#499]/[#500] cause refuted, and the 'exactly ONE row' boundary found stale at three sites; ruling — [#457] absorbs it, no new row"
  - `e676cd3f` 2026-08-05 — "Merge branch 'feat/480-review-artifact-organ' — review-artifact coverage made checkable [#480] [#499] [#500]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#303] Make seed_runbook.py child-class-aware

- **id:** `[#303]`
- **title:** Make seed_runbook.py child-class-aware
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "a --check/seed run against an ADR-36 child skips-or-redirects (never writes docs/handoffs/) with a test, and the seeder encodes the ADR-36 child class"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `94f9307b` 2026-08-16 — "Merge branch 'worktree-lane-k-293-seeding' -- batch 6 merge 11/12: [#293] cross-repo seeding -- SEEDED THEN REVERTED on ADR-60 conflict; row BLOCKED-ON-RULING"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
- **blocked on:** the ADR-60 conflict ruling (its seeding merge records BLOCKED-ON-RULING)
- **lean:** `NEEDS-RULING` — live probe (this session) — its one substantive merge records "SEEDED THEN REVERTED on ADR-60 conflict; row BLOCKED-ON-RULING".
- **deciding question:** Does the ADR-60 conflict that reverted `[#293]`'s seeding also hold this row, or is it independently buildable?

### [#324] Phase-6 axis-2 carrier

- **id:** `[#324]`
- **title:** Phase-6 axis-2 carrier
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P3M · serialize-group `audit-py`
- **acceptance (quoted):** "the night-batch standing routine carries a `· routine:` block that `routine_consumers` passes, the morning verdict-sheet consumer is named as that routine's `consumer=` with the sheet as its `consumption_path=`, and the audit-corpus verb-list is recorded in a `docs/audits/<date>-technical-*` artifact"
- **last touch:** `7d0a07b2` 2026-08-16 — "docs(tasks): W2G lane g -- contract of record + apply 5 ruled conversion drafts"
- **git evidence:** `9997bc32` 2026-08-16 — "Merge branch 'worktree-lane-g-271-conversions' -- batch 6 merge 6/11: [#271] [#324] [#391] [#412] [#491] Done-when conversions"
  - `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `65c9827e` 2026-07-11 — "Merge docs/audit-corpus-verb-list — #324 leg-c audit-corpus verb list [#324]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — live probe (this session) — `65c9827e` discharges leg c only ("#324 leg-c audit-corpus verb list"); the routine + consumer clauses are untouched.
- **deciding question:** Does leg c landing alone close the row, or do the routine + consumer clauses hold it open?

### [#497] Two stale claims on carrier/hook declarations

- **id:** `[#497]`
- **title:** Two stale claims on carrier/hook declarations
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "BOTH claims are corrected and the carrier's own test asserts the deployed shape against the live probe rather than against the prose"
- **last touch:** `23518240` 2026-08-05 — "docs(backlog): drain doc_rot accretion on four rows; disposition [#492] alone [#480]"
- **git evidence:** `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
  - `186efb5a` 2026-08-05 — "Merge branch 'chore/pre-seal-currency' — pre-seal doc-currency sweep + intake #24"
  - `0bfa64b0` 2026-08-05 — "Merge branch 'chore/fr8-flip-batch' — FR-8 flip batch adjudicated [#498] [#489]"
  - `8c0ed183` 2026-08-05 — "Merge branch 'claude/night-batch-review-prep-k1f2yr' -- night batch 2026-08-04 [night-batch]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#438] Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs

- **id:** `[#438]`
- **title:** Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `open` · P3S · serialize-group `playbook`
- **acceptance (quoted):** "`protocols/PLAYBOOK.md` carries the refusal-gate class rule, naming which arcs it binds and the questions the pre-build design pass must answer, and one arc's `docs/audits/` record shows its design pass preceding its first implementation commit"
- **last touch:** `6602e841` 2026-08-16 — "docs(backlog): convert [#438] Done-when to mechanical form (W2C step 1c)"
- **git evidence:** `b4862b9b` 2026-08-16 — "Merge branch 'worktree-lane-c-146-conversions' -- batch 6 merge 3/11: [#146] [#266] [#438] [#443] Done-when conversions"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `cb8c7b9d` 2026-07-28 — "Merge fix/437-closure-token-shared-core — [#437] shared closure-token detection, quoting contexts dead; [#444] filed"
  - `e53dee46` 2026-07-28 — "Merge feat/adr107-strangler-flip-step3 — ADR-107 ratified + strangler STEP 3: tasks/ becomes the source of truth [#439]"
  - (+1 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#506] Whole-set P10 grooming arc — the open set is unreconciled

- **id:** `[#506]`
- **title:** Whole-set P10 grooming arc — the open set is unreconciled
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "a `docs/audits/` sheet carries one row per `status: open` task with its last-touch date and closing-merge cross-check (count matching the live open count at generation time), each id carries a live / dead / awaiting-ruling verdict, and every id verdicted dead is closed per ADR-65 or named as deferred · footprint: `tasks/`, `BACKLOG.md`, one `docs/audits/` sheet"
- **last touch:** `ae531acf` 2026-08-13 — "docs(tasks): W4d batch 2/2 -- Done-when conversions for [#463] [#464] [#487] [#493] [#506] [#511]; 5 P3 skips recorded"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `87b993af` 2026-08-08 — "Merge branch 'worktree-lane-wave-closures' — Closure wave — 194 rows diff-verified, 3 proposals, none executed [#506]"
  - `15cc3ec9` 2026-08-08 — "Merge branch 'worktree-lane-506-groom-sheet' — Lane 506: whole-open-set grooming evidence sheet, 202 rows, zero verdicts [#506]"
  - `461fa233` 2026-08-06 — "Merge branch 'docs/arc1-intake26-adr-doctrine' — ARC-1: intake #26 filed, ADR-110 cut, STANDING_RULINGS section D + B2 label landed, [#505] [#506] born"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#329] VS Code ownership visualization

- **id:** `[#329]`
- **title:** VS Code ownership visualization
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "a generator emits `.vscode` folder icon/color config from the #328 manifest for ≥1 repo AND regenerates deterministically (no hand-edit)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `36cc842a` 2026-07-20 — "Merge fix/vscode-sort-folder-mode — folder-mode newest-first sorting @ 34c59b6d, 9ceb6fc6"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — live probe (this session) — the acceptance names the `#328` manifest, and `[#548]` records `#328` as a DEPARTED id — the criterion cites a referent that may not exist.
- **deciding question:** Does a Done-when that names the departed `#328` manifest survive at all, or must it be re-anchored before it can be judged?

### [#332] Fleet dependency-version parity

- **id:** `[#332]`
- **title:** Fleet dependency-version parity
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a versioned dependency manifest ships with the methodology package AND an automated check WARNs a version-drifted consumer while an at-parity (or `.methodology.yaml`-declared) one does not, with a test"
- **last touch:** `27ec8bc5` 2026-07-30 — "groom(backlog): arc 0731-g0-groom — 6 rows condensed, 5 dispositions retired, doc_rot clean [#426]"
- **git evidence:** `2bc02196` 2026-07-13 — "merge: #328 fleet_parity checker + parity manifest + hub §9a declarations [#328] [#332]"
  - `ff2118b2` 2026-07-12 — "Merge docs/journal-332 — anchor bde6b55/105cabc (JOURNAL entry for [#332])"
  - `105cabc9` 2026-07-12 — "Merge docs/backlog-332-dep-version-parity — file [#332] fleet dependency-version parity (#328 family, E6/S15)"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — live probe (this session) — `ecosystem/dependency-baseline.yaml` EXISTS and `scripts/fleet_parity.py` reads it — two clauses look discharged; the "with a test" clause has NO match under `tests/`.
- **deciding question:** Does a shipped manifest + a reader in `fleet_parity.py`, with no test, discharge a Done-when that says "with a test"?

### [#342] fleet_parity gate-ahead max-fidelity hardening

- **id:** `[#342]`
- **title:** fleet_parity gate-ahead max-fidelity hardening
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "each of the three lands with a test (an exported-id mismatch WARNs; an ambiguous remote match REFUSES; a provenance SHA mismatch WARNs)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `ca8d3903` 2026-07-17 — "Merge feat/336-gate-rev-axis — ARC 1: parity enforcement-gate-rev axis (ADR-102); clears the sole fleet_parity WARN, corp split now GATE_AHEAD_DECLARED. closes [#336]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#430] Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subject

- **id:** `[#430]`
- **title:** Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subject
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "(a) the conftest ruling is cited in `ecosystem/parity-surfaces.yaml` at the affected row and the root entry passes or is a declared divergence; and (b) two `ship-gate` runs on the same subject-repo state, from different checkouts, produce the same verdict — pinned by a test that varies the surrounding state"
- **last touch:** `41c040b4` 2026-08-15 — "docs(backlog): step 1 -- drain 6 of 8 top-decile accretion rows (CONTRACT R)"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `8c438220` 2026-08-07 — "Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: three fixed, one dispositioned, one filed [#505] [#511] [#512]"
  - `25ff8ec3` 2026-08-07 — "Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 rows filed, 0 closed [#505] [#430]"
  - (+9 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#244] Essence-spec lifecycle epic

- **id:** `[#244]`
- **title:** Essence-spec lifecycle epic
- **theme / story:** [E6] Cross-repo universalization / [S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)
- **status / size:** `open` · P2L · serialize-group `None`
- **acceptance (quoted):** "a tombstoned component's artifacts are demonstrably REMOVED from a consumer and verified ABSENT (leg-e mirrored), the roster regenerates without it, and per-repo drift surfaces in fleet_health"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `25b104ed` 2026-07-04 — "Merge feat/244-p4-sync-surfacing — [#244] P4 sync surfacing SHIPPED: Informant Tier-3 drift classifier + static_drift_summary + fleet_health per-consumer drift line; n=1 seb inject->DRIFT->rejected-non-waivable proven; version HELD 1.2.0; FU #250"
  - `a7504565` 2026-07-04 — "Merge feat/roster-gen-p3 — [#244] P3 generated methodology roster SHIPPED (n=1 hub; manifest->@.claude/methodology-roster.md @import, blocking roster-freshness gate, §7 trim; version HELD 1.2.0; FU #248/#249)"
  - `86aec774` 2026-07-04 — "Merge deploy/record-ai-council-1.2.0 — record ai-council @ methodology 1.2.0 [ADR-91/92]"
  - `2c869518` 2026-07-04 — "Merge feat/prune-remove-leg-p2 — [#244] P2 remove leg (deploy engine gains PRUNE)"
  - (+1 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — live probe (this session) — P2/P3/P4 merges each say SHIPPED; the leg-e clause is a CONSUMER-side removal verification not evidenceable from this repo.
- **deciding question:** Can a Done-when whose load-bearing clause is a CONSUMER-side verification ever be discharged from hub evidence alone?

### [#317] Default-parallel test invocation

- **id:** `[#317]`
- **title:** Default-parallel test invocation
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "verify cadence parallel by default (or D1 operator-ruled) AND the `not slow` run completes under 60s (measured time recorded at build) AND serial-nightly preserved"
- **last touch:** `6510427a` 2026-08-06 — "docs(backlog): grooming batch 2 — narrow [#338] to (b)-(e) and [#317] to leg (a)"
- **git evidence:** `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
  - `7c1b94fc` 2026-07-11 — "Merge docs/lane-cd-integration-journal — record LANE-C + LANE-D integration session [#302] [#309] [#312] [#316] [#317]"
  - `b1f7d618` 2026-07-11 — "Merge chore/trim-317-doc-rot — trim #317 to <1200 chars, clear doc_rot WARN [#317]"
  - `c7d45921` 2026-07-11 — "Merge docs/317-parallel-test-invocation — file [#317] parallel test invocation + slow-tier markers"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#470] `audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph

- **id:** `[#470]`
- **title:** `audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "the U+2192 is ASCII-swapped and a regression asserts every `ALL_CHECKS` docstring first line is cp1252-encodable"
- **last touch:** `3aab4d28` 2026-08-01 — "docs(backlog): file [#467]-[#470] + copier/rustworkx/evidence notes — night drafts promoted with architect re-rulings folded"
- **git evidence:** `4306a46a` 2026-08-04 — "Merge branch 'docs/file-484-485' — the two carried wrap items, filed not acted on"
  - `abbb1899` 2026-08-04 — "Merge branch 'feat/383-caches-wave' — the caches wave executes, 1 of 6 surfaces"
  - `b0af8e92` 2026-08-01 — "Merge branch 'docs/filing-batch-2026-08-01' — conformance absorbed, intake #23 filed, [#467]-[#470], [#460] REVERSED on live host evidence"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — 14 U+2192 glyphs remain in `scripts/audit.py`.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#528] Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost

- **id:** `[#528]`
- **title:** Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P1M · serialize-group `environment`
- **acceptance (quoted):** "(1) gate-run call sites use `-n auto --dist worksteal` (or a recorded reason one does not), (2) the tiered-suite rule is written in PLAYBOOK/ESSENTIALS, and (3) `test_run` duration events land via the telemetry leg — each with evidence in the closing commit"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** `7d1f6ce0` 2026-08-15 — "Merge branch 'worktree-lane-n-528-legs12-latency'"
  - `d62796ad` 2026-08-15 — "merge boot-acts 2026-08-15: gate 41->11, closes #524 #352, births #529 #530, threshold 1320"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#554] Devcontainer + provisioning script (NB4-G stage 1)

- **id:** `[#554]`
- **title:** Devcontainer + provisioning script (NB4-G stage 1)
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "one lane runs green (`audit.py health` **and** `pytest -m 'not slow'`) on the Codespaces free tier, and the *identical* script is runnable via `devcontainer up` on a VPS"
- **last touch:** `ba394476` 2026-08-18 — "docs(audits,backlog,journal): land the NB7 night, regen the index, trim [#554]/[#555] under the row ceiling"
- **git evidence:** `44d658bd` 2026-08-18 — "Merge branch 'docs/batch1-integration-wrap' -- batch-1 seat closure acts + the arc's JOURNAL anchor"
  - `80c7b9e8` 2026-08-18 — "Merge branch 'worktree-lane-c-554-devcontainer' -- devcontainer stage 1 + ADR-101 allowlist, C-1 fix applied [#554]"
  - `06bc65ab` 2026-08-18 — "Merge branch 'worktree-lane-h-554-codex-review' -- lane H terra review of frozen branches C + E [#554] [#502]"
  - `409374fd` 2026-08-18 — "Merge branch 'docs/nb7-morning-consolidation' -- NB7 night landed (2 of 4), index regen, [#554]/[#555] under the row ceiling"
  - (+1 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#440] Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable

- **id:** `[#440]`
- **title:** Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "a deleted retired record FAILs the gate, with a test seeding a retirement then deleting the file"
- **last touch:** `104a04f6` 2026-07-28 — "docs(backlog+audits): terra-H1 build-discovery — plugin bump is a release act; [#444] filed, in-arc bump reverted"
- **git evidence:** `78ab77b4` 2026-08-09 — "Merge branch 'docs/arc3-hygiene-closeout' — ARC-3 hygiene close-out: closes verified real, seven carried writes landed, decision sheet cut [#519] [#520]"
  - `e53dee46` 2026-07-28 — "Merge feat/adr107-strangler-flip-step3 — ADR-107 ratified + strangler STEP 3: tasks/ becomes the source of truth [#439]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#348] Backlog grooming as a standing routine, not ad-hoc

- **id:** `[#348]`
- **title:** Backlog grooming as a standing routine, not ad-hoc
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "the grooming cadence is captured as a routine definition (trigger, scope, consumption path) rather than per-session improvisation, gated behind #270's load-gauge"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
  - `da318c83` 2026-08-18 — "Merge branch 'worktree-lane-f-348-p10-evidence' -- P10 grooming evidence sheet regenerated deterministically [#348]"
  - `09bce194` 2026-08-13 — "Merge branch 'docs/arc2b-ruled-micro-tail' — ARC2b executes the five ruled packet items, births [#524], and decides the dispatch shape [#508] [#524]"
  - `461fa233` 2026-08-06 — "Merge branch 'docs/arc1-intake26-adr-doctrine' — ARC-1: intake #26 filed, ADR-110 cut, STANDING_RULINGS section D + B2 label landed, [#505] [#506] born"
  - (+3 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#419] We run routines whose output nobody consumes

- **id:** `[#419]`
- **title:** We run routines whose output nobody consumes
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2M · serialize-group `settings-json`
- **acceptance (quoted):** "`routine_consumers` reports zero routines missing `consumer:` or `consumption_path:` within its stated coverage; unconsumed output is reported by a detector rather than silently accumulating; and for the nightly conformance routine specifically — (i) the absorb has a trigger that fires without an operator remembering, (ii) a detector reports queue depth (the count of unmerged `claude/conformance-*` branches) at a surface the operator already reads, and (iii) a scheduler-run check distinguishes a night with no run from a night whose output went unabsorbed — each of (i)–(iii) proven by a test"
- **last touch:** `24fafaf9` 2026-08-16 — "docs(tasks): [#419] apply superseding Done-when draft + drain history (Y-3)"
- **git evidence:** `51d7fa08` 2026-08-16 — "Merge branch 'worktree-lane-a-409-conversions' -- batch 6 merge 1/11: [#409] [#410] [#411] [#419] Done-when conversions"
  - `bce5838a` 2026-08-15 — "Merge branch 'worktree-lane-s-w20-draft-landing'"
  - `d62796ad` 2026-08-15 — "merge boot-acts 2026-08-15: gate 41->11, closes #524 #352, births #529 #530, threshold 1320"
  - `bbacd6c0` 2026-08-11 — "Merge branch 'docs/arc9-qset-applications' — apply Q1-Q4: [#419]/[#426] organ amendment, [#241]/[#390] blocks, [#360] re-anchor, [#505] clause-2 re-peg + I-D3"
  - (+5 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#426] Declare `consumer` + `consumption_path` for every LIVE routine

- **id:** `[#426]`
- **title:** Declare `consumer` + `consumption_path` for every LIVE routine
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2M · serialize-group `settings-json`
- **acceptance (quoted):** "every live routine declares a consumer and consumption path or is retired; the dead-producer nags are resolved; and `routine_consumers`' stated boundary is closed or recorded permanent-defer-with-reason"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** `09bce194` 2026-08-13 — "Merge branch 'docs/arc2b-ruled-micro-tail' — ARC2b executes the five ruled packet items, births [#524], and decides the dispatch shape [#508] [#524]"
  - `d5d74612` 2026-08-12 — "Merge branch 'docs/arc2-adjudication-tail' — ARC2 converts the 143-item adjudication into landed law"
  - `3b711e87` 2026-08-11 — "Merge branch 'docs/batch4-go-recording' — the batch-4 GO: intakes #28-#32 ratified as one act, [#513] amended as intake #30 §A's organ, [#521]/[#522] born"
  - `bbacd6c0` 2026-08-11 — "Merge branch 'docs/arc9-qset-applications' — apply Q1-Q4: [#419]/[#426] organ amendment, [#241]/[#390] blocks, [#360] re-anchor, [#505] clause-2 re-peg + I-D3"
  - (+6 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#361] ADR-immutability's real coverage is declared only in code, never in the protocol

- **id:** `[#361]`
- **title:** ADR-immutability's real coverage is declared only in code, never in the protocol
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "either `protocols/AI_COUNCIL_PROCESS.md` and `templates/claude-regions/critical-rules-records.md` state the guard's real zone — `docs/decisions/transcripts/**` only, and that the zone is a live no-op since that tree was deleted — or `scripts/hooks/block_immutable_edits.py` widens to cover ADRs, handoffs and audits, with a test per newly-covered class"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `40dd51d8` 2026-08-16 — "Merge branch 'worktree-lane-b-210-conversions' -- batch 6 merge 2/11: [#210] [#285] [#361] Done-when conversions"
  - `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
  - `c0b40d37` 2026-07-28 — "Merge docs/recording-batch-2026-07-28 — recording batch: [E8] clause (b) AMENDED (D1), 7 conformance branches deleted (D2), North Star delta reviewed [#434] [#437] [#438]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#365] Promote `residual_completeness` from `exempt:` to `coverage_scope`

- **id:** `[#365]`
- **title:** Promote `residual_completeness` from `exempt:` to `coverage_scope`
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "doc marker + both code markers + `multi_site: 2` land in ONE commit, the edge resolves, the row moves to `coverage_scope:`, and ship-gate holds at the baseline"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `9f229f70` 2026-07-20 — "Merge docs/residual-rule-declaration — declare the residual-completeness rule, bind the exemption @ 70fb4cfc, 9c25f94f, cb3fac3a, 4772967e"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — `ecosystem/doc-code-edge.yaml:146-161` still carries `residual_completeness` under the TEMPORARY exemption block.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#369] Wire `boundary_headers.py --check` into pre-commit

- **id:** `[#369]`
- **title:** Wire `boundary_headers.py --check` into pre-commit
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `pre-commit-config`
- **acceptance (quoted):** "the hook is registered and blocks a hand-edited header, `CLAUDE.md` §9 lists it, and `ecosystem/doc-counts.md` agrees with the live hook roster · **RE-SCOPED 2026-08-12 — off the absolute gate count** (register M-7 `N2-R1-05`): the struck clause read "doc-counts reflects 16 gates" against a file reading **17**, and the roster has grown again since. An absolute number is the wrong predicate *regardless of repair* — it re-breaks every time a hook lands — so the clause above is agreement-with-the-regen, true at any roster size"
- **last touch:** `52d230cc` 2026-08-13 — "docs(backlog): ARC2b step 1 — condense the four over-cap rows, then write the frozen ARC2 step-3 obligations in"
- **git evidence:** `35eb6d98` 2026-08-03 — "Merge branch 'docs/file-482-glob-engine' — glob-engine repair filed per the 2026-08-03 ruling"
  - `0e5d015b` 2026-07-20 — "Merge docs/session-close-arc5 — session-close record, [#368] [#369], [#355] evidence @ 10f71693, d84e86c7, d48b2d8e"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — no `boundary_headers` entry in `.pre-commit-config.yaml`.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#383] Execution waves per surface

- **id:** `[#383]`
- **title:** Execution waves per surface
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S25] Converge surfaces in waves, with a mechanical done-signal
- **status / size:** `open` · P2L · serialize-group `architecture`
- **acceptance (quoted):** "for every `kind: gitignore-effect` row in `ecosystem/parity-surfaces.yaml`, (a) `desired_state_report.py` shows no `diverge` cell on those rows; AND (b) `fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared / 0 must-absent / 0 tombstone-violated across them for every repo it walks, naming any repo it could not walk rather than counting it clean; AND (c) both runs are pasted verbatim into the wave record and the operator has read them. · **RE-SCOPED at ARC2 to that `kind:` selector, off line ranges** (register M-7 `N2-R1-06`): the old range had drifted onto different rows and the set had grown 8 → 9, making (a)/(b) unverdictable; a selector survives layout edits, so no count is restated above"
- **last touch:** `52d230cc` 2026-08-13 — "docs(backlog): ARC2b step 1 — condense the four over-cap rows, then write the frozen ARC2 step-3 obligations in"
- **git evidence:** `abbb1899` 2026-08-04 — "Merge branch 'feat/383-caches-wave' — the caches wave executes, 1 of 6 surfaces"
  - `42ff1323` 2026-08-03 — "Merge branch 'docs/383-ratify-caches-wave' — ARC 0: [#383] ratified, caches wave named, [#424] trap cleared"
  - `67863180` 2026-08-01 — "Merge branch 'feat/462-membership-agreement-census' — closes [#462]: the membership blind spot mechanized, 9 governs"
  - `18576971` 2026-08-01 — "Merge branch 'fix/generator-newlines-and-groom' — generator newline defect fixed RED-first, A-3 groom rulings applied, net -3"
  - (+3 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#393] corp-sca rot review — confirm-live-or-retire 3 candidates

- **id:** `[#393]`
- **title:** corp-sca rot review — confirm-live-or-retire 3 candidates
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S26] Mine our own history before predicting anything
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "each of `config/category_mapping.yaml`, `requirements.txt` and `config/excluded.yaml` in `corp-sca-time-automation` carries a recorded confirmed-live or retired verdict, and a subsequent `fleet_analytics` run no longer flags the retired ones"
- **last touch:** `0bacab02` 2026-08-16 — "docs(tasks): W2D lane -- Done-when conversions for [#351] [#385] [#393] [#484] [#502]"
- **git evidence:** `4ca67eed` 2026-08-16 — "Merge branch 'worktree-lane-d-351-conversions' -- batch 6 merge 7/11: [#351] [#385] [#393] [#484] [#502] Done-when conversions"
  - `08aea7a7` 2026-08-08 — "Merge branch 'worktree-lane-c-393-rot' — Lane C: corp-sca rot review — 3 verdicts, 1 prepared patch, zero consumer writes [#393]"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

### [#385] L4 tech-currency lane

- **id:** `[#385]`
- **title:** L4 tech-currency lane
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S27] Make tech-currency a distributed rule, not a one-off
- **status / size:** `open` · P3M · serialize-group `architecture`
- **acceptance (quoted):** "one version-bump proposal is written into the desired-state contract, ruled, and distributed through the apply channel, with the resulting version visible in `ecosystem/deployed-versions.yaml` and the proposal at no point mutating the contract directly"
- **last touch:** `0bacab02` 2026-08-16 — "docs(tasks): W2D lane -- Done-when conversions for [#351] [#385] [#393] [#484] [#502]"
- **git evidence:** `4ca67eed` 2026-08-16 — "Merge branch 'worktree-lane-d-351-conversions' -- batch 6 merge 7/11: [#351] [#385] [#393] [#484] [#502] Done-when conversions"
  - `903638c5` 2026-07-26 — "Merge docs/0726-brake-discharge — [E9] brake discharged, ADR-105 activation gate, [#419] given teeth"
  - `2da5da22` 2026-07-21 — "Merge docs/north-star-ingestion — FLEET NORTH STAR ingested as intake #16 + theme [E9] @ b73319ef, 4d662e30"
- **blocked on:** NONE
- **lean:** `NEEDS-RULING` — a merge names this id in a substantive subject; whether it discharged the quoted criteria is the open question.
- **deciding question:** A merge touched this row's subject matter — did it discharge the QUOTED acceptance criteria, or only one leg of them?

## Cohort C4 — Row-management evidence only (54 rows)

**Shared deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#404] gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)

- **id:** `[#404]`
- **title:** gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P2S · serialize-group `handoff`
- **acceptance (quoted):** "an execution-mode render passes `verify_handoff_probes` with zero SUPPLEMENT references, pinned by a per-mode test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `de402b1c` 2026-07-23 — "Merge docs/handoff-execution — execution handoff bundle 2026-07-23 (hand-corrected to §13 shape; generator SUPPLEMENT leak) + file [#404] @ 0810fcd5 [refs #404]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#146] De-hardcode-first doctrine + sweep

- **id:** `[#146]`
- **title:** De-hardcode-first doctrine + sweep
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P3S · serialize-group `playbook`
- **acceptance (quoted):** "`protocols/PLAYBOOK.md`'s `amendment_coherence` honest-limits section carries de-hardcode-first as doctrine, and a `docs/audits/<date>-technical-*` sweep names every hand-maintained version surface with a per-surface verdict of de-hardcoded or kept-as-manifest — each kept-as-manifest surface carrying its reason"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `b4862b9b` 2026-08-16 — "Merge branch 'worktree-lane-c-146-conversions' -- batch 6 merge 3/11: [#146] [#266] [#438] [#443] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#112] adr_amend helper + ADR immutable-zone extension

- **id:** `[#112]`
- **title:** adr_amend helper + ADR immutable-zone extension
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `claude-md`
- **acceptance (quoted):** "an in-place ADR edit NOT routed through the helper is blocked and a helper-written Amendment passes (both with tests), and CLAUDE.md §5 rule 3 states the helper as the sanctioned in-place path with `last_reviewed` re-stamped in the same commit · Design caveat (live): a native `permissions.deny` path-glob on the transcripts/ADR zones is **defense-in-depth ONLY** — never a replacement for the PreToolUse guards (deny-globs are bypassable and cannot express exists-deny/new-allow; native OS sandbox is not available on native Windows, so the guards stay)"
- **last touch:** `449ad6b8` 2026-08-13 — "docs(tasks): W4a conversions — apply the 6 census P1/P2 drafts in the assigned set"
- **git evidence:** `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#485] A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha

- **id:** `[#485]`
- **title:** A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "repo writers route through one LF-enforcing helper, a test proves a CRLF write cannot land through it, and the gotcha entry is retired or re-scoped to what the mechanism does not cover"
- **last touch:** `aad1a235` 2026-08-04 — "docs(backlog): file [#484] and [#485] — the two carried wrap items"
- **git evidence:** `4306a46a` 2026-08-04 — "Merge branch 'docs/file-484-485' — the two carried wrap items, filed not acted on"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#518] `scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row because they are one fix.

- **id:** `[#518]`
- **title:** `scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row because they are one fix.
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "the call site scrubs the environment and decodes explicitly, with a test reproducing each defect first"
- **last touch:** `a4882b78` 2026-08-09 — "docs(backlog): ARC-2 Phase E — THREE rows born, not six; net 0 [#513] [#514] [#518]"
- **git evidence:** `7e024317` 2026-08-09 — "Merge branch 'docs/arc2-consolidation' — ARC-2 Phases B–F: ADR-111 proposed, 229 items triaged, 3 rows born, net 0"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#560] `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it

- **id:** `[#560]`
- **title:** `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "the reader parses EVERY triple in a file, a multi-branch artifact links every branch it reviews, the title predicate admits the forms actually in `docs/audits/` while still admitting 0 of the 13 non-review docs carrying `**Branch:**`, the leg emits one Finding per unlinked merge, and any residual WARN on an immutable artifact is dispositioned"
- **last touch:** `8f428e21` 2026-08-19 — "docs(backlog): birth [#560] -- the review_artifact_coverage reader-side linkage fix"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#534] `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition

- **id:** `[#534]`
- **title:** `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "each of `[#357]` `[#358]` `[#417]` `[#477]` cites its construct by anchor text (or by a locator that resolves live), and a check FAILs on a `scripts/*.py:<line>` locator in `tasks/` that does not resolve to its named construct"
- **last touch:** `b099f3ff` 2026-08-19 — "docs(backlog): [#534] gains N4's independent locator-rot corroboration [#534]"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
  - `fe6200bf` 2026-08-17 — "Merge branch 'worktree-lane-a-534-audit-dispositions' -- batch 7a lane a: the audit disposition ledger + 9 births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#552] Window-close disposition + archival routine — every new audit gets a disposition, every terminal ADR/intake is archived

- **id:** `[#552]`
- **title:** Window-close disposition + archival routine — every new audit gets a disposition, every terminal ADR/intake is archived
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "both legs are built with those tests, the ADR-100 exclusion is stated in the check's docstring, and one window closes with every new audit dispositioned and zero terminal-status documents outside an archive/"
- **last touch:** `aab0e1d7` 2026-08-17 — "docs(backlog): file [#552] -- the window-close disposition + archival routine"
- **git evidence:** `99ec4b19` 2026-08-17 — "Merge branch 'worktree-lane-b-546-currency-archival' -- batch 7a lane b: ADR/intake currency + 8 births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#234] Cross-repo probe validator

- **id:** `[#234]`
- **title:** Cross-repo probe validator
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "a cross-repo bundle whose floor-guard probe names a present `.claude/<file>` in the target PASSes and one naming an absent `.claude/<file>` FAILs, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `5b2ccadb` 2026-07-21 — "Merge worktree-cleanup-backlog — 2026-07-21 backlog-hygiene arc [#302] [#309] [#131] [#314] [#292] @ 0c7f04e9, 3e1e3f00, 9fc1a8b4, a9d25311"
  - `fef026ed` 2026-07-02 — "Merge docs/2026-07-02-ai-council-architect-handoff — v5 cross-repo architect handoff for ai-council + cross-repo probe-validator support (target resolution; [#234] filed)"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#277] propose_closures signal repair

- **id:** `[#277]`
- **title:** propose_closures signal repair
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "the two STRONG false positives no longer surface (pinned by a test seeding each), and a single run over the last 30 days of `main` yields a STRONG:WEAK-actioned ratio better than 49:0 with the run's numbers recorded in the closing commit, with tests"
- **last touch:** `59df6478` 2026-08-18 — "docs(backlog): STEP 2 batch 2 -- trim 6 rows under the 1320 ceiling"
- **git evidence:** `fa746e14` 2026-08-16 — "Merge branch 'worktree-lane-i-277-issues-evidence' -- batch 6 merge 9/11: [#277] D3 ratio evidence + 15 nightly-triage Issues closed"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `a54994a3` 2026-07-30 — "Merge branch 'docs/handoff-2026-07-31-architect-2' — closing handoff + intake #22 SEED"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#296] `audit.py repo <name> --repo-path` prints a report path that isn't there

- **id:** `[#296]`
- **title:** `audit.py repo <name> --repo-path` prints a report path that isn't there
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "the command writes the report where it says, or prints where it actually lands, with a test"
- **last touch:** `e4545b27` 2026-08-06 — "docs(backlog): [#296] correction — a misleading locator, not a lost report"
- **git evidence:** `3a466bf7` 2026-08-06 — "Merge branch 'docs/handoff-2026-08-06-consolidation' — successor architect bundle cut; 2026-08-06 window closed"
  - `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#220] MODIFY / semantic-drift axis

- **id:** `[#220]`
- **title:** MODIFY / semantic-drift axis
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2M · serialize-group `coherence`
- **acceptance (quoted):** "a committed fixture exercises a semantic/MODIFY change, a `docs/audits/` record names which organs fired and which did not against it, and the design leg stays deferred pending that result"
- **last touch:** `449ad6b8` 2026-08-13 — "docs(tasks): W4a conversions — apply the 6 census P1/P2 drafts in the assigned set"
- **git evidence:** `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `fbf4a2d0` 2026-07-01 — "Merge docs/backlog-reconcile — file audit-surfaced BACKLOG items #220–#229 (deploy-arc reconciliation + carrier residuals, MODIFY/semantic-drift axis, ARCHITECTURE currency + MEMORY migration, repo hygiene) + #131/#215 SPLIT; doc-only, opens/advances [#220][#221][#222][#223][#224][#225][#226][#227][#228][#229]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#478] `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the sentinel permanently

- **id:** `[#478]`
- **title:** `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the sentinel permanently
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "suffixed versions compare per PEP 440, with a test covering prerelease-then-GA and `.post`"
- **last touch:** `d2ba06ca` 2026-08-03 — "docs(backlog): file the night batch's four defect rows [#477]-[#480] + annotate [#457]"
- **git evidence:** `0c64a76a` 2026-08-03 — "Merge branch 'docs/file-night-batch-defect-rows' — night-batch defect rows [#477]-[#480] filed, [#457] annotated"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#170] Design + land the traceability-spine ADR

- **id:** `[#170]`
- **title:** Design + land the traceability-spine ADR
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3M · serialize-group `None`
- **acceptance (quoted):** "an ADR defines the issue-ID↔commit linkage, **and** the absorbed `#168` half — promoting the ADR-85 BACKLOG leg from advisory to a hard gate — is stated in this row's scope and ratified with the ADR"
- **last touch:** `2ae7bf39` 2026-08-12 — "docs(backlog): ARC2 step 9 — birth [#523], the [#439] executive-index render leg"
- **git evidence:** `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#520] No sanctioned way to retire a committed bundle whose seal is wrong

- **id:** `[#520]`
- **title:** No sanctioned way to retire a committed bundle whose seal is wrong
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2S · serialize-group `handoff`
- **acceptance (quoted):** "the marker surface is defined, that bundle carries one, and `check_seal_identity` skips a marked-retired bundle, with a test pinning both halves"
- **last touch:** `5f17b771` 2026-08-09 — "docs(consolidate): the seven-item post-integration write, carried since batch 2 [#519] [#520]"
- **git evidence:** `78ab77b4` 2026-08-09 — "Merge branch 'docs/arc3-hygiene-closeout' — ARC-3 hygiene close-out: closes verified real, seven carried writes landed, decision sheet cut [#519] [#520]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#405] Session-end leftover check — nothing verifies \"no leftovers\

- **id:** `[#405]`
- **title:** Session-end leftover check — nothing verifies \"no leftovers\
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2S · serialize-group `settings-json`
- **acceptance (quoted):** "the Stop-hook hygiene leg flags each named leftover class with a test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `b4dd3e48` 2026-07-27 — "Merge docs/window-close-batch — ARCHITECTURE currency, MERGE IS ATOMIC codified, supplement folded"
  - `f3ead30b` 2026-07-23 — "Merge chore/trim-405 — [#405] doc_rot trim (self-induced WARN cleared) [refs #405]"
  - `21a21e81` 2026-07-23 — "Merge chore/leftover-check-filing — [#405] session-end leftover check filed (organ unchosen) + teardown JOURNAL wrap [refs #405]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#442] Plugin command-cache staleness — cached command text can silently outlive a workflow change

- **id:** `[#442]`
- **title:** Plugin command-cache staleness — cached command text can silently outlive a workflow change
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2M · serialize-group `settings-json`
- **acceptance (quoted):** "a stale cached command cannot be served unnoticed — invalidation on edit, or a load-time stamp comparison that surfaces a mismatch — with a test that seeds a stale copy"
- **last touch:** `9ce96be8` 2026-07-28 — "docs(backlog): fit the six recorded rows under doc_rot cap without dispositioning"
- **git evidence:** `952c10ad` 2026-07-28 — "Merge docs/recording-batch-r — 2026-07-28 recording batch: owner=user ruled, [#441]/[#442] filed"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#454] `closure_ids` negation defect — the parser reads a negated closure mention as a closure

- **id:** `[#454]`
- **title:** `closure_ids` negation defect — the parser reads a negated closure mention as a closure
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "RED-first tests cover the three recorded reproduction strings, a bounded parser change makes negated mentions non-closing in BOTH copies, and terra reviews the diff pre-merge"
- **last touch:** `584ab835` 2026-07-31 — "docs(backlog): file [#453]-[#456] — night-batch follow-on rows"
- **git evidence:** `5eebee91` 2026-07-31 — "Merge branch 'docs/2026-07-31-grooming-and-reconciliation' — architect-ratified grooming + reconciliation"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#519] The close path is two edits, and nothing makes a half-done close visible

- **id:** `[#519]`
- **title:** The close path is two edits, and nothing makes a half-done close visible
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P1M · serialize-group `architecture`
- **acceptance (quoted):** "a test seeds a status-only close, runs the generator, and FAILS on the revert — the close path is atomic, or its non-atomicity is gate-visible"
- **last touch:** `5f17b771` 2026-08-09 — "docs(consolidate): the seven-item post-integration write, carried since batch 2 [#519] [#520]"
- **git evidence:** `78ab77b4` 2026-08-09 — "Merge branch 'docs/arc3-hygiene-closeout' — ARC-3 hygiene close-out: closes verified real, seven carried writes landed, decision sheet cut [#519] [#520]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#522] A re-cut handoff sibling carries its predecessor's payloads — the thinner-refill hole

- **id:** `[#522]`
- **title:** A re-cut handoff sibling carries its predecessor's payloads — the thinner-refill hole
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P2M · serialize-group `handoff`
- **acceptance (quoted):** "(a) `--allow-suffix` **refuses unless a predecessor is named** (e.g. `--carry-from <predecessor-bundle>`); (b) a test proves the refusal; (c) a test proves the carry — a re-cut sibling's FILL-IN regions are non-empty and reference the predecessor's payloads; (d) the validator's stated limit is closed for the re-cut path or re-annotated"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** `3b711e87` 2026-08-11 — "Merge branch 'docs/batch4-go-recording' — the batch-4 GO: intakes #28-#32 ratified as one act, [#513] amended as intake #30 §A's organ, [#521]/[#522] born"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#130] Memory-hygiene review

- **id:** `[#130]`
- **title:** Memory-hygiene review
- **theme / story:** [E3] Lessons feedback loop / [S9] Make lessons an active feedback loop, not a passive archive
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "one hygiene pass emits a ratify-only candidates digest to a `docs/audits/<date>-technical-*` artifact with per-class counts (duplicates / stale-RETIRED / cap-proximity), and the gotcha/memory write path carries a dedupe-against-existing step proven by a test that seeds a duplicate and asserts it is caught at write time"
- **last touch:** `ce439780` 2026-08-16 — "docs(tasks): lane f — Done-when conversions for #130, #274, #350, #417 per W2 wave-2 drafts"
- **git evidence:** `8e8d55a2` 2026-08-16 — "Merge branch 'worktree-lane-f-130-conversions' -- batch 6 merge 5/11: [#130] [#274] [#350] [#417] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#266] Codify the test-scoped-grant language lesson

- **id:** `[#266]`
- **title:** Codify the test-scoped-grant language lesson
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the grant-authoring guidance states that a narrow test-scoped grant includes the mechanical count/pinning assertions the change forces, at both `templates/handoff/epic/EPIC_BOOT.md.tmpl`'s FILE-BOUNDARY section and `ADR-97` §14a, citing the E4-1 precedent"
- **last touch:** `e58039fa` 2026-08-16 — "docs(backlog): convert [#266] Done-when to mechanical form (W2C step 1b)"
- **git evidence:** `b4862b9b` 2026-08-16 — "Merge branch 'worktree-lane-c-146-conversions' -- batch 6 merge 3/11: [#146] [#266] [#438] [#443] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#546] ADR-60's `docs/` taxonomy no longer describes the tree it governs

- **id:** `[#546]`
- **title:** ADR-60's `docs/` taxonomy no longer describes the tree it governs
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a reader of ADR-60 cannot be misled about which `docs/` genres exist — either an appended amendment marker re-scopes the enumeration while preserving Rule 5, or ADR-101 is recorded as the successor for the genre set — with the choice and its reason recorded, and no living doc still asserting the six-folder taxonomy"
- **last touch:** `77e3147f` 2026-08-17 — "docs(backlog): file [#546] -- ADR-60's docs/ taxonomy diverged from the tree"
- **git evidence:** `99ec4b19` 2026-08-17 — "Merge branch 'worktree-lane-b-546-currency-archival' -- batch 7a lane b: ADR/intake currency + 8 births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#285] Extend hub freshness gating to PLAYBOOK

- **id:** `[#285]`
- **title:** Extend hub freshness gating to PLAYBOOK
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "`protocols/PLAYBOOK.md` carries `last_reviewed` frontmatter, `protocols/PLAYBOOK.md` is a member of `_HUB_ONLY_FRESHNESS_FILES` in `scripts/audit.py`, `test_freshness_includes_hub_only_protocol_docs` no longer asserts PLAYBOOK's absence, and the re-read is evidenced by per-section notes in the commit that stamps it — not by the stamp alone"
- **last touch:** `18b2214c` 2026-08-16 — "docs(backlog): lane-b Done-when conversions for #210, #285, #361 (W2 wave-2 drafts, step 1)"
- **git evidence:** `40dd51d8` 2026-08-16 — "Merge branch 'worktree-lane-b-210-conversions' -- batch 6 merge 2/11: [#210] [#285] [#361] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** DEFERRED: it carries no `last_reviewed` frontmatter (a prose "Last updated" line only) and a genuine end-to-end re-read is its own arc — a bare stamp to green a
- **lean:** `LIKELY-LIVE` — live probe (this session) — `protocols/PLAYBOOK.md` frontmatter carries `reconciled_with:` only — no `last_reviewed`.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#388] The \"10–20 repo\" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is restated

- **id:** `[#388]`
- **title:** The \"10–20 repo\" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is restated
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `architecture`
- **acceptance (quoted):** "every surface restating the figure carries 5–8+ going forward, and the immutable four remain unedited with the correction record standing"
- **last touch:** `ae55ff8b` 2026-07-28 — "docs(intake): ratify intake #20, park #16 ACCEPTED/deferred, record the lesson-7 rulings"
- **git evidence:** `31fe0e01` 2026-07-28 — "Merge docs/intake-20-ratification — intake #20 ratified, #16 ACCEPTED/deferred, [#443] filed"
  - `2da5da22` 2026-07-21 — "Merge docs/north-star-ingestion — FLEET NORTH STAR ingested as intake #16 + theme [E9] @ b73319ef, 4d662e30"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#542] `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five

- **id:** `[#542]`
- **title:** `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "`ARCHITECTURE.md` names the five live `doc_rot` categories, and `ecosystem/doc-code-edge.yaml` carries the claim so `doc_claims` fails when the count and the detector disagree"
- **last touch:** `4836512f` 2026-08-17 — "docs(tasks): birth [#542] -- `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five"
- **git evidence:** `fe6200bf` 2026-08-17 — "Merge branch 'worktree-lane-a-534-audit-dispositions' -- batch 7a lane a: the audit disposition ledger + 9 births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#420] Does a TOP-LEVEL `docs/archive/` still make sense?

- **id:** `[#420]`
- **title:** Does a TOP-LEVEL `docs/archive/` still make sense?
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P3S · serialize-group `architecture`
- **acceptance (quoted):** "the top-level archive is ruled kept-with-a-restated-charter or dissolved into per-area homes, with each of the 22 files given a destination"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** `27f033df` 2026-07-25 — "Merge docs/lane-d-rulings — Lane D rulings + filings; closes [#262], closes [#295], closes [#304], closes [#339] @ 2945f894"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#227] Relocate AGENT_FRAMEWORK.md out of protocols/

- **id:** `[#227]`
- **title:** Relocate AGENT_FRAMEWORK.md out of protocols/
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "AGENT_FRAMEWORK.md lives under docs/ and every inbound ref resolves to the new path"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `fbf4a2d0` 2026-07-01 — "Merge docs/backlog-reconcile — file audit-surfaced BACKLOG items #220–#229 (deploy-arc reconciliation + carrier residuals, MODIFY/semantic-drift axis, ARCHITECTURE currency + MEMORY migration, repo hygiene) + #131/#215 SPLIT; doc-only, opens/advances [#220][#221][#222][#223][#224][#225][#226][#227][#228][#229]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — `protocols/AGENT_FRAMEWORK.md` present; `docs/AGENT_FRAMEWORK.md` absent.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#553] `docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and currently wrong in two places

- **id:** `[#553]`
- **title:** `docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and currently wrong in two places
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the ADR census figures are either machine-generated with a regen-and-diff gate on the `audit-index-freshness` model, or carry a dated re-measurement matching a live count; and the ADR-61 claim states the three-format parser hazard instead of asserting an absent status line"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** `99ec4b19` 2026-08-17 — "Merge branch 'worktree-lane-b-546-currency-archival' -- batch 7a lane b: ADR/intake currency + 8 births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#334] Fleet-wide ruff hook id migration `ruff` → `ruff-check`

- **id:** `[#334]`
- **title:** Fleet-wide ruff hook id migration `ruff` → `ruff-check`
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3S · serialize-group `pre-commit-config`
- **acceptance (quoted):** "all three repos use `ruff-check` and the legacy `ruff` alias is gone, witnessed per repo (a staged violating `.py` BLOCKED under the new id)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `97cf58e0` 2026-07-12 — "merge: file [#334] fleet-wide ruff id migration ruff -> ruff-check under [S15]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#559] Kernel/lab check tiering + `dev-knowledge-kernel` as an installable package

- **id:** `[#559]`
- **title:** Kernel/lab check tiering + `dev-knowledge-kernel` as an installable package
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P2L · serialize-group `audit-py`
- **acceptance (quoted):** "every `ALL_CHECKS` member carries a `kernel`/`hub` tier; `dev-knowledge-kernel` is installable from the hub at a git tag and at least one consumer resolves it as a pinned dependency; and the package pins `requires-python` + uv `required-version` and exposes the shared ruff config a consumer `extend`s"
- **last touch:** `25102406` 2026-08-22 — "docs(audits,backlog): S3 -- the annotation-and-rulings ledger, and five rows pointer-ized"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#273] Changelog-review staleness escalation

- **id:** `[#273]`
- **title:** Changelog-review staleness escalation
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "an over-threshold window renders an escalation line in the SessionStart digest (with a test) and the N/days thresholds are recorded"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `02389890` 2026-07-07 — "Merge worktree-arc5-platform-triage -- Arc-5 platform buy-vs-build triage epic landed: intake doc #2 CONSUMED, A1/A2 pins, 6 pilots, 4 verdicts; closes [#272] + [#118], files [#273]/[#274]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#274] Dogfood-signal prior in the /changelog-review ADOPT rubric

- **id:** `[#274]`
- **title:** Dogfood-signal prior in the /changelog-review ADOPT rubric
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "`.claude/commands/changelog-review.md`'s ADOPT rubric names the dogfood-signal prior, and one subsequent `docs/audits/<date>-changelog-review-*` digest cites that prior by name against at least one classified item"
- **last touch:** `ce439780` 2026-08-16 — "docs(tasks): lane f — Done-when conversions for #130, #274, #350, #417 per W2 wave-2 drafts"
- **git evidence:** `8e8d55a2` 2026-08-16 — "Merge branch 'worktree-lane-f-130-conversions' -- batch 6 merge 5/11: [#130] [#274] [#350] [#417] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
  - `02389890` 2026-07-07 — "Merge worktree-arc5-platform-triage -- Arc-5 platform buy-vs-build triage epic landed: intake doc #2 CONSUMED, A1/A2 pins, 6 pilots, 4 verdicts; closes [#272] + [#118], files [#273]/[#274]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#278] Test-suite hygiene epic

- **id:** `[#278]`
- **title:** Test-suite hygiene epic
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "both acceptance criteria from `docs/intake/archive/2026-07-07-test-suite-hygiene.md` hold with the criterion text quoted in the closing commit, and the theatricality review ships as a `docs/audits/` artifact and impacted-test selection is live in the verify cadence with a test"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#431] `codex-review` silently drops the doc lane on any mixed diff

- **id:** `[#431]`
- **title:** `codex-review` silently drops the doc lane on any mixed diff
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `codex-review`
- **acceptance (quoted):** "a mixed diff gets both profiles or emits a loud skipped-prose warning naming the unreviewed files, AND the counter agrees with the body, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `0c64a76a` 2026-08-03 — "Merge branch 'docs/file-night-batch-defect-rows' — night-batch defect rows [#477]-[#480] filed, [#457] annotated"
  - `18576971` 2026-08-01 — "Merge branch 'fix/generator-newlines-and-groom' — generator newline defect fixed RED-first, A-3 groom rulings applied, net -3"
  - `2f924424` 2026-07-29 — "Merge docs/window-winddown-2026-07-29 — window wind-down + bundle cut 2026-07-29"
  - `495b8a22` 2026-07-27 — "Merge docs/handoff-review-closing-batch — [#435] filed, [#434] fork RULED, [#428] narrowed, arc wrapped"
  - (+2 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#445] `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing

- **id:** `[#445]`
- **title:** `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `codex-review`
- **acceptance (quoted):** "a mixed diff can no longer report as reviewed while its prose went unreviewed — fail-loud or dual-route — with a test seeding a docstring-only `.py` beside prose"
- **last touch:** `99aceb54` 2026-07-29 — "docs: window wind-down — record the three 2026-07-29 rulings, fix H2, file [#445]"
- **git evidence:** `2f924424` 2026-07-29 — "Merge docs/window-winddown-2026-07-29 — window wind-down + bundle cut 2026-07-29"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#487] Closure-proposal consumption arc — repair the pipeline first

- **id:** `[#487]`
- **title:** Closure-proposal consumption arc — repair the pipeline first
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2L · serialize-group `None`
- **acceptance (quoted):** "(i)-(iv) as enumerated in this row land in both `scripts/propose_closures.py` and the `plugins/tier1-lifecycle` copy with a lockstep test, a ranked sheet in `docs/audits/` covers every parked proposal with a verdict per id, and a routine declaring `consumer:` + `consumption_path:` passes `routine_consumers`"
- **last touch:** `41c040b4` 2026-08-15 — "docs(backlog): step 1 -- drain 6 of 8 top-decile accretion rows (CONTRACT R)"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - `3a466bf7` 2026-08-06 — "Merge branch 'docs/handoff-2026-08-06-consolidation' — successor architect bundle cut; 2026-08-06 window closed"
  - `315a0345` 2026-08-06 — "Merge branch 'docs/2026-08-06-consolidation' — 2026-08-06 consolidation: night batch integrated, three repairs, nine grooming dispositions, four births"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#509] `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`

- **id:** `[#509]`
- **title:** `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the wrapper resolves `<PROMPTS_DIR>` / `$env:CLAUDE_PROMPTS_DIR` (default `~/Downloads`) in either shape, with a test, and a dispatch line in variable form launches unedited"
- **last touch:** `e351b685` 2026-08-07 — "chore(gates): PRE-2 gate hygiene — three doc_rot trims, one false-positive disposition, one filed HIGH [#505] [#511]"
- **git evidence:** `8c438220` 2026-08-07 — "Merge branch 'chore/pre-cut-gate-hygiene' — five inherited WARNs, honestly resolved: three fixed, one dispositioned, one filed [#505] [#511] [#512]"
  - `25ff8ec3` 2026-08-07 — "Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; 3 rows filed, 0 closed [#505] [#430]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#123] Routine observability convention + value review

- **id:** `[#123]`
- **title:** Routine observability convention + value review
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "the marker convention is recorded in `protocols/PLAYBOOK.md`, every routine declared under `routine_consumers` carries the marker, and one `docs/audits/<date>-technical-*` value review records per-routine findings-acted-on vs noise counts"
- **last touch:** `449ad6b8` 2026-08-13 — "docs(tasks): W4a conversions — apply the 6 census P1/P2 drafts in the assigned set"
- **git evidence:** `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#387] Rewrite the buy-vs-build intake BEFORE anything ingests it

- **id:** `[#387]`
- **title:** Rewrite the buy-vs-build intake BEFORE anything ingests it
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "`docs/intake/archive/2026-07-06-platform-feature-scan.md` either carries the ruled position (with an amendment marker) or a superseding intake doc exists and the old one's `status:` names it, and no `docs/decisions/ADR-*.md` cites the un-rewritten doc"
- **last touch:** `05fb0f37` 2026-08-15 — "chore(backlog): drain 8 history-accreted rows at tasks/ source"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `153eae1a` 2026-07-27 — "Merge docs/lane-filings-uv-bakeoff-extraction — three lane tickets [#432][#433][#434] + the uv/rtk/pilot-precedes-contract rulings"
  - `2da5da22` 2026-07-21 — "Merge docs/north-star-ingestion — FLEET NORTH STAR ingested as intake #16 + theme [E9] @ b73319ef, 4d662e30"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#523] Executive-index render leg on the generated `BACKLOG.md`

- **id:** `[#523]`
- **title:** Executive-index render leg on the generated `BACKLOG.md`
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2M · serialize-group `architecture`
- **acceptance (quoted):** "the `BACKLOG.md` opens with a P1→P3 index of one line per live row, AND `--check` still verifies it byte-identically against the tree, AND `--roundtrip` still proves losslessness, AND a `--status` (or equivalent) render mode prints velocity + horizon + top-priority ids from live data"
- **last touch:** `59df6478` 2026-08-18 — "docs(backlog): STEP 2 batch 2 -- trim 6 rows under the 1320 ceiling"
- **git evidence:** `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `d5d74612` 2026-08-12 — "Merge branch 'docs/arc2-adjudication-tail' — ARC2 converts the 143-item adjudication into landed law"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — `BACKLOG.md` opens with "Big picture", not a P1-P3 one-line-per-row index.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#561] Re-base the compute plan onto the Hetzner CX shared line

- **id:** `[#561]`
- **title:** Re-base the compute plan onto the Hetzner CX shared line
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2S · serialize-group `architecture`
- **acceptance (quoted):** "intake #32 carries an amendment or superseded-by pointer naming intake #39, and no live doc cites a CCX price as current — a grep for the stale figures returns only historical or quoted contexts"
- **last touch:** `25102406` 2026-08-22 — "docs(audits,backlog): S3 -- the annotation-and-rulings ledger, and five rows pointer-ized"
- **git evidence:** `7e793eca` 2026-08-19 — "Merge branch 'docs/seat-s1-night-adjudication' -- the S-1 night-adjudication seat arc [#348] [#323] [#407] [#450] [#449] [#406] [#281] [#494] [#534]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#271] Nightly proposal loop

- **id:** `[#271]`
- **title:** Nightly proposal loop
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3L · serialize-group `None`
- **acceptance (quoted):** "the loop runs nightly under a `· routine:` block that `routine_consumers` passes with `[#270]`'s load-gauge live; each §6 constraint — the ~5 proposals/night cap, the 7-day auto-expire, no autonomous semantic refactoring at night, and proposals landing in `docs/intake/` as `status: SEED` — is enforced by a check or a test rather than by convention; and a `docs/audits/<date>-technical-*` artifact records the first 2-week survival review with its measured accept-rate against the <20% kill threshold"
- **last touch:** `9f89ce3e` 2026-08-18 — "docs(backlog): STEP 2 batch 3 -- the trivial set, 6 rows under the ceiling"
- **git evidence:** `9997bc32` 2026-08-16 — "Merge branch 'worktree-lane-g-271-conversions' -- batch 6 merge 6/11: [#271] [#324] [#391] [#412] [#491] Done-when conversions"
  - `a4fc652d` 2026-08-13 — "Merge branch 'worktree-lane-h-conversions-w4a' — W4a conversions lane, 6 converted / 11 SKIPPED (no census draft) [#112] [#123] [#162] [#220] [#277] [#278]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#428] `nightly-triage` reports a dead producer to every session start

- **id:** `[#428]`
- **title:** `nightly-triage` reports a dead producer to every session start
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2S · serialize-group `settings-json`
- **acceptance (quoted):** "no session-start surface asserts pending work from a producer with no run in the last 30 days (with a test seeding a dead producer), and the GitHub Issue backlog is either closed out or `scripts/surface_triage.ps1` no longer reads it — with the Issue count at closing time recorded in the commit"
- **last touch:** `59df6478` 2026-08-18 — "docs(backlog): STEP 2 batch 2 -- trim 6 rows under the 1320 ceiling"
- **git evidence:** `fa746e14` 2026-08-16 — "Merge branch 'worktree-lane-i-277-issues-evidence' -- batch 6 merge 9/11: [#277] D3 ratio evidence + 15 nightly-triage Issues closed"
  - `b150bfe4` 2026-08-16 — "Merge branch 'worktree-lane-h-310-ledger-docs' -- batch 6 merge 8/11: [#310] [#428] finish-line ledger acts -- K1 declares, 14 permanent-defer re-annotations"
  - `8c9163e0` 2026-08-15 — "Merge branch 'worktree-lane-r-gateclose-drain8'"
  - `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
  - (+2 further spine merges naming the id)
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#493] B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days

- **id:** `[#493]`
- **title:** B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "a `docs/audits/` artifact names the cause with the evidence command that demonstrates it, and names the signal that would have surfaced the silence within one cadence — with that signal either filed as a `[#id]` or landed"
- **last touch:** `ae531acf` 2026-08-13 — "docs(tasks): W4d batch 2/2 -- Done-when conversions for [#463] [#464] [#487] [#493] [#506] [#511]; 5 P3 skips recorded"
- **git evidence:** `781bd4ff` 2026-08-13 — "Merge branch 'worktree-lane-k-conversions-w4d' — W4d conversions lane, 11 applied / 5 SKIPPED (no census draft) [#425] [#428] [#430] [#453] [#456] [#463] [#464] [#487] [#493] [#506] [#511]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#555] Closing campaign batch 1 + kill-candidates instrument

- **id:** `[#555]`
- **title:** Closing campaign batch 1 + kill-candidates instrument
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P1M · serialize-group `None`
- **acceptance (quoted):** "the first batch closes **net-negative** — closures strictly greater than births — measured against the live denominator at that batch's close, with the before/after figures both re-derived rather than carried"
- **last touch:** `25102406` 2026-08-22 — "docs(audits,backlog): S3 -- the annotation-and-rulings ledger, and five rows pointer-ized"
- **git evidence:** `409374fd` 2026-08-18 — "Merge branch 'docs/nb7-morning-consolidation' -- NB7 night landed (2 of 4), index regen, [#554]/[#555] under the row ceiling"
  - `883618e5` 2026-08-17 — "Merge branch 'docs/window-close-final' -- window close: lane r, two births, priority order v2, the seat handoff"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#357] Silent-rule census run 2

- **id:** `[#357]`
- **title:** Silent-rule census run 2
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "every `must|shall|never` occurrence in `docs/decisions/ADR-*.md` is enumerated in the sweep artifact and carries a state in ecosystem/silent-rule-baseline.yaml, and the file's combined denominator and N_silent replace the [E8] figures with `silent_rule_ratchet` green at the new numbers"
- **last touch:** `9ca3c8f3` 2026-08-13 — "docs(tasks): W4b batch 2/3 — mechanical Done-when for #349,#353,#356,#357,#358 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `12ac9a48` 2026-07-27 — "Merge docs/session-prep-morning-loop — intake #19 verbatim, R12 ruled F1, [#436], next architect bundle"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#402] Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling

- **id:** `[#402]`
- **title:** Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `architecture`
- **acceptance (quoted):** "README §4 carries the `<class>` grammar AND each of the 4 post-ratification off-pattern docs is dispositioned"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `fb868199` 2026-07-23 — "Merge worktree-enum-reconcile — [#398] ruled intake status-enum deployed (README S3/S5 + generator + template), 8 docs migrated onto the enum, 3 terminal docs archived byte-identical, CONTRIBUTING enum reconciled, doc-counts regen; file [#402] naming-clause ticket; JOURNAL prepend-collision resolved newest-first [refs #398, #402]"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#371] Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed

- **id:** `[#371]`
- **title:** Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `settings-json`
- **acceptance (quoted):** "an ADR names the carrier vehicle, both consumers carry the editor config under it (verified per repo), and `deploy/manifest-v1.4.0.yaml`'s `implemented:` value for this component matches the live per-consumer state with `fleet_parity` green"
- **last touch:** `ca49020a` 2026-08-13 — "docs(tasks): W4b batch 3/3 — mechanical Done-when for #362,#366,#371 per census P2 drafts; regenerate BACKLOG+manifest"
- **git evidence:** `8a091278` 2026-08-13 — "Merge branch 'worktree-lane-i-conversions-w4b' — W4b conversions lane, 13/18 applied / 5 SKIPPED (no census draft) [#338] [#341] [#344] [#346] [#347] [#349] [#353] [#356] [#357] [#358] [#362] [#366] [#371]"
  - `3fc9458d` 2026-07-20 — "Merge docs/352-render-diagnostic — [#352] (f) render-gap diagnostic + [#370] [#371] filed @ a8136b4, a2acc625"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#400] Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — same ruling family as [#370]

- **id:** `[#400]`
- **title:** Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — same ruling family as [#370]
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `claude-md`
- **acceptance (quoted):** "the ownership-model ruling explicitly covers the roster cell and is recorded"
- **last touch:** `9ce96be8` 2026-07-28 — "docs(backlog): fit the six recorded rows under doc_rot cap without dispositioning"
- **git evidence:** `952c10ad` 2026-07-28 — "Merge docs/recording-batch-r — 2026-07-28 recording batch: owner=user ruled, [#441]/[#442] filed"
  - `624b0485` 2026-07-23 — "Merge docs/night-batch-audit-0722 — NIGHT BATCH: transcripts/ deletion (operator ruling, guard kept armed) + archival audit (both terminal sets empty) + living-docs currency + [#400] filed @ 0d461e5b"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#413] Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)

- **id:** `[#413]`
- **title:** Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `claude-md`
- **acceptance (quoted):** "on or after 2026-10-22, either the colors semantics cite the ruled ownership model in `deploy/manifest-v1.4.0.yaml` (with `[#400]`'s ruling referenced), or ai-council's declaration carries a new `review_date:` later than 2026-10-22"
- **last touch:** `992891c4` 2026-08-13 — "docs(backlog): W4c batch 1/2 — Done-when conversions for #387, #389, #399, #408, #413"
- **git evidence:** `5eb1269f` 2026-08-13 — "Merge branch 'worktree-lane-j-conversions-w4c' — W4c conversions lane, 9/18 applied / 9 SKIPPED with reason [#387] [#389] [#399] [#408] [#413] [#414] [#415] [#418] [#423]"
  - `952c10ad` 2026-07-28 — "Merge docs/recording-batch-r — 2026-07-28 recording batch: owner=user ruled, [#441]/[#442] filed"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#427] Region templates carry a repo-POSITION-DEPENDENT path

- **id:** `[#427]`
- **title:** Region templates carry a repo-POSITION-DEPENDENT path
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P3S · serialize-group `claude-md`
- **acceptance (quoted):** "the carry mechanism supports a per-consumer substitution (or an explicit per-position variant), and ai-council's `claude-md-token-log-address` divergence retires by reference"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** `863cb804` 2026-07-26 — "Merge docs/427-position-dependent-template — file [#427] position-dependent region-template path"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#448] A11 staged-diff guard — cover EVERY candidate bundle, not just the active one

- **id:** `[#448]`
- **title:** A11 staged-diff guard — cover EVERY candidate bundle, not just the active one
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P2S · serialize-group `audit-py`
- **acceptance (quoted):** "a staged diff containing two candidate bundles fails the guard when either is uncovered, with a test"
- **last touch:** `6ae2acb0` 2026-07-30 — "chore(446): seal the window — closures [#446] [#421], file [#448], A6 record, LESSONS"
- **git evidence:** `a54994a3` 2026-07-30 — "Merge branch 'docs/handoff-2026-07-31-architect-2' — closing handoff + intake #22 SEED"
  - `3f4a1819` 2026-07-30 — "Merge branch 'chore/446-seal' — [#446] window seal: closures, [#448], A6 record, LESSONS"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

### [#391] Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter

- **id:** `[#391]`
- **title:** Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S26] Mine our own history before predicting anything
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "`scripts/fleet_analytics.py` fires on a schedule under a `· routine:` block that `routine_consumers` passes, fail-soft, with `[S20]`'s load-gauge discipline applied"
- **last touch:** `7d0a07b2` 2026-08-16 — "docs(tasks): W2G lane g -- contract of record + apply 5 ruled conversion drafts"
- **git evidence:** `9997bc32` 2026-08-16 — "Merge branch 'worktree-lane-g-271-conversions' -- batch 6 merge 6/11: [#271] [#324] [#391] [#412] [#491] Done-when conversions"
  - `bce5838a` 2026-08-15 — "Merge branch 'worktree-lane-s-w20-draft-landing'"
  - `423a372e` 2026-07-22 — "Merge docs/night-batch-close — night-batch integration close: evidence relocated to docs/audits + [#391]-[#396] filed @ 938b01c1"
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — every merge naming this id is row-management (conversion / filing / drain / grooming), never a build.
- **deciding question:** Is there any evidence beyond row-management (conversion / filing / drain / grooming merges) that this row was ever built?

## Cohort C5 — No git evidence at all (48 rows)

**Shared deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#547] Split-brain prevention is instructed against a handoff section shape v6 does not produce

- **id:** `[#547]`
- **title:** Split-brain prevention is instructed against a handoff section shape v6 does not produce
- **theme / story:** [E1] Handoff continuity / [S2] Finish the v5 handoff machinery deferred at the #149 flip
- **status / size:** `open` · P3S · serialize-group `playbook`
- **acceptance (quoted):** "the split-brain drift check either names v6 artifacts and sections that actually exist, or is recorded as retired with its successor mechanism named (the v6 P-probes are the candidate) — and no live surface instructs reading a handoff section absent from `HANDOFF_PROCESS.md`"
- **last touch:** `523411de` 2026-08-17 — "docs(backlog): file [#547] -- split-brain prevention has no referent under v6"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — `protocols/PLAYBOOK.md` still carries the split-brain instruction.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#242] ADR status-flip coherence check

- **id:** `[#242]`
- **title:** ADR status-flip coherence check
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a seeded ADR with a header↔README status divergence is flagged by an audit check, with tests"
- **last touch:** `43eced57` 2026-08-04 — "docs(adr): ratify ADR-82 with its version catch-up; flip ADR-88/89 to Pattern B; land two ruled registers"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#153] Enforcement-completeness pass

- **id:** `[#153]`
- **title:** Enforcement-completeness pass
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "each remaining prose-only constraint is mechanized or recorded as accepted-prose-only with a reason, the #5 `--no-ff` scope boundary is defined, and the ~/.claude-reach question is decided"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#345] Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermetization.py`

- **id:** `[#345]`
- **title:** Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermetization.py`
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `pre-commit-config`
- **acceptance (quoted):** "registry ships + gate reads it (frozensets gone), a compliant path per class passes + a violation blocks, lockstep collapsed, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#185] GAP-2 deterministic gotcha-injection guard

- **id:** `[#185]`
- **title:** GAP-2 deterministic gotcha-injection guard
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "a seeded commit-message / Edit-deletion pattern triggers injection of the matching gotcha (read-only, fail-soft), with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#451] CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ

- **id:** `[#451]`
- **title:** CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P2M · serialize-group `audit-py`
- **acceptance (quoted):** "a layer-edge check exists and runs in the hub gate set, its honest scope is stated (what it does NOT catch), and ADR-108's "mechanized check" clause cites it"
- **last touch:** `6bfa544f` 2026-07-30 — "docs(backlog): file [#449]-[#452] — the ratification-batch candidate rows"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#573] lychee as a zero-baseline markdown-link gate on the actionable corpus

- **id:** `[#573]`
- **title:** lychee as a zero-baseline markdown-link gate on the actionable corpus
- **theme / story:** [E2] Enforced governance / [S3] Turn advisory guards into enforced gates
- **status / size:** `open` · P3S · serialize-group `pre-commit-config`
- **acceptance (quoted):** "the gate is armed with its `lychee.toml`, a fixture proves it FAILs on an introduced broken link and passes on the live corpus, and the hook comment states its link-syntax-only scope"
- **last touch:** `92caed40` 2026-08-22 — "docs(backlog): S6 -- file f1-f5 [#572] [#573] [#574] [#575] [#576]; f6-f8 queued"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — no `lychee` hook in `.pre-commit-config.yaml`; no `lychee.toml`.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#99] FLEET-HEALTH digest names the failing check per red repo

- **id:** `[#99]`
- **title:** FLEET-HEALTH digest names the failing check per red repo
- **theme / story:** [E2] Enforced governance / [S4] Extend structural validation to more governance artifacts
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a red repo's digest line carries the failing check name(s)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#335] Exempt `templates/` from the `reconciled_versions` check

- **id:** `[#335]`
- **title:** Exempt `templates/` from the `reconciled_versions` check
- **theme / story:** [E2] Enforced governance / [S5] Catch spec/dependent drift mechanically, not by memory
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "`reconciled_versions` no longer flags a `templates/` file carrying a placeholder, with a test, and the standing disposition `warn-reconciled-versions-contributing-template` auto-clears"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#116] Hooks hygiene

- **id:** `[#116]`
- **title:** Hooks hygiene
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3S · serialize-group `settings-json`
- **acceptance (quoted):** "our PS hooks use exec-form `args:[]` and at least one PreToolUse guard carries an `if:` scope filter"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#189] Execute in ~/.claude

- **id:** `[#189]`
- **title:** Execute in ~/.claude
- **theme / story:** [E2] Enforced governance / [S7] Wire up the lifecycle hooks the workflow relies on
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a session-end check surfaces uncommitted `~/.claude` config/safety drift"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#289] Hub-own the OneDrive-Blue-Yonder guard

- **id:** `[#289]`
- **title:** Hub-own the OneDrive-Blue-Yonder guard
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P2M · serialize-group `settings-json`
- **acceptance (quoted):** "the guard has a hub-canonical versioned source + policy doc, ships via a deploy manifest, and is Informant-covered"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#496] `_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the Tier-3 DRIFT rows it produces are misfiled

- **id:** `[#496]`
- **title:** `_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the Tier-3 DRIFT rows it produces are misfiled
- **theme / story:** [E2] Enforced governance / [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "the organ maps to the component that actually carries it, or the mapping declares the split explicitly, and a test pins whichever is chosen"
- **last touch:** `4ca1ca23` 2026-08-05 — "docs(backlog): FR-8 flip batch — 8 rows opened, 3 re-pegged, [#489] retired into re-scoped [#218], [#498] filed"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#538] The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none landed

- **id:** `[#538]`
- **title:** The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none landed
- **theme / story:** [E3] Lessons feedback loop / [S10] Codify recurring patterns into the methodology
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "each of the 12 acts is landed in `protocols/PLAYBOOK.md` or recorded declined with its reason, and the coverage matrix is re-run reporting the new covered/partial/absent split"
- **last touch:** `606e9b11` 2026-08-17 — "docs(tasks): birth [#538] -- The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none landed"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#23] Validate ADR frontmatter relation-fields

- **id:** `[#23]`
- **title:** Validate ADR frontmatter relation-fields
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "an audit check flags an ADR whose supersedes/related/amends frontmatter names a non-existent ADR-id, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#548] Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows depend on it by name

- **id:** `[#548]`
- **title:** Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows depend on it by name
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "intake #12's TIER-1/TIER-2 manifest content has a live carrier — a row that owns building it or retiring it — OR the document's `trigger:` is re-anchored onto a live id or a date on the [#322] precedent (*"a peg whose referent will not occur tests nothing, so the trigger is a date"*), with [#329]/[#331]/[#332]'s dangling `#328` references repointed in the same act"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#550] Intake #14's ruled SIEM requirements outlived the ruling that shelved them, with no record of which half survives

- **id:** `[#550]`
- **title:** Intake #14's ruled SIEM requirements outlived the ruling that shelved them, with no record of which half survives
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "each ruled requirement clause in intake #14 is marked shelved-with-its-reason, live-and-carried-by-a-named-row, or dead, and the document's `trigger:` no longer names a departed id"
- **last touch:** `59df6478` 2026-08-18 — "docs(backlog): STEP 2 batch 2 -- trim 6 rows under the 1320 ceiling"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#564] Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag

- **id:** `[#564]`
- **title:** Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "every ADR meeting H3's zero-inbound-reference predicate is in `docs/decisions/archive/`, every intake in a terminal decided state is archived per the ADR-98 spine's convention, and an `audit.py` check reports a terminal-state record that has sat un-archived past a stated threshold — with a test that seeds one and sees it surface"
- **last touch:** `b6e2044b` 2026-08-20 — "docs(backlog): release the window's births -- [#562] [#563] [#564] [#565] [#566] [#567] [#568] [#569]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#572] Intake-funnel completion — #34 flip, #35–#37 transitions post-R7, funnel hygiene

- **id:** `[#572]`
- **title:** Intake-funnel completion — #34 flip, #35–#37 transitions post-R7, funnel hygiene
- **theme / story:** [E4] Decision management / [S11] Keep the decision corpus navigable and contradiction-aware
- **status / size:** `open` · P2M · serialize-group `architecture`
- **acceptance (quoted):** "#34 is flipped or its blocking source artifact is named with a dated trigger, #35–#37 each carry the transition their sub-fork permits or a recorded reason it cannot, and a P-2 sweep confirms every ACCEPTED intake has a live carrier or dated deferral"
- **last touch:** `92caed40` 2026-08-22 — "docs(backlog): S6 -- file f1-f5 [#572] [#573] [#574] [#575] [#576]; f6-f8 queued"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#71] Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents

- **id:** `[#71]`
- **title:** Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `environment`
- **acceptance (quoted):** "the ENVIRONMENT `~/.claude/` tree matches `ls ~/.claude/{commands,skills}` and the Codex/Rejected lines are reconciled to live state"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#526] Root-hygiene audit — which root files MUST be root, which are movable

- **id:** `[#526]`
- **title:** Root-hygiene audit — which root files MUST be root, which are movable
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P3S · serialize-group `architecture`
- **acceptance (quoted):** "an audit artifact enumerates every sanctioned Tier-1 root entry with a MUST-be-root/movable verdict and the tool-convention citation backing each"
- **last touch:** `2588d07d` 2026-08-14 — "docs(backlog): four ruled filings from the 2026-08-11 needs-review -- birth [#526]/[#527]/[#528], leg on [#523]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#569] Grouped hygiene — two standing suite REDs and the 19-finding PLAYBOOK census

- **id:** `[#569]`
- **title:** Grouped hygiene — two standing suite REDs and the 19-finding PLAYBOOK census
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P2M · serialize-group `playbook`
- **acceptance (quoted):** "both suite tests are green or retired with a recorded reason, H14 and H1/H2/H19b are corrected, and H13 is discharged through the `check-against-spec` re-stamp flow with each of the 11 sites individually verdicted stale-or-historical"
- **last touch:** `b6e2044b` 2026-08-20 — "docs(backlog): release the window's births -- [#562] [#563] [#564] [#565] [#566] [#567] [#568] [#569]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#571] Define \"architecture-described surface\" + the architecture-freshness check (intake #33 A1)

- **id:** `[#571]`
- **title:** Define \"architecture-described surface\" + the architecture-freshness check (intake #33 A1)
- **theme / story:** [E5] Canonical-file integrity / [S13] Keep canonical files accurate
- **status / size:** `open` · P2M · serialize-group `docs-gate`
- **acceptance (quoted):** "the definition is written and grep-evaluable, the check exists and fires on a fixture where an architecture-described surface changed with no `ARCHITECTURE.md` delta, Q3's advisory-vs-blocking posture is recorded as a decision rather than a default, and the three routed obligations are each named as discharged"
- **last touch:** `80af6da8` 2026-08-22 — "docs(backlog): S4 -- land the two intake carrier rows [#570] [#571]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — no `architecture_freshness` / `architecture-described` construct under `scripts/`.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#269] Audit-index count-tiered shape + freshness hook

- **id:** `[#269]`
- **title:** Audit-index count-tiered shape + freshness hook
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "`docs/audits/README.md` renders the count-tiered shape with the header repointed to ADR-100 (the freshness hook already landed)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — `docs/audits/README.md` header states in-tree: the count-tiered shape "is [#269] and is NOT built".
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#551] Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live one

- **id:** `[#551]`
- **title:** Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live one
- **theme / story:** [E5] Canonical-file integrity / [S14] Keep the day-to-day docs right-sized and current
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "`docs/audits/*.md` carry a `status:` field with its closed enum stated at a canonical home, the index generator reads it, a CONSUMED artifact is visibly folded rather than flat-listed, the writer of the field is named, and the implementing commit restates the ADR-100 no-move invariant"
- **last touch:** `98f4bbd4` 2026-08-18 — "docs(backlog): STEP 2 batch 1 -- trim 8 rows under the 1320 ceiling"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — 63 of 692 `docs/audits/*.md` carry a `status:` line; no closed enum at a canonical home.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#327] Protocols-as-interface genre ruling

- **id:** `[#327]`
- **title:** Protocols-as-interface genre ruling
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P2M · serialize-group `architecture`
- **acceptance (quoted):** "`protocols/` is documented as the interface genre AND each onboarded repo carries `protocols/README.md` + ≥1 interface doc (n≥1, corp included)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#331] Consumer BACKLOG schema adoption ruling

- **id:** `[#331]`
- **title:** Consumer BACKLOG schema adoption ruling
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "a recorded ruling states, per consumer, adopt-at-P6 vs accept-durable (declared in `.methodology.yaml` via the #328 mechanism)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#343] fleet_parity ship-gate-only scoping

- **id:** `[#343]`
- **title:** fleet_parity ship-gate-only scoping
- **theme / story:** [E6] Cross-repo universalization / [S15] Converge every child repo on the universal baseline
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "a hub pre-commit does not pay the fleet_parity walk (audit-health skips it) while `ship-gate` still runs + blocks on it, with a test proving both"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#245] Add-path status-awareness

- **id:** `[#245]`
- **title:** Add-path status-awareness
- **theme / story:** [E6] Cross-repo universalization / [S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "the add-path skips re-adding a `status: removed` component (no manual add-target drop needed) AND a source-drifted prune target classifies against last-deployed bytes, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#276] D2 per-consumer waiver-honoring

- **id:** `[#276]`
- **title:** D2 per-consumer waiver-honoring
- **theme / story:** [E6] Cross-repo universalization / [S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "a consumer-declared divergence for a component causes BOTH the prune sweep to SKIP it (no REFUSE-abort) AND the add/converge leg to NOT re-append it (no re-break) on a previously-deployed consumer, with tests"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#577] Adopt `AGENTS.md` as the portable instruction layer — the bounded execution lane

- **id:** `[#577]`
- **title:** Adopt `AGENTS.md` as the portable instruction layer — the bounded execution lane
- **theme / story:** [E6] Cross-repo universalization / [S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)
- **status / size:** `open` · P2M · serialize-group `claude-md`
- **acceptance (quoted):** "a root `AGENTS.md` ≤120 lines exists carrying the portable layer, `CLAUDE.md` carries only the Claude-runtime remainder plus the permitted pointer, the combined global+root payload is asserted **in bytes** against the 32 KiB cap by a test, the scope resolution for the `~/.codex` collision is stated in the `AGENTS.md` header, and `CLAUDE.md` §10's retired-AGENTS.md anti-pattern is corrected in the same commit"
- **last touch:** `9fd6a4e6` 2026-08-22 — "docs(intake,backlog): D5 filing -- intake #40 (doc-graph organ) and [#577] (AGENTS.md lane)"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — live probe (this session) — no root `AGENTS.md`.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#43] Decide +

- **id:** `[#43]`
- **title:** Decide +
- **theme / story:** [E6] Cross-repo universalization / [S17] Make new-repo scaffolding correct-by-default
- **status / size:** `open` · P3L · serialize-group `None`
- **acceptance (quoted):** "decision recorded + scaffold authored if approved"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#127] verify skill failure-output contract

- **id:** `[#127]`
- **title:** verify skill failure-output contract
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a seeded failure produces the file/expected/received/directive block and success stays 3-line"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#340] /ship pre-flight validator honors the consumer repo's canonical test gate

- **id:** `[#340]`
- **title:** /ship pre-flight validator honors the consumer repo's canonical test gate
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "/ship's code-diff validator applies the consumer's declared canonical marker filter (bare-suite fallback only when none is declared), witnessed green on a consumer carrying deselected-known-red tests (n=1 ai-council)"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#576] Telemetry read path — the lane `[#565]` was sequenced before

- **id:** `[#576]`
- **title:** Telemetry read path — the lane `[#565]` was sequenced before
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `environment`
- **acceptance (quoted):** "the read path answers at least one named operator question over the live store, grouped by `run_id`, with the question and its consumer named before the query is built (ADR-105 §2 named-consumer rule)"
- **last touch:** `92caed40` 2026-08-22 — "docs(backlog): S6 -- file f1-f5 [#572] [#573] [#574] [#575] [#576]; f6-f8 queued"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#575] Telemetry store: 98.5% of an emit, and silent drops under concurrent writers

- **id:** `[#575]`
- **title:** Telemetry store: 98.5% of an emit, and silent drops under concurrent writers
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `environment`
- **acceptance (quoted):** "per-event cost drops with a before/after measurement, ≥8 concurrent writers no longer drop events silently (retry or surface, with a test), and the store resolves via `--git-common-dir` with a two-worktree test"
- **last touch:** `92caed40` 2026-08-22 — "docs(backlog): S6 -- file f1-f5 [#572] [#573] [#574] [#575] [#576]; f6-f8 queued"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#574] gen_lane_contract emits the batch manifest — Q6's own failure class, recurring

- **id:** `[#574]`
- **title:** gen_lane_contract emits the batch manifest — Q6's own failure class, recurring
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `architecture`
- **acceptance (quoted):** "a batch manifest is machine-emitted with lane rows resolving to committed contract files, `check` refuses one naming an uncommitted contract, and a dispatched batch is reconstructable from repo artifacts alone"
- **last touch:** `92caed40` 2026-08-22 — "docs(backlog): S6 -- file f1-f5 [#572] [#573] [#574] [#575] [#576]; f6-f8 queued"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#540] `harvest_batch.py` — read the board, then fetch packets by `git show`, never by log-scraping

- **id:** `[#540]`
- **title:** `harvest_batch.py` — read the board, then fetch packets by `git show`, never by log-scraping
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "`scripts/harvest_batch.py` reports each lane's board state and fetches every done lane's packet by `git show`, with a test proving it never invokes `claude logs` and that an unreachable lane is reported rather than skipped silently"
- **last touch:** `fce8b5b0` 2026-08-18 — "docs(backlog,register,intake): batch-1 seat closure acts -- 6 rows banked, 0 births [#556] [#557] [#558] [#502] [#536]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#568] Provider config as code — `.dev-knowledge` as source of truth, machine-global dirs as junctions

- **id:** `[#568]`
- **title:** Provider config as code — `.dev-knowledge` as source of truth, machine-global dirs as junctions
- **theme / story:** [E7] Tooling & evaluation / [S18] Cut session friction with better tooling
- **status / size:** `open` · P2M · serialize-group `None`
- **acceptance (quoted):** "the four provider config dirs resolve to junctions into tracked paths in this repo, with the link topology asserted by a test that FAILs on an un-linked dir; one model registry file carries every model id with its effort enum and admission status; the routing table derives from it rather than restating it; and a test FAILs on a routed model absent from the registry"
- **last touch:** `b6e2044b` 2026-08-20 — "docs(backlog): release the window's births -- [#562] [#563] [#564] [#565] [#566] [#567] [#568] [#569]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#578] The earned mitigated rerun — one slot, role-reminder preamble baked in

- **id:** `[#578]`
- **title:** The earned mitigated rerun — one slot, role-reminder preamble baked in
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "all 14 pack items plus `C1-N3` are re-run on both candidates with the role-reminder preamble present in every item's dispatch text, the incumbent's `C1-N3` is either measured on the Anthropic path or its absence is recorded as transport evidence rather than as a judgement, per-lane refusal counts are reported so the guard's contribution is a number, the three gates are computed, and the artifact asserts **no verdict**"
- **last touch:** `b45e4146` 2026-08-23 — "docs(funnel): the wave-close funnel table over the 562-local run, and its two filings"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#570] Consume intake #27's W-wave rows — the deferred half of the tech-adoption ledger

- **id:** `[#570]`
- **title:** Consume intake #27's W-wave rows — the deferred half of the tech-adoption ledger
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2L · serialize-group `environment`
- **acceptance (quoted):** "every §A row still reading `DEFERRED(W-wave batch …)` has been either run (result recorded as an appended amendment), re-pegged to a live dated trigger, or refused with a reason — and no row is left pointing at a spent peg"
- **last touch:** `80af6da8` 2026-08-22 — "docs(backlog): S4 -- land the two intake carrier rows [#570] [#571]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** DEFERRED(W-wave batch — after intake #25 acceptance + births)` and #25 is already ACCEPTED, so the peg is live rather than pointing at a finished event. Scope i
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#535] `audit.py` has two module identities in one process, and a test's monkeypatch is invisible to one of them

- **id:** `[#535]`
- **title:** `audit.py` has two module identities in one process, and a test's monkeypatch is invisible to one of them
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2S · serialize-group `None`
- **acceptance (quoted):** "one spelling reaches `audit` from every caller, proven by a test asserting `sys.modules` holds exactly one module object for `audit.py` after both import paths run, and that a patch through one spelling is visible through the other"
- **last touch:** `fce8b5b0` 2026-08-18 — "docs(backlog,register,intake): batch-1 seat closure acts -- 6 rows banked, 0 births [#556] [#557] [#558] [#502] [#536]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#541] Scale-out substrate decision — unowned after two reports and a priced option set

- **id:** `[#541]`
- **title:** Scale-out substrate decision — unowned after two reports and a priced option set
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a ruling records the chosen scale-out substrate with its crossover rule and time-to-deploy, or records the decision deferred with a dated peg, citing the v2 report's option set"
- **last touch:** `353149ab` 2026-08-22 — "fix(audit,backlog): B3c routine_consumers 1->3 across all three surfaces; the A-DEFER narrowing acts"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#567] CX53 daily-driver substrate lane — the every-prompt requirement, carried under `[#561]`

- **id:** `[#567]`
- **title:** CX53 daily-driver substrate lane — the every-prompt requirement, carried under `[#561]`
- **theme / story:** [E7] Tooling & evaluation / [S19] Decide the undecided artifact/tool models
- **status / size:** `open` · P2M · serialize-group `architecture`
- **acceptance (quoted):** "`devcontainer up` is executed on a host we control and the result recorded (discharging lane J's D2), the same devcontainer boots on a CX53 with `claude` reachable over VS Code Remote, and the every-prompt requirement is measured against it rather than asserted — with the Codespaces monthly burn recorded alongside, so the two substrates are compared on evidence"
- **last touch:** `b6e2044b` 2026-08-20 — "docs(backlog): release the window's births -- [#562] [#563] [#564] [#565] [#566] [#567] [#568] [#569]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#288] Model-identity guard for unattended runs

- **id:** `[#288]`
- **title:** Model-identity guard for unattended runs
- **theme / story:** [E7] Tooling & evaluation / [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
- **status / size:** `open` · P3S · serialize-group `None`
- **acceptance (quoted):** "a mid-mission model change is detected and flagged AND the mission-ledger carries a line naming the model in effect, with a test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#354] W6 seed-1 recurrence half

- **id:** `[#354]`
- **title:** W6 seed-1 recurrence half
- **theme / story:** [E8] ARC-5 execution / [S21] Discharge the ARC-5 carried items that no wave has yet absorbed
- **status / size:** `open` · P2M · serialize-group `playbook`
- **acceptance (quoted):** "a staged amendment to ADR-36/41/101 lacking a companion PLAYBOOK/ESSENTIALS edit is flagged by the checker, with a test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#359] PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist.

- **id:** `[#359]`
- **title:** PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist.
- **theme / story:** [E8] ARC-5 execution / [S22] Discharge the silent-rule census findings
- **status / size:** `open` · P1M · serialize-group `handoff`
- **acceptance (quoted):** "the false claim is corrected or the mechanism built, AND the ledger model carries an explicit disposition for the phantom-enforcement class"
- **last touch:** `2ae7bf39` 2026-08-12 — "docs(backlog): ARC2 step 9 — birth [#523], the [#439] executive-index render leg"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

### [#392] fleet_analytics rename-alias loses history on path-reuse

- **id:** `[#392]`
- **title:** fleet_analytics rename-alias loses history on path-reuse
- **theme / story:** [E9] Fleet Desired-State System (North Star) / [S26] Mine our own history before predicting anything
- **status / size:** `open` · P3S · serialize-group `audit-py`
- **acceptance (quoted):** "a rename-back sequence carries full history with a covering test"
- **last touch:** `5c8a9d6d` 2026-07-28 — "feat(backlog): ADR-107 strangler STEP 3 — flip tasks/ to the source of truth [#439]"
- **git evidence:** NONE — no merge on `main`'s first-parent spine names this id
- **blocked on:** NONE
- **lean:** `LIKELY-LIVE` — no commit on any branch names this id outside its own task file.
- **deciding question:** Nothing in `main`'s history has ever mentioned this id outside its own task file — is the row still wanted, or was it filed and forgotten?

---

**End of sheet.** 212 rows, 212 evidence lines, 0 verdicts.
