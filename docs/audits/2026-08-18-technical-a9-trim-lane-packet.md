# LANE G — A9 trim route: per-row worksheet, trims, and the REPORT list

> **Lane artifact** for the frozen contract `docs/audits/2026-08-18-technical-a9-trim-lane-contract.md`
> (committed first, `4ec26fbf`). Route (i) — TRIM with a grep-verified carrier — **only**.
> Route (ii) dispositions are the seat's act and are **not written here**; candidates are REPORTED below.

## 0 · Baseline (measured, not remembered)

Measured on the **rendered `BACKLOG.md` line** (`validate_doc_rot._TASK_RE`, `len(line)`, ceiling
`_BACKLOG_ROW_CEILING = 1320`) at the lane's provisioning base `328d1086`:

```
BACKLOG.md task rows              218
rows over the 1320 ceiling         30
  in this lane's scope             23   (every scope row is over-ceiling)
  excluded by the contract          7   (#502 #529 #530 #533 #556 #557 #558)
```

`#554` and `#555` are named in the contract's EXCLUDED list and are **already under the ceiling**
(1296 / 1306) — they are the trim precedent this lane follows, not work.

**Rendered line == the `tasks/<id>-*.md` body line, byte-identical**, verified for all 23 rows before
any edit. So a trim measured in the `tasks/` source is the trim the ceiling sees; the write path is
still `tasks/` → `gen_task_tree --emit-source`, never a hand-edit of `BACKLOG.md`.

## 1 · The carrier rule as applied

The contract's operative term: *no prose is deleted unless a named carrier is grep-PROVEN to hold that
content.* Two consequences, both of which changed this lane's output:

1. **`source:` names provenance, not necessarily a carrier.** Six rows (`#546`–`#553`) carry
   `source: docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md`, and that contract is a
   *lane brief* — it orders the sweep, it does not record the findings. Read as a carrier it would
   have licensed deleting prose that exists nowhere else. Each row was therefore re-grepped against
   the corpus rather than trusted to its own `source:` line.
2. **Two rows have no carrier at all** and are REPORTED rather than trimmed (§4).

Carrier classes accepted here: intake docs, audit docs, ADRs, `protocols/STANDING_RULINGS.md`, and —
for the trivial set only — the row's own `Done when:` clause, where the body prose is a verbatim
restatement of a clause that survives the trim. Where `JOURNAL.md` is the *sole* carrier for a figure
that figure was **kept**, not cut.

## 2 · Per-row worksheet (all 23, completed before the first trim)

Legend — **cut**: the prose span proposed for deletion. **carrier**: path + matched phrase proving
that span survives elsewhere.

### 2.1 TRIM — carrier proven (21 rows)

| id | rendered | cut (span) | carrier + matched phrase |
|---|---|---|---|
| `#552` | 3576 | the two-leg mechanism build-out, the hand-archival SHA list, the ADR-status unreachability paragraph, the parser hazard | `docs/audits/2026-08-16-census-nb6-archive-sweep.md` §5.2 `:358` *"One new check `archival_residency` in the existing `scripts/audit_checks/` package"*; `:370` *"three ADR status-line formats coexist"*; `:176` *"Zero live ADRs carry `Superseded` or `Deprecated`"*; `:330` *"`216ce3a8` (ADRs), `6551d363` (intake, under `[#398]`)"*; `:186` the `[#242]`/`[#362]` honest limit |
| `#293` | 2864 | the whole lane-k execution narrative — 7 PR numbers, the revert, ai-council's hook, the two candidate homes | `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` `:53` *"corp-monorepo \| seeded, then reverted \| ~~rdwornik/corp-monorepo#54~~ closed"*; `:66` *"Why 7 were reverted — the ADR-60 conflict"*; `:114` *"Closed all 7 PRs (`gh pr close`, never merged)"*; `:129`/`:134` candidates (a)/(b); `:146` *"its own pre-commit hook `validate-docs-registry` refused the commit"* |
| `#553` | 2498 | the census arithmetic, the n=2 provenance, the silent-rot-class comparison | `docs/audits/2026-08-16-census-nb6-archive-sweep.md` `:190-191` *"the 86 ADR files in this folder and `archive/`" with **Accepted (81)** … is **stale by exactly one**"*; `:193` *"hand-maintained with no generator and no freshness gate — precisely the silent-rot class that `audit-index-freshness` guards"*; `:371` the three-format parser hazard. **KEPT** (uncarried): the second false claim about ADR-61's status line, and the number-swap-is-the-wrong-fix reasoning |
| `#514` | 2420 | the W1 discharge narrative — SHAs, the four pins, the negative control, the retroactive-safety proof | `docs/audits/2026-08-11-technical-batch-4-packet.md` `:279-280` *"leg 3 discharged in W1 (`92d735a7` + `ffc32099`); **leg 1 explicitly NOT discharged**"*; `protocols/STANDING_RULINGS.md` `:474` *"`92d735a7` collapsed the two rival constants, and `scripts/batch_manifest.py` now imports"*. **KEPT**: the re-measured *9 of 16* figure, whose only carrier is `JOURNAL.md:3384` |
| `#528` | 2397 | the six-item disposition list with its loci, and the R5 blob-identity evidence | `docs/audits/2026-08-15-technical-528-legs12-packet.md` `:96-104` *"`plugins/tier1-lifecycle/commands/ship.md` L37 … `.claude/commands/lane-integrate.md` L37, L59 … `.github/workflows/report-only-wall.yml` L141 — deliberately **not** a gate"*; `docs/audits/2026-08-15-technical-batch-phase1-packet.md` `:271` *"Blobs `41aa7bae` and `c01efd44`, byte-faithfulness verified"*, `:217` the still-owed `PLAYBOOK.md` L844/L866 |
| `#417` | 2360 | the landed-since-filing paragraph — the filter, the five test names, `4bef950`, the locator repair | `docs/audits/2026-08-16-verification-nb6-backlog-truth.md` §1.8 `:262-264` *"`_is_lane_owned_daily()` … `changes = [ln for ln in changes if not _is_lane_owned_daily(ln)]`"*, `:271-272` the Done-when quoted verbatim, `:280-281` *"`_commit_routine_outputs` is now at `:3759`"* |
| `#548` | 2167 | intake #12's frontmatter recital and the departed-`#328` finding | `docs/intake/2026-07-11-tech-ownership-manifest.md` `:5-8` `decided-by`/`disposition: deferred`/`trigger: "#328 build"`, `:8` *"#328's build consumes this as its FIXED charter target"*; `docs/audits/2026-08-16-census-nb6-archive-sweep.md` `:129` *"**`[#328]` no longer exists** … it survives only as a dangling reference inside `[#329]`, `[#331]` and `[#332]`"*, `:131-134` the *"schema-conformant and permanently parked at the same time"* paragraph |
| `#551` | 2154 | the three-boundaries paragraph — the no-move invariant, the ~78% figure, the R2(a) history | `docs/decisions/ADR-100-audit-retention-index-rule.md` `:18` *"~78% of citation lines sit in immutable ADRs / append-only LESSONS / immutable transcripts"*, `:27` *"never physically moved, rolled up, or compacted"*; `docs/audits/2026-08-16-census-nb6-archive-sweep.md` `:77` *"archive-inside-each-folder"*, `:368` *"`docs/audits/**` and `docs/handoffs/**` → **NOT CHECKED, by ADR-100 ruling**"* |
| `#531` | 2067 | the THIRD-OCCURRENCE enumeration and the measured `reference-transaction` mechanism | `docs/audits/2026-08-15-verification-night3-warn-ledger.md` `:565-566` *"batch-5 lanes S (`worktree-lane-s-w20-draft-landing`, id slot reads `w20`) + R (`worktree-lane-r-gateclose-drain8`, no id slot)"*, `:571-572` *"the `reference-transaction` git hook at the `prepared` stage, measured to refuse `worktree-lane-w20-draft-landing`"*, `:614` the measured refusal |
| `#428` | 2030 | the locator-correction paragraph and the leg-2-partial paragraph | `docs/audits/2026-08-15-technical-night3-decision-queue.md` `:190-200` (D6) *"Live: **`.github/` exists** … the *premise* holds … but the *evidence* as written is falsified by the tree"*; `:187` (D5) *"Closing the Issues without that test is a **partial** discharge"*; `docs/audits/2026-08-16-technical-277-issues-evidence-lane-contract.md` `:5` *"recording count 15 in the closing commit per D5"* |
| `#277` | 2006 | the appended ratio-evidence block | `docs/audits/2026-08-15-technical-night3-decision-queue.md` `:118` *"total 161 actioned 0 vs the 2026-07-07 baseline of 49:0"*, `:121` *"record 161:0 against `[#277]`; the row stays OPEN"*; `docs/audits/2026-08-16-technical-277-issues-evidence-lane-contract.md` `:5` *"append the 154:0 ratio evidence line to tasks/277-*.md per D3"* |
| `#549` | 1973 | intake #13's frontmatter recital and its architecture frame | `docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` `:6-9` `decided-by`/`trigger: "#328 build"`/`note: "the incoming sessions' comparison baseline per #301(iv) + the A-F build sequence"`, `:14` *"the hub is a SIEM-class information system (sensors → event pipeline → rules engine → dashboards → response)"*; census `:129` for the departed id |
| `#550` | 1869 | intake #14's frontmatter recital and the R7 single-clause disposition | `docs/intake/2026-07-12-siem-requirements-ruled-pack.md` `:5-9` `decided-by: "the 2026-07-12 A0 seal ruling (the RULED consolidation)"`, `consumers: "#328 build (charter requirements)"`; census `:129` for the departed id |
| `#492` | 1807 | the 2026-08-10 evidence line and the corpus-reconciliation line | `protocols/STANDING_RULINGS.md` `:818-819` *"`[#492]` Grok 4.6 — NOT released; the row parks behind a dated re-check **2026-08-17** — browser-verified 2026-08-10, with no model card and no API id"*; `docs/audits/2026-08-13-verification-492-corpus-reconciliation.md` `:1` *"the 12 seed verdicts re-derived against the landed spec"* |
| `#523` | 1738 | the renderer-defect rationale, the birth-ruling paragraph, the attached status-surface leg | `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md` `:22` *"executive-index render (priority-sorted task list linking `tasks/<id>`) as a leg on `[#439]` … The wall-of-text is a renderer defect, not a data defect"*, `:31` the richer-render candidate; `protocols/STANDING_RULINGS.md` `:1651` M-11 `A4` *"TAK — new row citing ADR-107/`[#439]` … keeps the closed row closed"*. The status-surface leg survives in the row's own `Done when:` |
| `#412` | 1389 | the (a)/(b) half-enumeration | in-row: `Done when:` retains *"a routing doctrine covering when to fan out, use a workflow, or use a subagent — configured fan-out included"* and the artifact clause covering (a) |
| `#484` | 1374 | the `audit.py`-glyph locus and the window-scope restatement | `BACKLOG.md` `[#470]` *"`audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph"* (a live row, already in this row's `refs`). The `desired_state_report.py` U+21C4 locus is **KEPT** — no carrier |
| `#443` | 1370 | the "either/or, no third option" restatement | in-row: `Done when:` retains *"either a stated rent/binding rule at its canonical home … or a section in `protocols/STANDING_RULINGS.md` naming `[#443]`"*, which is the same fork |
| `#271` | 1364 | the §6 constraint recital | `docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md` `:49` *"CAP — max ~5 proposals/night, untriaged items auto-expire in 7 days … accept-rate under ~20% after 2 weeks kills the routine"*, `:50` *"no autonomous semantic refactoring at night … judgment sleeps"*, `:48` *"functional feature ideas → `intake/` as status=SEED (no separate proposals/ folder)"* |
| `#361` | 1331 | the no-op restatement | in-row: `Done when:` retains *"and that the zone is a live no-op since that tree was deleted"* |
| `#146` | 1323 | the `{{VERSION}}` parenthetical | `protocols/PLAYBOOK.md` `:1109` *"the handoff skill/templates read `{{VERSION}}`"* — the `amendment_coherence` honest-limits paragraph, which is the same text the row points at |

### 2.2 REPORT — no carrier (2 rows) → §4

| id | rendered | why no trim |
|---|---|---|
| `#546` | 2227 | Nothing in the corpus holds the finding. Grepped: the row's own `source:` (`…batch-7a-lane-b-contract.md`) orders an *"ADR currency sweep"* and records no result; `…batch-7a-packet.md` records the birth, not the finding; `…census-nb6-archive-sweep.md` touches `docs/archive/`'s ADR-60 role but not the stale six-folder enumeration. `SANCTIONED_GENRES` appears in five audits, none of them about ADR-60's divergence. Every load-bearing claim (three false clauses · the five-genre live set · Rule 5 still live · never-rewrite-the-ADR) exists **only in this row**. |
| `#547` | 2099 | Same shape. `Future State` appears in exactly one audit corpus-wide (`2026-04-30-dev-knowledge-self-audit.md`, unrelated) and `Split-brain prevention` only at `protocols/PLAYBOOK.md:195/:4015` — which is the **defect site**, not a carrier. The measurement (v6.2.0, zero `current state\|future state` hits), the *"instruction with no referent"* claim and the explicit *"NOT [#362]'s defect"* discrimination exist only in this row. |

Both are route-(ii) candidates: the finding is real and cheap to read, and the length is the price of
being the only place it is written down. **This lane does not disposition them.**

## 3 · Trims executed

_(§3 is completed at STEP 2; see the per-batch commits.)_

## 4 · REPORT list for the seat's route-(ii) act

- **`[#546]`** — 2227 chars, no carrier. Trimming would delete the only record of the ADR-60
  taxonomy divergence.
- **`[#547]`** — 2099 chars, no carrier. Trimming would delete the only record of the split-brain
  instruction's missing referent.

Route-(ii) is the seat's register act. Nothing in this lane writes a disposition.

## 5 · Accretion arm — status before/after (`#293 #428 #550 #553`)

The `backlog-accretion` arm (ARM 1: >=3 distinct citation-blind history dates AND >=30d span AND
>700 chars) fires on **exactly four rows** at the lane base, and they are exactly the four the
contract names as the accretion arm:

```
BEFORE (328d1086)   backlog-accretion  4   BACKLOG#293  BACKLOG#428  BACKLOG#550  BACKLOG#553
```

This lane chases **length only**. The firing set is re-measured after the trims and any change is
stated in §3 rather than left to be discovered — the pre-existing accretion RED is the seat's.

_(after-state completed at STEP 3.)_
