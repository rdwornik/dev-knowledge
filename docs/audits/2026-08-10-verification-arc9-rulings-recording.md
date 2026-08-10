# ARC-9 — the operator's 2026-08-10 rulings recorded, the corrected N-B table, and the seed-corpus verification pass

**Arc:** ARC-9, primary checkout, branch `docs/arc9-rulings-recording`, merged `--no-ff` into `main`.
**Date:** 2026-08-10.
**What this file is:** the **in-repo carrier** for a ratifying act that happened off-repo. The
operator's answers arrived as a prompt against `RULING-CHECKLIST-2026-08-10.md` (operator's
`Downloads`), which is not a tracked artifact. Per the ADR-110 precedent for an off-repo
ratification, this file cites that source rather than claiming an in-repo locator that does not
exist, and carries the answers in the repo.

**What this file is not:** a decision surface. Every ruling below was issued by the operator; this
arc recorded them. Where this arc exercised judgment — twice, both on dates the operator did not
name — it is labelled as such in §4.

---

## 1. What was recorded

The checklist's DEFAULT BLOCK was ratified whole; the forks and inputs were answered individually.
The durable landing is `protocols/STANDING_RULINGS.md` **section I**, one line per ruling. This
section names only what changed on disk.

| # | Item | Landing site | What changed |
|---|---|---|---|
| 1 | The whole DEFAULT BLOCK (25 lines) + P0 + P1 | `protocols/STANDING_RULINGS.md` §I | New dated section I: I-P0 (inversion ratified), I-P1 (corrected N-B set adopted), I-D (25 default lines), I-F1/I-F2/I-F3 (forks 1–3), I-I1/I-I2 (the two inputs) |
| 1a | K-4 supersession pointer (3b-1) | §I-D | The immutable decision sheet's §2 source-recommendations are superseded by ARC-4's outcomes — recorded as a pointer, because the sheet is immutable and its K-4 row still reads as a kill recommendation |
| 1b | `[#508]` deliberately unmechanized (3a-2) | §I-D | Recorded with its reason; closes a P3 against an enum that currently agrees |
| 1c | FORK-2 banked line | §I-F2 | Intake #28 §B **DECIDED**, verbatim, with the flip explicitly deferred to the single ratification batch |
| 1d | I-2 answer | §I-I2 | 2026-08-06 — the scheduler job did not run; no branch because no run |
| 2 | ADR-111 ratification (FORK 1 = Option A) | `docs/decisions/ADR-111-finding-triage-pipeline.md`; `docs/decisions/README.md`; `.claude/generated/recent-adrs.md` | Status `Proposed` → `Accepted` **as written** (§4 departure intact) + a `Decided-by` line, per the ADR-94 status-line-only in-place exception; the index row's `**PROPOSED** —` prefix dropped per the status-prefix convention and a `RATIFIED 2026-08-10` clause added; the generated roster regenerated |
| 3 | The corrected N-B verdict table | §2 of this file | All 25 rows emitted below |
| 4 | `[#492]` evidence + dated re-check | `tasks/492-…md` | Evidence line *"Grok 4.6 not released as of 2026-08-10 (browser-verified)"* + `RE-CHECK 2026-08-17`. **Status unchanged** (`deferred`), as ruled |
| 5 | `[#511]` re-scope | `tasks/511-…md` | Done-when re-scoped to the **non-mechanized** cut load (probes · locator re-verification · answers); the machinery half declared out of scope with its ~4.5 s figure recorded VERIFIED |
| 6 | `[#322]` peg → dated review | `tasks/322-…md` | Dead peg *"C4 visualization research"* retired; `DATED REVIEW 2026-09-09`; row stays open |
| 7 | `[#360]` → dated review | `tasks/360-…md` | Author intent recorded unrecoverable (operator input I-1); `DATED REVIEW 2026-09-09` |
| 8 | `automation/*` branch protection (3c-3) | `.claude/rules/git-discipline.md` | `automation/*` added to the explicit-protection list beside `claude/conformance-*`, with the reason (an organ-produced replication lane exists to live outside `main`; `check_fleet_audit_replication` asserts it) and the `verify:` line updated |
| 9 | The `[#419]`/`[#426]` absorb-organ scope line | §I-I2 | A **scheduler-run check** belongs in the organ's scope. **The DRAFT does not exist on disk** — the digest-absorb-prep lane has produced no commits at recording time — so this is recorded as the DRAFT's *input*, not as an edit to it |

### Locator verification performed before recording

Every SHA this recording or its sources cite was resolved live, not carried:
`01410f94` · `9a7ffcb4` · `036385a6` · `201191f4` · `24882f8c` · `da274889` · `19b5d598` ·
`8aab4356` · `8f09c12d` · `f18419fc` — **10 of 10 resolve.**

**One locator had drifted and is corrected here.** The Fable review cites `JOURNAL.md:1905` for the
`[#511]` re-grade. That line no longer carries the anchor — `JOURNAL.md` is newest-first prepend, and
the ARC-8 entry pushed the text down. The anchor text
*"`collect_state` 525 ms · `collect_hints` 831 ms · `generate` 1,708 ms · cold CLI 3,321 ms ·
`verify_handoff_probes` 1.2 s — ~4.5 s of machinery, 0.25% of the complaint"* now sits at
`JOURNAL.md:1977–1978`. The claim is unaffected; the citation form is. This is the 3b-4 convention
(adopted in the same window) paying for itself within the hour: `tasks/511-…md` cites the anchor
text, not the line number.

---

## 2. The corrected N-B verdict table (all 25 rows)

Per preamble P1, rulings bind to `docs/audits/2026-08-10-technical-decision-sheet-verification.md`
only as corrected by the Fable findings M1-a/M1-b
(`docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md`).

**The four corrections, applied:** item 14 ≡ §4A is one claim counted once, documented rather than
silently deduped · both hybrid *"VERIFIED (as unverifiable)"* rows (items 1 and 7) count
**UNVERIFIABLE** for grounding · items 3 and 5 are re-graded **VERIFIED** on located evidence ·
items 10, 11 and §4B stay UNVERIFIABLE.

| # | Claim | Corrected verdict | Grounds |
|---|---|---|---|
| 1 | `[#492]` Grok 4.6 release is an external fact | **UNVERIFIABLE** (was "VERIFIED (as unverifiable)") | hybrid row; counts UNVERIFIABLE for grounding per M1-a. Now settled *externally* by the operator's browser check, not by the repo |
| 2 | Four kill proposals, each with an unmeetable clause | **PARTIALLY REFUTED** | unchanged — K-4's rationale is refuted; K-1/K-2/K-3 hold |
| 3 | OneDrive rule conflict across three surfaces | **VERIFIED** (was UNVERIFIABLE) | container-relative, not absolute. All three surfaces readable from the adjudication seat: `ai-council/.claude/rules/code-standards.md:13` *"NEVER touch 'OneDrive - Blue Yonder' paths"* (strict form) vs the global `~/.claude/rules/core-invariants.md` tiered T0/T1/T2 permissive-with-enumeration form. **Re-verified live this arc — the line is at :13 exactly** |
| 4 | ADR-111 Proposed at `da274889` | **VERIFIED** | `da274889` (2026-08-09), *"docs(adr): ADR-111 (Proposed) — the finding pipeline, four outcomes per finding"*. **Re-resolved live** |
| 5 | `[#511]` — ~4.5 s mechanized cost of a ~30-min wall clock | **VERIFIED** (was UNVERIFIABLE) | the figure IS in the tracked record with a component breakdown. Anchor text at `JOURNAL.md:1977–1978` (cited by Fable as `:1905` — drifted, see §1) plus `docs/audits/2026-08-07-technical-handoff-engine-thinning.md:142,170` |
| 6 | Intake #30/#31 filed verbatim at `036385a6`, zero births | **VERIFIED** | `036385a6` (2026-08-09) adds both intake files; no `tasks/` add in the diffstat. **Re-resolved live** |
| 7 | n=5 unattributed HEAD swaps; reflog gitignored | **UNVERIFIABLE** (was "VERIFIED (as unverifiable)") | hybrid row; counts UNVERIFIABLE for grounding per M1-a. Ruled accepted-and-closed (checklist 7) |
| 8 | `2h43m` / `~9 minutes` unlocated in the tracked record | **VERIFIED** | independent search reproduces the absence. Ruled STRICKEN (checklist 8) |
| 9 | `trailing-whitespace`/`end-of-file-fixer` collide with append-only invariants | **VERIFIED** | rewriters vs `LESSONS.md` / `logs/TOKEN-LOG.md` / ADR immutability is a real conflict per CLAUDE.md §5 |
| 10 | 153 pending closures at reading, 143 today; store gitignored | **UNVERIFIABLE** | store is untracked and unreachable from a cloud clone. Correctly self-classified; stays |
| 11 | Two engine amendments operator-endorsed but unratified | **UNVERIFIABLE** | endorsement is off-repo session context, not a tracked artefact. Stays — and the ruling (RATIFY BOTH) is precisely what converts it |
| 12 | *"ARCHITECTURE.md not re-read, not re-stamped … still true after this arc"* | **REFUTED** | `ARCHITECTURE.md:2` carries `last_reviewed: 2026-08-08`, set by `8f09c12d` whose subject says so. **Re-resolved live** |
| 13 | `[#322]` peg referent ruled against | **VERIFIED** | row is `status: deferred`, P2. Acted on this arc — peg converted to a dated review |
| 14 | `[#502]` is the mutmut row, not the import-convention row | **VERIFIED** | **≡ §4A — one claim, counted once.** `tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`. The sheet is right and the consolidation report it corrects was wrong |
| 15 | Intake #28 §B is DRAFT | **VERIFIED** | consistent with the intake index state — and still DRAFT after this arc, deliberately (I-F2) |
| K-1 | `[#102]`: `#262`/`#295` verified closed at `19b5d598`; peg will never occur | **VERIFIED** | `19b5d598` (2026-07-25) *"closes [#339], closes [#262], closes [#295]"*; neither task file exists. **Re-resolved live** |
| K-2 | `[#308]`: `#221` closed at `8aab4356` with no successor | **VERIFIED** | `8aab4356` (2026-07-07). **Re-resolved live** |
| K-3 | `[#325]`: same dead `#221` referent; `[#294]` nearest live carrier | **VERIFIED** | same `8aab4356`; `[#294]` open |
| K-4 | `[#310]`: escape precondition satisfied → close | **REFUTED** | the closure fact is true; the escape inference is false and was refuted 2026-07-21. Contained by ARC-4 at `9a7ffcb4`; supersession pointer recorded this arc (3b-1) |
| §3-i | ADR-111 declines the ARC-2 clause because it contradicts ADR-98 §3 | **VERIFIED** | the departure is stated in the ADR itself, not invented by the sheet |
| §3-ii | *"intakes #16, #26 and #25 were each accepted by recorded operator ruling in `decided-by`, not by ADR"* | **VERIFIED** | the load-bearing empirical claim behind FORK 1 = Option A, and it holds |
| §4A | No open row owns the `sys.path` substrate; `[#502]` misattributed | **VERIFIED** | **≡ item 14.** Counted once in the tallies below |
| §4B | `[#520]` birth-cap reading | **UNVERIFIABLE** | turns on intent in a contract, not on repo state. Stays — ruled KEEP BOTH + confirm the reading |
| §4C | *"8 rows are P1/P2 **and** deferred, two of them P1 (`[#218]`, `[#300]`)"* | **VERIFIED — exactly** | count and named ids both reproduced from `tasks/` frontmatter |
| §4D | 20th `undeclared_edges` WARN, 19 of 20 dispositioned | **VERIFIED, now discharged** | ARC-4 landed the 20th at `201191f4`. **Re-resolved live**; discharge confirmed (checklist item 6) |

### Corrected tallies

- **By row (25 rows as printed):** 17 VERIFIED · 5 UNVERIFIABLE · 2 REFUTED · 1 PARTIALLY REFUTED.
- **By distinct claim (24, item 14 ≡ §4A collapsed):** 16 VERIFIED · 5 UNVERIFIABLE · 2 REFUTED ·
  1 PARTIALLY REFUTED.
- **Movement from the original set:** two rows re-graded UNVERIFIABLE → VERIFIED (items 3, 5); two
  hybrid rows re-graded to UNVERIFIABLE for grounding (items 1, 7). The original *"15 VERIFIED /
  6 UNVERIFIABLE"* is not reproducible from either reading — which is M1-a's point, and why the
  join rule needed this table before any ruling could bind to it.

**Why both tallies are printed.** M1-a's finding was that the sheet's own tally was reachable only
through an undocumented dedupe *plus* an arbitrary reclassification of one of two hybrid rows.
Printing one number would reproduce that defect in the correction. The row count and the claim count
are different questions and are now separately answerable.

---

## 3. Seed-corpus verification pass (owed before first use)

Source: `SEEDED-DEFECT-CORPUS-v0.1.md` (operator's `Downloads`, browser-authored 2026-08-10),
§"CC's verification pass". Per seed, three criteria: **(1)** injectable without tripping a
pre-commit gate that would *mask* it from review, **(2)** detectable in principle from the reviewed
surface alone, **(3)** reversible in one revert.

**Method — measured, not reasoned.** The six code seeds were rendered as real Python and run through
this repo's actual ruff gate (`uv run ruff check --config pyproject.toml`, v0.15.5, `extend-select =
[]` — the **default** rule set, which is the whole question). The two format seeds were run through
the live `normalize-dated-headers` rewriter. SD-C3 was injected as a real staged file and
`scripts/audit.py health` was run to an exit code. Nothing below is inferred from reading a hook
config.

### Per-seed verdicts

| Seed | Verdict | Basis |
|---|---|---|
| **SD-V1** self-referential assertion | **SEEDABLE** | ruff clean. `PLR0124` (comparison-with-itself) is a pylint rule, absent from the default set; and the disguised form (locally-constructed expected value) would evade it anyway |
| **SD-V2** `assert len(result) >= 0` | **SEEDABLE** | ruff clean. No default rule covers a vacuous assertion; `PT`/`PLR` families are not selected |
| **SD-V3** mocked function asserted against its own mock | **SEEDABLE** | ruff clean. No static rule in any selected family models mock-exercises-itself |
| **SD-F1** `try/except Exception: return True` | **SEEDABLE** | ruff clean. `BLE001` (blind-except) is flake8-blind-except, not in the default set |
| **SD-F2** `except FileNotFoundError: pass` | **SEEDABLE** | ruff clean. `S110` (try-except-pass) is flake8-bandit, not in the default set |
| **SD-F3** `subprocess.run(..., check=False)`, returncode never read | **REWORK** | **the one code seed a gate catches** — and it catches the wrong thing. `F841 Local variable 'result' is assigned to but never used` fires on the *binding*, not on the unchecked returncode. Rework verified live: both `subprocess.run(...)` with no binding, and binding-then-consuming `result.stdout`, pass ruff clean while preserving the oracle (returncode still never read) |
| **SD-L1** `file:line` drifted ≥30 lines | **SEEDABLE** | no gate resolves prose `file:line` citations. Detectable from the surface: the reviewer opens the cited line. **Live proof this class is real, not hypothetical:** the Fable review's own `JOURNAL.md:1905` had drifted ~72 lines by this arc (§1) |
| **SD-L2** SHA edited by one hex digit | **SEEDABLE** | no gate resolves SHAs in prose. Detectable via `git log -1 <sha>`; this arc resolved 10 of 10 that way |
| **SD-L3** cross-doc anchor to a renamed section | **SEEDABLE** | `undeclared_edges` reasons about *declared* edges, not anchor resolution; no gate resolves in-document anchors |
| **SD-C1** unclosed triple-backtick fence | **SEEDABLE, with a named injection condition** | the fence is not repaired by any gate. **But `normalize-dated-headers` is a rewriter and it did touch the probe file** — it promoted `## <ISO-date>` → `### <ISO-date>` *outside* the fence while leaving the swallowed heading alone. It neither repairs nor conceals the fence, so the oracle survives; the condition is that the injected file carry no `## <ISO-date>` headings, or the seeded bytes change under the author. A JOURNAL/LESSONS-shaped dated log is therefore a poor injection site for this seed |
| **SD-C2** table row with mismatched pipe count | **SEEDABLE** | no gate parses markdown tables; verified untouched by the normalizer in the same probe |
| **SD-C3** duplicated YAML frontmatter key | **BLOCKED-BY-GATE** at the specified site | premise confirmed first: PyYAML resolves duplicate keys **last-wins, silently** (`{'id': …, 'status': 'done', …}` — no error, no warning). But the specified injection site is a **copy of a task file**, and `tasks/` is gated: staged, it produces `[!!] task_tree_coherence: BACKLOG.md is STALE vs the tasks/ source of truth`, and `audit.py health` **exits 1**, so the `audit-health` pre-commit hook refuses the commit. Measured, not predicted |

### Tally

**12 seeds: 9 SEEDABLE · 1 SEEDABLE-with-condition (SD-C1) · 1 REWORK (SD-F3) · 1 BLOCKED-BY-GATE
(SD-C3).**

By class: **V 3/3 seedable · F 2/3 seedable + 1 rework · L 3/3 seedable · C 1 seedable + 1
conditional + 1 blocked.**

### What the pass establishes, and what it does not

- **The gate surface does not mask this corpus.** Eleven of twelve seeds survive to a reviewer's
  eyes. That is the property the corpus needed, and it is now measured rather than assumed.
- **The reason is specific and fragile:** `[tool.ruff.lint] extend-select = []`. This repo runs
  ruff's **default** rules only. Every Class-V and Class-F seed survives *because of that one line*.
  Selecting `BLE`, `S`, or `PLR` would convert SD-F1, SD-F2 and SD-V1 into gate-regression seeds
  overnight — so this verdict table is pinned to a config value, and re-verification is owed if that
  line changes.
- **SD-C3 is not broken, its injection site is.** The seed's oracle (a silently last-wins duplicate
  key) is sound and its premise is confirmed. It needs a frontmatter-carrying file *outside* the
  generated-tree gates. Naming that site is left to the corpus SPEC (`wf-02c940ef`, Lane A), which
  governs.
- **Criterion (3), reversibility, holds for all twelve** — every seed is a single-file textual
  change on a throwaway branch, revertable in one `git revert` / branch delete. No seed requires a
  generated-artifact regen to undo, with the sole exception of SD-C3, which cannot be committed at
  its specified site in the first place.
- **Not established:** detection *rates*. This pass answers "can the seed reach a reviewer", not
  "does any given model catch it". The incumbent-vs-candidate scoring run is the corpus protocol's
  own next step and is not performed here.

---

## 4. Judgment calls this arc made, and what it deliberately left alone

**Two dates were chosen, not given.** Rulings 13 and I-1 both say *"convert to a dated review"* and
neither names a date. Both `[#322]` and `[#360]` are dated **2026-09-09** — the repo's own 30-day
review cadence (`scripts/canonical_freshness_gate.py::FRESHNESS_CADENCE_DAYS = 30`) counted from the
ruling date. The alternative — pegging them to the batch-4 GO — was rejected because that would
re-introduce an event-peg, which is the exact shape the ruling retires. Flagged for the operator to
overrule cheaply; changing a date is a one-line edit.

**Statuses were not moved.** `[#492]` stays `deferred` (explicitly ruled). `[#322]` stays `deferred`
and `[#360]` stays `open` — the checklist says *"row stays open"* for `[#322]` and says nothing about
`[#360]`'s status, so neither was moved. A dated review is a change of *trigger*, not of state.

**Deliberately not done, per the arc's own scope:**

- **FORK 4** (the births package at the batch-4 GO) — not answered, not recorded, nothing born.
- **The `[#241]` and `[#390]` row texts** — owed to the batch4-prep lane's DRAFT paste-blocks. The
  *rulings* are recorded in §I-D; the row edits are not drafted here.
- **Every intake `status:` / `decided-by` field** — untouched. Intake #28 §B is decided and banked
  (§I-F2); the flip is one atomic act at the batch-4 GO. **Intake #28 therefore carries an operator
  decision its own frontmatter does not show, and that gap is deliberate** — recorded here so a
  later seat reads it as a decision rather than an omission.
- **The `[#419]`/`[#426]` absorb-organ amendment DRAFT** — does not exist on disk. The
  digest-absorb-prep lane had produced zero commits at recording time (`git log main..HEAD` empty in
  its worktree). The scheduler-run scope line is recorded as that DRAFT's **input** (§I-I2) rather
  than applied to a file that is not there.

---

## 5. Standing authorization created by this arc

**Absorb ×7 is authorized** (FORK 3, reading (b)): `claude/conformance-2026-08-{03,04,05,07,08,09,10}`
merge into `main` as one serial batch, each branch deleting at its own merge per MERGE IS ATOMIC.
The authorization locator is **this arc's merge SHA**. Execution is sequenced *after* the
digest-absorb-prep lane merges, consuming that lane's DRAFT triage table.

**The authorization covers seven.** An eighth digest (`2026-08-11`) appearing before execution falls
outside it; the standing instruction on that case is to stop and report rather than extend the batch.

**Note the interaction with `automation/*` protection (3c-3), recorded so the two are not confused:**
`claude/conformance-*` branches are protected *until absorbed* and delete *at* their absorb merge.
`automation/*` branches are protected *permanently* — they exist to live outside `main`. Same
protection list, opposite lifecycles.
