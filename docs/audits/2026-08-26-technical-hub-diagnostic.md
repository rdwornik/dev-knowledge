# HUB DIAGNOSTIC REPORT — `.dev-knowledge`

**Contract:** PART X of `C:\Users\1028120\Downloads\WINDOW-RECORD-AND-DIAGNOSTIC.md`
**Run:** 2026-08-26, primary checkout `C:\Users\1028120\Documents\Dev\.dev-knowledge`, branch `main`, working tree clean at start and at finish.
**Mode:** READ-ONLY. No repo file was written, no commit, no branch, no regeneration of any generated file. The only artifact produced is this report, in `~\Downloads`. Scratch scripts live in the job tmp dir, outside the repo.
**Token estimates** are `bytes ÷ 4` throughout, as the contract specifies. They are a proxy, not a tokenizer count.

---

## Summary — one page

**The accumulation is real, it is recent, and it is almost entirely in one tree.** `docs/audits/` is **728 files / 12.3 MB / ~3.08 M tokens** — 49% of everything under `docs/` by bytes and 2.3× the size of the entire rest of the governance corpus (`tasks/` + `decisions/` + `intake/` + `protocols/` + `ecosystem/` = 4.0 MB). It grew from **196 files (ADR-100's own measured basis, 2026-07-07)** to **728 today** — **3.7× in 50 days**, ~10.6 new audit files per day.

**Nothing is archived because archiving audits is ratified policy, not drift.** ADR-100 §1 decides *keep-all-accepted*: audits are "**never physically moved, rolled up, or compacted**", because ~78% of their citations sit in immutable/append-only files that can never be re-pointed. Navigability was delegated to a **count-tiered index** — `docs/audits/README.md`. That file is now the single most-touched file in the repo after `JOURNAL.md` (**41 touches in 300 commits**) and it appears in **6 of the 7** merges that needed manual resolution in the last 20. **The retention decision and the concurrency defect are the same decision.**

**Consumption, measured for the first time.** Of 727 audits (README excluded), **212 (29%) are cited by a governance surface** — a `tasks/` row, an ADR, `STANDING_RULINGS.md`, a protocol, or a root canonical doc. **515 (71%) are not.** Of those 515: **241 appear only in `ecosystem/audit-funnel-baseline.json`** — a machine baseline that enumerates files rather than consuming them — **225 appear only in narrative surfaces** (`JOURNAL.md`, other handoff bundles), and **49 are cited by nothing anywhere in the repo at all**. The 49 are overwhelmingly **lane contracts, lane packets, codex review outputs and nightly conformance digests**: single-use scaffolding that was never intended to be re-read but was written into the immutable evidence tree anyway.

**ADRs and intakes are healthy; audits are not.** **88/88 ADRs are cited** by at least one governance surface (0 orphans). **49/50 intakes** are cited; only 11 have produced an ADR, but 26 more produced a live backlog row, so the intake pipeline converts. The orphan problem is specific to `docs/audits/`.

**Priority is nearly flat and dependencies are decorative.** 165 open rows: **9 P1 / 88 P2 / 68 P3**. Only **4 of 316 rows declare `depends-on` at all**, and **2 of those 4 are written bare (`383`, `390`) which `_DEPID_RE = re.compile(r"#(\d+)")` cannot match** — the defect the contract anticipated, confirmed live at `scripts/validate_backlog.py:83` and `scripts/export_backlog_view.py:148`. Consequence: the "ready now" list is effectively *the whole open backlog*, 165 rows, because nothing is expressed as blocked. **The repo already owns this** as `[#424]`, open 31 days.

**Nothing can be iceboxed at 90 days, because nothing is 90 days old.** The oldest surviving open row (`[#23]`) was born **86 days** ago; the bracketed-id convention itself is only **86 days** old. At 90d the icebox is empty. At **45d it would move 49 rows** and leave 116; at **60d it would move 19** and leave 146.

**The single largest boot cost is `CLAUDE.md` at ~10.5 k tokens** — 35% of the ~30.0 k-token contracted boot read. But the contracted read is not where the weight is: `protocols/PLAYBOOK.md` (~105 k), `BACKLOG.md` (~71 k) and `JOURNAL.md` (~737 k) sit one on-demand read away. **A one-line-per-row `BACKLOG.md` would fall from 283 KB / ~70.8 k tokens to ~59.7 KB / ~14.9 k tokens — a 79% cut, and 91% off the row payload itself.**

**One defect found incidentally, not asked for:** two intake files both declare `intake-id: 42` (`2026-08-23-tech-generated-artifact-currency.md` and `2026-08-24-tech-agents-md-admission-vs-adr53.md`).

---

## Section 1 — Inventory and size

**Measurement command (per surface):**
```
find <dir> -type f | wc -l
find <dir> -type f -printf '%s\n' | awk '{s+=$1} END{print s}'
find <dir> -type f -exec cat {} + | wc -l
find <dir> -type f -printf '%s %p\n' | sort -rn | head -10
```

| surface | files | bytes | lines | ~tokens (B÷4) |
|---|---:|---:|---:|---:|
| `docs/audits/` | 728 | 12,319,698 | 167,915 | 3,079,924 |
| `docs/decisions/` | 91 | 1,045,646 | 12,951 | 261,411 |
| `protocols/` | 14 | 908,901 | 12,686 | 227,225 |
| `ecosystem/` | 107 | 795,215 | 11,258 | 198,803 |
| `docs/intake/` | 52 | 636,544 | 8,181 | 159,136 |
| `tasks/` | 318 | 581,401 | 5,690 | 145,350 |
| `docs/archive/` | 22 | 572,374 | 3,819 | 143,093 |
| *(not in contract, reported for scale)* `docs/handoffs/` | 737 | 10,580,882 | — | 2,645,220 |
| *(not in contract)* `logs/` | 95 | 45,120,292 | — | 11,280,073 |

`docs/` as a whole: **1,630 files / 25.2 MB**. All 7 contracted surfaces are 100% git-tracked except `ecosystem/` (98 tracked of 107 on disk — the 9 extras are `__pycache__` and gitignored state).

**Root canonical files**

| file | bytes | lines | avg chars/line | ~tokens |
|---|---:|---:|---:|---:|
| `JOURNAL.md` | 2,946,829 | 24,322 | 121.2 | 736,707 |
| `BACKLOG.md` | 283,019 | 464 | **610.0** | 70,754 |
| `LESSONS.md` | 263,463 | 668 | **394.4** | 65,865 |
| `ARCHITECTURE.md` | 103,666 | 1,160 | 89.4 | 25,916 |
| `CLAUDE.md` | 41,959 | 239 | 175.6 | 10,489 |
| `CONTRIBUTING.md` | 22,066 | 270 | 81.7 | 5,516 |
| `VISION.md` | 9,937 | 192 | 51.8 | 2,484 |
| `uv.lock` | 87,230 | 595 | 146.6 | 21,807 |
| `pyproject.toml` | 13,178 | 185 | 71.2 | 3,294 |
| `package.json` | 439 | 9 | 48.8 | 109 |

The three the contract singles out: **`BACKLOG.md` 610 chars/line** and **`LESSONS.md` 394 chars/line** are the outliers — both are one-record-per-line formats where the record is a paragraph. `JOURNAL.md` at 121 chars/line is ordinary prose; its cost is volume (**999 entries**, mean 2,948 bytes each), not density.

**Ten largest items per surface**

```
docs/audits/
  305453  2026-08-23-technical-backlog-adjudication-prep.md
  121571  2026-08-19-technical-c3-grooming-wave2.md
  121382  2026-08-15-technical-night2-consolidated-briefing.md
  115882  2026-08-25-technical-dispatch-surface-measured.md
  111084  2026-08-12-technical-night-2-lessons-governance-strategy.md
  100553  2026-08-23-technical-funnel-retro-classification.md
   92660  README.md                              <- the generated index
   82458  2026-08-10-technical-backlog-testability-census.md
   79378  2026-08-23-technical-phase0-preconditions.md
   78030  2026-08-23-technical-lane-562-local-admission.md
docs/decisions/
   89207  README.md                              <- the editorial index, 244 chars/line
   39715  ADR-101-hermetization.md
   37133  ADR-107-backlog-restructure-engine-schema-viewer.md
   29759  ADR-85-session-lifecycle-enforcement.md
   27711  ADR-89-computed-code-dependency-edges.md
   27020  ADR-109-fleet-desired-state-contract-v1.md
   26087  ADR-115-agents-md-portable-instruction-layer.md
   22959  ADR-45-handoff-architecture-v4.md
   22748  ADR-39-file-lifecycle-governance.md
   22702  ADR-104-fleet-repository-shape.md
protocols/
  419018  PLAYBOOK.md
  196050  STANDING_RULINGS.md
   83544  HANDOFF_PROCESS.md
   53121  archive/HANDOFF_PROCESS_v3.4.md
   39856  archive/HANDOFF_PROCESS_v4.4.md
   25538  AI_COUNCIL_PROCESS.md
   17196  HANDOFF_BOOT.md
   16308  ESSENTIALS.md
   15237  ENVIRONMENT.md
   14421  REPO_ONBOARDING.md
tasks/
   64623  manifest.json
    4778  README.md
    4313  480-code-impact-merge-without-review-artifact.md
    4273  582-substrate-router-one-gated-enum-a-capability-key.md
    4024  562-grok-4-6-guarded-rerun-a-no-pack-sandbox-before-th.md
    4021  491-gemini-scanning-lane-ruling-r-g-plus-an-acceptan.md
    3930  552-window-close-disposition-and-archival-routine.md
    3670  473-handoff-suffix-sibling-resolution.md
    3668  584-claude-md-10-in-lockstep-with-its-form-a-templat.md
    3624  583-green-by-skip-sweep-a-check-that-cannot-obtain-g.md
docs/intake/
   40967  manifest.json
   35808  archive/2026-07-13-siem-fleet-management-requirements-codex.md
   33065  archive/2026-07-13-siem-fleet-management-requirements.md
   27434  2026-08-06-tech-adoption-consolidation-intake.md
   27210  2026-07-27-tech-handoff-process-v6-proposal.md
   24606  2026-08-05-func-simplification-distribution-wave.md
   21729  2026-07-16-satellite-onboarding-prompts.md
   21102  README.md
   19047  2026-07-25-tech-consolidation-decision.md
   18056  2026-08-17-tech-repository-autonomy-and-gate-liveness.md
docs/archive/
   71703  2026-04-27-handoff-patterns-external-research.md
   38914  2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md
   35621  2026-08-09-research-code-style-doctrine-wf-8a83eb70.md
   35511  2026-08-17-research-multi-repo-config-standardization-wf-460fee76.md
   34325  2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md
   33517  2026-08-09-research-compute-placement-wf-1dc18e42.md
   32232  2026-08-17-research-repository-autonomy-and-gate-liveness-wf-76d68c06.md
   32059  2026-08-17-research-agent-instruction-layers-and-distillation-wf-50111a08.md
   31291  2026-04-24-claude-md-best-practices.md
   29676  2026-08-09-research-dependency-ontology-graph-wf-f6851745.md
ecosystem/
   92126  disposition-register.yaml
   54769  parity-surfaces.yaml
   41927  conformance.html
   41735  index.yaml
   33343  audit-funnel-baseline.json
   31122  conformance.md
   30826  schema/__pycache__/desired_state.cpython-312.pyc
   29493  .dev-knowledge/state.yaml
   23378  .dev-knowledge/history/2026-05-16.md
   22768  schema/desired_state.py
```

**Repo scale for context:** 2,491 tracked files, 28.3 MiB packed, 5,789 commits, 1,281 first-parent merges, first commit 2026-03-30 (149 days). On disk, excluding `.git` and `node_modules`: 268.7 MB, of which `.venv` 146.4 MB, `logs/` 43.0 MB (**untracked except one file** — `PROPOSALS-YYYY-MM-DD.md` runs ~1.7 MB/day and no retention rule covers it), `tests/` 42.7 MB, `docs/` 24.0 MB.

---

## Section 2 — Age and staleness

### 2.1 `tasks/` rows — and why filesystem age is the wrong instrument here

**Measurement:** `git log --pretty=format:@%at --name-only -- tasks/`, first occurrence per path = most recent commit touching it.

| bucket | all 316 rows | of the 165 open |
|---|---:|---:|
| < 7 d | 73 | 29 |
| 7–30 d | 243 | 136 |
| 30–90 d | 0 | 0 |
| > 90 d | 0 | 0 |

**This distribution is an artefact and must not be read as freshness.** `tasks/` was created **2026-07-27** by the ADR-107 §7.2 source-of-truth flip — the directory is 30 days old, so *no file in it can be older than 30 days by mtime*, and parallel lane batches rewrite many rows at once. **A second, honest age axis was therefore computed:** the first appearance of each `[#id]` in `BACKLOG.md`'s own 781-revision history.

**Measurement:** `git log --reverse --format=@%at -U0 -- BACKLOG.md`, scanning added lines for `\[#(\d+)\]`. 548 distinct ids ever seen.

| birth age (BACKLOG history) | open rows |
|---|---:|
| < 7 d | 21 |
| 7–30 d | 50 |
| 30–60 d | 75 |
| 60–90 d | 19 |
| > 90 d | **0** |

**Twenty oldest rows by last-touch** (the ceiling above makes these all 29 d; ids and titles as the contract asks):

```
[#116]  29d open      Hooks hygiene
[#127]  29d open      verify skill failure-output contract
[#139]  29d deferred  merged-arc->record verifier
[#144]  29d deferred  Feature DoD = end-to-end / user-flow test
[#153]  29d open      Enforcement-completeness pass
[#166]  29d deferred  doctrine_enforcement_coherence check
[#169]  29d deferred  Ungated-doc staleness detection
[#181]  29d deferred  Coherence v2 nudge-response
[#185]  29d open      GAP-2 deterministic gotcha-injection guard
[#188]  29d deferred  Deny-rule + hook completeness audit
[#189]  29d open      Execute in ~/.claude
[#19]   29d deferred  Complete the ADR-39 register
[#190]  29d deferred  General intra-file duplication detector
[#227]  29d open      Relocate AGENT_FRAMEWORK.md out of protocols/
[#23]   29d open      Validate ADR frontmatter relation-fields
[#231]  29d deferred  Consumer -> hub feedback report
[#234]  29d open      Cross-repo probe validator
[#240]  29d deferred  Follow-up
[#244]  29d open      Essence-spec lifecycle epic
[#245]  29d open      Add-path status-awareness
```

> **Stated limitation.** The twenty above are a *sample of the 29-day plateau*, not a genuine "oldest twenty" - 243 of 316 rows share the same last-touch value, so the ordering inside that tie is arbitrary (it fell out as id-lexical). Note that **9 of the 20 are already `deferred`**, which is the corpus's existing icebox. The birth-age axis below is the load-bearing measurement; use it, not the list above.

**Twenty oldest OPEN rows by BACKLOG-history birth age** - the honest answer to the contract's question:

```
[#23]   86d P3 S  Validate ADR frontmatter relation-fields
[#43]   86d P3 L  Decide + (title truncated in frontmatter)
[#71]   85d P3 S  Reconcile ENVIRONMENT.md's ~/.claude/ directory tree with live contents
[#82]   83d P3 M  Define per-repository agentic-review profiles
[#123]  80d P2 S  Routine observability convention + value review
[#112]  80d P2 M  adr_amend helper + ADR immutable-zone extension
[#116]  80d P3 S  Hooks hygiene
[#117]  80d P3 S  Evaluate prompt/agent-based hooks
[#127]  80d P3 S  verify skill failure-output contract
[#99]   80d P3 S  FLEET-HEALTH digest names the failing check per red repo
[#130]  79d P3 S  Memory-hygiene review
[#146]  77d P3 S  De-hardcode-first doctrine + sweep
[#145]  77d P3 M  Codification-completeness pass
[#153]  76d P2 M  Enforcement-completeness pass
[#170]  70d P3 M  Design + land the traceability-spine ADR
[#171]  70d P3 M  Build the conformance dashboard at ecosystem/conformance.md
[#185]  69d P2 M  GAP-2 deterministic gotcha-injection guard
[#189]  68d P3 S  Execute in ~/.claude
[#210]  61d P3 S  Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule
[#220]  55d P2 M  MODIFY / semantic-drift axis
```

**14 of these 20 are P3.** The oldest cohort is not deferred important work; it is low-priority work that has never been either done or killed.

### 2.2 `docs/intake/`

**Measurement:** `grep -h '^status:' docs/intake/*.md | sort | uniq -c`, plus git last-touch per file.

50 intake documents (README and `manifest.json` excluded), of which **7 are already relocated to `docs/intake/archive/`**.

| status | count |
|---|---:|
| ACCEPTED | 19 |
| SEED | 10 |
| READY | 7 |
| DRAFT | 7 |
| CONSUMED | 1 |
| *(unparseable — `status: <see §5>`)* | 1 |

**Undecided (DRAFT / SEED / READY, live directory): 24.** Ages, days since last commit touch:

```
 50d  SEED  #4   2026-07-07-arc5-pilot-followup-seeds.md
 50d  SEED  #5   2026-07-07-changelog-review-seeds.md
 50d  SEED  #8   2026-07-08-func-night-routines-suite.md
 49d  SEED  #7   2026-07-08-func-ai-council-interface.md
 49d  SEED  #9   2026-07-08-func-dashboards-local-html.md
 34d  SEED  #6   2026-07-08-func-new-project-bootstrap.md
 34d  READY #15  2026-07-16-satellite-onboarding-prompts.md
 29d  SEED  #19  2026-07-27-func-operator-design-input-night-shift-handoff-reform.md
 27d  SEED  #21  2026-07-30-tech-browser-architect-orientation.md
 25d  SEED  #23  2026-08-01-func-distillation-and-library-first.md
 22d  SEED  #22  2026-07-30-func-operator-decision-routing-and-standards.md
  5d  DRAFT #35  2026-08-17-tech-agent-instruction-layers-and-distillation.md
  5d  DRAFT #37  2026-08-17-tech-machine-verifiable-done-when.md
  5d  DRAFT #36  2026-08-17-tech-repository-autonomy-and-gate-liveness.md
  3d  DRAFT #40  2026-08-22-tech-document-dependency-graph-organ.md
  3d  DRAFT #41  2026-08-23-tech-nopack-guard-refusal-surface.md
  2d  DRAFT #34  2026-08-16-code-architecture-enforcement.md
  1d  DRAFT #42  2026-08-23-tech-generated-artifact-currency.md
  1d  READY #42  2026-08-24-tech-agents-md-admission-vs-adr53.md     <- DUPLICATE intake-id 42
  1d  READY #46  2026-08-24-tech-contract-integrity-gate.md
  1d  READY #44  2026-08-24-tech-disposition-register-schema.md
  1d  READY #43  2026-08-24-tech-ruling-register-landing-gap.md
  1d  READY #45  2026-08-24-tech-substrate-router.md
  1d  READY #47  2026-08-24-tech-supplement-probe-fill-state-defect.md
```

**The shape is bimodal:** 11 undecided intakes are 22–50 days old and all but one are `SEED`; the other 13 are ≤ 5 days old. **The `SEED` cohort of 2026-07-07/08 (#4–#9, six documents, 34–50 days) is the standing backlog of undecided intake** — everything filed since has either been decided or is still warm.

**Incidental defect: `intake-id: 42` is used twice** — `2026-08-23-tech-generated-artifact-currency.md` (DRAFT) and `2026-08-24-tech-agents-md-admission-vs-adr53.md` (READY). Verified with `grep -l '^intake-id: 42' docs/intake/*.md`.

### 2.3 `docs/decisions/` — superseded / rejected / parked still in the live directory

**Measurement:** first `Status` line of each `docs/decisions/ADR-*.md` (non-recursive), classified.

**Result: 2.**

- `ADR-114-readme-recreation-legality.md` — **PARKED** (operator ruling 2026-08-22)
- `ADR-115-agents-md-portable-instruction-layer.md` — **Proposed** (2026-08-25, in flight)

**Zero superseded and zero rejected ADRs sit in the live directory.** The two that reached those states were moved: `docs/decisions/archive/ADR-40-scale-tier-evaluation.md` (Deprecated) and `ADR-52-agents-md-convention.md` (Superseded), both relocated 2026-07-22 by `216ce3a8` under an operator ruling. The remaining 86 live ADRs are Accepted.

> **Method note, stated because it changes a number:** an initial regex expecting `**Status:**` classified 13 ADRs as "other". They are all plain `Status: Accepted` (no bold) — ADR-34 through ADR-47 era formatting, plus `ADR-61` which uses lowercase `status:`. Re-read individually; all Accepted. **The status line has at least three shapes in the live corpus** (`- **Status:**`, `**Status:**`, bare `Status:`, and `status:`), which is itself a small machine-readability defect.

### 2.4 `docs/audits/` — age distribution

**Measurement:** `git log --diff-filter=A --pretty=format:@%at --name-only -- docs/audits`, oldest add per path.

| bucket | files |
|---|---:|
| < 7 d | 111 |
| 7–30 d | 329 |
| 30–90 d | 212 |
| > 90 d | 75 |

727 audits (README excluded). **60% of the tree was created in the last 30 days.** The oldest is `2026-03-30-dev-practice-os-state-audit.md` (added 2026-04-14).

**"How many predate the current wave":** taking the current wave as the ADR-110 parallel-batch era beginning 2026-08-06, **351 audits (48%) predate it and 376 (52%) were produced inside it** — 20 days producing more audit artefacts than the preceding 129.

---

## Section 3 — CONSUMPTION

**Definition used, exactly as the contract states it:** an artifact is **CITED** if it is named by *any* `tasks/` row, *any* ADR, *any* `STANDING_RULINGS.md` section, or *any* protocol document. Root canonical docs (`BACKLOG.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `LESSONS.md`, `VISION.md`, `CONTRIBUTING.md`) and `docs/intake/` were included in the same governance pool — they are decision-bearing surfaces and excluding them would overstate the orphan count.

**Deliberately *excluded* from the governance pool, and this is the crux:** `JOURNAL.md`, `docs/handoffs/**`, `ecosystem/*.yaml|json`, `scripts/`, `tests/`, `.claude/`, `templates/`, `deploy/`. A mention in a session log or a machine baseline is a *record that the file existed*, not evidence that anything consumes it. Those are reported separately below so the distinction is visible rather than assumed.

**Measurement:** substring match of each artifact's basename (with and without `.md`) across the full text of every file in each pool; self-matches excluded. For ADRs the needle is the token `ADR-<n>` with a digit-boundary guard (`ADR-0*n(?![0-9])`) as well as the filename, because ADRs are cited by number, not by path.

### 3.1 Audits — headline

| | count | % of 727 |
|---|---:|---:|
| **CITED** by a governance surface | **212** | 29% |
| cited only by a **machine register** (`ecosystem/`) | 241 | 33% |
| cited only by a **narrative surface** (`JOURNAL.md`, other handoff bundles) | 225 | 31% |
| **CITED BY NOTHING, anywhere in the repo** | **49** | 7% |

**Governance citers of the 212, by edge count:** `tasks/` 161 · `docs/decisions/` 78 · `BACKLOG.md` 71 · `docs/intake/` 57 · `protocols/` 51 (of which `STANDING_RULINGS.md` 35) · `LESSONS.md` 12 · `ARCHITECTURE.md` 8 · `CLAUDE.md` 1.
106 audits are cited by at least one `tasks/` row; 49 by at least one protocol; 35 by `STANDING_RULINGS.md`.

**The 241 "machine register only" cohort is the finding under the finding.** `ecosystem/audit-funnel-baseline.json` alone names **441** of the 466 non-governance-cited audits. It is a baseline that *enumerates* audit filenames for the ADR-111 funnel; being in it means the machine has seen the file, not that any decision rests on it. **241 audits appear in that file and in no other file in the repository outside their own tree.** That, plus the 49 that appear nowhere at all, is **290 audit files (40% of the tree) with no human or governance consumer of any kind.**

### 3.2 ADRs

**0 of 88 ADRs are uncited.** Every live ADR is named by at least one governance surface. The thinnest:

- `ADR-115-agents-md-portable-instruction-layer.md` — 1 citer (`docs/decisions/README.md`) — *Proposed, 1 day old; expected.*
- `ADR-83-protocols-archive-convention.md` — 1 citer (`docs/decisions/README.md`) — **the genuine thin one.** A ratified convention that nothing in `protocols/`, `CLAUDE.md` §4 file-lifecycle, or any task row points back to, despite `CLAUDE.md` §4 describing the very lifecycle it governs.
- `ADR-50-machine-document-encoding.md` — 2 citers · `ADR-95-ai-council-query-lane-split.md` — 2 · `ADR-114` — 3 · `ADR-103`, `ADR-63` — 4 · `ADR-30`, `ADR-90` — 5.

**Coverage of ADRs by surface (number of ADRs each surface cites at least once):** `docs/decisions/` 88 · `protocols/` 75 · `tasks/` 64 · `ARCHITECTURE.md` 64 · `BACKLOG.md` 60 · `LESSONS.md` 38 · `CLAUDE.md` 31 · `CONTRIBUTING.md` 21 · `VISION.md` 12.

### 3.3 Intakes — which produced a decision, which are dead ends

**49 of 50 cited.** Verdicts (`DECISION` = named by an ADR; `ROW-ONLY` = named by a `tasks/` row but no ADR; `PROSE-ONLY` = named only in protocol/canonical prose; `DEAD-END` = named by nothing):

| verdict | count |
|---|---:|
| **DECISION** (produced an ADR) | 11 |
| **ROW-ONLY** (produced a backlog row, no ADR yet) | 26 |
| **PROSE-ONLY** | 12 |
| **DEAD-END** | **1** |

The single dead end is listed in full below. **The intake pipeline converts** — 37 of 50 intakes reached an ADR or a live row. That is the contrast with `docs/audits/`, and it is the argument that the problem is genre-specific rather than systemic.


---

## Section 4 — Priority reality

**Measurement:** frontmatter of `tasks/*.md` (316 row files; `README.md` and `manifest.json` excluded).

### 4.1 Open rows and priority distribution

| status | count |
|---|---:|
| **open** | **165** |
| closed | 120 |
| deferred | 26 |
| retired | 4 |
| superseded | 1 |
| **total** | **316** |

**Every row carries a priority marker** — the field is mandatory in the schema, so coverage is 316/316. Distribution across the 165 **open** rows:

| priority | open rows | share |
|---|---:|---:|
| P1 | 9 | 5% |
| P2 | 88 | 53% |
| P3 | 68 | 41% |

**P2 is not a priority, it is the default.** 53% of the open backlog sits in one band, and P2+P3 together are 95%. The signal carried by the field is effectively binary: *is this one of the 9 P1s, or not*.

### 4.2 What is genuinely READY NOW — and the dependency-field defect

**The contract's suspicion is confirmed, and it is worse than stated.**

- `scripts/validate_backlog.py:83` — `_DEPID_RE = re.compile(r"#(\d+)")`
- `scripts/export_backlog_view.py:148` — `_ID_TOKEN_RE = re.compile(r"#(\d+)")`

Both consumers of the `depends-on` field require a literal `#`. **Only 4 of 316 rows declare `depends-on` at all**, and **2 of the 4 are written bare and are therefore inert**:

| row | `depends-on:` | parses? | target state |
|---|---|---|---|
| `[#112]` | `"#23"` | yes | `[#23]` is **open** → genuinely blocked |
| `[#169]` | `"#171"` | yes | `[#171]` is not open → satisfied (row itself is `deferred`) |
| `[#385]` | `383` | **NO — inert** | `[#383]` is not open |
| `[#389]` | `390` | **NO — inert** | `[#390]` is **open** → this row is blocked and nothing knows it |

**Rows affected: 2 inert of 4 declared (50%).** In absolute terms the blast radius is small because *almost nothing declares dependencies* — but that is the deeper finding: **with 4 declarations across 316 rows, the dependency graph does not exist**, so "unblocked" is not a computable property of this backlog. What *does* exist is `serialize-group:`, carried by **204 of 316 rows** — the repo expresses contention (which lanes may not run concurrently) but not sequencing (what must precede what).

**The repo already owns this defect.** `[#424]` — *"Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare"* — P2/S, open, born 31 days ago. It is item 28 on the ranked list below.

**Consequence for this section:** with only one genuinely blocked row (`[#112]`, and `[#389]` if its inert edge were honoured), **"ready now" is 163–165 of the 165 open rows**. The ranked list below is therefore a *prioritisation*, not a filter. Ranked by priority, then size (S before M before L, so quick wins surface), then birth age descending. Capped at 60 per the contract.

**Ages shown are BACKLOG-history birth ages** (see §2.1 for why last-touch is unusable).

```
 #   row     pri sz theme  age   title
 --  ------  --- -- -----  ----  ------------------------------------------------------------
  1. [#359]  P1  M  E8      37d  PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechani
  2. [#514]  P1  M  E2      16d  Two rival `LANE_BRANCH_RE` constants ship in one repo
  3. [#519]  P1  M  E2      16d  The close path is two edits, and nothing makes a half-done close visible
  4. [#528]  P1  M  E7      11d  Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch 
  5. [#555]  P1  M  E7       8d  Closing campaign batch 1 + kill-candidates instrument
  6. [#580]  P1  M  E7       0d  State-as-data: atomic id allocation, and `tasks/` as the SOLE source (packet ARC-B)
  7. [#579]  P1  L  E2       0d  Code doctrine & FDD — one ADR merging intakes #31 and #34 (packet ARC-A)
  8. [#581]  P1  L  E7       0d  Backlog vitals — three flow instruments, a committed digest, and what-is-unblocked-now (
  9. [#582]  P1  L  E7       0d  Substrate router — one gated enum, a capability-keyed table, and the generator that read
 10. [#123]  P2  S  E7      80d  Routine observability convention + value review
 11. [#241]  P2  S  E2      54d  Undeclared-edge groom
 12. [#267]  P2  S  E2      51d  Scope-exercising arc extension
 13. [#303]  P2  S  E2      47d  Make seed_runbook.py child-class-aware
 14. [#331]  P2  S  E6      45d  Consumer BACKLOG schema adoption ruling
 15. [#340]  P2  S  E7      40d  /ship pre-flight validator honors the consumer repo's canonical test gate
 16. [#341]  P2  S  E7      40d  Codex producer-lane activation mechanism
 17. [#371]  P2  S  E8      36d  Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed
 18. [#387]  P2  S  E7      35d  Rewrite the buy-vs-build intake BEFORE anything ingests it
 19. [#389]  P2  S  E2      35d  Prompt-lint — gate the five architect fields before a lane runs
         ^^ depends-on 390 INERT (bare, no '#'; target OPEN)
 20. [#390]  P2  S  E1      35d  Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template
 21. [#401]  P2  S  E2      34d  ai-council routing still ARMED at the deleted hub landing zone
 22. [#404]  P2  S  E1      34d  gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)
 23. [#405]  P2  S  E2      33d  Session-end leftover check — nothing verifies \"no leftovers\
 24. [#413]  P2  S  E8      32d  Colors semantics — visually distinguish global/hub-managed vs per-repo content in govern
 25. [#414]  P2  S  E2      32d  Self-acting-on-main incident family — a session changed `main` with no operator GO and n
 26. [#418]  P2  S  E2      32d  `automation/fleet-audit` records 0–10 baselines a day, not one
 27. [#422]  P2  S  E1      31d  `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-c
 28. [#424]  P2  S  E2      31d  Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is wri
 29. [#428]  P2  S  E7      31d  `nightly-triage` reports a dead producer to every session start
 30. [#431]  P2  S  E7      30d  `codex-review` silently drops the doc lane on any mixed diff
 31. [#440]  P2  S  E7      29d  Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable
 32. [#445]  P2  S  E7      28d  `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing
 33. [#448]  P2  S  E8      26d  A11 staged-diff guard — cover EVERY candidate bundle, not just the active one
 34. [#454]  P2  S  E2      26d  `closure_ids` negation defect — the parser reads a negated closure mention as a closure
 35. [#457]  P2  S  E2      26d  Two live-repo tests fail on main against green gates — test-vs-organ mismatch
 36. [#477]  P2  S  E2      23d  `deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `
 37. [#478]  P2  S  E2      23d  `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silence
 38. [#493]  P2  S  E7      21d  B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days
 39. [#518]  P2  S  E2      16d  `scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row becau
 40. [#520]  P2  S  E2      16d  No sanctioned way to retire a committed bundle whose seal is wrong
 41. [#531]  P2  S  E2      10d  Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it
 42. [#534]  P2  S  E2       9d  `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition
 43. [#535]  P2  S  E7       9d  `audit.py` has two module identities in one process, and a test's monkeypatch is invisib
 44. [#548]  P2  S  E4       9d  Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows 
 45. [#551]  P2  S  E5       9d  Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live
 46. [#560]  P2  S  E2       7d  `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one tit
 47. [#561]  P2  S  E7       7d  Re-base the compute plan onto the Hetzner CX shared line
 48. [#585]  P2  S  E5       0d  Suite RED — `test_anchor_gate_probe_distinguishes_installed_from_absent` does not discri
 49. [#112]  P2  M  E2      80d  adr_amend helper + ADR immutable-zone extension
         ^^ depends-on #23 (OPEN - blocked)
 50. [#153]  P2  M  E2      76d  Enforcement-completeness pass
 51. [#185]  P2  M  E2      69d  GAP-2 deterministic gotcha-injection guard
 52. [#220]  P2  M  E2      55d  MODIFY / semantic-drift axis
 53. [#242]  P2  M  E2      54d  ADR status-flip coherence check
 54. [#245]  P2  M  E6      53d  Add-path status-awareness
 55. [#276]  P2  M  E6      50d  D2 per-consumer waiver-honoring
 56. [#277]  P2  M  E2      50d  propose_closures signal repair
 57. [#278]  P2  M  E7      50d  Test-suite hygiene epic
 58. [#289]  P2  M  E2      49d  Hub-own the OneDrive-Blue-Yonder guard
 59. [#317]  P2  M  E7      46d  Default-parallel test invocation
 60. [#327]  P2  M  E6      45d  Protocols-as-interface genre ruling
```

**Rows 61-165 are omitted by the contract's cap of 60.** All of them are P2 or P3; the cut falls inside the P2/M band. The full 165-row set is reproducible with the frontmatter parse in the method appendix.

### 4.3 Themes

**Open rows per theme:**

| theme | open rows |
|---|---:|
| `[E2]` Enforced governance | **54** |
| `[E7]` Tooling & evaluation | **43** |
| `[E6]` Cross-repo universalization | 16 |
| `[E5]` Canonical-file integrity | 15 |
| `[E8]` ARC-5 execution *(time-boxed arc)* | 13 |
| `[E1]` Handoff continuity | 8 |
| `[E4]` Decision management | 6 |
| `[E3]` Lessons feedback loop | 5 |
| `[E9]` Fleet Desired-State System (North Star) | 5 |

**`[E2]` + `[E7]` hold 97 of 165 open rows (59%)** — the repo's open work is dominated by *governing itself* and *tooling itself*. `[E9]`, named the North Star, holds **5**.

**Which themes have had no activity in 30+ days: none — and the measurement cannot answer the question.** Last-touch per theme (max over all its rows) ranges 0–9 days, because `tasks/` is 30 days old and lane batches rewrite rows in bulk. Using birth age instead, the newest row in each theme is: `[E2]` 0 d, `[E5]` 0 d, `[E7]` 0 d, `[E1]` 1 d, `[E4]` 1 d, `[E8]` 1 d, `[E3]` 1 d, `[E6]` 3 d, `[E9]` 9 d. **On either instrument, no theme is dormant at 30 days.** That is a real answer, not an evasion: this corpus has no dormant themes because the whole corpus is younger than the dormancy threshold.

---

## Section 5 — The concurrency defect, verified not assumed

### 5.1 Does `BACKLOG.md` carry a whole-file digest?

**No.** `grep -c 'sha256' BACKLOG.md` → **0**. Its only header guard is a prose comment:

```
<!-- GENERATED FILE — do not edit directly. Source of truth: tasks/ (per-task .md bodies + manifest.json).
     Regenerate: python scripts/gen_task_tree.py --emit-source   ·   ADR-107 strangler step 3, [#439]. -->
```

**The digest exists one level down, on the source rather than the view.** `tasks/manifest.json` carries a `generated_sha256` key (top-level keys: `schema`, `role`, `generates`, `generated_sha256`, `generator`, `nodes`). So the *source of truth* is digest-guarded and the *rendered view every lane regenerates* is not — which is the wrong way round for a concurrency defect, because the view is what merges conflict on.

### 5.2 Which files are regenerated by every lane

Touch counts over the last **300** commits (`git log -300 --name-only`):

| file | touches / 300 | regen gate |
|---|---:|---|
| `JOURNAL.md` | **56** | append-only, not generated |
| `docs/audits/README.md` | **41** | `gen_audit_index.py --check` (`audit-index-freshness`) |
| `BACKLOG.md` | 17 | `gen_task_tree.py` (`check_task_tree_coherence`) |
| `tasks/manifest.json` | 17 | same generator |
| `ecosystem/doc-counts.md` | 14 | `gen_doc_counts.py` |
| `ecosystem/disposition-register.yaml` | 5 | hand + tooling |
| `docs/intake/README.md` | 4 | `gen_intake_index.py --check` |
| `.claude/generated/recent-adrs.md` | 3 | `gen_claude_rosters.py --check` |
| `ecosystem/conformance.md` | 3 | `gen_dashboard.py` |
| `ecosystem/organ-index.md` | 2 | `generate_organ_index.py --check` |
| `.claude/methodology-roster.md` | 0 | `gen_methodology_roster.py --check` |
| `.claude/generated/commands-repo.md` | 0 | `gen_claude_rosters.py --check` |

**`docs/audits/README.md` is the hot one, and by a wide margin** — it is touched more than twice as often as `BACKLOG.md`, because *every lane that writes an audit artifact must regenerate the index*, and in the ADR-110 batch protocol every lane writes an audit artifact. The regen-and-diff pre-commit gate makes regeneration mandatory, so a lane cannot opt out.

### 5.3 Conflict rate over the last 20 merges

**Measurement:** for each of the last 20 first-parent merges, `git show --format= --cc --name-only <sha>`. A combined diff lists only paths whose content differs from **every** parent — i.e. paths the merger had to resolve or otherwise edit into the merge commit. This is the standard proxy for "this merge required manual resolution"; it also catches deliberate evil merges, and it is a floor, not a ceiling (a conflict resolved by taking one side wholesale leaves no combined-diff hunk).

**Result: 7 of 20 merges (35%) carry combined-diff content.**

| merge | date | resolved paths | subject |
|---|---|---:|---|
| `2626ff5b` | 2026-08-26 | 4 | `worktree-lane-g-governance` |
| `1858849a` | 2026-08-26 | 2 | `docs/rl-registry-filings-dispatch` |
| `d74a9809` | 2026-08-26 | 2 | `worktree-lane-x-failloud` |
| `257e745d` | 2026-08-25 | 1 | `claude/lane-v5-register-verification` |
| `7d3b2425` | 2026-08-25 | 1 | `claude/lane-v4-lifecycle-verification` |
| `71b4dfe4` | 2026-08-25 | 1 | `claude/verify-register-v2` |
| `9704ad31` | 2026-08-25 | 1 | `claude/lane-v1-verify` |
| *(13 others)* | 2026-08-24…26 | 0 | clean |

**Conflict rate per file:**

| path | merges it appears in | % of the 20 | % of the 7 |
|---|---:|---:|---:|
| **`docs/audits/README.md`** | **6** | **30%** | **86%** |
| `ecosystem/provider-registry.yaml` | 1 | 5% | 14% |
| `BACKLOG.md` | 1 | 5% | 14% |
| `tasks/manifest.json` | 1 | 5% | 14% |
| `docs/audits/2026-08-25-technical-green-by-skip-sweep.md` | 1 | 5% | 14% |
| `docs/audits/2026-08-19-technical-n3-ratification-pack.md` | 1 | 5% | 14% |
| `tasks/583-green-by-skip-sweep-a-check-that-cannot-obtain-g.md` | 1 | 5% | 14% |

**This is what integration costs today, quantified: one generated file causes 86% of the manual merge resolution in this repo.** `docs/audits/README.md` is an append-mostly index over a directory that every parallel lane writes into; two lanes each adding an audit both regenerate it, and the regenerated blocks collide. The generated `BACKLOG.md` / `manifest.json` pair — the file most often *blamed* for merge pain — appears in exactly **1 of 20** merges.

---

## Section 6 — Archive state

### 6.1 Does an archive convention exist?

**Yes — three of them, plus one explicit refusal to archive. All are governed and quotable.**

**(a) `protocols/archive/` — ADR-83 (Accepted, 2026-06-11).** Path, naming and tombstone are all specified:

> Superseded or dead protocols move to `protocols/archive/<name>.md` carrying a blockquote tombstone at the top of the file. `protocols/` (top level) holds only live specs.

The tombstone must carry the archived date (`> **ARCHIVED YYYY-MM-DD:**`), the superseded-by target and path, and a frozen-record line (`Do NOT edit this file; it is a frozen historical record.`).

**(b) `docs/archive/` — ADR-60 amendment 2026-05-27**, per `docs/archive/README.md`:

> Holding zone for artifacts whose destination isn't yet decided. Reviewed periodically; each item is either deleted (git history retains it), or promoted to `decisions/`, `audits/`, `handoffs/`, `diagrams/`, or authored into an ADR. **Not a dumping ground — a triage queue. If something sits here across two reviews with no decision, default to deletion.**

**(c) `docs/decisions/archive/` and `docs/intake/archive/`** — no dedicated ADR; both were established by operator ruling and are populated by byte-identical relocation (`216ce3a8` 2026-07-22, "operator ruling 2026-07-22"; `6551d363` 2026-07-23 `[#398]`).

**(d) The refusal — ADR-100 (Accepted, 2026-07-07), for `docs/audits/**` and `docs/handoffs/**`.** Quoted in full because it is the answer to the question the contract is really asking:

> Every accepted audit is **kept, unbounded**; audit files are **never physically moved, rolled up, or compacted.** Audits are the **evidence spine** — ADRs, LESSONS, transcripts, and the tooling cite them by path, and ~78% of those citations are in immutable/append-only files that can never be re-pointed. The storage cost is trivial; the referential cost of a move is permanent breakage. Keep-all is the deliberate, recorded call — not silent drift.

> Navigability is provided by the **index** (`docs/audits/README.md`), **count-tiered, not age-tiered** … **Everything older moves to an archive *section of the index*** — **a section of the index, not the filesystem.** **Files never move; only their index grouping does.**

**So the answer to "why is nothing archived" is: for the two trees that account for 93% of `docs/` by bytes, not archiving is ratified policy, taken deliberately on measured evidence.** The absence is a decision, not an omission.

**But that decision was priced against 196 audit files.** ADR-100 §Context records its own evidence base: *"196 audit files, flat tree, no `archive/` dir exists. 125 citation lines across 42 citing docs."* Today there are **728 files** — **3.7×** — and this report measures **212 governance-cited** of 727. ADR-100 also flagged its own gap: *"the citation scan covered the doc corpus only — audit→audit cross-references and `ecosystem/*.yaml` were NOT scanned."* **Section 3 above closes that gap, and the answer changes the arithmetic the decision rested on:** the largest single citer of audit files is `ecosystem/audit-funnel-baseline.json`, a machine register, and 290 files (40%) have no consumer at all.

### 6.2 How much has ever been archived, and when

**Total ever archived: 31 files across four trees.**

| tree | files | how they got there |
|---|---:|---|
| `docs/archive/` | 21 + README | 14 relocated 2026-05-28 from `research/` + `council-questions/`; the rest landed directly as incoming research |
| `docs/intake/archive/` | 7 | renamed in, 2026-07-23 (`[#398]`) and 2026-08-12 |
| `protocols/archive/` | 2 | `HANDOFF_PROCESS_v3.4.md` 2026-05-29, `v4.4.md` 2026-06-11 |
| `docs/decisions/archive/` | 2 | ADR-40 + ADR-52, 2026-07-22 |

**Every archival act on record** (`git log -M --diff-filter=R --name-status`, filtered to `archive/` destinations):

```
2026-05-28  71febc10  retire research/ per ADR-60 amendment              -> docs/archive/       (7 files)
2026-05-28  81e57e54  retire council-questions/ per ADR-60 amendment     -> docs/archive/       (7 files)
2026-05-29  90267cfc  archive HANDOFF_PROCESS v3.4 prior to v4 rewrite   -> protocols/archive/  (1)
2026-06-11  c3ba6d4f  promote v5 to canonical; archive v4.4 (#149)       -> protocols/archive/  (1)
2026-06-26  ca2e8ce9  archive the 3 flat v3/v4 handoff templates         -> templates/archive/  (3)
2026-07-22  216ce3a8  archive ADR-40 (Deprecated) + ADR-52 (Superseded)  -> docs/decisions/archive/ (2)
2026-07-23  6551d363  relocate the 3 newly-terminal docs [#398]          -> docs/intake/archive/ (3)
2026-08-12  f095a81f  intake #10 REJECTED and relocated                  -> docs/intake/archive/ (1)
```

**Last archival act: 2026-08-12 — 14 days ago.** Archival is not dead; it happens roughly monthly and always as a deliberate, ruled act tied to a specific supersession.

### 6.3 The convention that is not being honoured

**`docs/archive/`'s own two-review deletion rule has never fired.** Its README records: *"First review: 2026-05-28 — 7 council-out transcripts promoted; 7 external-research / scoping / evidence files kept pending second review."* Those seven files are still present, **90 days later**, and no second review is recorded:

```
docs/archive/2026-04-23-llm-dev-patterns-2026.md
docs/archive/2026-04-24-claude-md-best-practices.md
docs/archive/2026-04-24-multi-agent-debate-patterns.md
docs/archive/2026-04-27-handoff-patterns-external-research.md
docs/archive/2026-05-17-kimi-k2-scoping.md
docs/archive/2026-05-25-handoff-failures-evidence.md
docs/archive/2026-05-25-handoff-methodology-council-index.md
```

Under the folder's own stated rule — *"if something sits here across two reviews with no decision, default to deletion"* — these seven are past due. **This is the one place where the archive story is genuine drift rather than ratified policy.** (Four of the newer research memos in the same folder are additionally cited by nothing — see the consumption lists.)

**And one surface has no retention convention at all: `logs/`.** 43 MB, 95 files, **untracked** (only `logs/PARITY-EVENTS.jsonl` appears in `.gitignore`; `git ls-files logs | wc -l` → 1). `logs/PROPOSALS-YYYY-MM-DD.md` runs ~1.7 MB **per day** and there are 26 of them. No ADR, no hook and no audit check governs their lifetime. It costs nothing in git and nothing in context — but it is the fastest-accumulating surface in the repo and the contract's question *"does an archive convention exist"* is answered **no** for it. That absence is a finding.

---

## Section 7 — The five questions, answered directly

### Q1 — If the generated view carried one line per row instead of full bodies, what would `BACKLOG.md` weigh?

**Computed from the actual data.** `BACKLOG.md` today: 464 lines / 283,019 bytes, of which **191 are row lines totalling 245,486 bytes** (mean **1,284 bytes per row**) and 273 are scaffolding (headings, theme/story prose, the story-map frame) totalling 37,533 bytes. The view renders `open` + `deferred` = 191 rows.

A one-line row synthesised from the frontmatter that already exists — `- [#id] [P][size] title · theme` — measures **22,127 bytes for the same 191 rows** (mean 116 bytes/row).

| view | row payload | + scaffolding | total | ~tokens | vs today |
|---|---:|---:|---:|---:|---:|
| **today** (full bodies, 191 rows) | 245,486 B | 37,533 B | **283,019 B** | **70,754** | — |
| one line per row, same 191 rows | 22,127 B | 37,533 B | **59,660 B** | **14,915** | **−79%** |
| one line per row, open only (165) | 19,580 B | 37,533 B | 57,113 B | 14,278 | −80% |
| one line per row, all 316 incl. closed | 37,899 B | 37,533 B | 75,432 B | 18,858 | −73% |

**Answer: ~59.7 KB / ~14.9 k tokens, down from 283 KB / ~70.8 k — a 79% reduction overall and a 91% reduction of the row payload itself.** Note the scaffolding (37.5 KB) would then be *63% of the file*; if the goal is a scannable index, the theme/story prose blocks become the next target. Nothing is lost: the full bodies already live in `tasks/*.md`, which is the ratified source of truth.

### Q2 — How many open rows would remain if everything untouched for 90+ days were iceboxed?

**All 165 — the icebox would be empty.** No open row has a birth age ≥ 90 days (oldest: `[#23]` at 86 d) and none has a last-touch age above 29 days. The 90-day threshold is longer than the lifetime of the id convention itself.

At usable thresholds:

| threshold (birth age) | rows iceboxed | open rows remaining |
|---|---:|---:|
| 90 d | 0 | 165 |
| 75 d | 14 | 151 |
| 60 d | 19 | 146 |
| **45 d** | **49** | **116** |
| 30 d | 94 | 71 |

**The meaningful cut is 45 days: it moves 49 rows and leaves 116.** Note the corpus already has an icebox — `status: deferred`, holding 26 rows — so the mechanism exists and the question is threshold, not machinery.

### Q3 - How many documents in `docs/` are cited by nothing?

**Two numbers, because the granularity and the keying change the answer, and reporting only one would mislead.**

**Raw, by file: 436 of 1,597 `docs/**/*.md` (27%)** have no citer outside their own directory and outside the generated indices. Broken down: `docs/handoffs/` **422**, `docs/decisions/` 8, `docs/archive/` 4, `docs/intake/` 2.

**Three of those four buckets are artefacts of the matching method, and each was re-measured rather than left standing:**

- **`docs/handoffs/` 422 -> 2.** A handoff bundle is cited **as a directory**, not by its inner filenames - nobody writes "`03_PLAYBOOK.md`". Re-measured at **bundle** granularity: **113 of 115 bundles are cited** from outside themselves (`docs/handoffs/` 237 edges, `docs/audits/` 122, `JOURNAL.md` 112, `docs/decisions/` 13, `BACKLOG.md` 11). **Only 2 bundles are uncited:** `2026-07-05-dev-knowledge-epic-llm-first-docs` and `2026-07-05-dev-knowledge-epic-test-tiering`.
- **`docs/decisions/` 8 -> 0.** `ADR-106`, `ADR-112`, `ADR-68`, `ADR-77`, `ADR-84`, `ADR-90`, `ADR-95`, `ADR-99` are flagged only because this pass matched **filenames**; ADRs are cited by the token `ADR-<n>`. The token-keyed pass in section 3.2 finds **all 88 cited**.
- **`docs/archive/` 4 -> 0.** The four 2026-08-17 research memos carry their commissioning id as a trailing filename token (`-wf-50111a08` etc.) and are cited **by that token**, not by filename - verified: `wf-50111a08`, `wf-bfb9405b`, `wf-460fee76`, `wf-76d68c06` each resolve to `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` plus their originating intake. That trailing-token convention is documented in `docs/archive/README.md` precisely so the file resolves back to its source, and it works.
- **`docs/intake/` 2 -> 0.** `2026-08-24-tech-disposition-register-schema.md` and `2026-08-24-tech-supplement-probe-fill-state-defect.md` are cited as `intake #44` / `intake #47`, by number rather than path.

**Corrected answer: 49 documents in `docs/` are genuinely cited by nothing - and all 49 are audits.** Plus **2 whole handoff bundles**. The audit tree carries 100% of the file-level orphan count.

If the question is widened from "cited by nothing at all" to **"has no human or governance consumer"** - the reaper's real criterion - the answer is **290 audit files (40% of `docs/audits/`)**, per section 3.1: 49 cited nowhere plus 241 appearing only inside `ecosystem/audit-funnel-baseline.json`.

**The lesson inside the method:** three of the four false-positive buckets were false because the corpus cites by *identifier* (`ADR-<n>`, `intake #<n>`, `wf-<id>`) rather than by path, and one was false because it cites by *directory*. Any future reaper that keys on filenames alone would have proposed deleting 14 live documents and 420 live handoff files.

### Q4 — What fraction of the last 20 merges conflicted on a generated file?

**6 of 20 = 30%.** All six are `docs/audits/README.md`; one further merge (`1858849a`) conflicted on `BACKLOG.md` + `tasks/manifest.json`, which are also generated — so **counting every generated file, 7 of 20 = 35%**, and generated files account for **7 of the 7 conflicted merges (100%)**. Not one of the last 20 merges required manual resolution of hand-authored content alone.

### Q5 — What is the single largest context cost an agent pays on boot, in tokens, and which file?

**`CLAUDE.md` — ~10,489 tokens (41,959 bytes).** It is 35% of the entire contracted boot read.

The full `CLAUDE.md` §1 boot contract, measured:

| file | ~tokens |
|---|---:|
| **`CLAUDE.md`** | **10,489** |
| `JOURNAL.md` — last 5 entries only (§1 item 4) | 5,948 |
| `docs/handoffs/README.md` (§1 item 3, the operator runbook) | 4,198 |
| `protocols/ESSENTIALS.md` | 4,077 |
| active bundle `2026-08-25-dev-knowledge-architect/HANDOFF_BOOT.md` | 2,755 |
| `~/.claude/CLAUDE.md` (global, loaded by the harness) | 1,224 |
| `@.claude/methodology-roster.md` | 598 |
| `@.claude/generated/commands-repo.md` | 446 |
| `@.claude/generated/recent-adrs.md` | 271 |
| **TOTAL contracted boot** | **~30,006** |

**Two caveats that matter more than the headline:**

1. **`CLAUDE.md` is 41,959 bytes across 239 lines — 176 chars/line.** Its own §4 budget checker (`validate_doc_rot.scan_file_budget`) counts it at **195/200 lines**, i.e. the file is governed on a *line* budget while its cost is *bytes*. The budget instrument and the cost being managed are not the same quantity. A 5-line "headroom" is ~1 KB of headroom on a 42 KB file.
2. **The boot read is the small part.** One step past it sit `protocols/PLAYBOOK.md` (**~104,754 tokens**), `BACKLOG.md` (~70,754), `LESSONS.md` (~65,865), `protocols/STANDING_RULINGS.md` (~49,012), `ARCHITECTURE.md` (~25,916), `docs/audits/README.md` (~23,165), `docs/decisions/README.md` (~22,301), and the active bundle's `PASTE_THIS.md` (~12,713). `JOURNAL.md` in full is **~736,707 tokens** — 24× the entire boot read, and any tool that reads it whole rather than head-limited blows a 1 M window's budget on one file. **`PLAYBOOK.md` is the largest single artifact any agent is routinely told to consult, at 3.5× the whole boot contract.**

---

## Questions I could not answer, and exactly what blocked it

1. **"Age of `tasks/` rows"** — cannot be answered from filesystem or git mtime. `tasks/` was created 2026-07-27 by the ADR-107 §7.2 flip, so 30 days is a hard ceiling, and lane batches rewrite rows in bulk. **Worked around**, not skipped: a second axis was derived from `BACKLOG.md`'s 781-revision history (first appearance of each `[#id]`), giving real birth ages up to 86 days. Both are reported; the birth axis is the one to use. **Residual limitation:** birth age is bounded at 86 days by the age of the bracketed-id convention itself, so a row that predates the convention under a different label cannot be dated.
2. **"Which themes have had no activity in 30+ days"** — answered as *none*, on both instruments, but the answer is structurally uninformative for the same reason as (1). A real dormancy measure would need per-row status-transition history, which is not recorded as data anywhere; it would have to be reconstructed by diffing `status:` across `tasks/` history, and `tasks/` history is 30 days deep.
3. **Conflict detection is a floor, not an exact count.** `git show --cc` finds paths whose content differs from every parent. A conflict resolved by taking one side wholesale (`--ours` / `--theirs`) leaves no combined-diff hunk and is invisible to this method. **The true conflict rate is ≥ 35%.** Git records no per-merge conflict flag, so an exact count is not recoverable from history — it would require instrumenting merges going forward.
4. **Token counts are `bytes ÷ 4`**, per the contract's instruction. For dense markdown with heavy backtick/punctuation use this typically **understates** real tokenizer counts by 10–25%. Every token figure here should be read as a lower bound.
5. **Citation is substring matching**, not a parsed reference graph. It will over-count where a filename appears inside a longer string, and under-count a citation phrased purely descriptively ("the funnel-coverage lane's artifact") with no locator. The ADR pass uses the `ADR-<n>` token with a digit-boundary guard; the audit and intake passes use filenames, which is how those artifacts are actually cited in this corpus. **The §3.2-vs-Q3 divergence on ADRs is a worked example of this limitation, disclosed rather than smoothed.**
6. **`ecosystem/` line and byte counts include 9 untracked files** (`__pycache__`, gitignored state). The tracked figure is 98 files. Every other contracted surface is 100% tracked.

---

## Method appendix — how each number was obtained

```
Section 1  find <dir> -type f | wc -l
           find <dir> -type f -printf '%s\n' | awk '{s+=$1} END{print s}'
           find <dir> -type f -exec cat {} + | wc -l
           find <dir> -type f -printf '%s %p\n' | sort -rn | head -10
           avg chars/line = bytes / lines ; est tokens = bytes / 4
           git ls-files <dir> | wc -l                        (tracked-vs-disk)

Section 2  git log --pretty=format:@%at --name-only -- tasks/          (last touch)
           git log --diff-filter=A --pretty=format:@%at --name-only -- docs/audits
           git log --reverse --format=@%at -U0 -- BACKLOG.md           (row birth)
             -> scan added lines for \[#(\d+)\], first occurrence wins
           grep -h '^status:' docs/intake/*.md | sort | uniq -c
           first Status line of each docs/decisions/ADR-*.md, classified

Section 3  full-text substring scan, self-excluded, two pools:
             governance = tasks/*.md, docs/decisions/**, protocols/**,
                          docs/intake/**, BACKLOG/ARCHITECTURE/CLAUDE/
                          LESSONS/VISION/CONTRIBUTING
             secondary  = JOURNAL.md, docs/handoffs/**, ecosystem/**,
                          scripts/, tests/, .claude/, templates/, deploy/
           audits + intakes keyed by filename (with and without .md)
           ADRs keyed by ADR-0*<n>(?![0-9]) AND filename

Section 4  frontmatter parse of tasks/*.md (id/title/status/priority/
             size/theme/story/depends-on/serialize-group)
           grep -n '_DEPID_RE\|_ID_TOKEN_RE' scripts/*.py

Section 5  grep -c 'sha256' BACKLOG.md            -> 0
           python -c "json.load(open('tasks/manifest.json')).keys()"
           git log -300 --pretty=format:@ --name-only    (churn)
           git log --merges --first-parent -20 --pretty=format:%H|%ad|%s
           git show --format= --cc --name-only <merge>   (resolution proxy)

Section 6  git log -M --diff-filter=R --name-status       (archival acts)
           read of ADR-83, ADR-100, docs/archive/README.md
           git ls-files logs | wc -l                      -> 1

Section 7  row lines = lines of BACKLOG.md starting '- [#'
           one-line synthesis built from tasks/ frontmatter, bytes summed
           boot set taken from CLAUDE.md §1 + its three @-imports
```

**Read-only compliance:** every command above is a read (`find`, `wc`, `awk`, `grep`, `git log`, `git show`, `git ls-files`, `cat`, Python file reads). No `git add`, `commit`, `checkout`, `merge`, `branch`, or generator invocation was issued. `git status --porcelain` was empty at the start of this run and is empty at the end.

---

## Appendix A — CONSUMPTION list 1: CITED audits (212)

Each line: audit path — the governance surfaces that name it (`task`, `ADR`, `RULINGS`, `protocol`, `intake`, or a named root doc), with edge counts where > 1.


- `docs/audits/2026-04-21-council-27-brief.md` — cited by: ADR
- `docs/audits/2026-04-21-dev-knowledge-inventory.md` — cited by: ADR
- `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md` — cited by: ADRx2
- `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md` — cited by: ADR
- `docs/audits/2026-04-27-deep-cleansing-diagnostic.md` — cited by: ADR
- `docs/audits/2026-04-30-dev-knowledge-self-audit.md` — cited by: ADR
- `docs/audits/2026-05-11-ai-council-scrum-master-review.md` — cited by: protocol, LESSONS.md
- `docs/audits/2026-05-12-handoff-process-audit.md` — cited by: ADR
- `docs/audits/2026-05-19-cohort1-verification.md` — cited by: ADRx2
- `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` — cited by: protocol
- `docs/audits/2026-05-20-handoff-process.md` — cited by: ADRx2
- `docs/audits/2026-05-23-ai-council-deep-audit.md` — cited by: ADR
- `docs/audits/2026-05-24-backlog-audit-and-universalization-scoping.md` — cited by: ADR
- `docs/audits/2026-05-25-council-pipeline-audit.md` — cited by: ADR
- `docs/audits/2026-05-25-council-pipeline-proposal.md` — cited by: ADR
- `docs/audits/2026-05-26-cross-repo-universalization-verification.md` — cited by: ADR
- `docs/audits/2026-05-27-concurrency-anomaly-cleanup-2026-05-26.md` — cited by: ADR
- `docs/audits/2026-05-27-taxonomy-simplification-verification.md` — cited by: ADR
- `docs/audits/2026-05-29-ecosystem-coherence-audit.md` — cited by: ADR
- `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` — cited by: ADRx8
- `docs/audits/2026-05-31-backlog-architecture-diagnosis.md` — cited by: ADRx2
- `docs/audits/2026-06-01-backlog-migration-inventory.md` — cited by: ADR
- `docs/audits/2026-06-01-child-repo-relocation-proposal.md` — cited by: BACKLOG.md
- `docs/audits/2026-06-03-codemap-grounding.md` — cited by: ADR
- `docs/audits/2026-06-03-doc-tooling-inventory.md` — cited by: ADRx2
- `docs/audits/2026-06-03-protocols-rot-audit.md` — cited by: LESSONS.md
- `docs/audits/2026-06-04-pilot81-hub-conformance-digest.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-06-05-conformance-nightly-digest.md` — cited by: ADR, protocol
- `docs/audits/2026-06-05-living-doc-staleness.md` — cited by: protocol, ARCHITECTURE.md
- `docs/audits/2026-06-06-85-validation-record.md` — cited by: ADR
- `docs/audits/2026-06-06-conformance-nightly-digest.md` — cited by: ADR
- `docs/audits/2026-06-07-conformance-nightly-digest.md` — cited by: ADR
- `docs/audits/2026-06-07-copilot-collections-peer-audit-v2.md` — cited by: task
- `docs/audits/2026-06-07-methodology-transfer-audit.md` — cited by: ARCHITECTURE.md, BACKLOG.md
- `docs/audits/2026-06-07-platform-max-audit.md` — cited by: taskx3, ADR, protocol, BACKLOG.md
- `docs/audits/2026-06-11-architecture-coherence-audit.md` — cited by: LESSONS.md
- `docs/audits/2026-06-11-surface-responsibility-audit.md` — cited by: LESSONS.md
- `docs/audits/2026-06-14-ecosystem-audit.md` — cited by: ADR
- `docs/audits/2026-06-15-changelog-review.md` — cited by: ADR
- `docs/audits/2026-06-19-hook-completeness-audit.md` — cited by: ADR
- `docs/audits/2026-06-20-pyright-reverse-dep-oracle-findings.md` — cited by: ADR
- `docs/audits/2026-06-20-removal-closure-spike-findings.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-06-21-audit-ops-findings.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-06-21-doc-code-edge-fit-check.md` — cited by: ADR
- `docs/audits/2026-06-23-handoff-process-audit-findings.md` — cited by: ADR
- `docs/audits/2026-07-04-fable-architecture-review.md` — cited by: task, protocol
- `docs/audits/2026-07-05-ai-council-measurement-2.md` — cited by: LESSONS.md
- `docs/audits/2026-07-05-draft-tier2-nightly-layer.md` — cited by: taskx2, BACKLOG.md
- `docs/audits/2026-07-06-ai-council-measurement-3.md` — cited by: task, LESSONS.md, BACKLOG.md
- `docs/audits/2026-07-06-arc5-buy-vs-build-verdicts.md` — cited by: intakex2
- `docs/audits/2026-07-06-arc5-must-verification.md` — cited by: intake
- `docs/audits/2026-07-06-arc5-routines-pilot-design.md` — cited by: intake
- `docs/audits/2026-07-06-changelog-review.md` — cited by: protocol
- `docs/audits/2026-07-07-changelog-review.md` — cited by: intakex2
- `docs/audits/2026-07-07-overnight-mission-ledger.md` — cited by: LESSONS.md
- `docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-08-fleet-consistency-census.md` — cited by: taskx6, BACKLOG.md, intake
- `docs/audits/2026-07-09-deletion-candidates-report.md` — cited by: task
- `docs/audits/2026-07-09-night-hygiene-audit.md` — cited by: ADR
- `docs/audits/2026-07-11-census-consolidated-morning-brief.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-11-technical-fleet-boundary-marker-design.md` — cited by: task, protocol
- `docs/audits/2026-07-11-technical-fleet-boundary-matrix.md` — cited by: task
- `docs/audits/2026-07-11-technical-fleet-parity-register.md` — cited by: taskx3, ADRx2, intakex2, BACKLOG.md
- `docs/audits/2026-07-11-technical-fleet-structure-comparison.md` — cited by: intakex2
- `docs/audits/2026-07-12-codex-ruff-hub-pin.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-12-technical-night-c4-requirements.md` — cited by: intake
- `docs/audits/2026-07-12-technical-night-codex-review.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-12-technical-night-delete-candidates.md` — cited by: task
- `docs/audits/2026-07-13-technical-satellite-onboarding-census.md` — cited by: intake
- `docs/audits/2026-07-16-technical-fleet-structure-census.md` — cited by: ADR
- `docs/audits/2026-07-19-census-silent-rule-ledger.md` — cited by: LESSONS.md, BACKLOG.md
- `docs/audits/2026-07-19-codex-cycle-close-terra-review.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-19-codex-residual-completeness-gate.md` — cited by: task
- `docs/audits/2026-07-19-codex-residual-rule-declaration.md` — cited by: taskx2
- `docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-19-technical-night-s4-handoff-playbook-currency.md` — cited by: task
- `docs/audits/2026-07-19-technical-night-s7-prompt-authoring-quality.md` — cited by: task, protocol, BACKLOG.md, intake
- `docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-21-technical-night-vision-audit.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md` — cited by: taskx2
- `docs/audits/2026-07-22-technical-night-batch-deep-audit.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-22-verification-night-batch-integration-386-384.md` — cited by: taskx5, BACKLOG.md
- `docs/audits/2026-07-23-technical-status-enum-reconcile.md` — cited by: task, ARCHITECTURE.md, BACKLOG.md
- `docs/audits/2026-07-27-census-silent-rule-ratchet-arm-measurement.md` — cited by: BACKLOG.md
- `docs/audits/2026-07-27-codex-436-ratchet-final.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-27-codex-adversarial-review-adr-107-sol.md` — cited by: ADR
- `docs/audits/2026-07-27-codex-conformance-extraction-aggregate.md` — cited by: ADR
- `docs/audits/2026-07-27-verification-433-schema-spike.md` — cited by: ADRx2
- `docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md` — cited by: ADR
- `docs/audits/2026-07-27-verification-handoff-process-audit.md` — cited by: task, intake
- `docs/audits/2026-07-28-technical-382-charter.md` — cited by: ADR
- `docs/audits/2026-07-29-codex-postflip-fix-batch-review.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-29-technical-postflip-stale-procedure-audit.md` — cited by: protocol
- `docs/audits/2026-07-30-technical-intake18-ratification-record.md` — cited by: intakex2
- `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md` — cited by: task, BACKLOG.md, intake
- `docs/audits/2026-07-30-technical-vscode-w1-execution-record.md` — cited by: intake
- `docs/audits/2026-07-31-technical-382-registry-prep-dossier.md` — cited by: ADR
- `docs/audits/2026-07-31-technical-382-schema-derivation-sol.md` — cited by: ADR
- `docs/audits/2026-07-31-technical-p10-grooming-dossier.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-07-31-technical-v6-open-rulings.md` — cited by: task, protocol
- `docs/audits/2026-07-31-verification-382-ladder-evidence.md` — cited by: ADRx2, task
- `docs/audits/2026-08-01-technical-codex-wrapper-model-pin-and-lf.md` — cited by: task
- `docs/audits/2026-08-01-technical-night-batch-l2-repomix-pilot.md` — cited by: task
- `docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md` — cited by: task
- `docs/audits/2026-08-01-technical-window-metrics.md` — cited by: task
- `docs/audits/2026-08-03-technical-383-caches-wave-record.md` — cited by: taskx2, BACKLOG.md
- `docs/audits/2026-08-03-technical-night-la-w2-verification.md` — cited by: task
- `docs/audits/2026-08-03-technical-night-lb-groom.md` — cited by: ADR
- `docs/audits/2026-08-03-technical-night-lf-rulings-prep.md` — cited by: intake
- `docs/audits/2026-08-04-codex-481-organ-id-rename.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-04-codex-483-preflight-discrimination.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-04-technical-483-enforcement-ruling.md` — cited by: task, RULINGS
- `docs/audits/2026-08-05-codex-498-hook-exec-bit.md` — cited by: task
- `docs/audits/2026-08-05-technical-night-batch-morning-report.md` — cited by: taskx2
- `docs/audits/2026-08-06-technical-batch1-verification.md` — cited by: ADR
- `docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md` — cited by: task, RULINGS
- `docs/audits/2026-08-06-technical-night-prep-packs.md` — cited by: task, ADR, ARCHITECTURE.md
- `docs/audits/2026-08-07-codex-pre-cut-retro-handoff-engine-thinning.md` — cited by: task
- `docs/audits/2026-08-07-technical-batch-2-lessons.md` — cited by: protocol
- `docs/audits/2026-08-07-technical-batch-2-packet.md` — cited by: task, RULINGS, BACKLOG.md
- `docs/audits/2026-08-08-technical-502-pythonpath-measurement.md` — cited by: task, RULINGS, LESSONS.md
- `docs/audits/2026-08-08-technical-batch-3-packet.md` — cited by: intakex2
- `docs/audits/2026-08-08-technical-library-research.md` — cited by: intake
- `docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md` — cited by: intake
- `docs/audits/2026-08-08-technical-successor-prep.md` — cited by: intake
- `docs/audits/2026-08-09-technical-consolidation-report.md` — cited by: intakex3, RULINGS
- `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md` — cited by: intakex2
- `docs/audits/2026-08-10-technical-backlog-testability-census.md` — cited by: task, RULINGS
- `docs/audits/2026-08-10-technical-batch-4-execution-plan-draft.md` — cited by: task
- `docs/audits/2026-08-10-technical-decision-sheet-verification.md` — cited by: RULINGS
- `docs/audits/2026-08-10-technical-research-corpus-distillate.md` — cited by: RULINGS, intake
- `docs/audits/2026-08-10-verification-arc9-rulings-recording.md` — cited by: ADR, RULINGS, intake
- `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` — cited by: RULINGS, ARCHITECTURE.md
- `docs/audits/2026-08-11-codex-lane-b-270-load-gauge.md` — cited by: task
- `docs/audits/2026-08-11-codex-lane-f-521-syspath-substrate.md` — cited by: RULINGS
- `docs/audits/2026-08-11-technical-batch-4-brief-next-architect.md` — cited by: intake
- `docs/audits/2026-08-11-technical-batch-4-manifest.md` — cited by: RULINGS
- `docs/audits/2026-08-11-technical-batch-4-packet.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-11-technical-batch-4-w2-lane-contract.md` — cited by: task
- `docs/audits/2026-08-12-technical-night-2-lessons-governance-strategy.md` — cited by: RULINGS, LESSONS.md, intake
- `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md` — cited by: taskx2, ARCHITECTURE.md, BACKLOG.md
- `docs/audits/2026-08-12-verification-night-1-truth-audit-and-handoff-numbers.md` — cited by: RULINGS
- `docs/audits/2026-08-13-verification-492-corpus-reconciliation.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-14-census-night2-census.md` — cited by: taskx2
- `docs/audits/2026-08-14-codex-524-check-extensions.md` — cited by: task
- `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` — cited by: task
- `docs/audits/2026-08-14-technical-night2-latency.md` — cited by: protocol
- `docs/audits/2026-08-14-technical-night2-research.md` — cited by: protocol
- `docs/audits/2026-08-15-technical-528-legs12-packet.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-15-technical-batch-phase1-packet.md` — cited by: taskx3
- `docs/audits/2026-08-15-technical-night2-consolidated-briefing.md` — cited by: taskx2
- `docs/audits/2026-08-15-technical-night3-decision-queue.md` — cited by: taskx2, BACKLOG.md
- `docs/audits/2026-08-15-technical-night3-research.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-15-verification-night3-warn-ledger.md` — cited by: taskx2, BACKLOG.md
- `docs/audits/2026-08-16-census-nb4-closing-campaign.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-census-nb6-archive-sweep.md` — cited by: taskx6, BACKLOG.md
- `docs/audits/2026-08-16-technical-533-audit-decompose-lane-contract.md` — cited by: task, RULINGS, BACKLOG.md
- `docs/audits/2026-08-16-technical-batch-6-manifest.md` — cited by: task, RULINGS, BACKLOG.md
- `docs/audits/2026-08-16-technical-batch-6-packet.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-technical-nb5-seam-repoint.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-verification-nb4-equilibrium.md` — cited by: task
- `docs/audits/2026-08-16-verification-nb4-playbook-gap.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-16-verification-nb6-backlog-truth.md` — cited by: taskx5, BACKLOG.md
- `docs/audits/2026-08-17-census-nb7-orphan-census.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-17-technical-audit-disposition-ledger.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md` — cited by: taskx3, BACKLOG.md
- `docs/audits/2026-08-17-technical-batch-7a-manifest.md` — cited by: intakex2
- `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` — cited by: intakex5
- `docs/audits/2026-08-18-technical-554-devcontainer-lane-contract.md` — cited by: ADR
- `docs/audits/2026-08-18-technical-phase0-baselines.md` — cited by: LESSONS.md
- `docs/audits/2026-08-19-technical-backlogmd-trial.md` — cited by: task
- `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md` — cited by: task, RULINGS
- `docs/audits/2026-08-19-technical-c4-ruling-prework.md` — cited by: task
- `docs/audits/2026-08-19-technical-n3-ratification-pack.md` — cited by: RULINGS
- `docs/audits/2026-08-19-technical-n4-grooming-wave1.md` — cited by: task, RULINGS, BACKLOG.md
- `docs/audits/2026-08-19-technical-n5-codification-pack.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-19-technical-s1-seat-arc-contract.md` — cited by: ADRx2, intakex2, RULINGS
- `docs/audits/2026-08-20-technical-codespaces-audit.md` — cited by: taskx3, ARCHITECTURE.md, BACKLOG.md
- `docs/audits/2026-08-20-technical-gemini-ab-results.md` — cited by: task, LESSONS.md, BACKLOG.md
- `docs/audits/2026-08-20-technical-grok-ab-results-2.md` — cited by: task
- `docs/audits/2026-08-20-technical-playbook-status.md` — cited by: taskx2, protocol, RULINGS, BACKLOG.md
- `docs/audits/2026-08-20-technical-transcription-seat-contract.md` — cited by: RULINGS
- `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` — cited by: ADRx2
- `docs/audits/2026-08-21-technical-graph-and-workflows.md` — cited by: intake
- `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md` — cited by: intakex5, task, BACKLOG.md
- `docs/audits/2026-08-21-technical-lane-tel-run-id.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-21-technical-library-first-research.md` — cited by: task, BACKLOG.md, intake
- `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` — cited by: taskx7, RULINGS, BACKLOG.md
- `docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md` — cited by: taskx2, ADR, RULINGS, ARCHITECTURE.md, BACKLOG.md, intake
- `docs/audits/2026-08-22-technical-intake-r1-decision-packet.md` — cited by: task, ADR, RULINGS, BACKLOG.md
- `docs/audits/2026-08-23-technical-backlog-adjudication-prep.md` — cited by: RULINGS
- `docs/audits/2026-08-23-technical-lane-562-local-admission.md` — cited by: taskx3, RULINGS, BACKLOG.md, intake
- `docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md` — cited by: task, ADR, BACKLOG.md, intake
- `docs/audits/2026-08-23-technical-lane-docs-actual-state.md` — cited by: task, CLAUDE.md, BACKLOG.md
- `docs/audits/2026-08-23-technical-lane-docs-governance.md` — cited by: ADR
- `docs/audits/2026-08-23-technical-phase0-preconditions.md` — cited by: ADR, intake
- `docs/audits/2026-08-23-technical-ruling-provenance-audit.md` — cited by: intake
- `docs/audits/2026-08-23-technical-wave-close-funnel.md` — cited by: task, BACKLOG.md, intake
- `docs/audits/2026-08-24-technical-discharge-38-ruling-packet.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-dispatch-brief-to-architect.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-dispatch-consolidation-plan.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-dispatch-surface-measured.md` — cited by: protocol, RULINGS
- `docs/audits/2026-08-25-technical-green-by-skip-sweep.md` — cited by: task, BACKLOG.md
- `docs/audits/2026-08-25-technical-harvest-v-consolidation.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-probe-dsh-report.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-probe-providers-report.md` — cited by: RULINGS
- `docs/audits/2026-08-25-technical-register-ruling-packet.md` — cited by: taskx8, ADRx3, RULINGS, BACKLOG.md
- `docs/audits/2026-08-25-technical-research-agents-md-standard.md` — cited by: ADRx2, intake
- `docs/audits/2026-08-25-technical-research-delivery-telemetry-attribution.md` — cited by: task, BACKLOG.md


---

## Appendix B — CONSUMPTION list 2: audits CITED BY NOTHING (49)

**This is the reaper's evidence.** No `tasks/` row, no ADR, no `STANDING_RULINGS.md` section,
no protocol, no root canonical doc, no intake — and also no `JOURNAL.md` entry, no other handoff
bundle, no `ecosystem/` register, no script or test. These 49 files are referenced by nothing in
the repository outside themselves.

**Read the shape before reading the list:** they are almost entirely **lane contracts, lane
packets, per-lane retros, codex review outputs, nightly conformance digests and the `nb`-series
consolidated briefings** — machine-and-session scaffolding for work that has since been
integrated. They were written into an immutable, keep-forever evidence tree because that is where
the taxonomy puts a `docs/audits/*.md` file, not because anyone intended them to be durable.


- `docs/audits/2026-08-07-codex-lane-1-490-430-parity-manifest.md`
- `docs/audits/2026-08-07-codex-lane-a-501-retro.md`
- `docs/audits/2026-08-07-codex-lane-b-503-retro.md`
- `docs/audits/2026-08-07-codex-morning-f4-retro.md`
- `docs/audits/2026-08-07-codex-mutmut-sandbox-skip.md`
- `docs/audits/2026-08-07-codex-pre2-arc-retro.md`
- `docs/audits/2026-08-07-codex-pre2-selfreview-arc.md`
- `docs/audits/2026-08-07-conformance-nightly-digest.md`
- `docs/audits/2026-08-08-codex-deploy-doc-carrier.md`
- `docs/audits/2026-08-08-codex-lane-e-396-512-gitenv-scrub.md`
- `docs/audits/2026-08-08-conformance-nightly-digest.md`
- `docs/audits/2026-08-08-technical-closure-wave-proposals.md`
- `docs/audits/2026-08-08-technical-lane-c-393-corpsca-rot-review.md`
- `docs/audits/2026-08-10-conformance-nightly-digest.md`
- `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md`
- `docs/audits/2026-08-15-codex-m-review.md`
- `docs/audits/2026-08-15-codex-n-review.md`
- `docs/audits/2026-08-15-codex-o-review.md`
- `docs/audits/2026-08-15-codex-p-review.md`
- `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md`
- `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-packet.md`
- `docs/audits/2026-08-15-technical-527-block-main-lane-contract.md`
- `docs/audits/2026-08-15-technical-528-legs12-latency-lane-contract.md`
- `docs/audits/2026-08-15-technical-528-legs12-manifest.md`
- `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-contract.md`
- `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-packet.md`
- `docs/audits/2026-08-15-technical-530-single-flight-lane-contract.md`
- `docs/audits/2026-08-15-technical-530-single-flight-lane-packet.md`
- `docs/audits/2026-08-15-technical-gateclose-drain8-lane-contract.md`
- `docs/audits/2026-08-15-technical-night3-sessionplan.md`
- `docs/audits/2026-08-15-technical-w20-draft-landing-lane-contract.md`
- `docs/audits/2026-08-15-verification-night3-landed-review.md`
- `docs/audits/2026-08-16-technical-210-conversions-lane-contract.md`
- `docs/audits/2026-08-16-technical-271-conversions-lane-contract.md`
- `docs/audits/2026-08-16-technical-277-issues-evidence-lane-contract.md`
- `docs/audits/2026-08-16-technical-310-ledger-docs-lane-contract.md`
- `docs/audits/2026-08-16-technical-409-conversions-lane-a-contract.md`
- `docs/audits/2026-08-16-technical-532-docrot-arms-lane-contract.md`
- `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-contract.md`
- `docs/audits/2026-08-16-technical-nb4-consolidated-briefing.md`
- `docs/audits/2026-08-16-technical-nb4-fleet-parity.md`
- `docs/audits/2026-08-16-technical-nb4-llm-acceptance.md`
- `docs/audits/2026-08-16-technical-nb4-telemetry-read.md`
- `docs/audits/2026-08-16-technical-nb5-consumer-home.md`
- `docs/audits/2026-08-16-technical-nb6-handoff-prep.md`
- `docs/audits/2026-08-16-technical-w2c-conversions-lane-contract.md`
- `docs/audits/2026-08-16-technical-w2d-lane-contract.md`
- `docs/audits/2026-08-16-technical-w2f-conversions-lane-contract.md`
- `docs/audits/2026-08-16-verification-nb6-achievements.md`


---

## Appendix C — audits cited ONLY by a machine register (241)

Not orphans in the strict sense, and not consumed either. Each of these appears in
`ecosystem/audit-funnel-baseline.json` (and in a few cases `ecosystem/disposition-register.yaml`
or `ecosystem/.dev-knowledge/state.yaml`) and **nowhere else outside its own tree** — no
governance surface, no `JOURNAL.md` entry, no other bundle. Being enumerated by the ADR-111 funnel
baseline means the machine has seen the filename; it is not evidence that any decision rests on
the file.

**Together with Appendix B this is 290 files — 40% of `docs/audits/` — with no human or
governance consumer of any kind.**


- `docs/audits/2026-05-25-ai-council-universalization-audit-refresh.md` — only: eco
- `docs/audits/2026-05-25-council-debate-forensics.md` — only: eco
- `docs/audits/2026-05-25-council-mechanism-discovery.md` — only: eco
- `docs/audits/2026-05-25-council-pipeline-discovery.md` — only: eco
- `docs/audits/2026-05-25-council-pipeline-index.md` — only: eco
- `docs/audits/2026-05-26-ai-council-audit-status-reference.md` — only: eco
- `docs/audits/2026-05-26-corp-monorepo-audit-refresh.md` — only: eco
- `docs/audits/2026-05-26-corp-monorepo-execution-plan.md` — only: eco
- `docs/audits/2026-05-26-corp-ops-audit-refresh.md` — only: eco
- `docs/audits/2026-05-26-corp-ops-execution-plan.md` — only: eco
- `docs/audits/2026-05-26-corp-sca-time-automation-audit-refresh.md` — only: eco
- `docs/audits/2026-05-26-corp-sca-time-automation-execution-plan.md` — only: eco
- `docs/audits/2026-05-26-cross-repo-audit-discovery.md` — only: eco
- `docs/audits/2026-05-26-cross-repo-universalization-synthesis.md` — only: eco
- `docs/audits/2026-05-26-handoff-stabilization-discovery.md` — only: eco
- `docs/audits/2026-05-26-handoff-stabilization-validation-report.md` — only: eco
- `docs/audits/2026-05-27-ai-council-visual-pattern-retrofit-plan.md` — only: eco
- `docs/audits/2026-05-27-corp-monorepo-visual-pattern-retrofit-plan.md` — only: eco
- `docs/audits/2026-05-27-corp-ops-visual-pattern-retrofit-plan.md` — only: eco
- `docs/audits/2026-05-27-corp-sca-time-automation-visual-pattern-retrofit-plan.md` — only: eco
- `docs/audits/2026-05-27-cross-repo-retrofit-verification.md` — only: eco
- `docs/audits/2026-05-29-harness-engineering-positioning.md` — only: eco
- `docs/audits/2026-06-01-backlog-commit-naming-retro.md` — only: eco
- `docs/audits/2026-06-01-codex-precommit-enforcement-gate.md` — only: eco
- `docs/audits/2026-06-01-fresh-eyes-backlog-migration.md` — only: eco
- `docs/audits/2026-06-01-fresh-eyes-precommit-enforcement-gate.md` — only: eco
- `docs/audits/2026-06-01-fresh-eyes-sacred-files-cadence.md` — only: eco
- `docs/audits/2026-06-01-fresh-eyes-story-map.md` — only: eco
- `docs/audits/2026-06-02-codex-canonical-standard-lock.md` — only: eco
- `docs/audits/2026-06-02-codex-no-leftovers-detector.md` — only: eco
- `docs/audits/2026-06-02-codex-pytest-ini-exception.md` — only: eco
- `docs/audits/2026-06-03-codex-audit-self-documenting.md` — only: eco
- `docs/audits/2026-06-03-codex-dynamic-toc.md` — only: eco
- `docs/audits/2026-06-03-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-04-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-06-04-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-05-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-07-codex-max-audit.md` — only: eco
- `docs/audits/2026-06-08-corp-sca-time-automation-audit.md` — only: eco
- `docs/audits/2026-06-08-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-08-floor-repilot-corp-sca-validation.md` — only: eco
- `docs/audits/2026-06-09-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-06-09-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-10-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-06-10-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-11-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-06-11-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-12-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-06-12-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-13-codex-163-basename-fallback.md` — only: eco
- `docs/audits/2026-06-13-codex-163-probe-validator.md` — only: eco
- `docs/audits/2026-06-13-ecosystem-audit.md` — only: eco
- `docs/audits/2026-06-14-codex-q9-automation-isolation.md` — only: eco
- `docs/audits/2026-06-14-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-07-05-audit-vs-reality.md` — only: eco
- `docs/audits/2026-07-06-codex-consumer-instrument-hardening.md` — only: eco
- `docs/audits/2026-07-07-ai-council-measurement-4.md` — only: eco
- `docs/audits/2026-07-07-stage3-adjudication-memo.md` — only: eco
- `docs/audits/2026-07-08-demo-prep-global-infra-incident.md` — only: eco
- `docs/audits/2026-07-12-technical-night-e2e-evidence.md` — only: eco
- `docs/audits/2026-07-12-technical-night-plan-continuity-proposal.md` — only: eco
- `docs/audits/2026-07-12-technical-night-rollout-corp-monorepo.md` — only: eco
- `docs/audits/2026-07-17-technical-night-divergence-ledger.md` — only: eco
- `docs/audits/2026-07-17-technical-night-handoff-evidence-pack.md` — only: eco
- `docs/audits/2026-07-17-technical-night-live-fire-sheet.md` — only: eco
- `docs/audits/2026-07-17-technical-night-verdict-sheet.md` — only: eco
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v2.md` — only: eco
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v3.md` — only: eco
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v4.md` — only: eco
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path-v5.md` — only: eco
- `docs/audits/2026-07-18-codex-adr-101-two-tier-new-path.md` — only: eco
- `docs/audits/2026-07-18-codex-ruling-w-adr-amendment-v2.md` — only: eco
- `docs/audits/2026-07-19-codex-cycle-close-sol-adversarial-diff.md` — only: eco
- `docs/audits/2026-07-19-technical-night-luna-carrier-inventory.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s1-intake-adr-lifecycle.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s2-backlog-decision-ops.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s3-archives-lifecycle-records.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s5-consumer-disk-info-audit.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s6-worktree-discipline.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md` — only: eco
- `docs/audits/2026-07-19-technical-night-s9-testing-harness-agentic.md` — only: eco
- `docs/audits/2026-07-19-verification-night-e1-probe-fire-evidence.md` — only: eco
- `docs/audits/2026-07-20-codex-leg1-fleet-parity-gitdir-scrub.md` — only: eco
- `docs/audits/2026-07-20-codex-leg2-handoff-bundle-selection.md` — only: eco
- `docs/audits/2026-07-25-codex-fix-live-backlog-test.md` — only: eco
- `docs/audits/2026-07-26-codex-routine-consumer-prose.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-clear.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate10.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate5.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate6.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate7.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate8.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-gate9.md` — only: eco
- `docs/audits/2026-07-27-codex-436-ratchet-recheck.md` — only: eco
- `docs/audits/2026-07-27-codex-436-silent-rule-ratchet.md` — only: eco
- `docs/audits/2026-07-28-codex-437-closure-design.md` — only: eco
- `docs/audits/2026-07-28-codex-437-closure-diff.md` — only: eco
- `docs/audits/2026-07-28-codex-437-closure-recheck.md` — only: eco
- `docs/audits/2026-07-28-technical-364-cap-option-matrix.md` — only: eco
- `docs/audits/2026-07-28-technical-vscode-sizing-decision-surface.md` — only: eco
- `docs/audits/2026-07-29-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-07-30-codex-446-v6-boot-prose.md` — only: eco
- `docs/audits/2026-07-30-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-07-30-technical-proposals-2026-07-29-triage.md` — only: eco
- `docs/audits/2026-07-31-codex-intake-split-generality-discharge.md` — only: eco
- `docs/audits/2026-07-31-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-07-31-technical-433-spike-prep.md` — only: eco
- `docs/audits/2026-07-31-technical-closure-ids-negation-defect.md` — only: eco
- `docs/audits/2026-07-31-technical-intake22-d-research-rows.md` — only: eco
- `docs/audits/2026-08-01-codex-460-replication-and-close.md` — only: eco
- `docs/audits/2026-08-01-codex-462-membership-agreement-census.md` — only: eco
- `docs/audits/2026-08-01-codex-generator-newlines-and-groom.md` — only: eco
- `docs/audits/2026-08-01-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-l1-filing-pre-pack.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-l3-copier-record.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-l5-delta-groom.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-l6-460-decision-pack.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md` — only: eco
- `docs/audits/2026-08-01-technical-night-batch-plan-prep.md` — only: eco
- `docs/audits/2026-08-02-technical-night-batch-lc-agents-md-analysis.md` — only: eco
- `docs/audits/2026-08-02-technical-night-batch-ld-currency-audit.md` — only: eco
- `docs/audits/2026-08-02-technical-night-batch-le-library-first.md` — only: eco
- `docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md` — only: eco
- `docs/audits/2026-08-02-technical-night-ladder-and-plan-audit.md` — only: eco
- `docs/audits/2026-08-03-codex-472-declaration-anchor.md` — only: eco
- `docs/audits/2026-08-03-codex-472-terra-round2.md` — only: eco
- `docs/audits/2026-08-03-codex-arc2-terra-round2.md` — only: eco
- `docs/audits/2026-08-03-codex-arc2-vacuous-green-trio.md` — only: eco
- `docs/audits/2026-08-03-codex-arc3-mechanical-adoptions.md` — only: eco
- `docs/audits/2026-08-03-codex-arc3-terra-round2.md` — only: eco
- `docs/audits/2026-08-03-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-08-03-technical-night-lc-w4-staging.md` — only: eco
- `docs/audits/2026-08-03-technical-night-ld-472-option-b.md` — only: eco
- `docs/audits/2026-08-03-technical-night-le-library-first.md` — only: eco
- `docs/audits/2026-08-04-codex-465-leg4-inert-check-detector.md` — only: eco
- `docs/audits/2026-08-04-codex-465-terra-round2.md` — only: eco
- `docs/audits/2026-08-04-codex-483-preflight-contract.md` — only: eco
- `docs/audits/2026-08-04-codex-483-terra-round2.md` — only: eco
- `docs/audits/2026-08-04-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-08-04-technical-480-ruling-input-pack.md` — only: eco
- `docs/audits/2026-08-05-codex-480-review-artifact-organ.md` — only: eco
- `docs/audits/2026-08-05-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-08-06-technical-lane-a-architecture-rows.md` — only: eco
- `docs/audits/2026-08-06-technical-night-library-research.md` — only: eco
- `docs/audits/2026-08-06-technical-night-morning-packet.md` — only: eco
- `docs/audits/2026-08-06-technical-night-window-review.md` — only: eco
- `docs/audits/2026-08-06-verification-lane-c-arch-327.md` — only: eco
- `docs/audits/2026-08-07-codex-lane-2-worktree-portability.md` — only: eco
- `docs/audits/2026-08-08-technical-506-open-set-grooming-sheet.md` — only: eco
- `docs/audits/2026-08-08-technical-archival-lifecycle-audit.md` — only: eco
- `docs/audits/2026-08-09-conformance-nightly-digest.md` — only: eco
- `docs/audits/2026-08-09-technical-n1-position-northstar.md` — only: eco
- `docs/audits/2026-08-09-technical-n4-code-review.md` — only: eco
- `docs/audits/2026-08-09-technical-night-n2-mechanism-map.md` — only: eco
- `docs/audits/2026-08-09-technical-night-n5-library-first-sweep.md` — only: eco
- `docs/audits/2026-08-10-technical-origin-branch-census.md` — only: eco
- `docs/audits/2026-08-10-technical-satisfied-row-census.md` — only: eco
- `docs/audits/2026-08-11-codex-batch4-w5-organ-index.md` — only: eco
- `docs/audits/2026-08-13-technical-batch-4-w3-lane-contract.md` — only: eco
- `docs/audits/2026-08-17-technical-batch-7a-lane-c-contract.md` — only: eco
- `docs/audits/2026-08-18-census-adoption-preflight.md` — only: eco
- `docs/audits/2026-08-18-census-p10-grooming-evidence.md` — only: eco
- `docs/audits/2026-08-18-codex-review-batch1-a.md` — only: eco
- `docs/audits/2026-08-18-codex-review-batch1-c-e.md` — only: eco
- `docs/audits/2026-08-18-technical-502-mutmut-attribution.md` — only: eco
- `docs/audits/2026-08-18-technical-502-mutmut-lane-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-533-leg2-lane-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-533-leg2-measurements.md` — only: eco
- `docs/audits/2026-08-18-technical-a9-trim-lane-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-a9-trim-lane-packet.md` — only: ecox2
- `docs/audits/2026-08-18-technical-adoption-preflight-lane-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-batch1-integrator-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-p10-regen-lane-contract.md` — only: eco
- `docs/audits/2026-08-18-technical-review-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-171-dashboard-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-486-cp1252-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-554-proof-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-backlogmd-trial-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c1-seeded-defects-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c2-review-profiles-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c2-review-profiles.md` — only: eco
- `docs/audits/2026-08-19-technical-c3-grooming-wave2-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c3-grooming-wave2.md` — only: eco
- `docs/audits/2026-08-19-technical-c4-ruling-prework-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c6-telemetry-readpath-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-c6-telemetry-readpath.md` — only: eco
- `docs/audits/2026-08-19-technical-cloud-c1-brief.md` — only: eco
- `docs/audits/2026-08-19-technical-cloud-c2-brief.md` — only: eco
- `docs/audits/2026-08-19-technical-cloud-c3-brief.md` — only: eco
- `docs/audits/2026-08-19-technical-cloud-c4-brief.md` — only: eco
- `docs/audits/2026-08-19-technical-cloud-c6-brief.md` — only: eco
- `docs/audits/2026-08-19-technical-l2-wiring-lane-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md` — only: eco
- `docs/audits/2026-08-19-technical-n1-wiring-spec-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-n2-seam-worksheet-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-n2-seam-worksheet.md` — only: eco
- `docs/audits/2026-08-19-technical-n3-ratification-pack-contract.md` — only: eco
- `docs/audits/2026-08-19-technical-n5-codification-pack-contract.md` — only: eco
- `docs/audits/2026-08-20-technical-grok-ab-lane-contract-2.md` — only: eco
- `docs/audits/2026-08-20-technical-parallel-flip-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-census-cloud-r4-adr-review.md` — only: eco
- `docs/audits/2026-08-21-fresh-eyes-cloud-r1-governance-drift.md` — only: eco
- `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` — only: eco
- `docs/audits/2026-08-21-technical-ch8-dispatch-codification-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-cloud-r1-brief.md` — only: eco
- `docs/audits/2026-08-21-technical-cloud-r2-brief.md` — only: eco
- `docs/audits/2026-08-21-technical-cloud-r3-brief.md` — only: eco
- `docs/audits/2026-08-21-technical-cloud-r4-brief.md` — only: eco
- `docs/audits/2026-08-21-technical-graph-and-workflows-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-lane-554-cloud-provisioning-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-lane-554-cloud-provisioning.md` — only: eco
- `docs/audits/2026-08-21-technical-lane-arch-lifecycle-archival-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-lane-rat-intake-ratification-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-lane-tel-run-id-lane-contract.md` — only: eco
- `docs/audits/2026-08-21-technical-seat-act0-act1-contract.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r10.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r11.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r12.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r2.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r3.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r4.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r5.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r6.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r7.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r8.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra-r9.md` — only: eco
- `docs/audits/2026-08-22-codex-562-guard-fix-terra.md` — only: eco
- `docs/audits/2026-08-22-codex-563-view-layer-terra.md` — only: eco
- `docs/audits/2026-08-22-codex-cloud4v2-registries-terra.md` — only: eco
- `docs/audits/2026-08-22-fresh-eyes-cloud-4v2.md` — only: ecox2
- `docs/audits/2026-08-22-technical-cloud-1-562-admission-rerun.md` — only: eco
- `docs/audits/2026-08-22-technical-cloud-3-566-axis-lean.md` — only: eco
- `docs/audits/2026-08-22-technical-lane-fix-562-guard.md` — only: eco
- `docs/audits/2026-08-23-technical-lane-provider-config.md` — only: ecox4
- `docs/audits/2026-08-24-technical-lane-v1-register-verification.md` — only: ecox2
- `docs/audits/2026-08-24-technical-lane-v3-gates-and-ci.md` — only: ecox2
- `docs/audits/2026-08-24-technical-lane-v4-lifecycle-verification.md` — only: ecox2
- `docs/audits/2026-08-24-technical-lane-v5-register-verification.md` — only: ecox2
- `docs/audits/2026-08-24-technical-probe-substrate.md` — only: ecox2
- `docs/audits/2026-08-24-technical-verify-register-v2.md` — only: ecox2
- `docs/audits/2026-08-25-technical-lane-g-governance-spine.md` — only: ecox2


---

## Appendix D — audits cited ONLY by narrative surfaces (225)

These appear in `JOURNAL.md` and/or other handoff bundles but in no governance surface. This is
the *weakest* consumption class that is still real consumption: a JOURNAL line records that the
artifact was produced in a session; a handoff bundle may point a successor seat at it. Neither is
a decision resting on the file. Listed separately from Appendix C so the reaper can price them
differently — a JOURNAL mention is at least a human act, a funnel-baseline entry is not.


- `docs/audits/2026-03-30-dev-practice-os-state-audit.md` — only: handoffx8, eco
- `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md` — only: handoffx9, eco, JOURNAL
- `docs/audits/2026-04-24-council-28-29-consolidated-actions.md` — only: handoffx8, eco
- `docs/audits/2026-04-24-playbook-tagging-sanity-check.md` — only: handoffx8, eco
- `docs/audits/2026-04-24-stream-a-gap-report.md` — only: handoffx9, eco, JOURNAL
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — only: handoffx10, eco, JOURNAL
- `docs/audits/2026-04-25-claude-code-features-inventory.md` — only: handoffx10, eco, JOURNAL
- `docs/audits/2026-04-27-numbers-audit.md` — only: handoffx13, eco, JOURNAL
- `docs/audits/2026-04-27-pre-debate-audit-cross-repo-and-handoff.md` — only: handoffx11, eco
- `docs/audits/2026-04-30-ai-council-audit-report.md` — only: handoffx8, eco
- `docs/audits/2026-04-30-ai-council-discovery.md` — only: handoffx8, eco, JOURNAL
- `docs/audits/2026-04-30-ai-council-rediscovery.md` — only: handoffx8, eco
- `docs/audits/2026-05-11-codex-prompt-b-docs-alignment.md` — only: handoffx7, eco
- `docs/audits/2026-05-12-codex-ai-council-handoff-stage3.md` — only: handoffx6, eco
- `docs/audits/2026-05-12-hooks-discovery-resolution.md` — only: handoffx6, eco
- `docs/audits/2026-05-12-hooks-discovery.md` — only: handoffx6, eco, JOURNAL
- `docs/audits/2026-05-15-ecosystem-audit.md` — only: handoffx7, eco, tests
- `docs/audits/2026-05-16-ecosystem-audit.md` — only: handoffx4, eco
- `docs/audits/2026-05-17-corp-monorepo-governance-rollout-plan.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-05-17-skills-hooks-usage-review.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-05-19-rollout-readiness.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-05-20-posture-audit-verification.md` — only: handoff, eco, JOURNAL
- `docs/audits/2026-05-22-codex-codemap-generator-tool.md` — only: handoff, eco
- `docs/audits/2026-05-22-codex-drift-burndown-2026-05-22.md` — only: handoff, eco
- `docs/audits/2026-05-23-.dev-knowledge-audit.md` — only: handoff, eco, JOURNAL
- `docs/audits/2026-05-23-codex-codemap-amendment-and-dogfood.md` — only: handoff, eco
- `docs/audits/2026-05-23-codex-codemap-mermaid-fence-wrap.md` — only: handoff, eco
- `docs/audits/2026-05-23-corp-monorepo-deep-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-05-23-ecosystem-audit.md` — only: handoff, eco
- `docs/audits/2026-05-24-dev-knowledge-self-audit.md` — only: handoff, eco, scripts, tests, JOURNAL
- `docs/audits/2026-05-25-ai-council-universalization-execution-plan.md` — only: eco, JOURNAL
- `docs/audits/2026-05-28-final-state-and-process-diagrams-verification.md` — only: eco, JOURNAL
- `docs/audits/2026-05-28-mermaid-dark-theme-verification.md` — only: eco, JOURNAL
- `docs/audits/2026-05-28-mermaid-readability-v2-verification.md` — only: eco, JOURNAL
- `docs/audits/2026-05-28-universalization-durability-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-05-29-handoff-v3.4-fix-campaign-verification.md` — only: eco, JOURNAL
- `docs/audits/2026-05-29-overnight-morning-briefing.md` — only: eco, JOURNAL
- `docs/audits/2026-05-31-backlog-reconciliation-classification.md` — only: eco, JOURNAL
- `docs/audits/2026-05-31-methodology-canonical-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-01-codex-backlog-migration-adr64.md` — only: eco, JOURNAL
- `docs/audits/2026-06-01-codex-backlog-story-map.md` — only: eco, JOURNAL
- `docs/audits/2026-06-01-codex-sacred-files-cadence-check10.md` — only: eco, JOURNAL
- `docs/audits/2026-06-02-ecosystem-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-03-codex-doctools-hook-repo.md` — only: eco, JOURNAL
- `docs/audits/2026-06-03-codex-tier1-precommit-stage-fix.md` — only: eco, JOURNAL
- `docs/audits/2026-06-03-phase0-workflow-gates-findings.md` — only: eco, JOURNAL
- `docs/audits/2026-06-04-conformance-rerun-delta-digest.md` — only: eco, JOURNAL
- `docs/audits/2026-06-05-machinery-inventory.md` — only: handoff, eco, JOURNAL
- `docs/audits/2026-06-06-codex-85-fleet-scheduler.md` — only: eco, JOURNAL
- `docs/audits/2026-06-06-codex-immutability-guard.md` — only: eco, JOURNAL
- `docs/audits/2026-06-06-corp-monorepo-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-06-ecosystem-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-07-changelog-review.md` — only: eco, JOURNAL
- `docs/audits/2026-06-07-ecosystem-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-07-wave-a-validation.md` — only: eco, JOURNAL
- `docs/audits/2026-06-08-floor-pilot-corp-sca-validation.md` — only: eco, JOURNAL
- `docs/audits/2026-06-09-codex-prose-state-checker-89.md` — only: eco, JOURNAL
- `docs/audits/2026-06-10-codex-147-ship-gate.md` — only: eco, JOURNAL
- `docs/audits/2026-06-10-codex-amendment-gate-11.md` — only: eco, JOURNAL
- `docs/audits/2026-06-10-consolidation-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-10-fleet-handoff-readiness.md` — only: eco, JOURNAL
- `docs/audits/2026-06-13-codex-156-taskgraph.md` — only: eco, JOURNAL
- `docs/audits/2026-06-13-conformance-nightly-digest.md` — only: handoff, eco
- `docs/audits/2026-06-17-codex-coherence-integration.md` — only: eco, JOURNAL
- `docs/audits/2026-06-19-consolidation-state-report.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-06-19-playbook-essentials-currency-audit.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-06-21-audit-process-findings.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-06-21-audit-technical-findings.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-06-23-architecture-fidelity-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-23-canonical-corpus-coherence-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-23-playbook-fidelity-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-06-25-dependency-architecture-coverage-audit.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-06-25-process-trigger-usage-audit.md` — only: handoffx2, eco
- `docs/audits/2026-06-26-corpus-graph-justify-or-retire.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-06-26-playbook-condensation-rule-inventory.md` — only: eco, JOURNAL
- `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md` — only: handoffx6, eco, JOURNAL
- `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-04-coherence-spine-review.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-04-handoff-adoption-review.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-04-rot-algorithm-design.md` — only: handoffx4, eco, JOURNAL
- `docs/audits/2026-07-05-codex-consumer-arc.md` — only: eco, JOURNAL
- `docs/audits/2026-07-05-codex-slice-b-fix-batch.md` — only: eco, JOURNAL
- `docs/audits/2026-07-05-draft-tier3-claudemd-generability.md` — only: eco, scripts
- `docs/audits/2026-07-05-overnight-autonomy-run.md` — only: eco, JOURNAL
- `docs/audits/2026-07-06-codex-g7-mirror.md` — only: eco, JOURNAL
- `docs/audits/2026-07-08-grooming-worksheet.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-08-qa-role-incident-evidence.md` — only: eco, JOURNAL
- `docs/audits/2026-07-09-changelog-review.md` — only: handoffx2, ecox2, JOURNAL
- `docs/audits/2026-07-09-night-verification-report.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-07-11-changelog-review-codex-cc.md` — only: eco, JOURNAL
- `docs/audits/2026-07-11-technical-audit-corpus-verb-list.md` — only: eco, JOURNAL
- `docs/audits/2026-07-12-technical-night-rollout-ai-council.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-07-12-technical-night-verdict-sheet.md` — only: eco, JOURNAL
- `docs/audits/2026-07-13-technical-a0-traceability-closure.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-13-technical-content-parity-inventory.md` — only: eco, JOURNAL
- `docs/audits/2026-07-13-technical-wave3-reading-friction-census.md` — only: eco, JOURNAL
- `docs/audits/2026-07-16-codex-tail-firstread-lessons.md` — only: eco, JOURNAL
- `docs/audits/2026-07-17-codex-adr29-legacy-split-amendment.md` — only: eco, JOURNAL
- `docs/audits/2026-07-17-codex-arc3-ownership-axis.md` — only: eco, JOURNAL
- `docs/audits/2026-07-17-codex-gate-rev-axis.md` — only: eco, JOURNAL
- `docs/audits/2026-07-17-codex-role-governance.md` — only: eco, JOURNAL
- `docs/audits/2026-07-18-codex-ruling-w-adr-amendment.md` — only: eco, JOURNAL
- `docs/audits/2026-07-18-technical-arc4-leg1-ruff-equalization.md` — only: eco, JOURNAL
- `docs/audits/2026-07-19-codex-canon-inoculation.md` — only: eco, JOURNAL
- `docs/audits/2026-07-19-technical-arc5-educate.md` — only: eco, JOURNAL
- `docs/audits/2026-07-21-technical-night-backlog-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-07-21-technical-night-code-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-07-25-codex-lane-d-rulings.md` — only: eco, JOURNAL
- `docs/audits/2026-07-25-codex-vision-reread-recheck.md` — only: eco, JOURNAL
- `docs/audits/2026-07-25-codex-vision-reread.md` — only: eco, JOURNAL
- `docs/audits/2026-07-26-codex-routine-consumers-check.md` — only: eco, JOURNAL
- `docs/audits/2026-07-27-codex-handoff-v6-pack.md` — only: eco, JOURNAL
- `docs/audits/2026-07-27-codex-lane-filings-uv-bakeoff-extraction.md` — only: eco, JOURNAL
- `docs/audits/2026-07-28-codex-444-release-0-1-11.md` — only: eco, JOURNAL
- `docs/audits/2026-07-28-codex-p6-prep-review.md` — only: eco, JOURNAL
- `docs/audits/2026-07-28-technical-437-closure-token-design.md` — only: eco, JOURNAL
- `docs/audits/2026-07-28-technical-d-queue-0826.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-28-technical-drain-slice-prep.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md` — only: handoffx4, eco
- `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-07-30-census-fleet-state-boot-prep.md` — only: eco, JOURNAL
- `docs/audits/2026-07-30-codex-446-v6-boot-build.md` — only: eco, JOURNAL
- `docs/audits/2026-07-30-qa-assemble-paste-test-gap-review.md` — only: eco, JOURNAL
- `docs/audits/2026-07-30-technical-night-batch-standing-section-draft.md` — only: eco, JOURNAL
- `docs/audits/2026-07-30-technical-v6-open-questions-ruling-dossier.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-codex-382-w2-schema-v1.md` — only: eco, tests, JOURNAL
- `docs/audits/2026-07-31-codex-382-w3-loader.md` — only: eco, tests, JOURNAL
- `docs/audits/2026-07-31-codex-382-w4-report.md` — only: eco, scripts, tests, JOURNAL
- `docs/audits/2026-07-31-ecosystem-audit.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-technical-382-arc-educate.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-technical-intake-split-generality-discharge.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-technical-v6-frozen-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-07-31-verification-first-live-v6-boot-report.md` — only: eco, JOURNAL
- `docs/audits/2026-08-02-conformance-nightly-digest.md` — only: eco, JOURNAL
- `docs/audits/2026-08-02-technical-night-batch-lb-fleet-audit-commits.md` — only: eco, tests
- `docs/audits/2026-08-03-codex-474-gen-task-tree-write-guard-retro.md` — only: eco, JOURNAL
- `docs/audits/2026-08-03-codex-475-seal-identity-precommit-gate-retro.md` — only: eco, JOURNAL
- `docs/audits/2026-08-03-codex-adr85-integration-enforcement.md` — only: eco, JOURNAL
- `docs/audits/2026-08-03-technical-night-batch-digest.md` — only: eco, JOURNAL
- `docs/audits/2026-08-04-codex-482-glob-engine-true-glob.md` — only: eco, JOURNAL
- `docs/audits/2026-08-04-technical-closure-proposal-ranked-sheet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-06-codex-batch-protocol.md` — only: eco, JOURNAL
- `docs/audits/2026-08-06-codex-lane-c-504-failclosed.md` — only: ecox3, JOURNAL
- `docs/audits/2026-08-06-technical-batch-1-integration-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-07-codex-pre-cut-retro-batch2-consolidation.md` — only: eco, JOURNAL
- `docs/audits/2026-08-07-technical-batch-2-manifest.md` — only: eco, tests
- `docs/audits/2026-08-07-technical-fleet-backup-posture.md` — only: eco, JOURNAL
- `docs/audits/2026-08-07-technical-handoff-engine-thinning.md` — only: handoffx4, eco, JOURNAL
- `docs/audits/2026-08-07-technical-lane-2-worktree-portability.md` — only: eco, tests
- `docs/audits/2026-08-08-codex-batch-3-integrator-arc.md` — only: eco, JOURNAL
- `docs/audits/2026-08-08-codex-lane-290-floor-teeth.md` — only: eco, deploy
- `docs/audits/2026-08-08-technical-batch-3-consolidation-report.md` — only: eco, JOURNAL
- `docs/audits/2026-08-08-technical-batch-3-manifest.md` — only: eco, JOURNAL
- `docs/audits/2026-08-08-technical-handoff-cut-staging.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-codex-arc1-doc-defects-retro.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-codex-batch-3-integrator-arc.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-technical-batch-night-manifest.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-technical-batch-night-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-technical-challenge-retrieval.md` — only: eco, JOURNAL
- `docs/audits/2026-08-09-technical-decision-sheet.md` — only: handoffx6, eco, JOURNAL
- `docs/audits/2026-08-09-technical-night-batch-findings-index.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-census-conformance-digest-content.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-technical-batch-4-prep-evidence.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md` — only: handoffx2, eco
- `docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` — only: handoffx2, eco
- `docs/audits/2026-08-10-technical-night-n1-window-synthesis.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-technical-night-n3-ratification-pack.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-technical-research-ingest-reconcile-and-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md` — only: handoffx4, eco, JOURNAL
- `docs/audits/2026-08-11-codex-arc9-absorb-m6-gen-audit-index.md` — only: eco, JOURNAL
- `docs/audits/2026-08-11-codex-batch4-w1-lane-regex.md` — only: eco, JOURNAL
- `docs/audits/2026-08-11-technical-batch-4-w1-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-11-technical-batch-4-w5-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-11-technical-batch-4-w521-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-11-verification-batch-4-challenge-answer.md` — only: eco, JOURNAL
- `docs/audits/2026-08-12-codex-closing-arc-organ-index-guard.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-08-13-codex-w3-landing-predicate.md` — only: scriptsx2, eco, tests, JOURNAL
- `docs/audits/2026-08-13-technical-492-corpus-reconciliation-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-13-technical-524-check-extensions-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-13-technical-batch-4-w4c-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-13-technical-batch-4-w4d-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-13-technical-w4a-conversions-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-13-technical-w4b-conversions-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-14-qa-night2-quality.md` — only: JOURNAL
- `docs/audits/2026-08-14-technical-525-arch-organ-rows-lane-contract.md` — only: JOURNAL
- `docs/audits/2026-08-14-verification-night2-hygiene.md` — only: JOURNAL
- `docs/audits/2026-08-14-verification-night2-plancheck.md` — only: JOURNAL
- `docs/audits/2026-08-15-technical-batch-phase1-manifest.md` — only: JOURNAL
- `docs/audits/2026-08-16-technical-82-conversions-lane-contract.md` — only: JOURNAL
- `docs/audits/2026-08-17-census-north-star-inventory.md` — only: eco, JOURNAL
- `docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md` — only: ecox2, scripts
- `docs/audits/2026-08-17-technical-batch-7a-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-17-technical-nb7-lifecycle-instrument-verdict.md` — only: eco, JOURNAL
- `docs/audits/2026-08-18-technical-batch1-integrator-packet.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-19-technical-554-proof.md` — only: eco, scripts, tests
- `docs/audits/2026-08-19-technical-c-lanes-consolidated.md` — only: handoffx3, eco, JOURNAL
- `docs/audits/2026-08-19-technical-l2-wiring-lane-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-19-technical-morning-consolidation-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-19-technical-s1-seat-arc-packet.md` — only: eco, JOURNAL
- `docs/audits/2026-08-20-technical-final-integrator-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-20-technical-gemini-ab-lane-contract-slot1.md` — only: eco, JOURNAL
- `docs/audits/2026-08-20-technical-gemini-ab-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-20-technical-gemini-ab-results-slot1.md` — only: eco, JOURNAL
- `docs/audits/2026-08-20-technical-playbook-status-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-21-technical-ch8-dispatch-codification.md` — only: eco, JOURNAL
- `docs/audits/2026-08-21-technical-lane-arch-lifecycle-archival.md` — only: eco, JOURNAL
- `docs/audits/2026-08-21-technical-library-first-research-lane-contract.md` — only: eco, JOURNAL
- `docs/audits/2026-08-21-technical-north-star-position.md` — only: eco, JOURNAL
- `docs/audits/2026-08-22-codex-562-nopack-sandbox-terra.md` — only: eco, JOURNAL
- `docs/audits/2026-08-22-technical-cloud-2-563-view-layer.md` — only: eco, scripts
- `docs/audits/2026-08-23-technical-funnel-retro-classification.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-23-technical-lane-dispatch-codification.md` — only: ecox3, JOURNAL
- `docs/audits/2026-08-23-technical-lane-funnel-coverage.md` — only: eco, tests
- `docs/audits/2026-08-23-technical-lane-status-grammar.md` — only: scriptsx3, ecox2, tests, JOURNAL
- `docs/audits/2026-08-23-technical-research-model-bus.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-23-technical-window-seal.md` — only: handoffx2, eco, JOURNAL
- `docs/audits/2026-08-24-technical-batch-close.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-24-technical-research-candidate-register.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-24-technical-research-register-addendum.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-24-technical-warn-triage-and-teardown.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-24-verification-integrator-merged-result.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-24-verification-l6-rulings-landing.md` — only: ecox2, JOURNAL
- `docs/audits/2026-08-26-verification-batch-1-close-packet.md` — only: eco, JOURNAL


---

## Appendix E — INTAKE consumption: which intakes produced a decision

`DECISION` = named by at least one ADR · `ROW-ONLY` = named by a live `tasks/` row but no ADR ·
`PROSE-ONLY` = named only in protocol / canonical prose · `DEAD-END` = named by nothing.

Totals: **11 DECISION · 26 ROW-ONLY · 12 PROSE-ONLY · 1 DEAD-END.** The single dead end is
`docs/intake/archive/2026-07-11-tech-fleet-divergence-register.md` — status `SUPERSEDED` and
already relocated to the archive, i.e. the pipeline handled it correctly.


- `docs/intake/2026-07-07-arc5-pilot-followup-seeds.md` — status `SEED` — **ROW-ONLY** — ADRs: (none) — rows: #579 — 3 governance citers
- `docs/intake/2026-07-07-changelog-review-seeds.md` — status `SEED` — **ROW-ONLY** — ADRs: (none) — rows: #579 — 3 governance citers
- `docs/intake/2026-07-08-func-ai-council-interface.md` — status `SEED` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-07-08-func-dashboards-local-html.md` — status `SEED` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 3 governance citers
- `docs/intake/2026-07-08-func-new-project-bootstrap.md` — status `SEED` — **ROW-ONLY** — ADRs: (none) — rows: #43 — 3 governance citers
- `docs/intake/2026-07-08-func-night-routines-suite.md` — status `SEED` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-07-11-tech-ownership-manifest.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-101-hermetization.md — rows: #548 — 10 governance citers
- `docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #332, #549 — 8 governance citers
- `docs/intake/2026-07-12-siem-requirements-ruled-pack.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #550 — 6 governance citers
- `docs/intake/2026-07-16-satellite-onboarding-prompts.md` — status `READY` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-07-21-func-fleet-north-star.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-104-fleet-repository-shape.md, ADR-109-fleet-desired-state-contract-v1.md, ADR-113-l0-l5-maturity-ladder-ratification.md — rows: #382, #383, #385, #386, #388, #443 — 16 governance citers
- `docs/intake/2026-07-25-tech-consolidation-decision.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-107-backlog-restructure-engine-schema-viewer.md — rows: #403, #431 — 9 governance citers
- `docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md` — status `SEED` — **DECISION** — ADRs: ADR-82-handoff-process-v5-model-c.md — rows: #446 — 6 governance citers
- `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #421, #435, #441, #446 — 12 governance citers
- `docs/intake/2026-07-28-north-star-delta-review.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #388, #443 — 6 governance citers
- `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md` — status `SEED` — **DECISION** — ADRs: ADR-108-decision-routing-and-engineering-standards.md, ADR-109-fleet-desired-state-contract-v1.md, ADR-111-finding-triage-pipeline.md — rows: #451 — 9 governance citers
- `docs/intake/2026-07-30-tech-browser-architect-orientation.md` — status `SEED` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 2 governance citers
- `docs/intake/2026-08-01-func-distillation-and-library-first.md` — status `SEED` — **ROW-ONLY** — ADRs: (none) — rows: #467, #471 — 3 governance citers
- `docs/intake/2026-08-05-func-simplification-distribution-wave.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-110-parallel-execution-batch-protocol.md, ADR-111-finding-triage-pipeline.md, ADR-115-agents-md-portable-instruction-layer.md — rows: #294, #308, #559, #561, #570 — 17 governance citers
- `docs/intake/2026-08-05-tech-currency-wave-1.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #570 — 7 governance citers
- `docs/intake/2026-08-06-func-parallel-execution-system.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-110-parallel-execution-batch-protocol.md — rows: #505 — 6 governance citers
- `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-110-parallel-execution-batch-protocol.md — rows: #570 — 11 governance citers
- `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #529, #565, #576 — 10 governance citers
- `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md` — status `ACCEPTED` — **DECISION** — ADRs: ADR-112-two-tier-adoption-bar.md — rows: (none) — 5 governance citers
- `docs/intake/2026-08-09-func-code-style-doctrine.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #579 — 4 governance citers
- `docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #513 — 4 governance citers
- `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #561 — 8 governance citers
- `docs/intake/2026-08-12-func-repo-self-description-consolidation.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #571 — 4 governance citers
- `docs/intake/2026-08-16-code-architecture-enforcement.md` — status `DRAFT` — **ROW-ONLY** — ADRs: (none) — rows: #572, #579 — 4 governance citers
- `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md` — status `DRAFT` — **ROW-ONLY** — ADRs: (none) — rows: #577 — 7 governance citers
- `docs/intake/2026-08-17-tech-fleet-config-standardization.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #555, #559 — 8 governance citers
- `docs/intake/2026-08-17-tech-machine-verifiable-done-when.md` — status `DRAFT` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 5 governance citers
- `docs/intake/2026-08-17-tech-off-machine-agent-substrate.md` — status `ACCEPTED` — **ROW-ONLY** — ADRs: (none) — rows: #554, #561 — 8 governance citers
- `docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md` — status `DRAFT` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 5 governance citers
- `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md` — status `DRAFT` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-08-23-tech-generated-artifact-currency.md` — status `DRAFT` — **DECISION** — ADRs: ADR-115-agents-md-portable-instruction-layer.md — rows: #584 — 5 governance citers
- `docs/intake/2026-08-23-tech-nopack-guard-refusal-surface.md` — status `DRAFT` — **ROW-ONLY** — ADRs: (none) — rows: #578 — 3 governance citers
- `docs/intake/2026-08-24-tech-agents-md-admission-vs-adr53.md` — status `READY` — **DECISION** — ADRs: ADR-115-agents-md-portable-instruction-layer.md — rows: #584 — 5 governance citers
- `docs/intake/2026-08-24-tech-contract-integrity-gate.md` — status `READY` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-08-24-tech-disposition-register-schema.md` — status `READY` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-08-24-tech-ruling-register-landing-gap.md` — status `READY` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/2026-08-24-tech-substrate-router.md` — status `READY` — **ROW-ONLY** — ADRs: (none) — rows: #582 — 3 governance citers
- `docs/intake/2026-08-24-tech-supplement-probe-fill-state-defect.md` — status `READY` — **PROSE-ONLY** — ADRs: (none) — rows: (none) — 1 governance citers
- `docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md` — status `CONSUMED` — **ROW-ONLY** — ADRs: (none) — rows: #271 — 2 governance citers
- `docs/intake/archive/2026-07-06-platform-feature-scan.md` — status `CONSUMED` — **ROW-ONLY** — ADRs: (none) — rows: #273, #274, #387 — 4 governance citers
- `docs/intake/archive/2026-07-07-test-suite-hygiene.md` — status `CONSUMED` — **ROW-ONLY** — ADRs: (none) — rows: #278 — 2 governance citers
- `docs/intake/archive/2026-07-11-tech-c4-visualization-memo.md` — status `REJECTED` — **ROW-ONLY** — ADRs: (none) — rows: #552 — 7 governance citers
- `docs/intake/archive/2026-07-11-tech-fleet-divergence-register.md` — status `SUPERSEDED` — **DEAD-END** — ADRs: (none) — rows: (none) — 0 governance citers
- `docs/intake/archive/2026-07-13-siem-fleet-management-requirements-codex.md` — status `CONSUMED` — **ROW-ONLY** — ADRs: (none) — rows: #550 — 4 governance citers
- `docs/intake/archive/2026-07-13-siem-fleet-management-requirements.md` — status `CONSUMED` — **ROW-ONLY** — ADRs: (none) — rows: #550 — 5 governance citers


---

*End of report. Read-only run: no repo file written, no commit, no branch, no generated file
regenerated. `git status --porcelain` empty at start and at finish.*
