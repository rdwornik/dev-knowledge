# Nightly Conformance Digest — 2026-09-25

- **Lane:** nightly READ-ONLY documentation-conformance review, `.dev-knowledge` / `rdwornik/dev-knowledge`
- **Posture:** proposals only. Nothing was fixed, nothing merged, nothing written to `main`.
- **Bound at:** `main` HEAD `2b5a4ef8b59c383fc0cb69f602d6adae99629395` (*Merge branch 'worktree-lane-merge-hygiene' @ 239beb29*)

## Run

**Path: NATIVE Workflow launcher** — `.claude/workflows/conformance-hub.js` ran directly via the `Workflow` tool (`name: "conformance-hub"`, run id `wf_6580ffca-6da`). The native launcher **was enabled** tonight, unlike the most recent prior re-probe recorded in `docs/audits/2026-08-10-conformance-nightly-digest.md` (native launcher unavailable that night). No spec-orchestration fallback was needed.

**Actual models per stage** (from the run's own `workflowProgress` records — this is the platform re-probe record the prompt asks for):

| Stage | Agent | Requested model | **Actual model** |
|---|---|---|---|
| 1 — verifiers | V1-journal-vs-git | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V2-livingdoc-claims | `claude-sonnet-5` | `claude-sonnet-5` |
| 1 — verifiers | V3-backlog-closures | `claude-sonnet-5` | `claude-sonnet-5` |
| 2 — skeptic | skeptic-adversarial | *(no override in script; comment says "intended: Opus")* | **`claude-sonnet-5`** |
| 3 — digest | digest-synthesis | *(no override in script; comment says "intended: Opus")* | **`claude-sonnet-5`** |

**Flag for the operator:** the script's own comments (`conformance-hub.js:6-7`) say Stage 2/3 are *intended* to run on Opus, but the `agent()` calls for `skeptic` and `digest` carry no `model:` override, so they fell through to whatever default the runtime resolved — which was Sonnet tonight, same as Stage 1. This is a platform/script observation, not a documentation-conformance finding, so it is **not** counted in the raw/survived/killed tallies below; noting it here per the "actual model each stage used" requirement.

Total: 5 agents, 65 tool calls, 405,917 subagent tokens, ~313s wall time.

## Delta vs prior digest

**Baseline consulted:** `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` — the highest-dated file under `docs/audits/` matching `conformance` in its name.

**Shape mismatch, flagged rather than silently reconciled:** that baseline is **not** a standard V1/V2/V3 nightly digest. It is a targeted, differently-scoped review (`[#171]` leg-2 scope ambiguity + `ecosystem/conformance.html` / `scripts/gen_dashboard.py`, findings F1–F10), produced outside this pipeline's schema (no `domain`/`evidence_command`/`counts_marker` contract, no verifier/skeptic/digest fan-out). None of tonight's V1 (JOURNAL-vs-git), V2 (living-doc claims), or V3 (BACKLOG closures) domains overlap F1–F10's subject (the conformance dashboard generator), so **F1–F10 were not re-verified this run** — their status is unknown, not resolved, and they are out of scope for this delta.

For a same-shape comparison, the last standard V1/V2/V3 digest is `docs/audits/2026-08-10-conformance-nightly-digest.md` (3 findings, 0 killed). None of that run's 3 survivors (a stale `/override` reference in the now-deleted `protocols/ESSENTIALS.md`, a "five carriers" vs six-carrier ARCHITECTURE.md count, and an ADR-109-vs-110 Purpose-line lag) were re-checked tonight either — V2's scope this run was `VISION.md` / `ARCHITECTURE.md` / `CLAUDE.md` / `CONTRIBUTING.md`, and none of those three specific line-items were re-scanned, so they are also **not asserted resolved** here; they simply weren't retested.

**Delta table (best-effort — see caveats above):**

| Class | Count | Detail |
|---|---|---|
| RESOLVED | 0 | No baseline item (F1–F10 or the 2026-08-10 survivors) was in tonight's checked scope, so none can be marked resolved from this run's evidence |
| PERSISTING | 0 | Same reason — no overlap to confirm persistence |
| NEW | 4 | All 4 of tonight's survivors are newly raised this run (see Findings below) |
| **Raw → Survived → Killed** | **5 → 4 → 1** | Stage 1 raw findings: 5 (V1=0, V2=5, V3=0). Stage 2 skeptic: 4 survived, 1 killed, 0 dropped for missing evidence. |

## Findings (survivors — proposals only)

### HIGH — `docs/archive/VISION.md:18` — stale `CANONICAL_MANDATORY` membership claim

- **Claim:** *"it is `canonical_docs.CANONICAL_MANDATORY[0]`"*
- **Evidence command:** `grep -n -A4 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py`
- **Verdict:** contradicted
- **Note:** `scripts/canonical_docs.py:114-116` defines `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)` — VISION is absent entirely (index 0 is `ARCHITECTURE`). The module's own comments describe VISION as retired into a separate `CANONICAL_RETIRED` tuple. No ADR exempts VISION.md's own prose from staying accurate about this.
- **Proposed fix (proposal only):** Update the VISION.md paragraph to state VISION was retired from `CANONICAL_MANDATORY` into `CANONICAL_RETIRED`, rather than claiming current index-0 membership.

### HIGH — `docs/archive/VISION.md:17` — stale MUST-tier / nine-member claim

- **Claim:** *"It is a `MUST` on all nine ADR-104 fleet members (`ecosystem/parity-surfaces.yaml`, `canonical-doc-vision`)"*
- **Evidence command:** `grep -n -A50 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml | sed -n '1,12p;48,51p'`
- **Verdict:** contradicted
- **Note:** `ecosystem/parity-surfaces.yaml`'s `canonical-doc-vision` row sets `tier: {hub: SHOULD, consumer: SHOULD}`, not MUST, and its own `reason:` field states the row was demoted from MUST on 2026-08-31 ([#614] lane-a, ADR-114) and that the old "all nine" claim was refuted — VISION.md is tracked in eight of nine members. VISION.md's still-live prose has not been reconciled with the decision that superseded it.
- **Proposed fix (proposal only):** Update VISION.md's paragraph to reflect the SHOULD/SHOULD demotion and the corrected eight-of-nine tracking count.

### MED — stale "43.50 KiB" wholesale-copy figure (3 files)

- **Claim:** *"a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently"* — repeated in `CLAUDE.md:212`, `AGENTS.md:35-37`, `CONTRIBUTING.md:31-32`
- **Evidence command:** `wc -c CLAUDE.md; git show 56ec7dc:CLAUDE.md | wc -c`
- **Verdict:** contradicted
- **Note:** CLAUDE.md measures 23,988 B (23.43 KiB) today — under, not over, the 32 KiB cap. The skeptic went further: at the commit that first introduced this figure verbatim, CLAUDE.md itself measured only 23,651 B — the number was never accurate at any checkable point in tracked history. This is the exact anti-pattern the repo's own conventions warn against ("a number typed into a doc is stale at the next commit"). The underlying policy (don't copy CLAUDE.md wholesale into AGENTS.md) is unaffected — only the illustrative figure is wrong.
- **Proposed fix (proposal only):** Recompute/correct the figure in all three files, or replace it with a pointer to a live-computed size instead of a fixed number.

### LOW — `CONTRIBUTING.md:19` — AGENTS.md byte-count drift

- **Claim:** *"`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"*
- **Evidence command:** `wc -c AGENTS.md`
- **Verdict:** contradicted
- **Note:** AGENTS.md currently measures 5,843 B, a 129 B drift from edits made after the figure was recorded and never refreshed. Low severity: no gate depends on this number, but it's the same stale-count class the repo's own conventions single out by name.
- **Proposed fix (proposal only):** Drop the byte figure (cite `wc -c AGENTS.md` as the live surface) or refresh it.

## Killed finding (adversarial skeptic)

- **Claim:** *"BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB"* for ARCHITECTURE.md's own size (`ARCHITECTURE.md:17`)
- **Kill reason:** true-but-irrelevant
- **Kill detail:** Re-read in full, the line is a historical record of a past cut plus a stated aspirational target at the time of that lane — not a present-tense compliance claim. ARCHITECTURE.md's current 23,849 B exceeding an unmet target doesn't contradict a sentence that never asserted current compliance. Unlike CLAUDE.md (which has a live byte-cap gate and "bytes bind" language), this line is retrospective, not a live budget claim.

## Checked-clean (selected — absence of findings is informative)

**V1 (JOURNAL vs git, last 10 entries, 2026-09-24(l) through 2026-09-25(b)):** every cited commit SHA and merge commit exists with content matching the JOURNAL narrative (spot-checked: `aeab4577`'s `scripts/view_budget.yaml` verbatim values; doc-counts 7503→7504 progression across a merge; `tasks/1015-...md` registered in `tasks/manifest.json`); all 9 claimed-new scripts/files exist on disk at HEAD; clean working tree at HEAD with no significant un-journaled merged work. History goes back to 2026-09-19, well before the window — no shallow-clone exclusions needed.

**V2 (living-doc claims, scope: VISION.md/ARCHITECTURE.md/CLAUDE.md/CONTRIBUTING.md):** CLAUDE.md's ≤24,576 B budget matches `tests/test_claude_md_byte_cap.py` and current size (23,988 B) is within it · ARCHITECTURE.md's "29 requirements, 8 measured, 21 candidate" matches an exact grep of `ecosystem/quality-requirements.yaml` · ARCHITECTURE.md's "8 classes" organ-index claim matches `ecosystem/organ-index.md`'s heading count exactly · CONTRIBUTING.md's ruff pin (v0.15.5) matches `.pre-commit-config.yaml` and the `pyproject.toml` floor · `.github/workflows/report-only-wall.yml` exists as a standalone workflow, confirming ARCHITECTURE.md Ch6 · cited ADRs (114, 115, 94, 101, etc.) all exist under `docs/decisions/` · CLAUDE.md §9's "B2 lane4 armed 13" matches an exact count of `RE-ARMED 2026-09-18` lines in `.pre-commit-config.yaml`.

**V3 (BACKLOG closure coherence, ~3-week window):** only one true closure landed in the window — `04439e1` closing `[#960]`. Traced the full 8-commit lane history against the pre-closure task's 6-item Done-when checklist; every item is backed by a real, locatable artifact (lane-diff selection mode, tree-keyed record, two registry-gap fixes, a merge-queue measurement audit, a Codex terra review). `BACKLOG.md`, `tasks/manifest.json`, and the task file's `status: closed` are mutually consistent with the JOURNAL's description of an operator-scoped approval covering only #960.

## Next actions (proposals for the operator — no action taken)

1. Update `docs/archive/VISION.md:18` — retired from `CANONICAL_MANDATORY`, not current index-0 member.
2. Update `docs/archive/VISION.md:17` — SHOULD/SHOULD tier, eight-of-nine tracking, per ADR-114 / [#614] lane-a.
3. Correct or remove the "43.50 KiB" figure in `CLAUDE.md:212`, `AGENTS.md:35-37`, `CONTRIBUTING.md:31-32`.
4. Refresh or drop the AGENTS.md byte figure in `CONTRIBUTING.md:19`.
5. **(Process)** `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md`'s F1–F10 (the `[#171]` conformance-dashboard review) were not re-verified tonight — out of this run's V1/V2/V3 scope. If those findings are still open, they need a dedicated re-check; this digest cannot speak to their current status.
6. **(Process)** Stage 2/3 of `conformance-hub.js` are commented as Opus-intended but carry no `model:` override and ran on Sonnet tonight — worth a script fix or a comment correction so the "Run:" record stops needing manual reconciliation.

## Safety Tripwire

`git status --porcelain` output at digest write time (captured after writing this file, before commit):

```
?? docs/audits/2026-09-25-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. ✓ Safety check passes.

<!-- counts: raw=5 survived=4 killed=1 -->
