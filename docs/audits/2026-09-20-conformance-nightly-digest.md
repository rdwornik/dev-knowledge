<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-20

**Date:** 2026-09-20
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded**, third consecutive clean run (2026-09-18 and 2026-09-19 both ran to completion; before that, native was either unavailable or failed on a permission-handler bug — see 2026-08-10's digest). `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`) and ran to completion in one pass — no spec-orchestration fallback needed.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 88,636 | 12 | 88s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 149,363 | 29 | 312s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 118,781 | 24 | 228s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 80,925 | 26 | 160s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 51,923 | 1 | 37s |

Total: 489,628 subagent tokens, 92 tool calls, ~520s (8.7 min) wall time.

**Model-pin note (script vs. meta, informational):** `conformance-hub.js`'s `meta.phases` describes Stage 2 ("skeptic") and Stage 3 ("digest") as intended for Opus, but neither `agent()` call in the script body passes an explicit `model` for those two stages (only Stage 1's three calls pin `model: 'claude-sonnet-5'`). Tonight, as on 2026-09-18/19, both unpinned stages ran on `claude-sonnet-5` by default. Not a doc-conformance finding (it's the workflow script's own behavior, not the target repo's docs) — flagged for the platform record since the meta description and actual behavior diverge.

**Harness safety-neutralization fired twice (non-incident).** `[harness: subagent output matched instruction-shaped pattern(s): settings-json. Control tags below are neutralized...]` fired on the V2 and digest-synthesis outputs — same class of event the 2026-09-19 digest already investigated and cleared: `.claude/settings.json` carries operator-authored keys/comments (e.g. `//pretooluse-deny-and-point-UNWIRED-2026-09-18`, `still_off_not_restored_by_this_act`) that read as imperative instructions when quoted verbatim inside a verifier's structured-output string fields. This is the repo's own tracked configuration being cited as evidence, not an external or adversarial injection — no verifier's behavior was redirected. Flagged per this reviewer's standing instruction to surface suspected-injection-shaped content transparently.

**Known-advisory infra note (unrelated to doc conformance):** the session's Stop-hook backpressure fired on every turn boundary throughout this run with `Required uv version ==0.11.19 does not match the running version 0.8.17`. `uv self update 0.11.19` was attempted as a diagnostic and failed with `error: The version 0.11.19 was not found for the app uv in workspace uv` — this cloud runtime cannot currently reach that pinned release at all, not merely "hasn't been updated yet." Same systemic mismatch flagged since the 2026-08-10 digest's Next Actions #7, now **41+ days unresolved**. Advisory-only per `CLAUDE.md` §9 — not a doc-conformance finding.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-09-19-conformance-nightly-digest.md`, fetched read-only from the **unmerged** branch `origin/claude/conformance-2026-09-19` (`git show origin/claude/conformance-2026-09-19:docs/audits/2026-09-19-conformance-nightly-digest.md`). No `docs/audits/*-conformance-nightly-digest.md` file exists on `main` more recent than 2026-08-10 — `origin/claude/conformance-2026-09-18` and `origin/claude/conformance-2026-09-19` are both still unmerged (see Next Actions #1 — this is now the **third** consecutive night in this state). `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` remains excluded from baseline consideration for the same reason the 2026-09-19 digest gave: differently-scoped, no counts-marker contract.
**Gap:** 1 day (2026-09-19 → 2026-09-20).

All 6 open items carried in the 2026-09-19 digest's own delta narrative (3 formally written up plus 3 more named only in its delta table — see that digest's own internal gap, noted below) were independently re-checked against current `origin/main` head (`9be43b2`) with fresh evidence:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **RESOLVED** | prior HIGH (new 09-19): `ARCHITECTURE.md:17-24`'s BUILD MODE header claimed only 2 hooks ran locally post-cut, stale against the 2026-09-18 B2-lane4 re-arm | `sed -n '10,30p' ARCHITECTURE.md` → the box now reads "at the cut only four hooks ran locally; B2 lane 4 (2026-09-18) re-armed a subset. The live set is whatever in `.pre-commit-config.yaml` carries no `stages: [manual]` (roster: `CLAUDE.md` §9)" — accurate, and now points at the live source instead of hardcoding a count. Commit `02b2bca` ("re-read end-to-end and restamp 2026-09-19... correct stale hook-wiring claims") is the fix, landing the same day the 2026-09-19 digest ran. |
| **PERSISTING** | prior HIGH: `docs/archive/VISION.md:16-19` self-describes `CANONICAL_MANDATORY[0]` / MUST-tier; ADR-114 retired it to `CANONICAL_RETIRED` | `python3 -c "import sys; sys.path.insert(0,'scripts'); import canonical_docs as c; print(c.VISION in c.CANONICAL_MANDATORY, c.VISION in c.CANONICAL_RETIRED)"` → `False True`. Text at `VISION.md:16-18` unchanged verbatim. |
| **PERSISTING** | prior MED: `docs/archive/VISION.md:18-19` overstates its footprint ("thirteen machine constants plus five deploy manifests") | `sed -n '16,20p' docs/archive/VISION.md` → identical text, unchanged since 2026-09-18. Not independently re-derived this cycle (count not re-run); carried on direct text match. |
| **PERSISTING** | prior HIGH: `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff check` "is also a pre-commit gate ... and blocks" | `grep -n "ruff check" CLAUDE.md AGENTS.md` → both lines unchanged; `.pre-commit-config.yaml`'s `ruff` hook is still `stages: [manual]` with its "NOT RE-ARMED 2026-09-18" comment. Tonight's own independent V2 fan-out separately re-derived the same underlying drift via `CONTRIBUTING.md`'s Validators table (see NEW below) — same root cause, different file. |
| **PERSISTING** | prior MED: `CLAUDE.md` self-contradicts on the ADR-77 guard (§4 "stays armed" vs §9 "stays off ([#863])") | `grep -n "ADR-77" CLAUDE.md` → line 80 still "the ADR-77 guard stays armed"; line 194 still "the ADR-77 guard stays off ([#863])". Both lines present, contradiction unresolved. |
| **PERSISTING** | prior MED (carried since ≥2026-08-10 via the 2026-08-22 pre-ADR-115-split measurement): "43.50 KiB vs 32 KiB cap, truncates silently" byte-count justification | Tonight's own independent V1/V2/V3 fan-out re-derived this same claim fresh (see Findings below) — `wc -c CLAUDE.md AGENTS.md` → 23,651 + 5,843 = 29,494 B, still under the 32 KiB cap but nowhere near the stated 43.50 KiB figure. **Note on the 2026-09-19 digest:** that digest's own delta table listed this as "PERSISTING... not re-raised" but its formal "## Findings" section omitted a full write-up for it — an internal gap in that digest, not a resolution. It is written up in full below since tonight's fan-out re-surfaced it independently. |
| **PERSISTING** | prior LOW: `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count (5,714 B) | `grep -n "5,714" CONTRIBUTING.md` → still present, line 19; `wc -c AGENTS.md` → 5,843 B, same 129 B gap measured on 2026-09-19. |

**NEW this cycle** (3 findings, all survived the skeptic):

| Status | Finding | Severity |
|---|---|---|
| **NEW** | `CONTRIBUTING.md`'s Validators table (`last_reviewed: 2026-09-10`) still describes hooks like `ruff`, `audit-health`, `toc-freshness-playbook` as commit-time blocking gates ("Blocks on violations", "FAIL-level findings block the commit"); the 2026-09-17 operator ruling moved nearly all of them to `stages: [manual]` report-only, predating this table's own `last_reviewed` stamp | HIGH |
| **NEW** | `CLAUDE.md` §5 rule 7 states `git-discipline.md` "carries three `verify:` lines"; the file now has five | LOW |
| **NEW** | `ARCHITECTURE.md`'s box note "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB" reads as a live target; the file is now 23,849 B (55% over) and survived an end-to-end restamp (`02b2bca`, `last_reviewed=2026-09-19`) without reconciling this specific line, even though that same commit fixed the adjacent hook-wiring claim in the same box | LOW |

**Delta counts:** 1 resolved · 6 persisting · 3 new
**This run's own raw → survived → killed:** 6 → 4 → 2
**Skeptic kill-rate:** 33% (2 of 6) — both kills were genuine corrections, not weak-evidence calls: one a disclosed-and-tracked ADR-111 CLOSE-PRE gap ([#613]/[#829]), one an inconclusive shallow-clone SHA-resolution artifact the skeptic explicitly declined to treat as a confirmed contradiction (see Killed Findings).

---

## Summary

Doc health this cycle is a genuine mixed picture rather than pure accumulation: one item resolved (the 2026-09-19 digest's own top HIGH finding — `ARCHITECTURE.md`'s stale hook-wiring claim — was fixed the same day by commit `02b2bca`, which explicitly names that exact repair in its message), six items persist unchanged from the prior baseline, and three new items surfaced from tonight's independent fan-out. None of the six persisting items are freshly re-broken; all are the same unfixed drift the last one to three nightly runs already named. Two of the three new items live in the same paragraph/box as the just-resolved hook-wiring claim (`ARCHITECTURE.md`'s stale `≤15 KB` size target) or the same drift family as an already-persisting item (`CONTRIBUTING.md`'s Validators table vs. `CLAUDE.md`/`AGENTS.md`'s already-flagged `ruff` line) — both are "the same restamp fixed one claim in a box but not its neighbor" pattern, worth a single combined re-read rather than four separate edits. A broad set of independent checks — 10 JOURNAL entries against git, ~20 living-doc factual claims, 3 BACKLOG closures — came back clean, so the persisting drift is narrow and named, not systemic.

The more consequential finding for the record remains procedural: this is now the **third consecutive night** whose digest sits on an unmerged `claude/conformance-<date>-*` branch (`2026-09-18` and `2026-09-19` both still unabsorbed on origin, this run's `2026-09-20` will be the third), which is the exact operator-consumption gap [#426] already named on 2026-08-10 and re-flagged on 2026-09-19. Every finding in this digest, and in both of its unmerged predecessors, is currently invisible to anyone who reads only `main`.

<!-- counts: raw=6 survived=4 killed=2 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 6 · **Survived skeptic:** 4 · **Killed false positives:** 2
**Plus 6 persisting findings carried forward from the 2026-09-18/2026-09-19 runs (independently re-verified above with fresh evidence, not re-run through tonight's skeptic pipeline) and 1 resolution**

### High (3)

**PERSISTING — carried since ≥2026-09-18** — `docs/archive/VISION.md:16-19` self-describes a MUST-tier tracking status ADR-114 retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members ... it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-18`
- **Evidence:** `python3 -c "import sys; sys.path.insert(0,'scripts'); import canonical_docs as c; print(c.VISION in c.CANONICAL_MANDATORY, c.VISION in c.CANONICAL_RETIRED)"` → `False True`.
- **Verdict:** contradicted
- **Proposed fix:** Rewrite VISION.md's "why this file is still here" paragraph to state its actual current status (`CANONICAL_RETIRED`, per ADR-114) instead of its pre-ADR-114 status.
- **Note:** Unchanged since 2026-09-18 (two nights now). Same paragraph carries the persisting machine-site-footprint MED below; one re-read closes both.

**PERSISTING — carried since ≥2026-09-19** — `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; it is currently report-only
- **Claim:** "`uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks."
- **Location:** `CLAUDE.md:65`; `AGENTS.md:66`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, comment "NOT RE-ARMED 2026-09-18 (B2 lane4 hook-role review) ... Left manual; flagged as a B3+ candidate."
- **Verdict:** contradicted
- **Proposed fix:** Reword to state `ruff` is currently `stages: [manual]` / report-only via the Actions conductor, pending a B3+ re-arm decision.
- **Note:** Unchanged since 2026-09-19. Same underlying drift as the NEW `CONTRIBUTING.md` finding below — a combined re-read of all three files would close both.

**NEW** — `CONTRIBUTING.md`'s Validators table describes manual/report-only hooks as commit-time blocking gates
- **Claim:** The table lists `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `audit-health`, `ruff`, `coherence-nudge` (and others) as running at pre-commit stage "commit" and blocking — e.g. `ruff`: "Blocks on violations"; `audit-health`: "FAIL-level findings block the commit."
- **Location:** `CONTRIBUTING.md:159-171` (Validators section, `last_reviewed: 2026-09-10`)
- **Evidence:** `grep -n 'stages: \[manual\]' .pre-commit-config.yaml` → every one of those hooks is `stages: [manual]`; the `.pre-commit-config.yaml` header records a 2026-09-17 operator ruling that stripped them from the local commit stage in favor of report-only execution via `.github/workflows/conductor.yml` job `commit-gate`.
- **Verdict:** contradicted
- **Proposed fix:** Re-read `CONTRIBUTING.md`'s Validators table against `.pre-commit-config.yaml`'s current stages, mark the manual/report-only hooks accordingly, and bump `last_reviewed` past 2026-09-17.
- **Note:** Skeptic independently confirmed by reading `.pre-commit-config.yaml` directly; `CLAUDE.md` §9's own roster ("B2 lane4 armed 13... rest stages: [manual]") is already accurate, so this is `CONTRIBUTING.md` specifically lagging a sibling doc and the live config (`last_reviewed` predates the 2026-09-17 ruling it fails to reflect) — the same drift family as the persisting `ruff` finding above, different file.

### Med (3)

**PERSISTING — carried since ≥2026-08-10 (41+ days), independently re-derived tonight** — the CLAUDE.md/AGENTS.md split's byte-count justification is stale
- **Claim:** "a wholesale copy [of CLAUDE.md into AGENTS.md] measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently" — stated as present-tense fact.
- **Location:** `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`, `templates/claude-regions/antipatterns-universal.md:4`
- **Evidence:** `wc -c CLAUDE.md AGENTS.md` → CLAUDE.md=23,651 B; a wholesale copy today would land at ~23.1 KiB, comfortably under the 32 KiB cap — contradicting the stated 43.50 KiB/truncates-silently claim.
- **Verdict:** contradicted
- **Proposed fix:** Attribute the number to its source measurement (`docs/audits/2026-08-22-fresh-eyes-cloud-4v2.md`, taken pre-ADR-115-split when CLAUDE.md alone was ~44 KB) instead of stating it as a current fact, or re-measure and update all four occurrences together.
- **Note:** Longest-running item in this digest's tracked history — present at 08-10, carried through 09-18/09-19 per those digests' own delta narratives (though 09-19 dropped it from its formal Findings write-up), and re-derived fresh and independently by tonight's own V1/V2/V3 fan-out. CLAUDE.md's own conventions section warns "a number typed into a doc is stale at the next commit" — this is exactly that failure, repeated in four files for 41+ days.

**PERSISTING — carried since ≥2026-09-19** — `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status
- **Claim:** `CLAUDE.md:80` (§4): "the ADR-77 guard stays armed" vs. `CLAUDE.md:194` (§9): "the ADR-77 guard stays off ([#863])."
- **Location:** `CLAUDE.md:80` vs `CLAUDE.md:194`
- **Evidence:** `grep -n -i 'ADR-77' CLAUDE.md` → both lines present verbatim, unchanged.
- **Verdict:** contradicted
- **Proposed fix:** Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," matching §9 and the live `.claude/settings.json` emergency-disable entry.
- **Note:** Plain internal self-contradiction within one file, unresolved for a second night; §9 is already correct, only §4 needs the fix.

**PERSISTING — carried since ≥2026-09-18** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine."
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `grep -n "thirteen machine constants plus five deploy" docs/archive/VISION.md` → still present verbatim.
- **Verdict:** contradicted (per the 2026-09-18 digest's own re-verified counts: eleven sites / six manifests)
- **Proposed fix:** Correct the counts, or drop the hardcoded numbers per the hub's own "never restate a count or roster in prose" convention. The same re-read that fixes the HIGH VISION.md finding above closes this too.
- **Note:** Not independently re-derived by tonight's fan-out (verifier-coverage gap on this specific paragraph); carried on direct text match against the 09-18/09-19 baselines.

### Low (3)

**PERSISTING — carried since ≥2026-09-18** — `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count
- **Claim:** "`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)."
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B — same 129 B gap measured on 2026-09-19.
- **Verdict:** contradicted
- **Proposed fix:** Update the byte figure or drop the hardcoded count.
- **Note:** Two nights unchanged.

**NEW** — `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale
- **Claim:** "`git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES)."
- **Location:** `CLAUDE.md:102` (Critical rules, item 7)
- **Evidence:** `grep -n '^- verify:' .claude/rules/git-discipline.md` → 5 matches (lines 12, 51, 76, 87, 102), not 3.
- **Verdict:** contradicted
- **Proposed fix:** Change "three" to "five", or drop the exact count per the repo's own "never restate a count in prose" rule.
- **Note:** The file grew two more `verify:` lines via the "THE HANDOFF MERGE IS ATOMIC WITH TEARDOWN" subsection (2026-08-28) and the 2026-09-19 "Scope refinement" addendum; the "two standing operator orders" half of the claim still holds.

**NEW** — `ARCHITECTURE.md`'s size-target note is stale and survived a restamp that fixed its neighbor
- **Claim:** "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB" reads as a live target still governing the file's size.
- **Location:** `ARCHITECTURE.md:17-18`
- **Evidence:** `wc -c ARCHITECTURE.md` → 23,849 B, 55% over the stated 15 KB target; `git log --oneline -- ARCHITECTURE.md` shows `80df075` and `02b2bca` both post-date the `c0c920a` cut and grew the file back without touching this line, even though `02b2bca`'s own message ("re-read end-to-end and restamp 2026-09-19... correct stale hook-wiring claims") shows the adjacent hook-wiring claim in the *same box* was fixed in that pass.
- **Verdict:** omitted (from that same restamp)
- **Proposed fix:** Either drop the numeric target (nothing enforces it — only `CLAUDE.md` is in `scripts/validate_doc_rot.py`'s `_FILE_SIZE_BUDGETS`) or update the note to record that `[#513]` R-2 deliberately grew the file back past it.
- **Note:** `CLAUDE.md`'s own freshness-cadence rule says a `last_reviewed` stamp means "re-read end-to-end and confirmed accurate, or drift filed" — that didn't happen for this specific line in the 09-19 restamp, even though it evidently did for the line right above it.

---

## Killed Findings

**Killed (2 of 6 raw this cycle):**

- **Claim:** "[#613] was marked CLOSED on 2026-09-16 while its own Done-when acceptance witness (`tests/test_routing_agreement.py::test_the_live_table_is_well_formed`) was known-failing at closure time and remains failing today."
- **Kill reason:** documented-decision
- **Kill detail:** Disclosed, not hidden — the same closing commit's companion census explicitly states "[#613] is CLOSE-PRE on its recorded witness... that separate defect is [#829]," and `tasks/829-613.md` exists (open, P1) tracking exactly this gap. This is the ADR-111 decision-funnel CLOSE-PRE pattern working as designed, not an undisclosed conformance failure — the live-failing-test fact is already the entire content of open row `[#829]`, so it is not a new finding.

- **Claim:** "16 of 25 'Proving SHA' witnesses cited in the 2026-09-16 closure census cannot be resolved to any object in this clone."
- **Kill reason:** evidence-not-definitive
- **Kill detail:** The repo is a shallow clone (boundary 2026-09-15); the finding's own note already conceded "very plausibly just history predating the fetch depth rather than a fabricated citation" and carried an `unsupported` verdict. Per the 2026-09-19 digest's own retraction of an near-identical finding (that digest unshallowed the repo and found all such SHAs resolve as real ancestors), this class of finding is a known shallow-clone artifact, not a live defect — correctly not carried as a survivor.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries through 2026-09-19):**
- All 10 checked entries' commit anchors and merge SHAs (`68c71f4`, `9be43b2`, `8094e4d`, `14cd47f`, and 6 more full arcs) match `git log` exactly, including commit-message wording ✓
- Every backlog task-id claimed as filed (`[#912]`–`[#928]`) has a corresponding file under `tasks/` ✓
- HEAD (`9be43b2`) is exactly the merge commit the last entry cites as its own anchor — no unjournaled significant work ✓
- Shallow-history guard: available history reaches back to at least 2026-09-15, before all 10 checked entries — none of the checked SHAs are out-of-scope ✓

**V2 (living-doc factual claims):**
- `CLAUDE.md` header budget "≤24,576 B" — actual 23,651 B, under budget ✓
- `ARCHITECTURE.md` Codemap "orphan modules: codemap, toc" — confirmed live via `python3 -m scripts.codemap.cli check` ✓
- `ARCHITECTURE.md` generated Quality-requirements block "29 requirement(s), 8 measured, 21 candidate" — matches `ecosystem/quality-requirements.yaml` exactly ✓
- `CLAUDE.md` recent-ADRs roster (ADR-115/116/117/118/119) — each file exists, statuses match ✓
- `CLAUDE.md` §9 "B2 lane4 armed 13 (counter+expiry)" — exactly 13 hook ids non-manual with "RE-ARMED 2026-09-18" comments; `ruff` correctly stays manual ✓
- `CLAUDE.md` §9 "Of nine measured-broken hooks eight are off" — `.claude/settings.json` lists exactly 9 entries, 8 disabled, `propose_closures.py` explicitly running ✓
- `CLAUDE.md` §9 PreToolUse `[#727]` UNWIRED and ADR-77 guard off (`[#863]`) — both confirmed in `.claude/settings.json` (the §9 line itself is accurate; only §4 line 80 contradicts it — see Findings) ✓
- ~12 `ARCHITECTURE.md` references to scripts/workflows (`conductor.py`, `fleet_health.py`, `arm_hooks.py`, `session_end_backpressure.py`, `file_purpose_graph.py`, `organ-index.md`, etc.) all exist on disk ✓

**V3 (BACKLOG closure semantic coherence):**
- `[#743]` closure (`0c120be`, 2026-09-16) — commit directly implements stated Done-when with RED-first witnesses shown. Coherent ✓
- `[#744]` closure (`0c120be`, 2026-09-16) — commit directly implements stated Done-when matching the row's prescribed test shape. Coherent ✓
- `[#785]` closure (`0c120be`, 2026-09-16) — ten-outcome provider bench delivered with priced/unpriced legs matching the row's Done-when allowance for `RateUnavailable`-by-name. Coherent ✓

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, now 3 nights running)** Absorb the queue of unmerged `claude/conformance-*` branches — `2026-09-18`, `2026-09-19`, and this run's `2026-09-20`. This is the same [#426] operator-consumption gap named on 2026-08-10 and re-flagged on 2026-09-19; every finding in all three unmerged digests is currently invisible to anyone reading only `main`.
2. **HIGH — persisting** — Re-read `docs/archive/VISION.md:16-19` end-to-end: fix the `CANONICAL_RETIRED` status claim and the machine-site/manifest counts in one pass (closes one HIGH + one MED below).
3. **HIGH — persisting + new, same drift family** — Correct `CLAUDE.md:65`, `AGENTS.md:66`, and `CONTRIBUTING.md`'s Validators table (lines 159-171) together: all three describe `ruff` (and other now-manual hooks) as local commit-blocking gates when they are `stages: [manual]` / report-only since the 2026-09-17 ruling. Bump `CONTRIBUTING.md`'s `last_reviewed` past that date once fixed.
4. **MED — persisting** — Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," resolving the self-contradiction with `CLAUDE.md:194`.
5. **MED — persisting, 41+ days** — Re-measure or attribute-to-source the "43.50 KiB / 32 KiB cap" byte-count claim across `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `templates/claude-regions/antipatterns-universal.md` so all four stay consistent with the post-ADR-115-split reality.
6. **LOW — new** — Correct `CLAUDE.md` §5 rule 7's "three `verify:` lines" to five, or drop the exact count per the repo's own no-restated-counts convention.
7. **LOW — persisting + new, same box** — Reconcile `ARCHITECTURE.md`'s stale `≤15 KB` size-target note (grown back to 23,849 B) and `CONTRIBUTING.md:19`'s stale `AGENTS.md` byte figure (5,714 B → 5,843 B) — both are small numeric-drift items a single pass could close alongside item 3's re-read.
8. **(INFRASTRUCTURE, persisting since ≥2026-08-02, now 41+ nights unresolved)** Cloud runtime `uv` (`0.8.17`) cannot be updated to the pinned `0.11.19` — `uv self update 0.11.19` fails with "version not found," meaning this is a distribution-availability problem, not merely a deferred update. Fires on every Stop-hook check.

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-20-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
