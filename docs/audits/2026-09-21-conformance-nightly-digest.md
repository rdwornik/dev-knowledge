<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-21

**Date:** 2026-09-21
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded**, fourth consecutive clean run (2026-09-18 through 2026-09-20 also ran to completion). `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`) per the re-probe instruction and ran to completion in one pass — no spec-orchestration fallback needed.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 101,548 | 15 | 130s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 151,153 | 44 | 321s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 137,115 | 58 | 373s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 85,790 | 17 | 207s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 53,195 | 1 | 37s |

Total: 528,801 subagent tokens, 135 tool calls, ~751s (12.5 min) wall time.

**Model-pin note (script vs. meta, informational, unchanged since 2026-09-18):** `conformance-hub.js`'s `meta.phases` describes Stage 2 ("skeptic") and Stage 3 ("digest") as intended for Opus, but neither `agent()` call in the script body passes an explicit `model` for those two stages (only Stage 1's three calls pin `model: 'claude-sonnet-5'`). Tonight, as on every prior successful run, both unpinned stages ran on `claude-sonnet-5` by default. Not a doc-conformance finding (it's the workflow script's own behavior, not the target repo's docs) — flagged for the platform record since the meta description and actual behavior still diverge.

**Harness safety-neutralization fired twice (non-incident, same class as 2026-09-19/20).** `[harness: subagent output matched instruction-shaped pattern(s): settings-json. Control tags below are neutralized...]` fired on the V2 and digest-synthesis outputs — the same recurring trigger: `.claude/settings.json` carries operator-authored keys/comments (e.g. `//pretooluse-deny-and-point-UNWIRED-2026-09-18`) that read as imperative instructions when quoted verbatim inside a verifier's structured-output string fields. This is the repo's own tracked configuration being cited as evidence, not an external or adversarial injection — no verifier's behavior was redirected.

**Known-advisory infra note (unrelated to doc conformance):** the session's Stop-hook backpressure fired on every turn boundary throughout this run with `Required uv version ==0.11.19 does not match the running version 0.8.17`. Same systemic mismatch flagged since the 2026-08-10 digest's Next Actions #7 — this cloud runtime cannot reach the pinned `uv` release at all (`uv self update 0.11.19` fails with "version not found"). Now **50 days unresolved** (2026-08-02 → 2026-09-21). Advisory-only per `CLAUDE.md` §9 — not a doc-conformance finding.

**Recurring killed-finding pattern, worth a platform note:** for the second consecutive night, V3 raised a "16-of-25 proving-SHA citations in the 2026-09-16 closure census don't resolve as git objects" claim, and the skeptic killed it both times for the same reason — a shallow-clone SHA-resolution false-negative the repo's own history already names (intake `#95`, discovered by lane z-11). The claim and its kill are byte-for-byte the same shape as 2026-09-20's. Not itself a doc-conformance finding, but if this keeps recurring nightly it may be worth teaching V3's prompt the shallow-clone guard V1 already carries, so the same non-finding doesn't keep consuming Stage 2 budget.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-09-20-conformance-nightly-digest.md`, fetched read-only from the **unmerged** branch `origin/claude/conformance-2026-09-20` (`git show origin/claude/conformance-2026-09-20:docs/audits/2026-09-20-conformance-nightly-digest.md`). No `docs/audits/*-conformance-nightly-digest.md` file exists on `main` more recent than 2026-08-10 — `origin/claude/conformance-2026-09-18`, `-19`, and `-20` are all still unmerged (verified fresh this run via `git merge-base --is-ancestor origin/claude/conformance-2026-09-{18,19,20} origin/main` → `NO` for all three). This is now the **fourth** consecutive night in this state.
**Gap:** 1 day (2026-09-20 → 2026-09-21).

All 9 survivors from the 2026-09-20 digest's own Findings section were independently re-checked against current `origin/main` head (`71be4ac`) with fresh evidence — 5 of the 9 were independently re-derived by tonight's own V1/V2/V3 fan-out; the other 4 (the 43.50 KiB byte-count item, the ADR-77 self-contradiction, `CONTRIBUTING.md:19`'s stale `AGENTS.md` byte figure, and `CLAUDE.md` §5 rule 7's stale `verify:`-line count) were not independently re-derived by tonight's verifiers — a verifier-coverage gap, same pattern the 2026-09-20 digest itself noted for the VISION.md manifest-count claim — so they were re-verified directly with fresh `grep`/`wc` commands instead, not re-run through tonight's skeptic pipeline:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING** | HIGH: `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` lane-a retired 2026-08-31 | Tonight's own V2 fan-out independently re-derived this, citing the same `ecosystem/parity-surfaces.yaml` retirement comment and `scripts/canonical_docs.py`'s `CANONICAL_RETIRED = (VISION,)` tuple. Unchanged text, now day 4. |
| **PERSISTING** | HIGH: `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; still `stages: [manual]` | `grep -n "ruff check" CLAUDE.md AGENTS.md` → both lines unchanged verbatim. Tonight's V2 fan-out independently re-derived the `CLAUDE.md:65` half; `AGENTS.md:66` re-verified directly (not in V2's declared scan list). |
| **PERSISTING** | HIGH: `CONTRIBUTING.md`'s Validators table still describes now-manual hooks as commit-time blocking gates | Tonight's V2 fan-out independently re-derived this, now split into two precise sub-findings: the `ruff` row (`CONTRIBUTING.md:170`, HIGH) and five more rows — `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `audit-health` (`CONTRIBUTING.md:159,161,167-169`, MED). Same underlying drift, same file, unreconciled since the 2026-09-17 commit-gate strip. |
| **PERSISTING** | MED (carried since ≥2026-08-10, 41+ days at last count): the 43.50 KiB CLAUDE.md/AGENTS.md byte-count justification | `grep -rn "43.50 KiB" CLAUDE.md AGENTS.md CONTRIBUTING.md templates/claude-regions/antipatterns-universal.md` → all 4 occurrences unchanged; `wc -c CLAUDE.md AGENTS.md` → 23,651 B + 5,843 B = 29,494 B, still nowhere near 43.50 KiB. Not independently re-derived by tonight's V2 fan-out (a verifier-coverage gap — V2's declared scan list is VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING and this claim also lives in `AGENTS.md` and a `templates/` file); directly re-verified instead. Now **42 days** unresolved (2026-08-10 → 2026-09-21). |
| **PERSISTING** | MED: `CLAUDE.md` self-contradicts on the ADR-77 guard (§4 line 80 "stays armed" vs §9 line 194 "stays off ([#863])") | `grep -n -i "ADR-77" CLAUDE.md` → both lines present verbatim at the same line numbers, contradiction unresolved. Not independently re-derived by tonight's V2 fan-out; directly re-verified. |
| **PERSISTING** | MED→**severity revised to LOW by tonight's skeptic**: `docs/archive/VISION.md:18-19` overstates its own machine-site footprint ("thirteen machine constants plus five deploy manifests") | Tonight's V2 fan-out independently re-derived this against current counts: 6 deploy manifests carry a `VISION.md:` key (not 5), and `scripts/canonical_docs.py`'s own docstring enumerates "the ten machine constants" (not thirteen). Both numbers in the sentence are wrong. Tonight's skeptic kept it but reclassified severity MED→LOW; not re-litigated here, just noted as a severity change on an unchanged claim. |
| **PERSISTING** | LOW: `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count (5,714 B) | `grep -n "5,714\|5,843" CONTRIBUTING.md` → line 19 still states 5,714 B; `wc -c AGENTS.md` → 5,843 B, same 129 B gap measured on 2026-09-19/20. Not independently re-derived by tonight's V2 fan-out; directly re-verified. |
| **PERSISTING** | LOW: `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale | `grep -c "^- verify:" .claude/rules/git-discipline.md` → 5, not 3; `CLAUDE.md:102` still reads "carries three `verify:` lines." Not independently re-derived by tonight's V2 fan-out; directly re-verified — still unfixed since first flagged 2026-09-20. |
| **PERSISTING** | LOW: `ARCHITECTURE.md`'s BUILD MODE header states an unqualified ≤15 KB size target the file no longer meets | Tonight's V2 fan-out independently re-derived this: `wc -c ARCHITECTURE.md` → 23,849 B, the exact same figure as 2026-09-20's measurement — the file has not moved at all in either direction since then. Still 59% over the stated target, still no enforcing gate. |

**NEW this cycle** (1 finding, survived the skeptic):

| Status | Finding | Severity |
|---|---|---|
| **NEW** | `tasks/780-*.md` and the 2026-09-16 closure census (`docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25`) both cite commit `5f270cd9` as the "proving SHA" for lane z-11's three-repo-comparison deliverables; `5f270cd9` is actually an unrelated lane's sync-merge (`chore(lane): step-2 sync ... for the anchor gate [#772]`) — the real merge is `b81c554`, authored by `87b3670` (gap matrix) and `1a57a77` (both lists) | MED |

**Delta counts:** 0 resolved · 9 persisting · 1 new
**This run's own raw → survived → killed:** 8 → 7 → 1 (from tonight's V1/V2/V3 fan-out through the skeptic; the 4 carried items not independently re-derived tonight are additional and not counted in this ratio, matching the convention the 2026-08-10 and 2026-09-20 digests both used)
**Skeptic kill-rate:** 12.5% (1 of 8) — the kill was a genuine, evidence-grounded correction: a shallow-clone SHA-resolution false-negative the repo's own history already names via intake `#95` (see Run section above — this is the second consecutive night the identical claim shape was raised and killed for the identical reason).

---

## Summary

Doc health this cycle shows **zero resolutions and one new finding** against an unusually stable baseline: all 9 survivors carried from the 2026-09-20 digest are still live on `origin/main`, byte-for-byte unchanged in every case that was directly re-checked (including `ARCHITECTURE.md`'s exact byte count, which has not moved since 2026-09-20 in either direction). None of the 9 widened or narrowed in scope; the only change within a carried item is a severity reclassification (VISION.md's stale machine-constant/manifest counts, MED→LOW per tonight's skeptic) on an otherwise-unchanged claim. The one new item (`[#780]`'s wrong proving-SHA citation) is fully verifiable in this non-shallow clone and distinct in kind from the recurring shallow-clone-artifact class of killed finding — it is a real citation-pointing error, not a fabrication or an unresolvable-in-this-clone symptom.

The concentration of drift remains exactly where the last several nights placed it: (1) the 2026-09-17 pre-commit-gate strip to `stages: [manual]` still hasn't propagated into `CLAUDE.md` §4, `AGENTS.md`, or `CONTRIBUTING.md`'s Validators table, now expressed as 3 HIGH + 1 MED finding across those files; (2) VISION.md's 2026-08-31 retirement from MUST/`CANONICAL_MANDATORY` to SHOULD/`CANONICAL_RETIRED` still isn't reflected in the file's own header prose, alongside two stale restated counts in the same paragraph; and (3) three small, independent numeric-drift items (the 43.50 KiB byte-count claim, the ADR-77 self-contradiction, `CONTRIBUTING.md:19`'s byte figure, and `CLAUDE.md`'s stale `verify:`-count) none of which tonight's V2 fan-out happened to re-derive on its own — the same verifier-coverage-gap pattern noted on 2026-09-20, now confirmed to recur across multiple nights for the same specific claims. A broad set of independent checks came back clean (all 37 JOURNAL-cited commit SHAs, ~20 living-doc factual claims, 7 of the 9 sampled BACKLOG closures' Done-when-vs-commit match), so this remains narrow, named, persistent drift rather than systemic rot.

The more consequential finding for the record remains procedural, now compounding: this is the **fourth consecutive night** whose digest sits on an unmerged `claude/conformance-<date>` branch (`2026-09-18`, `-19`, `-20`, and this run's `-21`), the same [#426] operator-consumption gap first named on 2026-08-10. Every finding in all four unmerged digests — including all 3 HIGH-severity items above — remains invisible to anyone who reads only `main`.

<!-- counts: raw=8 survived=7 killed=1 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 8 · **Survived skeptic:** 7 · **Killed false positives:** 1
**Plus 4 persisting findings carried forward from the 2026-08-10/2026-09-19/2026-09-20 baselines (independently re-verified above with fresh evidence, not run through tonight's skeptic pipeline since tonight's fan-out did not happen to re-scan those specific claims)**

### High (3)

**PERSISTING — carried since ≥2026-09-18 (day 4)** — `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members ... it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-18`
- **Evidence:** `grep -n 'canonical-doc-vision' -A12 ecosystem/parity-surfaces.yaml; grep -n 'CANONICAL_MANDATORY\|CANONICAL_RETIRED' -A3 scripts/canonical_docs.py` → `ecosystem/parity-surfaces.yaml`'s `canonical-doc-vision` row reads `tier: {hub: SHOULD, consumer: SHOULD}` with an explicit "RETIRED FROM MUST, 2026-08-31, by [#614] lane-a" comment; `scripts/canonical_docs.py`'s `CANONICAL_MANDATORY` tuple no longer includes VISION, which now lives in a separate `CANONICAL_RETIRED = (VISION,)` tuple.
- **Verdict:** contradicted
- **Proposed fix:** Rewrite VISION.md's header paragraph to state its actual current tier (SHOULD/SHOULD, retired from MUST 2026-08-31 by `[#614]` lane-a) instead of the pre-retirement MUST/`CANONICAL_MANDATORY` claim.
- **Note:** Unchanged for a 4th consecutive night; the retirement decision itself created this doc-rot and nothing has closed the loop back to VISION.md's own prose.

**PERSISTING — carried since ≥2026-09-19 (day 3)** — `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; it is currently report-only
- **Claim:** "`uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks." (`CLAUDE.md:65`); "lint (also a pre-commit gate)" (`AGENTS.md:66`)
- **Location:** `CLAUDE.md:65`; `AGENTS.md:66`
- **Evidence:** `grep -n -A10 '^      - id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, comment "NOT RE-ARMED 2026-09-18 (B2 lane4 hook-role review) ... Left manual; flagged as a B3+ candidate."
- **Verdict:** contradicted
- **Proposed fix:** Reword both to state `ruff` is currently `stages: [manual]` / report-only via the Actions conductor job `commit-gate`, matching `CLAUDE.md`'s own §9 roster which already gets this right.
- **Note:** Also an internal self-contradiction within `CLAUDE.md` alone (§4 vs §9), not just staleness against the live config.

**PERSISTING — carried since ≥2026-09-20 (day 2), now split into a precise sub-finding** — `CONTRIBUTING.md:170`'s Validators table row lists `ruff` as a blocking commit-stage gate
- **Claim:** "| `ruff` | commit | Lint gate ... Blocks on violations. [#13] closed. |"
- **Location:** `CONTRIBUTING.md:170`
- **Evidence:** `grep -n -A10 '^      - id: ruff$' .pre-commit-config.yaml; sed -n '1,6p' CONTRIBUTING.md` → `ruff`'s live stage is `[manual]`, not `commit`; `CONTRIBUTING.md`'s frontmatter stamps `last_reviewed: 2026-09-10`, seven days before the 2026-09-17 "commit gate stripped" change, and was never reconciled afterward.
- **Verdict:** contradicted
- **Proposed fix:** Re-reconcile `CONTRIBUTING.md`'s hook table against the current `.pre-commit-config.yaml` (post 2026-09-17 strip) and bump `last_reviewed` past that date.
- **Note:** Same underlying drift as the `CLAUDE.md`/`AGENTS.md` ruff finding above — a combined re-read of all three files, plus the MED finding below (same table, different rows), would close all four in one pass.

### Med (4)

**NEW** — `[#780]`'s closure evidence and the 2026-09-16 closure census cite the wrong proving commit for lane z-11's three-repo comparison
- **Claim:** "Three-repo comparison: a gap matrix, adopt-candidates, and an explicit will-NOT-adopt list" was closed 2026-09-16 with evidence commit `5f270cd9`.
- **Location:** `tasks/780-three-repo-comparison-gaps-adopt-candidates-and-an-explicit-will-not-adopt-list.md:12`; `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25`
- **Evidence:** `git log -1 --format='%H %s' 5f270cd9` → `chore(lane): step-2 sync -- merge main into the z-4 lane for the anchor gate [#772]` (an unrelated lane's sync-merge); `git log -1 --format='%H %s' b81c554` → `Merge branch lane-z-11 @ f304a76c -- three-repo comparison: 4 intakes, 7 recorded refusals...` (the actual work), authored by `87b3670` ("the gap matrix") and `1a57a77` ("both lists").
- **Verdict:** unsupported
- **Proposed fix:** Repoint `[#780]`'s "CLOSED ... evidence" line and the census's Table 1 row from `5f270cd9` to `b81c554` (or the specific authoring commits `87b3670`/`1a57a77`).
- **Note:** Skeptic confirmed both cited hashes resolve fine in this clone — this is a fully verifiable citation-pointing error, distinct in kind from the shallow-clone-artifact class of finding killed this same run (see Killed Findings).

**PERSISTING — carried since ≥2026-09-20 (day 2), now split into a precise sub-finding** — `CONTRIBUTING.md`'s Validators table lists five more manual hooks as blocking commit-stage gates
- **Claim:** `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, and `audit-health` are all listed with Stage=`commit`.
- **Location:** `CONTRIBUTING.md:159,161,167-169`
- **Evidence:** `grep -n -B1 -A3 '^      - id: audit-health$\|^      - id: validate-backlog$\|^      - id: check-seal-identity$\|^      - id: toc-freshness-playbook$\|^      - id: normalize-dated-headers$' .pre-commit-config.yaml` → all five are `stages: [manual]`, with the same 2026-09-17 "MOVED to the Actions conductor" comment.
- **Verdict:** contradicted
- **Proposed fix:** Same fix as the `ruff` row above — regenerate/reconcile the table's Stage column from the live config; consider generating the table instead of hand-maintaining it, per the repo's own "never restate a computed surface in prose" convention.
- **Note:** Same root cause as the HIGH `ruff`-row finding, distinct table cells.

**PERSISTING — carried since ≥2026-08-10 (42 days), not independently re-derived tonight** — the CLAUDE.md/AGENTS.md split's byte-count justification is stale
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — stated as present-tense fact.
- **Location:** `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`, `templates/claude-regions/antipatterns-universal.md:4`
- **Evidence:** `grep -rn "43.50 KiB" CLAUDE.md AGENTS.md CONTRIBUTING.md templates/claude-regions/antipatterns-universal.md` → all 4 occurrences unchanged; `wc -c CLAUDE.md AGENTS.md` → CLAUDE.md=23,651 B, AGENTS.md=5,843 B — a wholesale copy today would land at ~29.0 KiB, comfortably under the 32 KiB cap, contradicting the stated 43.50 KiB/truncates-silently claim.
- **Verdict:** contradicted
- **Proposed fix:** Attribute the number to its source measurement (pre-ADR-115-split, when CLAUDE.md alone was ~44 KB) instead of stating it as a current fact, or re-measure and update all four occurrences together.
- **Note:** Longest-running item in this digest's tracked history — present since 2026-08-10, carried through every run since, and not independently re-derived by tonight's V2 fan-out (its declared scan list is VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING; two of the four occurrences live in `AGENTS.md` and `templates/`) — re-verified directly instead. The repo's own conventions section warns "a number typed into a doc is stale at the next commit"; this is that failure, in four files, for 42 days.

**PERSISTING — carried since ≥2026-09-19 (day 3), not independently re-derived tonight** — `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status
- **Claim:** `CLAUDE.md:80` (§4): "the ADR-77 guard stays armed" vs. `CLAUDE.md:194` (§9): "the ADR-77 guard stays off ([#863])."
- **Location:** `CLAUDE.md:80` vs `CLAUDE.md:194`
- **Evidence:** `grep -n -i 'ADR-77' CLAUDE.md` → both lines present verbatim, unchanged, at the same line numbers as 2026-09-20.
- **Verdict:** contradicted
- **Proposed fix:** Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," matching §9 and the live `.claude/settings.json` emergency-disable entry.
- **Note:** Plain internal self-contradiction within one file, unresolved for a 3rd night; §9 is already correct, only §4 needs the fix. Not independently re-derived by tonight's V2 fan-out; re-verified directly.

### Low (4)

**PERSISTING — carried since ≥2026-09-20 (day 2), tonight's skeptic revised severity MED→LOW** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine."
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `grep -l 'VISION\.md:' deploy/manifest-v*.yaml | wc -l; sed -n '50,58p' scripts/canonical_docs.py` → 6 deploy manifests carry a `VISION.md:` key (v1.1.0 through v1.5.0), not 5; `scripts/canonical_docs.py`'s own docstring enumerates "the ten machine constants" (not thirteen).
- **Verdict:** contradicted
- **Proposed fix:** Update the counts to six manifests / ten machine constants, or drop the hardcoded numbers per the repo's own "never restate a count in prose" convention.
- **Note:** Same paragraph as the HIGH VISION.md finding above; one re-read closes both. Severity reclassified from MED (2026-09-20) to LOW by tonight's skeptic — the claim itself is unchanged.

**PERSISTING — carried since ≥2026-09-18 (day 4), not independently re-derived tonight** — `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)."
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `grep -n "5,714\|5,843" CONTRIBUTING.md` → line 19 unchanged; `wc -c AGENTS.md` → 5,843 B — same 129 B gap measured on 2026-09-19/20.
- **Verdict:** contradicted
- **Proposed fix:** Update the byte figure or drop the hardcoded count.
- **Note:** Four nights unchanged. Not independently re-derived by tonight's V2 fan-out; re-verified directly.

**PERSISTING — carried since ≥2026-09-20 (day 2), not independently re-derived tonight** — `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale
- **Claim:** "`git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES)."
- **Location:** `CLAUDE.md:102` (Critical rules, item 7)
- **Evidence:** `grep -c '^- verify:' .claude/rules/git-discipline.md` → 5 matches, not 3.
- **Verdict:** contradicted
- **Proposed fix:** Change "three" to "five", or drop the exact count per the repo's own no-restated-counts convention.
- **Note:** Unfixed since first flagged 2026-09-20. Not independently re-derived by tonight's V2 fan-out; re-verified directly.

**PERSISTING — carried since ≥2026-09-20 (day 2)** — `ARCHITECTURE.md`'s size-target note is stale
- **Claim:** "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB" reads as a live target still governing the file's size.
- **Location:** `ARCHITECTURE.md:17`
- **Evidence:** `wc -c ARCHITECTURE.md` → 23,849 B — the identical figure measured on 2026-09-20, i.e. the file has not changed size at all since then, still 59% over the stated ≤15 KB target; `grep -n '_FILE_SIZE_BUDGETS' scripts/validate_doc_rot.py` → no entry for ARCHITECTURE.md.
- **Verdict:** omitted
- **Proposed fix:** Either drop the numeric target (nothing enforces it) or update the note to record that the file has stabilized well past it, and consider adding it to `validate_doc_rot._FILE_SIZE_BUDGETS` the way `CLAUDE.md` already is.
- **Note:** Second night this exact byte count has been measured — file is stable, just the header note is stale.

---

## Killed Findings

**Killed (1 of 8 raw this cycle):**

- **Claim:** "The 2026-09-16 closure batch (commit `0c120be`) closed 25 rows 'with the proving SHAs below', but 16 of those 25 cited SHAs are not valid git objects in this repository, so the closure census's own proof mechanism is fabricated/unverifiable for the majority of the batch."
- **Kill reason:** documented-decision
- **Kill detail:** This clone is confirmed shallow, and the boundary includes `0c120be` itself as a grafted commit. Re-running `git cat-file -t` on the 16 flagged hashes reproduces "fatal: Not a valid object name" here, but the repo's own history already documents this exact symptom as a known shallow-clone false-negative, not proof of fabrication: commit `b81c554`'s own message (lane z-11's finding, filed as intake `#95`) states that a SHA outside a shallow clone's depth renders as "not present in this repo's object store" — 3,774 false refusals of 3,894 in one cloud session, the identical evidence-command pattern this finding used. Since 9 of the 25 cited SHAs in the same table resolve fine, a uniform-fabrication theory doesn't fit either. **This is the second consecutive night the identical claim shape was raised and killed for the identical reason** (see Run section, "Recurring killed-finding pattern" note above).

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries, 2026-09-19(at) through 2026-09-21(d)):**
- All 37 commit hashes cited as anchors across the window exist in git history with matching commit-message subjects ✓
- The 10 merge commits in range `bdd8dc1^..71be4ac` map one-to-one and in order to the 10 JOURNAL entries — no merged work is unmentioned, no entry lacks a corresponding merge ✓
- HEAD (`71be4ac`) matches both `origin/main` and the newest JOURNAL entry's own anchor — nothing merged/pushed postdates the JOURNAL ✓
- Every entry's precise file/insertion/deletion count claim reconciles exactly against `git diff --numstat` once each entry's own stated methodology (excluding merge-commit housekeeping regenerations) is applied — checked for all 6 lane entries plus the loop-eval entry ✓
- Files/tests cited as newly existing in the newest entries are present on disk (`tests/test_gate_scoping_926.py`, `scripts/audit_checks/check_substrate_declaration.py`, `tasks/916-*`/`926-*`/`928-*`, the full `docs/handoffs/2026-09-19-dev-knowledge-architect/` bundle) ✓
- No shallow-history concerns apply — local history extends back to 2026-09-15, and no cited SHA is close to that boundary ✓

**V2 (living-doc factual claims):**
- `CLAUDE.md`'s ≤24,576 B byte cap is enforced by `tests/test_claude_md_byte_cap.py`; file measures 23,651 B ✓
- `ecosystem/quality-requirements.yaml` counts (29 total, 8 measured, 21 candidate, v1.0.0) match `ARCHITECTURE.md`'s generated block exactly ✓
- `ecosystem/organ-index.md`'s "67 organs across 8 classes" / "git-hook 36" matches `ARCHITECTURE.md` Ch2 and an independent count of 36 hook ids ✓
- `CLAUDE.md` §9's "B2 lane4 armed 13 (counter+expiry)" matches the 2026-09-18 audit's own title and the live config's non-manual hook count ✓
- `CLAUDE.md` §11's ADR-116..120 statuses/dates match each ADR's frontmatter exactly, including the non-standard "Proposed <!-- DRAFT -->" wording ✓
- ADR-115 (Accepted, 2026-08-25) as cited by `CONTRIBUTING.md`/`CLAUDE.md` matches its own frontmatter ✓
- `CLAUDE.md` §7's 10-entry `commands-repo.md` roster exactly matches the 10 files under `.claude/commands/` ✓
- tier1-lifecycle plugin enabled plus `/review-closures` and `/ship` ship, per `.claude/settings.json` and the plugin's commands dir ✓
- `CLAUDE.md` §9's session-hooks and PreToolUse-UNWIRED claims match the live `.claude/settings.json` hooks block ✓
- `scripts/validate_hermetization.py`'s `SANCTIONED_TIER1_FILES` does admit `AGENTS.md`, as `CONTRIBUTING.md` claims ✓

**V3 (BACKLOG closure semantic coherence, 2026-09-16 closure batch, commit `0c120be`):**
- `[#743]`, `[#744]`, `[#750]`, `[#751]`, `[#752]`, `[#765]`, `[#785]` — Done-when criteria each match their cited proving commit exactly ✓
- `[#470]`, `[#591]`, `[#600]` — closed work independently confirmed present in the codebase even though their cited evidence hashes don't resolve in this shallow clone (treated as the known shallow-clone false-negative pattern per intake `#95`, not a live finding) ✓
- No new "done-work with zero backlog entry" was found in the ~3-week window: the only `tasks/*.md` deletions in that window are dedup/title-restore housekeeping, not silent closures ✓

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, now 4 nights running)** Absorb the queue of unmerged `claude/conformance-*` branches — `2026-09-18`, `2026-09-19`, `2026-09-20`, and this run's `2026-09-21`. This is the same `[#426]` operator-consumption gap named on 2026-08-10; every finding in all four unmerged digests, including all 3 HIGH items in this one, is currently invisible to anyone reading only `main`.
2. **HIGH — persisting, day 4** — Re-read `docs/archive/VISION.md:16-19` end-to-end: fix the `CANONICAL_RETIRED` status claim and the machine-site/manifest counts in one pass (closes one HIGH + one LOW below).
3. **HIGH — persisting, day 3, plus 1 MED sub-finding** — Correct `CLAUDE.md:65`, `AGENTS.md:66`, and `CONTRIBUTING.md`'s full Validators table (the `ruff` row at line 170 plus five more rows at 159,161,167-169) together: all describe now-manual hooks as local commit-blocking gates. Bump `CONTRIBUTING.md`'s `last_reviewed` past 2026-09-17 once fixed.
4. **MED — new** — Repoint `[#780]`'s closure-evidence line and the 2026-09-16 census's Table 1 row from `5f270cd9` to `b81c554` (or the authoring commits `87b3670`/`1a57a77`).
5. **MED — persisting, 42 days** — Re-measure or attribute-to-source the "43.50 KiB / 32 KiB cap" byte-count claim across `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `templates/claude-regions/antipatterns-universal.md` so all four stay consistent with the post-ADR-115-split reality.
6. **MED — persisting, day 3** — Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," resolving the self-contradiction with `CLAUDE.md:194`.
7. **LOW — persisting, day 2 (severity revised)** — Correct `VISION.md:18-19`'s stale counts (six manifests / ten machine constants, not five/thirteen), or drop them per the repo's own no-restated-counts rule. Same re-read as item 2.
8. **LOW — persisting, day 4** — Update `CONTRIBUTING.md:19`'s stale `AGENTS.md` byte figure (5,714 B → 5,843 B).
9. **LOW — persisting, day 2** — Correct `CLAUDE.md` §5 rule 7's "three `verify:` lines" to five, or drop the exact count.
10. **LOW — persisting, day 2** — Reconcile `ARCHITECTURE.md`'s stale ≤15 KB size-target note (file stable at 23,849 B for 2 nights running) — either drop the target or add `ARCHITECTURE.md` to `validate_doc_rot._FILE_SIZE_BUDGETS`.
11. **(INFRASTRUCTURE, persisting since ≥2026-08-02, now 50 days unresolved)** Cloud runtime `uv` (`0.8.17`) still cannot reach the pinned `0.11.19` release — `uv self update 0.11.19` fails with "version not found." Fires on every Stop-hook check.
12. **(PLATFORM, observational, recurring 2 nights)** V3's prompt does not carry the shallow-clone SHA-resolution guard V1's prompt already has; the same "16/25 proving SHAs don't resolve" claim was raised and killed for the identical reason on both 2026-09-20 and tonight. Teaching V3 the same guard would save Stage 2 skeptic budget without losing coverage (the underlying claim has never once survived).

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-21-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
