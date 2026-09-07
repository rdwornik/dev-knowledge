# Census — `docs/intake/` (SWEEP 2026-09-07, lane S-02, READ-ONLY)

**Consumer:** `[#548]`, `[#549]`, `[#550]` — the three open rows that already own the
ACCEPTED-but-un-parkable intakes #12 / #13 / #14; this census re-measures their subject and adds
the four findings below. Substantive citations are by path throughout.
**Class:** `technical` · **Verb:** RETIRE-PROPOSED / KEEP — **the operator rules every verdict here.**
**Nothing in `docs/intake/` was moved, edited, renamed or deleted by this lane.** The tree this
census measured is the tree it left.

**Authority.** Batch file `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md`. **NOT READ** — the Drive
transport `CLAUDE PROMPT DIR` is not mounted in this execution environment (`H:\` absent; no
`to-cc/` in the repo or on this filesystem). This lane ran from the working copy of the contract
in its own dispatch prompt and **cannot certify agreement with the frozen original.** Recorded
here rather than assumed, per §2 of that working copy.

**Measured at:** `main` merged clean into `claude/census-docs-intake`; base `5f27b20`
(`Merge branch 'docs/anchor-w2u2f1-2026-09-07'`). `git merge origin/main` → *Already up to date*.

---

## Inventory

80 files under `docs/intake/` — 66 live intake docs at depth 1, 12 at `archive/`, plus the
generated `README.md` and `manifest.json`. The two counts are corroborated by the ruled organ,
not by this lane's `ls`:

```
scripts/funnel_lifecycle.measure(Path('.')) ->
Measurement(detector='funnel-lifecycle/v1', live_intakes=66, archived_intakes=12,
            live_adrs=90, rows=364, post_cutoff_rows=28, ready_intakes=19,
            threshold_days=30, threshold_locator='protocols/FUNNEL_LIFECYCLE.md:322',
            violations=[])
```

`violations=[]` is the load-bearing half: legs **a1** (a terminal-status doc still at depth 1),
**a2** (an ACCEPTED doc consumed in substance but never flipped) and **d** (a READY doc past the
30-day threshold with no review date) each measure **0** on this tree. `README.md`'s generated
Contents block independently renders **66 intake documents** — SEED 10 · DRAFT 18 · READY 19 ·
ACCEPTED 19.

*Witness column:* consumer counts are `grep` over all 2,914 tracked non-intake files, keyed on the
filename **and** on the `intake #N` textual form; a bare `#N` is deliberately **not** resolved,
because the backlog and intake id namespaces collide (`funnel_lifecycle.py` records the same
refusal). "d idle" = days since the last non-merge commit touching the file, as of 2026-09-07.

**The 80-row table is an appendix**, per the contract's own >40 KB remedy:
`docs/audits/2026-09-07-technical-census-docs-intake-appendix.md`. Verdict totals and every
finding stay here; the appendix carries only the per-file rows and their witnesses.

---

## Proposals

### KEEP — 74 files

Every file not named under RETIRE below. Sixty-six of them carry a live consumer, an ADR, a
`tasks/` row, or an age below the ruled survival metric; the twelve at `archive/` are already at
their retention home and the two generated files are emitted, not authored. **No `RELOCATE`
proposal exists in this folder**: leg a1 measures 0, so no terminal-status document is sitting at
depth 1. That is a change from the state `tests/test_audit.py` still describes — its
`check_funnel_lifecycle` note says leg a1 *"FAILs on live main by design (intake #19/#26 ruled
CONSUMED 2026-08-29 and still at `docs/intake/` depth 1)"*. Both are now at
`docs/intake/archive/` (`a5f71b1f`, 2026-08-29), so **the module's own promote-to-`TIER_COMMIT`
condition — "when leg a1 measures 0 on main" — is met and the tier has not been promoted.**
Reported, not acted on.

### RETIRE — 6 files, all SEED, all PROPOSED

The ruled bar is `docs/intake/README.md` §7: *"intake docs sitting unconsumed after ~1 month of
operation trigger a review of the scene for removal"* (ADR-98 §6). It has fired exactly once —
`protocols/STANDING_RULINGS.md` I-D7, on intake #10 at 32 days — and the operator's disposition
then was REJECT-and-archive with a reason. `docs/intake/archive/2026-07-16-satellite-onboarding-prompts.md`
records the same shape at 48 days. These six clear that bar with no carrier row of any kind:

| id | file | idle | `tasks/` rows | ADRs |
|---|---|---|---|---|
| #4 | `2026-07-07-arc5-pilot-followup-seeds.md` | 62 d | 0 | 0 |
| #5 | `2026-07-07-changelog-review-seeds.md` | 62 d | 0 | 0 |
| #7 | `2026-07-08-func-ai-council-interface.md` | 62 d | 0 | 0 |
| #8 | `2026-07-08-func-night-routines-suite.md` | 62 d | 0 | 0 |
| #9 | `2026-07-08-func-dashboards-local-html.md` | 62 d | 0 | 0 |
| #21 | `2026-07-30-tech-browser-architect-orientation.md` | 40 d | 0 | 0 |

**What the verdict is NOT.** These six are cited 7–13 times each across `docs/audits/` — but an
audit that *measures* a SEED is not a consumer that *carries* it, and the rent rule in
README §7 names the technical-architect triage as the consumer, not the census corpus. The
distinction is the whole point of the verdict.

**Route, not a move.** RETIRE here means the I-D7 shape: open the survival review, the operator
rules REJECT-with-reason (or re-scopes, or fires the arc), and only that ruling relocates the file
to `archive/`. This lane proposes; it moved nothing.

**Deliberately NOT proposed for retirement**, though they are also old: **#6** (47 d, but one live
`tasks/` row), **#22** and **#23** (SEED, but 2 and 3 live rows plus three ADRs between them),
**#36 / #37** (DRAFT, 17 d — under the bar), and the READY cohort #43–#47 / #51 (14 d and 12 d —
under the bar, and leg d agrees at 0).

### UNDETERMINED — 0 files

Every one of the 80 resolved to a verdict with at least one witness. What this census could **not**
establish is recorded in *Honest limits*, and none of it blocks a per-file verdict.

---

## The three questions this lane was asked

### 1 · Orphans — no row, no ADR, no audit consumes them

**Two, both one day old.**

| id | file | first commit | consumers outside `docs/intake/` |
|---|---|---|---|
| #74 | `2026-09-06-tech-cross-session-communication-protocol.md` | `7c5432ea`, 2026-09-06 | **none** |
| #75 | `2026-09-06-tech-copilot-offload-role-and-account-map.md` | `e49844bb`, 2026-09-06 | **none** |

Both are cited **only** by `docs/intake/README.md` and `docs/intake/manifest.json` — and both of
those are generated from the folder itself, so the folder is citing itself. Verified by filename
grep across the whole tracked tree.

**This is not rot, and the verdict is KEEP.** Both are DRAFT, filed within the last 24 hours; the
survival metric is ~1 month. What the measurement establishes is that the carrier is **not yet
born**, which is exactly the pre-`ACCEPTED` state ADR-98 expects. They are named here so that if
they are still orphaned at the next sweep the clock is already recorded.

**A namespace trap this census had to walk around, recorded so the next reader does not fall in
it.** `JOURNAL.md` and `docs/decisions/ADR-70-three-tier-process-automation.md` both carry
`#74` and `#75` — those are **BACKLOG** ids, filed 2026-06-02, and have nothing to do with
intakes #74/#75. A bare `#N` resolves into two namespaces here, which is why this census keys on
paths and on the literal `intake #N` form.

### 2 · ACCEPTED intakes whose Done-when is witnessed on main — ARCHIVE candidates

**Zero establishable — and the reason is a defect, not a clean folder.**

The ruled detector is `funnel_lifecycle` leg **a2**: an ACCEPTED doc whose `consumed-by:` names at
least one `[#id]` row, every named row terminal. It measures 0. But it measures 0 **vacuously**:
`consumed-by:` is populated on **no live ACCEPTED intake at all** (see finding B below), so the
field the detector reads is empty on all 19. The module records this against itself —
*"Leg a2 reads `consumed-by:`, which today NO live ACCEPTED intake carries with a row token"* —
and this census confirms it holds. **The ARCHIVE-candidate detector for ACCEPTED intakes cannot
fire on the current corpus.**

So the question was answered by hand instead. Of the 19 ACCEPTED docs, **two carry zero `tasks/`
rows** and are therefore the only ones where "consumed in substance" is even arguable:

- **#28** `2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md` — **not a candidate, by
  ruling.** `ADR-112-two-tier-adoption-bar.md` is its carrier, and `funnel_lifecycle.py` names
  this exact pair as the standing-authority class ADR-98 *"deliberately keeps live"*. README §5
  is explicit that ACCEPTED is **not** in the terminal set. KEEP.
- **#65** `2026-09-01-tech-consumer-at-landing-identifier-gap.md` — **not a candidate, because its
  Done-when is NOT witnessed on main.** The doc's own RULED section (line 90 ff.) leaves owed:
  a **PROVENANCE-CONSUMED** class in `consumer_at_landing`, a `DETECTOR_ID` bump, and a
  re-measure-and-re-stamp. On main today `scripts/consumer_at_landing.py:110` still reads
  `DETECTOR_ID = "consumer-at-landing/v2"` and the string `PROVENANCE` appears nowhere in the
  module. KEEP — **and see finding A.**

**The structural point.** Even had one qualified, "ARCHIVE an ACCEPTED intake" is not a move
README §5 permits: the terminal set is CONSUMED | SUPERSEDED | REJECTED, and ACCEPTED is excluded
by design so a standing authority stays visible. The lawful path is a **status flip to CONSUMED
with `consumed-by:` filled**, which then makes the doc terminal and the relocation follows. Any
future ARCHIVE proposal in this folder is really a proposal to flip a status.

### 3 · Duplicate ids after W1-5

**Zero, by the ratified predicate — measured, not restated:**

```
python -c "import sys; sys.path.insert(0,'scripts'); import gen_intake_index as g; print(len(g.duplicate_id_reasons()))"
-> 0
```

A raw file-level count says something different and it is worth stating why it is not a
contradiction. **`intake-id: 14` appears on three files:**

- `2026-07-12-siem-requirements-ruled-pack.md` — ACTIVE, ACCEPTED, holds the id live
- `archive/2026-07-13-siem-fleet-management-requirements.md` — CONSUMED, `consumed-by:` the pack
- `archive/2026-07-13-siem-fleet-management-requirements-codex.md` — CONSUMED, same

`gen_intake_index.duplicate_id_reasons` rules this **legal and deliberate**: one ACTIVE holder
plus archived provenance drafts is the join-key model README §5 ratifies; the collision classes
are *two ACTIVE docs on one id* and *two ARCHIVED docs with no active holder*, and neither
obtains. W1-5 (`lane-u-000-intake-id-next-free`) reached the same conclusion the hard way — it
refused the contract's instruction to renumber #14, because doing so would have stripped `#14`
from the live authority and handed it to an archived draft, breaking carrier row `[#550]`. Its
honest before→after was `1 → 0`, not the contract's `4 → 0` (JOURNAL.md 2026-09-07 (d)).

**The id namespace is otherwise contiguous 1–75, 77 — with 76 absent from `main`.** That is not a
gap in the allocator. `JOURNAL.md:748-750` records intake **#76** as **HELD, not merged**, on
`docs/intake-031-two-chats @ b6b7cb08`, and this lane **resolved the locator rather than relaying
it**: the ref exists on origin, and #76 is
`docs/intake/2026-09-06-tech-browser-window-shape-and-decision-carriage.md`, `status: DRAFT`.

Two corrections to the JOURNAL's picture, both measured this run. **(a)** The branch has advanced
past the SHA the JOURNAL names — tip is `949b8961` (*"date the #76 correction against all three
refs, not one"*), and `git merge-base --is-ancestor` confirms it is **still unmerged**, 7 commits
ahead of `origin/main` and 61 behind. **(b)** #76 carries the same empty `consumed-by:` at DRAFT
as the 23 docs in finding B — independent confirmation that the template, not any one author, is
the cause.

The all-refs allocator W1-5 shipped exists precisely so the next filing sees this; a `main`-only
`max()` would hand out 76 again.

---

## Four findings — reported, not fixed

### A · An ACCEPTED intake with zero carriers and an unbuilt deliverable — a live P-2 breach

`protocols/STANDING_RULINGS.md` P-2 (line 1817): *"An intake flipped to `ACCEPTED` carries at
least one live carrier row, or a `disposition: deferred` naming a live, DATED trigger. `ACCEPTED`
with zero carriers and no dated deferral is not a lawful terminal state."*

**Intake #65** is `status: ACCEPTED`, `disposition: active`, and carries **zero** `tasks/` rows
(grep over `tasks/*.md` for both the path and `intake #65`: 0 hits). Its owed work is unbuilt on
main. This is the unlawful state P-2 names, live, six days after the ruling that created it.

Related and **already owned, so not re-filed**: intakes **#12 / #13 / #14** are all
`disposition: deferred` behind `trigger: "#328 build"` — and `[#328]` does not exist in `tasks/`
or `tasks/archive/` (verified this run). An undated trigger pointing at a departed row is not the
"live, DATED trigger" P-2 requires. Rows `[#548]`, `[#549]` and `[#550]` each state this defect in
their own bodies; they are this census's declared consumer.

### B · `consumed-by:` is present-and-empty on 22 live docs, and the template is the cause

README §3 says the companion fields are *"REQUIRED at their status … leave absent at any other
status"*. `templates/intake-template.md` line 5 says the opposite — it ships `consumed-by:` in the
skeleton with *"leave blank until status: CONSUMED"*. Docs built from the template inherit an
empty key at SEED / DRAFT / READY / ACCEPTED.

Measured: **23 live docs** carry `consumed-by:` with an empty value at a non-CONSUMED status
(#4, #5, #6, #7, #8, #9, #16, #22, #23, #42, #62, #63, #65, #66, #67, #68, #69, #70, #71, #72,
#74, #75, #77 — of which #16 and #65 are ACCEPTED), plus one archived REJECTED doc (#64).

This is not cosmetic. It is why finding *2* above is vacuous: leg a2's whole predicate reads a
field that the template guarantees will be present and blank. **Two documents disagree and the
template wins in practice.** The fix is a ruling on which text is authoritative, not an edit by a
census lane.

### C · README §3's key allowlist is stale — `reconciled_with` is live and off it

README §3 closes with *"Any other key is off-schema."* Four live intakes carry
`reconciled_with:` — **#40, #53, #61, #68**. The key is not a mistake: `CLAUDE.md` §4 names the
`reconciled_with:` stamp as live spec-driven-development machinery, `scripts/gen_intake_index.py`
docstrings call `last_reviewed` and `reconciled_with` *"both live"*, and `[#241]` / `[#335]` /
`[#367]` all govern it as a first-class corpus edge. **The README is behind practice, not the four
files.** Proposal: add it to §3's optional-key list. Not this lane's edit.

### D · Nothing gates intake frontmatter against README §3

`gen_intake_index._parse_frontmatter` reads exactly two keys (`intake-id`, `status`);
`gen_intake_tree.py` projects the same two. `duplicate_id_reasons` gates ids. `funnel_lifecycle`
gates status-vs-location and READY age. **No organ validates the companion-field rules** —
which is why B and C were both invisible until a census read all 78 files. This is the same class
README §5 already admits about the archive move (*"the status-coupled validator … is wave work,
not built"*), one field wider. Reported for triage, not proposed as a build.

---

## Counts before → proposed after

```
files under docs/intake/ (whole tree)      80  ->  80   (nothing created, nothing deleted)
  live intake docs, depth 1                66  ->  60   (6 RETIRE-PROPOSED relocate on an operator ruling)
  archived intake docs, archive/           12  ->  18
  generated (README.md, manifest.json)      2  ->   2

verdicts                     KEEP 74 · RETIRE 6 · RELOCATE 0 · ARCHIVE 0 · UNDETERMINED 0

duplicate intake-ids (ratified predicate)   0  ->   0   (unchanged; W1-5 closed 1 -> 0)
funnel_lifecycle violations                 0  ->   0
orphans (no row, no ADR, no audit)          2  ->   2   (#74, #75 — both 1 day old; KEEP)
ACCEPTED docs, zero carrier rows            2  ->   2   (#28 ruled standing-authority; #65 = finding A)
frontmatter schema deviations              27  ->  27   (23 live empty consumed-by + 1 archived + 4 reconciled_with, less 1 overlap; findings B/C)
```

**Every "after" number is conditional on an operator ruling.** This lane changed nothing; if no
ruling lands, every "after" equals its "before".

---

## Honest limits

**1 · The frozen authority was not read.** `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (5422 B) is
on the operator's Drive transport, which is **not mounted in this execution environment** — no
`H:\`, no `to-cc/` on this filesystem or in the repo (`find / -name
BATCH-2026-09-07-SWEEP-CONTRACTS.md` → nothing). Its own §Authority says *"if they disagree with
it, it wins"*, and this lane **cannot certify that its working copy agrees with it.** Every
verdict below inherits that.

**2 · Gemini fan-out: `NONE`.** `which gemini` → exit 1, not on PATH. **Gemini-read files: 0.
Fabricated locators: 0 — of 0 returned.** A zero fabrication count from a CLI that never ran is
not evidence of accuracy and must not be read as one. **Copilot Enterprise offload was NOT used**
and was not available: it is gated on `[#75]`… which is intake **#75**, one of this census's own
subjects, and it is `status: DRAFT` — unratified, and one of the two orphans in finding 1.

**3 · The clone arrived SHALLOW and the witness class was nearly lost.** `.git/shallow` was
present; history began 2026-09-01 at 278 commits, and **every one of the 78 intake docs reported
the same "last content commit" — `428656f`, the graft boundary.** Had that gone unnoticed, the
entire `last content commit` witness column would have been a uniform artifact reported as
measurement. It was fixed by `git fetch --unshallow` (6,876 commits), which touches the local
object store only and wrote nothing to the tree. **Any peer lane tonight that reported a commit
date without checking `.git/shallow` should be re-read.**

**4 · The declared environment could not be built, so no gate was run end-to-end.**
`pyproject.toml` pins `uv` at `==0.11.19`; this container ships `0.8.17`, so every
`uv run --locked …` refuses. The three organs cited above were imported directly under a scratch
venv (`click`, `pyyaml`, `rich`, `pydantic`, `packaging`, `markdown-it-py`) — so
`funnel_lifecycle.measure` and `gen_intake_index.duplicate_id_reasons` are **live-run** results,
but they are run outside the locked environment. **`scripts/audit.py health` was not run. No test
was run** (contract §6: no full suite). The `Measurement` and the `-> 0` are real; their
environment is not the declared one.

**5 · What "consumes" means here is a `grep`, and a `grep` over-reports.** The consumer counts
credit any file that names the intake by path or by `intake #N`. A `docs/audits/` file that
*measures* a doc scores identically to a `tasks/` row that *carries* it. That is why the RETIRE
verdicts key on `tasks/` rows and ADRs only, and why the audit column is shown but never
load-bearing. **Under-reporting is also possible**: an intake consumed under a paraphrase, or
under a bare `#N` this census deliberately refuses to resolve, is invisible to it.

**6 · Done-when was not adjudicated per criterion for 17 of the 19 ACCEPTED docs.** Question 2 was
answered structurally — via leg a2, then by hand for the two docs with zero carrier rows. The
other seventeen all carry at least one live `tasks/` row, which is sufficient to establish *not
yet fully consumed* but **not** sufficient to establish *how much* of each doc's acceptance
criteria is witnessed on main. Reading 19 acceptance-criteria sections against the tree is a
larger act than this census, and pretending otherwise would be the padding §3 of the contract
forbids.

**7 · The id namespace was checked against every ref this clone can see — after the unshallow, and
not before.** #76 was resolved on `origin/docs/intake-031-two-chats` (tip `949b8961`, unmerged).
But the sweep for *further* held ids was a scan of `origin`'s refs only: an id living in an
unpushed local tree on the operator's machine — the exact case ruling D8 was written for, and the
one that produced `77` — is **outside this container's reach and is not established**. The
correct statement is "no additional held id on origin", not "no additional held id".

**8 · Two things this census names but did not verify to their root.** The
`check_funnel_lifecycle` tier-promotion condition (KEEP section) is inferred from the module's own
recorded criterion plus a measured `violations=[]`; whether the promotion is *desirable* is a
ruling, and this lane did not read `[#590]` or the FM-2 contract. And finding D's claim that *no*
organ validates intake companion fields rests on reading the two generators, `funnel_lifecycle`
and the pre-commit config — **not** on an exhaustive sweep of all 54 `audit.py` checks.

**9 · Read-only is verified, not asserted.** `git status --porcelain -- docs/intake/` is empty at
the time of writing; the only file this lane creates is this one.

---

## Lane packet

```
lane:                S-02 (census) · docs/intake/
branch:              claude/census-docs-intake
mode:                READ-ONLY — 0 files moved / edited / renamed / deleted in docs/intake/
deliverable:         this file (1 new file; no appendix — 33.8 KB, under the 40 KB cap)
gemini fan-out:      NONE (CLI absent from PATH) · files read by gemini: 0 · fabricated locators: 0 of 0
copilot offload:     NOT USED, NOT AVAILABLE — gated on intake #75, which is DRAFT/unratified
review:              NONE (no reviewer CLI available in this environment)
suite:               NOT RUN (contract §6) · audit.py health NOT RUN (uv version mismatch, limit 4)
organs run live:     funnel_lifecycle.measure · gen_intake_index.duplicate_id_reasons
journal entry:       NONE · merge: NONE · self-merge: NONE
```

---

## Addendum — post-merge re-measure, 2026-09-07

**The tree moved under this census between its measurement and its push.** `git fetch origin main`
before the push brought in W2-F5's erratum lane, which touched three files inside this census's
folder. Recorded here rather than folded into the body above, so the difference between what was
measured and what is now true stays legible.

**What changed.** `docs/intake/2026-09-05-tech-aj-second-pass.md` (**intake #70**) flipped
**DRAFT → ACCEPTED** under ruling F-5 of `DECLARE-F-2026-09-06.md`, gaining `decided-by:`,
`disposition: active`, `note:` and `consumers:`, and losing its empty `consumed-by:`.
`README.md` and `manifest.json` were regenerated to match.

**What that does to the numbers above.** Re-run on the merged tree at `3398d3b3`:

```
funnel_lifecycle.measure -> live_intakes=66, archived_intakes=12, violations=[]   (unchanged)
gen_intake_index.duplicate_id_reasons -> 0                                        (unchanged)

status distribution      SEED 10 - DRAFT 18 -> 17 - READY 19 - ACCEPTED 19 -> 20
consumed-by empty at a non-CONSUMED status      23 live -> 22 live  (#70 leaves)
frontmatter schema deviations                        27 -> 26
ACCEPTED docs with zero `tasks/` carrier rows         2 ->  3
```

**Everything else in this census stands**, including all 80 per-file verdicts: #70's verdict was
KEEP and remains KEEP, and no RETIRE row is affected.

**One finding got wider, not narrower.** Finding A named #65 as a live P-2 breach — ACCEPTED,
`disposition: active`, zero carrier rows. **#70 is now the same shape**: grep over `tasks/*.md`
for its path and for `intake #70` returns **0 hits** on the merged tree. Its `consumers:` field
names two `docs/audits/` artifacts, which is forward-looking provenance and legal at any status —
it is **not** a carrier row, and P-2's text asks for *"at least one live carrier row, or a
`disposition: deferred` naming a live, DATED trigger."* Neither obtains.

So the P-2 population is **#65 and #70**, and the second one was created by a merge that landed
tonight. That is the mechanism finding underneath finding A: **nothing at flip time requires the
carrier**, so each ACCEPTED flip is free to open a new breach, and only a census notices. Reported
for triage; this lane proposes no fix and edited nothing.

---

## Addendum 2 — the gates, actually run, 2026-09-07

**Honest limit 4 above is now partly FALSIFIED and is corrected here rather than left standing.**
It said no gate ran end-to-end because `uv` could not resolve. The declared version (`0.11.19`)
was obtainable after all and is now on PATH, so the gates ran. A census that leaves a testable
claim untested when the test becomes available has stopped being evidence.

**What still stands from limit 4:** the two organs cited in the *Inventory* section were run under
a scratch venv at measurement time, and their numbers are unchanged under the locked environment.

### `uv run --locked python scripts/audit.py health` → `DEGRADED`, exit 0

Self-audit **36/116 pass**, **62 WARN**, **3 FAIL**. **None of the three is this lane's**, and two
were established by controlled removal rather than asserted:

| FAIL | attribution |
|---|---|
| `repos registered (none)` | environment — no `ecosystem/` repo state in this container |
| `hooks_armed` — pre-commit, commit-msg and pre-push all absent; `merge.ours.driver` unset | environment — **see below, this one matters** |
| `silent_rule_ratchet: baseline raise rejected: 443 -> 447 (+4)` | **pre-existing** — byte-identical evidence string with and without this census file on the tree |

**The `hooks_armed` FAIL is the one worth reading twice.** The git hooks are **not armed in this
clone**, so **both of this lane's commits passed through zero pre-commit gates** — no `ruff`, no
`validate-hermetization`, no `audit-health`, no `consumer_at_landing`, no `block-commit-on-main`.
Nothing in this lane's landing was gate-verified at commit time; the verification is this addendum,
run after the fact. Any peer lane in an identically provisioned container is in the same position
and should not report its commits as gated.

### Targeted tests for a docs-only audit addition → 3 failed, 226 passed

`test_gen_audit_index` (×2) and `test_consumer_at_landing::test_the_live_corpus_measures_and_the_baseline_matches_it`.
**All three reproduce identically with this census file moved off the tree** (`3 failed, 57 passed`
both ways), so all three are pre-existing on the merged tree. The audit-index pair is *expected and
contractually correct*: the sweep contract forbids regenerating `docs/audits/README.md`, which the
integrator does once after the last merge. Neither is the known main RED the contract names
(`test_manifest_link_route.py`), which was not in this selection. **No full suite was run.**

### A correction to this lane's own earlier reporting

`consumer_at_landing` has two legs and this lane initially verified only one. **Leg 1 passes** —
this census declares its consumer, and `read_artifact` resolves all four citation classes
(`[#id]`, `ADR-NN`, `STANDING_RULINGS`, `intake #N`). **Leg 2 WARNs on it**: *"cited by no
governance surface and is not in the arm-time baseline — the unconsumed set grew."* That is the
other direction — nothing in the governance pool cites this file *yet* — and it is shared with all
nineteen `LANE-u-000-*` batch-U contracts plus `SEED_RUBRIC.md` and `VERDICT_RULE.md`.

It is also, precisely, the defect **intake #65** was ACCEPTED to fix: an audit-to-audit reference
has no declared class, so a landed artifact reads as unconsumed until a row cites it. Finding A
said #65's deliverable is absent from main. **This census tripping the very gate #65 exists to
narrow is the cheapest possible demonstration that it is still absent.**
