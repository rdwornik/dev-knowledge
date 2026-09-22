<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-22

**Date:** 2026-09-22
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded**, fifth consecutive clean run (2026-09-18 through 2026-09-21 also ran to completion). `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`) per the re-probe instruction (task id `w56not797`, run id `wf_1fee2e2c-ba7`) and ran to completion in one pass — no spec-orchestration fallback needed.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 73,209 | 16 | 71s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 114,396 | 26 | 211s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 121,471 | 42 | 245s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 60,614 | 8 | 93s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 52,596 | 1 | 51s |

Total: 422,286 subagent tokens, 93 tool calls, ~464s (7.7 min) wall time (Stage 1's three verifiers ran in parallel).

**Model-pin note (script vs. meta, informational, unchanged since 2026-09-18):** `conformance-hub.js`'s `meta.phases` describes Stage 2 ("skeptic") and Stage 3 ("digest") as intended for Opus, but neither `agent()` call in the script body passes an explicit `model` for those two stages (only Stage 1's three calls pin `model: 'claude-sonnet-5'`). Tonight, as on every prior successful run, both unpinned stages ran on `claude-sonnet-5` by default. Not a doc-conformance finding — flagged for the platform record since the meta description and actual behavior still diverge.

**Known-advisory infra note (unrelated to doc conformance):** the orchestrating session's own Stop-hook backpressure fired repeatedly throughout this run with `Required uv version ==0.11.19 does not match the running version 0.8.17`. Same systemic mismatch flagged since the 2026-08-10 digest's Next Actions #7 — this cloud runtime cannot reach the pinned `uv` release. Now **51 days unresolved** (2026-08-02 → 2026-09-22). Advisory-only per `CLAUDE.md` §9 — not a doc-conformance finding.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-09-21-conformance-nightly-digest.md`, fetched read-only from the **unmerged** branch `origin/claude/conformance-2026-09-21` (`git show origin/claude/conformance-2026-09-21:docs/audits/2026-09-21-conformance-nightly-digest.md`). No `docs/audits/*-conformance-nightly-digest.md` file exists on `main` more recent than 2026-08-10 — `origin/claude/conformance-2026-09-18` through `-21` are all still unmerged (verified fresh this run: none is an ancestor of `origin/main`). This is now the **fifth** consecutive night in this state (this run's own branch will be the sixth once pushed).
**Gap:** 1 day (2026-09-21 → 2026-09-22).

All 11 survivors from the 2026-09-21 digest's own Findings section were independently re-checked against current `origin/main` head (`df0c1ac`) with fresh evidence — 6 were independently re-derived by tonight's own V1/V2/V3 fan-out (one of them, the VISION.md header claim, split by tonight's V2 into two precise sub-findings covering the same location; two others — the `43.50 KiB` figure and the `ARCHITECTURE.md` size-target note — were re-derived with a **severity revision downward**, matching this repo's recurring pattern of the skeptic downgrading a stale-but-inert numeric claim). The other 5 were not independently re-derived by tonight's verifiers (the same verifier-coverage gap the 2026-09-20/21 digests both noted for a fixed subset of claims) and were re-verified directly instead with fresh `grep`/`wc` commands:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING (re-derived, split into 2 sub-claims)** | HIGH: `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` lane-a retired 2026-08-31 | Tonight's V2 independently re-derived both halves as separate raw findings: `grep -n -A5 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py` → `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)`, VISION absent; `grep -n -A15 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml` → `tier: {hub: SHOULD, consumer: SHOULD}`, "tracked in eight; terminal-setup has never had one." Unchanged text, now day 5. |
| **PERSISTING (re-derived, AGENTS.md half not separately flagged)** | HIGH: `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; still `stages: [manual]` | Tonight's V2 independently re-derived the `CLAUDE.md:65` half (`grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, unchanged comment). `AGENTS.md:66` re-verified directly: `grep -n "ruff check" AGENTS.md` → line 66 unchanged verbatim. Day 4. |
| **PERSISTING (re-derived)** | HIGH: `CONTRIBUTING.md:170`'s Validators table row lists `ruff` as a blocking commit-stage gate | Tonight's V2 independently re-derived this (same evidence command as above). Day 3. |
| **PERSISTING, not independently re-derived tonight** | MED: `[#780]`'s closure evidence and the 2026-09-16 closure census cite the wrong proving commit (`5f270cd9` instead of `b81c554`) for lane z-11's three-repo comparison | Tonight's V3 fan-out raised 0 findings (checked the closure window clean by its own criteria) — a verifier-coverage gap, since this is a citation-pointing defect rather than a Done-when/diff mismatch. Re-verified directly: `tasks/780-*.md` and `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25` still cite `5f270cd9`; `git log -1 --format='%H %s' 5f270cd9` still resolves to the unrelated `chore(lane): step-2 sync` commit, not the actual lane z-11 merge (`b81c554`). Day 2. |
| **PERSISTING (partially re-derived: 2 of 5 rows)** | MED/LOW: `CONTRIBUTING.md`'s Validators table lists five manual hooks as blocking commit-stage gates (`ruff` counted separately above; the remaining five are `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `audit-health`) | Tonight's V2 independently re-derived 2 of the 5: `audit-health` (`CONTRIBUTING.md:169`, MED — `grep -n -A7 'id: audit-health' .pre-commit-config.yaml` → `stages: [manual]`) and `validate-backlog` (`CONTRIBUTING.md:168`, LOW — same pattern). The other 3 rows (`normalize-dated-headers` line 159, `toc-freshness-playbook` line 161, `check-seal-identity` line 167) were not re-raised by tonight's fan-out; re-verified directly: all three still `stages: [manual]` in `.pre-commit-config.yaml` with the identical 2026-09-17 "MOVED to the Actions conductor" comment. Day 3. |
| **PERSISTING (re-derived, severity revised MED→LOW)** | MED, carried since ≥2026-08-10 (42 days at last count): the 43.50 KiB CLAUDE.md/AGENTS.md byte-count justification | Tonight's V2 independently re-derived this: `wc -c CLAUDE.md AGENTS.md` → 23,651 B + 5,843 B, still well under the 32 KiB cap the claim says it would exceed. Tonight's skeptic kept it but reclassified severity MED→LOW, reasoning the underlying anti-pattern rule's intent is unaffected — only its illustrative figure is stale. Now **43 days** unresolved (2026-08-10 → 2026-09-22). |
| **PERSISTING, not independently re-derived tonight** | MED: `CLAUDE.md` self-contradicts on the ADR-77 guard (§4 line 80 "stays armed" vs §9 line 194 "stays off ([#863])") | Not raised by tonight's V2 fan-out (same verifier-coverage gap as 2026-09-20/21). Re-verified directly: `grep -n -i "ADR-77" CLAUDE.md` → both lines present verbatim at the same line numbers, contradiction unresolved. Day 4. |
| **PERSISTING, not independently re-derived tonight** | LOW: `docs/archive/VISION.md:18-19` overstates its own machine-site footprint ("thirteen machine constants plus five deploy manifests") | Not raised by tonight's V2 fan-out. Re-verified directly: `grep -l 'VISION\.md:' deploy/manifest-v*.yaml \| wc -l` → 6, not 5; `scripts/canonical_docs.py`'s docstring still enumerates "the ten machine constants," not thirteen. Day 3. |
| **PERSISTING (re-derived)** | LOW: `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count (5,714 B) | Tonight's V2 independently re-derived this: `wc -c AGENTS.md` → 5,843 B, same 129 B gap measured since 2026-09-19. Day 5. |
| **PERSISTING, not independently re-derived tonight** | LOW: `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale | Not raised by tonight's V2 fan-out. Re-verified directly: `grep -c "^- verify:" .claude/rules/git-discipline.md` → 5, not 3; `CLAUDE.md:102` still reads "carries three `verify:` lines." Day 3. |
| **PERSISTING (re-derived, unchanged severity)** | LOW: `ARCHITECTURE.md`'s BUILD MODE header states an unqualified ≤15 KB size target the file no longer meets | Tonight's V2 independently re-derived this: `wc -c ARCHITECTURE.md` → 23,849 B, the identical figure measured on 2026-09-20/21 — the file has not changed size at all in three nights. Still ~55% over the stated target, still no enforcing gate (`_FILE_SIZE_BUDGETS` covers only `CLAUDE.md`). Day 3. |

**NEW this cycle:** none. All 9 of tonight's raw findings map onto items already carried from the 2026-09-21 baseline (one item split by tonight's fan-out into two sub-findings, another's severity revised downward).

**RESOLVED this cycle:** none. All 11 baseline survivors are still live on `origin/main`, byte-for-byte unchanged in every case that was directly re-checked.

**Delta counts:** 0 resolved · 11 persisting · 0 new
**This run's own raw → survived → killed:** 9 → 9 → 0 (tonight's V1/V2/V3 fan-out through the skeptic; the items carried forward but not independently re-derived tonight are additional and not counted in this ratio, matching the convention the 2026-08-10, 2026-09-20, and 2026-09-21 digests all used)
**Skeptic kill-rate:** 0% (0 of 9) — every raw finding tonight was confirmed by direct repo-state evidence (grep/wc/yaml parse); the 0% rate reflects well-targeted raw findings, not a lax pass — the skeptic actively downgraded two items' severity (the 43.50 KiB claim MED→LOW, matching the ARCHITECTURE.md size-target item already at LOW) after independently re-confirming the underlying facts rather than merely re-asserting them.

<!-- counts: raw=9 survived=9 killed=0 -->

---

## Summary

Doc health this cycle shows **zero resolutions and zero new findings** against an unusually stable baseline for a sixth consecutive measurement window: all 11 survivors carried from the 2026-09-21 digest are still live on `origin/main`, unchanged in every case that was directly re-checked, including `ARCHITECTURE.md`'s exact byte count (unmoved for three nights running) and `AGENTS.md`'s exact byte count. The only changes within carried items are two severity revisions (the 43.50 KiB byte-count claim MED→LOW, matching the earlier VISION.md machine-constants revision's pattern) and one item split into two precise sub-findings by tonight's independent fan-out (the VISION.md MUST-tier/`CANONICAL_MANDATORY[0]` claim, previously reported as a single combined finding).

The concentration of drift remains exactly where the last several nights placed it: (1) the 2026-09-17 pre-commit-gate strip to `stages: [manual]` still hasn't propagated into `CLAUDE.md` §4, `AGENTS.md`, or `CONTRIBUTING.md`'s Validators table — now expressed as 3 HIGH + 2 MED + 1 LOW findings across those files, none of it fixed in the five nights since first flagged; (2) VISION.md's 2026-08-31 retirement from MUST/`CANONICAL_MANDATORY` to SHOULD/`CANONICAL_RETIRED` still isn't reflected in the file's own header prose, alongside its stale machine-constant/manifest counts in the same paragraph; and (3) a handful of small, independent numeric-drift items (the 43.50 KiB byte-count claim, the ADR-77 self-contradiction, `CONTRIBUTING.md:19`'s byte figure, `CLAUDE.md`'s stale `verify:`-count, and `[#780]`'s wrong proving-SHA citation) that tonight's fan-out did not happen to re-derive on its own — the same verifier-coverage-gap pattern noted on 2026-09-20/21, now confirmed to recur for the identical specific claims across multiple nights. A broad set of independent checks came back clean (all 11 JOURNAL-cited lane merges plus one filed row, 6 living-doc factual cross-checks, and 4 BACKLOG closure-coherence checks — a supersession, an id-renumber, three row-body archivals, and a duplicate-filing delete, all internally coherent), so this remains narrow, named, persistent drift rather than systemic rot.

The more consequential finding for the record remains procedural, now compounding for a fifth night: `origin/claude/conformance-2026-09-18` through `-21` are all still unmerged, the same `[#426]` operator-consumption gap first named on 2026-08-10 (still OPEN per `BACKLOG.md:498` / `tasks/426-*.md` — its Done-when explicitly requires a queue-depth detector for exactly this branch count, which does not yet exist). Every finding in all four unmerged digests — including all 3 HIGH-severity items above — remains invisible to anyone who reads only `main`. This run's own branch will be the fifth to join that queue once pushed.

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 9 · **Survived skeptic:** 9 · **Killed false positives:** 0
**Plus 2 findings carried forward from the 2026-08-10/2026-09-19/2026-09-20/2026-09-21 baselines that were not independently re-derived by tonight's own fan-out** (the `[#780]` SHA-citation error and the ADR-77 self-contradiction and stale `verify:`-count are grouped under their prior severities below; each was independently re-verified above with fresh evidence)

### High (3)

**PERSISTING — carried since ≥2026-09-18 (day 5), tonight split into 2 precise sub-claims** — `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` lane-a retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members ... it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-18`
- **Evidence:** `grep -n -A5 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py` → `CANONICAL_MANDATORY = (ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)`, VISION nowhere in it (`ARCHITECTURE` is actually `[0]`); `grep -n -A15 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml` → `tier: {hub: SHOULD, consumer: SHOULD}`, reason field states the 2026-08-31 demotion and that "tracked in all nine members" "was REFUTED by the same re-measurement — it is tracked in eight; terminal-setup has never had one."
- **Verdict:** contradicted
- **Proposed fix:** Rewrite VISION.md's header paragraph in one pass to state its actual current tier (SHOULD/SHOULD, retired from MUST 2026-08-31 by `[#614]` lane-a, tracked in eight of nine members) instead of the pre-retirement MUST/`CANONICAL_MANDATORY[0]`/all-nine claim.
- **Note:** Unchanged for a 5th consecutive night. `VISION.md`'s own `last_reviewed: 2026-08-29` predates the 2026-08-31 retirement that falsifies it, so this is genuine unreconciled drift, not a documented-decision carve-out.

**PERSISTING — carried since ≥2026-09-19 (day 4)** — `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; it is currently report-only
- **Claim:** "`uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks." (`CLAUDE.md:65`); "lint (also a pre-commit gate)" (`AGENTS.md:66`)
- **Location:** `CLAUDE.md:65`; `AGENTS.md:66`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, comment "NOT RE-ARMED 2026-09-18 (B2 lane4 hook-role review) ... Left manual; flagged as a B3+ candidate."
- **Verdict:** contradicted
- **Proposed fix:** Reword both to state `ruff` is currently `stages: [manual]` / report-only via the Actions conductor job, matching `CLAUDE.md`'s own §9 roster which already gets this right.
- **Note:** Also an internal self-contradiction within `CLAUDE.md` alone (§4 vs §9). Tonight's V2 fan-out independently re-derived the `CLAUDE.md:65` half only; `AGENTS.md:66` re-verified directly.

**PERSISTING — carried since ≥2026-09-20 (day 3)** — `CONTRIBUTING.md:170`'s Validators table row lists `ruff` as a blocking commit-stage gate
- **Claim:** "| `ruff` | commit | Lint gate ... Blocks on violations. [#13] closed. |"
- **Location:** `CONTRIBUTING.md:170`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`; `CONTRIBUTING.md`'s frontmatter stamps `last_reviewed: 2026-09-10`, seven days before the 2026-09-17 "commit gate stripped" change, never reconciled afterward.
- **Verdict:** contradicted
- **Proposed fix:** Re-reconcile `CONTRIBUTING.md`'s hook table against the current `.pre-commit-config.yaml` (post 2026-09-17 strip) and bump `last_reviewed` past that date.
- **Note:** Same underlying drift as the `CLAUDE.md`/`AGENTS.md` ruff finding above and the MED/LOW findings below (same table, different rows) — a single combined re-read of `CLAUDE.md`, `AGENTS.md`, and `CONTRIBUTING.md` would close all of them in one pass.

### Med (2)

**PERSISTING — carried since ≥2026-09-21 (day 2), not independently re-derived tonight** — `[#780]`'s closure evidence and the 2026-09-16 closure census cite the wrong proving commit for lane z-11's three-repo comparison
- **Claim:** "Three-repo comparison: a gap matrix, adopt-candidates, and an explicit will-NOT-adopt list" was closed 2026-09-16 with evidence commit `5f270cd9`.
- **Location:** `tasks/780-three-repo-comparison-gaps-adopt-candidates-and-an-explicit-will-not-adopt-list.md:12`; `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25`
- **Evidence:** `git log -1 --format='%H %s' 5f270cd9` → `chore(lane): step-2 sync -- merge main into the z-4 lane for the anchor gate [#772]` (an unrelated lane's sync-merge); `git log -1 --format='%H %s' b81c554` → `Merge branch 'lane-z-11' @ f304a76c -- three-repo comparison: 4 intakes, 7 recorded refusals...` (the actual work).
- **Verdict:** unsupported
- **Proposed fix:** Repoint `[#780]`'s "CLOSED ... evidence" line and the census's Table 1 row from `5f270cd9` to `b81c554` (or the specific authoring commits `87b3670`/`1a57a77`).
- **Note:** Tonight's V3 fan-out raised 0 findings — a verifier-coverage gap, since this is a citation-pointing error rather than a Done-when/diff mismatch, distinct from V3's usual closure-coherence checks. Re-verified directly; unchanged since first flagged 2026-09-21.

**PERSISTING — carried since ≥2026-09-20 (day 3), tonight re-derived 2 of 5 rows** — `CONTRIBUTING.md`'s Validators table lists five manual hooks as blocking commit-stage gates
- **Claim:** `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, and `audit-health` are all listed with Stage=`commit`.
- **Location:** `CONTRIBUTING.md:159,161,167,168,169`
- **Evidence:** `grep -n -A3 'id: audit-health' .pre-commit-config.yaml` → `stages: [manual]` (tonight's V2, MED, `CONTRIBUTING.md:169`); `grep -n -A3 'id: validate-backlog' .pre-commit-config.yaml` → `stages: [manual]` (tonight's V2, LOW, `CONTRIBUTING.md:168`); the remaining three (`normalize-dated-headers` line 159, `toc-freshness-playbook` line 161, `check-seal-identity` line 167) re-verified directly — all `stages: [manual]` with the same 2026-09-17 "MOVED to the Actions conductor" comment, not re-raised by tonight's fan-out.
- **Verdict:** contradicted
- **Proposed fix:** Same fix as the `ruff` row above — regenerate/reconcile the table's Stage column from the live config in one pass; consider generating the table instead of hand-maintaining it, per the repo's own "never restate a computed surface in prose" convention.
- **Note:** Same root cause as the HIGH `ruff`-row finding, distinct table cells. `audit-health` kept at MED (contradicts `ARCHITECTURE.md`'s already-reconciled text on the same fact); the other four rows kept at LOW (comparatively lower-stakes hooks, same fix).

### Low (6)

**PERSISTING — carried since ≥2026-08-10 (43 days), tonight's skeptic revised severity MED→LOW** — the CLAUDE.md/AGENTS.md split's byte-count justification is stale
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — stated as present-tense fact.
- **Location:** `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`, `templates/claude-regions/antipatterns-universal.md:4`
- **Evidence:** `wc -c CLAUDE.md AGENTS.md` → CLAUDE.md=23,651 B, AGENTS.md=5,843 B — a wholesale copy today would land at ~29.0 KiB, comfortably under the 32 KiB cap, contradicting the stated 43.50 KiB/truncates-silently claim.
- **Verdict:** contradicted
- **Proposed fix:** Attribute the number to its source measurement (ADR-115 decision packet, 2026-08-22, when CLAUDE.md was much larger) instead of stating it as a current fact, or re-measure and update all four occurrences together.
- **Note:** Longest-running item in this digest's tracked history — present since 2026-08-10, now 43 days. Tonight's V2 fan-out independently re-derived it (unlike most prior nights, where it fell into the AGENTS.md/templates verifier-coverage gap) and its skeptic downgraded severity from MED to LOW, reasoning the underlying anti-pattern rule's intent is unaffected — only its illustrative figure is stale.

**PERSISTING — carried since ≥2026-09-19 (day 4), not independently re-derived tonight** — `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status
- **Claim:** `CLAUDE.md:80` (§4): "the ADR-77 guard stays armed" vs. `CLAUDE.md:194` (§9): "the ADR-77 guard stays off ([#863])."
- **Location:** `CLAUDE.md:80` vs `CLAUDE.md:194`
- **Evidence:** `grep -n -i 'ADR-77' CLAUDE.md` → both lines present verbatim, unchanged, at the same line numbers as prior nights.
- **Verdict:** contradicted
- **Proposed fix:** Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," matching §9 and the live `.claude/settings.json` emergency-disable entry.
- **Note:** Plain internal self-contradiction within one file, unresolved for a 4th night; §9 is already correct, only §4 needs the fix. Not independently re-derived by tonight's V2 fan-out; re-verified directly.

**PERSISTING — carried since ≥2026-09-20 (day 3), tonight's skeptic kept prior LOW severity** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine."
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `grep -l 'VISION\.md:' deploy/manifest-v*.yaml | wc -l` → 6 deploy manifests carry a `VISION.md:` key, not 5; `scripts/canonical_docs.py`'s own docstring enumerates "the ten machine constants," not thirteen.
- **Verdict:** contradicted
- **Proposed fix:** Update the counts to six manifests / ten machine constants, or drop the hardcoded numbers per the repo's own "never restate a count in prose" convention.
- **Note:** Same paragraph as the HIGH VISION.md finding above; one re-read closes both. Not raised by tonight's V2 fan-out; re-verified directly.

**PERSISTING — carried since ≥2026-09-18 (day 5), tonight re-derived** — `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)."
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B — same 129 B gap measured since 2026-09-19; `git log --oneline -- AGENTS.md` shows only the initial-add commit, so the figure was mismeasured at authoring time rather than having drifted.
- **Verdict:** contradicted
- **Proposed fix:** Correct the byte figure to the current measured value, or drop the hardcoded count.
- **Note:** Five nights unchanged. Tonight's V2 fan-out independently re-derived this.

**PERSISTING — carried since ≥2026-09-20 (day 3), not independently re-derived tonight** — `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale
- **Claim:** "`git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES)."
- **Location:** `CLAUDE.md:102` (Critical rules, item 7)
- **Evidence:** `grep -c '^- verify:' .claude/rules/git-discipline.md` → 5 matches, not 3.
- **Verdict:** contradicted
- **Proposed fix:** Change "three" to "five", or drop the exact count per the repo's own no-restated-counts convention.
- **Note:** Unfixed since first flagged 2026-09-20. Not independently re-derived by tonight's V2 fan-out; re-verified directly.

**PERSISTING — carried since ≥2026-09-20 (day 3), tonight re-derived, unchanged severity** — `ARCHITECTURE.md`'s size-target note is stale
- **Claim:** "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB" reads as a live target still governing the file's size.
- **Location:** `ARCHITECTURE.md:17`
- **Evidence:** `wc -c ARCHITECTURE.md` → 23,849 B — the identical figure measured on 2026-09-20 and 2026-09-21, i.e. the file has not changed size at all in three nights, still ~55% over the stated ≤15 KB target; `grep -n '_FILE_SIZE_BUDGETS' scripts/validate_doc_rot.py` → no entry for `ARCHITECTURE.md`.
- **Verdict:** omitted
- **Proposed fix:** Either drop the numeric target (nothing enforces it) or update the note to record that the file has stabilized well past it, and consider adding it to `validate_doc_rot._FILE_SIZE_BUDGETS` the way `CLAUDE.md` already is.
- **Note:** Third night this exact byte count has been measured — file is stable, just the header note is stale. Tonight's skeptic kept severity at LOW, reasoning that since no gate enforces `ARCHITECTURE.md`'s size, nothing is silently failing — but a live doc still asserts a number the repo no longer matches.

---

## Killed Findings

None. All 9 findings raised by tonight's V1/V2/V3 fan-out survived adversarial skeptic review (0% kill rate this cycle).

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries, 2026-09-20(e) through 2026-09-21(n)):**
- All 11 merge/lane entries (LANE-L6, L7, L8-batch, W3-A through W3-F, plus row `#936`'s filing) corroborate exactly against git history — merge commit hashes, anchor SHAs, audit-doc paths, and a precise code locator (`scripts/preflight_contract.py:371`) all match ✓
- HEAD (`df0c1ac`) matches both `origin/main` and the newest JOURNAL entry's own anchor — nothing merged/pushed postdates the JOURNAL ✓
- History is not shallow over this window — git log runs 298 commits back past all cited JOURNAL entries ✓

**V2 (living-doc factual claims):**
- `ARCHITECTURE.md`'s quality-requirements block ("29 requirement(s), 8 measured, 21 candidate") matches `ecosystem/quality-requirements.yaml` exactly (verified via YAML parse) ✓
- `ARCHITECTURE.md` Ch2's "35 rows vs the index's 8 classes" — `ecosystem/organ-index.md` has exactly 8 `## ` class headings ✓
- `CLAUDE.md` §9's "B2 lane4 armed 13 (counter+expiry)" — exactly 13 hooks carry the matching re-armed comment in `.pre-commit-config.yaml` ✓
- `docs/audits/2026-09-18-technical-b2-lane4-hook-role-review.md` (cited by `CLAUDE.md` §9) exists on disk ✓
- `CLAUDE.md` §11's ADR-116..120 roster matches the actual highest-numbered files in `docs/decisions/` ✓
- `CLAUDE.md`'s current byte size (23,651 B) is under its own stated ≤24,576 B cap ✓

**V3 (BACKLOG closure semantic coherence):**
- `[#782]` removed from `BACKLOG.md` (commit `750f3fb`, 2026-09-15) is a declared non-discharging supersession by `[#765]`, not a claimed completion — commit body states "closed would be a lie here" ✓
- `[#746]` disappearance is a same-diff id-renumber to `[#747]` (commit `20684e6`), resolving a duplicate-id collision, not a closure ✓
- `tasks/archive/*.md` adds (commits `0c56a7c`, `a82e142`, `a86354f`) are row-body-archival relocations (`record: row-body-archival` frontmatter) — the rows themselves remain open ✓
- The only non-archive `tasks/` deletion in the window (`929`, commit `1db485b`) is a stated duplicate-filing cleanup, not a work closure ✓

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, now 5 nights running)** Absorb the queue of unmerged `claude/conformance-*` branches — `2026-09-18`, `2026-09-19`, `2026-09-20`, `2026-09-21`, and this run's `2026-09-22`. This is the same `[#426]` operator-consumption gap named on 2026-08-10 (`BACKLOG.md:498`, still OPEN — its Done-when explicitly calls for a queue-depth detector, which does not yet exist); every finding in all five unmerged digests, including all 3 HIGH items in this one, is currently invisible to anyone reading only `main`.
2. **HIGH — persisting, day 5** — Re-read `docs/archive/VISION.md:16-19` end-to-end: fix the `CANONICAL_RETIRED` status claim and the machine-site/manifest counts in one pass (closes one HIGH + one LOW below).
3. **HIGH — persisting, day 3/4, plus 1 MED + 4 LOW sub-findings** — Correct `CLAUDE.md:65`, `AGENTS.md:66`, and `CONTRIBUTING.md`'s full Validators table (the `ruff` row at line 170 plus five more rows at 159,161,167,168,169) together in one pass: all describe now-manual hooks as local commit-blocking gates. Bump `CONTRIBUTING.md`'s `last_reviewed` past 2026-09-17 once fixed.
4. **MED — persisting, day 2** — Repoint `[#780]`'s closure-evidence line and the 2026-09-16 census's Table 1 row from `5f270cd9` to `b81c554` (or the authoring commits `87b3670`/`1a57a77`).
5. **LOW — persisting, 43 days, severity revised down** — Re-measure or attribute-to-source the "43.50 KiB / 32 KiB cap" byte-count claim across `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `templates/claude-regions/antipatterns-universal.md`.
6. **LOW — persisting, day 4** — Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," resolving the self-contradiction with `CLAUDE.md:194`.
7. **LOW — persisting, day 3** — Correct `VISION.md:18-19`'s stale counts (six manifests / ten machine constants, not five/thirteen). Same re-read as item 2.
8. **LOW — persisting, day 3** — Correct `CLAUDE.md` §5 rule 7's "three `verify:` lines" to five, or drop the exact count.
9. **LOW — persisting, day 3** — Reconcile `ARCHITECTURE.md`'s stale ≤15 KB size-target note (file stable at 23,849 B for 3 nights running) — either drop the target or add `ARCHITECTURE.md` to `validate_doc_rot._FILE_SIZE_BUDGETS`.
10. **(INFRASTRUCTURE, persisting since ≥2026-08-02, now 51 days unresolved)** Cloud runtime `uv` (`0.8.17`) still cannot reach the pinned `0.11.19` release. Fires on every Stop-hook check.

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-22-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
