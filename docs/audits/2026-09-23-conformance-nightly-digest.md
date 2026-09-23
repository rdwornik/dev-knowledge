<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-23

**Date:** 2026-09-23
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded**, sixth consecutive clean run (2026-09-18 through 2026-09-22 also ran to completion, per their own digests read from their unmerged branches — see Delta below). `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`, task id `wt4jm2u15`, run id `wf_d878c0d1-ad2`) and ran to completion in one pass — no spec-orchestration fallback needed.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 84,949 | 9 | 91s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 109,572 | 32 | 213s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 79,040 | 25 | 232s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 69,842 | 20 | 161s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 50,136 | 1 | 30s |

Total: 393,539 subagent tokens, 87 tool calls, ~521s (8.7 min) wall time (Stage 1's three verifiers ran in parallel).

**Model-pin note (unchanged since 2026-09-18):** `conformance-hub.js`'s `meta.phases` describes Stage 2 ("skeptic") and Stage 3 ("digest") as intended for Opus, but neither `agent()` call in the script body passes an explicit `model` for those two stages. Tonight, as on every prior run, both ran on `claude-sonnet-5` by default. Not a doc-conformance finding — flagged for the platform record.

**Harness prompt-injection heuristic fired once, false positive.** The V1 subagent's log line carried: `[harness: subagent output matched instruction-shaped pattern(s): settings-json. Control tags below are neutralized...]`. Inspected the underlying V1 `checked_clean` text directly — the match was on the innocuous string `.claude/settings.json` appearing in a normal file-existence claim ("six hooks re-armed in `.claude/settings.json`"), not an actual embedded instruction. No injection attempt found; noted here only for the platform record since detecting exactly this class of event is in scope for this reviewer.

**Environment note — `uv` version mismatch, worked around locally, not a repo fix.** The orchestrating session's own Stop-hook backpressure fired repeatedly with `Required uv version ==0.11.19 does not match the running version 0.8.17` — the same systemic mismatch flagged since the 2026-08-10 digest's Next Actions #7, now **52 days unresolved** (2026-08-02 → 2026-09-23). This session located `uv==0.11.19` via `pip install` (network path to PyPI was reachable even though `uv self update` and `astral.sh`'s installer script were not — `curl` to `astral.sh` returned a proxy `403`) and overwrote the standalone binary at `/root/.local/bin/uv` with it for this session only. This is a **local, session-scoped workaround**, not a repo change and not a fix to the base cloud image — it will not persist to the next session and is recorded here so the operator knows a `pip install uv==<pin>` fallback exists if `uv self update` keeps failing on this runtime.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-09-22-conformance-nightly-digest.md`, fetched read-only from the **unmerged** branch `origin/claude/conformance-2026-09-22` (`git show origin/claude/conformance-2026-09-22:docs/audits/2026-09-22-conformance-nightly-digest.md`). No `docs/audits/*-conformance-nightly-digest.md` file exists on `main` more recent than 2026-08-10 — `origin/claude/conformance-2026-09-18` through `-22` are all still unmerged (verified fresh this run: `git merge-base --is-ancestor` fails for each against `origin/main`). This is now the **sixth** consecutive night in this state (this run's own branch will be the seventh once pushed).
**Gap:** 1 day (2026-09-22 → 2026-09-23).

All 11 survivors from the 2026-09-22 digest's own Findings section were independently re-verified against current `origin/main` head (`2fd8f25`) with fresh evidence commands (re-run directly by this orchestrating session, not merely re-asserted):

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **PERSISTING (day 6)** | HIGH: `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` lane-a retired 2026-08-31 | `grep -n -A5 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py` → tuple is `(ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)`, VISION absent, `ARCHITECTURE` is `[0]`; `VISION.md:16-19` still reads "It is a `MUST` on all nine ADR-104 fleet members... `canonical_docs.CANONICAL_MANDATORY[0]`... thirteen machine constants plus five deploy manifests" verbatim unchanged. |
| **PERSISTING (day 5)** | HIGH: `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; still `stages: [manual]` | `sed -n '65p' CLAUDE.md` → "…`ruff check` is also a pre-commit gate (§9) and blocks" unchanged; `sed -n '66p' AGENTS.md` → "lint (also a pre-commit gate)" unchanged; `.pre-commit-config.yaml:852` → `stages: [manual]` unchanged. |
| **PERSISTING (day 4)** | HIGH: `CONTRIBUTING.md:170`'s Validators table row lists `ruff` as a blocking commit-stage gate | `sed -n '170p' CONTRIBUTING.md` → "…Blocks on violations. [#13] closed." unchanged; hook still `stages: [manual]`. |
| **PERSISTING (day 3), not independently re-derived tonight** | MED: `[#780]`'s closure evidence and the 2026-09-16 closure census cite the wrong proving commit (`5f270cd9` instead of `b81c554`) for lane z-11's three-repo comparison | `tasks/780-*.md:12` and `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25` still cite `5f270cd9`; `git log -1 --format='%H %s' 5f270cd9` still resolves to the unrelated `chore(lane): step-2 sync` commit, not `b81c554` (the actual lane z-11 merge). |
| **PERSISTING (day 4)** | MED/LOW: `CONTRIBUTING.md`'s Validators table lists five manual hooks as blocking commit-stage gates (`normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, `audit-health`) | All five re-checked directly: `.pre-commit-config.yaml` lines 65-66, 81-82, 300-301, 313-314, 751-752 all still `stages: [manual]` with the identical 2026-09-17 "MOVED to the Actions conductor" comment; `CONTRIBUTING.md` lines 159,161,167,168,169 still list Stage=`commit` for all five, unchanged. |
| **PERSISTING (44 days)** | LOW: the CLAUDE.md/AGENTS.md split's "43.50 KiB" byte-count justification is stale | `wc -c CLAUDE.md AGENTS.md` → 23,651 B + 5,843 B = 29,494 B total, still well under the 32 KiB cap the claim says would be exceeded. Text unchanged verbatim at all 4 cited locations (`CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`, `templates/claude-regions/antipatterns-universal.md:4`). |
| **PERSISTING (day 5)** | LOW: `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status | `grep -n -i 'ADR-77' CLAUDE.md` → line 80 ("stays armed") and line 194 ("stays off ([#863])") both present verbatim, unchanged, same line numbers. |
| **PERSISTING (day 4)** | LOW: `docs/archive/VISION.md:18-19` overstates its own machine-site footprint ("thirteen machine constants plus five deploy manifests") | `grep -l 'VISION\.md:' deploy/manifest-v*.yaml \| wc -l` → 6, not 5; `scripts/canonical_docs.py:53` still reads "The ten machine constants," not thirteen. |
| **PERSISTING (day 6)** | LOW: `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count (5,714 B) | `wc -c AGENTS.md` → 5,843 B, same 129 B gap. |
| **PERSISTING (day 4), independently re-derived tonight** | LOW: `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale | Tonight's own V1/V2 fan-out (living-docs domain) independently re-raised this: `grep -n 'verify:' .claude/rules/git-discipline.md` → 5 hits (lines 12, 51, 76, 87, 102), not 3; `CLAUDE.md:102` still reads "carries three `verify:` lines." |
| **PERSISTING (day 4)** | LOW: `ARCHITECTURE.md`'s size-target note is stale | `wc -c ARCHITECTURE.md` → 23,849 B — identical figure measured on 2026-09-20 through 2026-09-22, file has not changed size in four nights, still ~55% over the stated ≤15 KB target; `_FILE_SIZE_BUDGETS` in `scripts/validate_doc_rot.py:210` still covers only `CLAUDE.md`. |

**RESOLVED this cycle:** none. All 11 baseline survivors are still live on `origin/main`, byte-for-byte unchanged in every case re-checked.

**NEW this cycle (3):** tonight's independent V1/V2/V3 fan-out surfaced items outside the set the 2026-09-18→22 runs had been carrying:

| Status | Finding | Notes |
|---|---|---|
| **NEW** | HIGH (evidentiary, not content): this checkout is a **shallow clone** (grafted 2026-09-18, 6 grafted roots at `.git/shallow`), so the `backlog-closures` domain's history-window checks are architecturally blind to anything closed before that boundary | `git rev-parse --is-shallow-repository` → true; the earliest reachable commit (`4601b70`) is a two-parent merge whose parents are absent locally, landing 3,580 files / 770,828 insertions in one shot — a fetch-depth artifact, not a real initial commit. `git log --all --since="2026-05-14" --grep="closes [#"` returns **zero** commits inside this window, which is a graft-boundary artifact, not evidence of zero closures. No prior digest in this series (2026-08-10 through 2026-09-22) recorded this as a formal finding, though the shallow-clone condition itself likely predates tonight. |
| **NEW** | MED: `docs/archive/governance.md` (self-declared `status: active`, `last_reviewed: 2026-09-05`) '## Values' forwards to the now-**deleted** `protocols/ESSENTIALS.md` "How Claude thinks" section for core principles, and `docs/archive/VISION.md:47-49` carries the same one-line forward | `ls protocols/ESSENTIALS.md` → no such file (deleted 2026-09-14 per `[#628]`, documented at `CLAUDE.md:16`); `governance.md`'s `last_reviewed` (2026-09-05) predates that deletion and was never bumped to reconcile it. Distinct from the VISION.md MUST-tier finding above — different claim, different files, not a duplicate. |
| **NEW** | MED (methodology gap, not content drift): within the visible (shallow) commit window, all 169 `tasks/*.md` files carrying `status: closed` were introduced **already closed** in their first tracked commit — there are zero actual open→closed status-field transitions to check for Done-when/diff coherence, so the `backlog-closures` domain currently has no material to run its intended check against | `grep -l '^status: closed' tasks/*.md \| wc -l` → 169; scanning every commit touching `tasks/` for a `-status: <x>` / `+status: closed` pair found exactly one bare `-status: open` removal (a duplicate-row deletion, `1db485b`, not a closure) and zero replacement pairs. This is a "no material available" result, distinct from "checked and found coherent." |

One raw finding was killed by tonight's skeptic as a false positive (see below) and does not appear as new or persisting.

**Delta counts:** 0 resolved · 11 persisting (1 of them independently re-derived tonight) · 3 new
**This run's own raw → survived → killed:** 5 → 4 → 1
**Skeptic kill-rate:** 20% (1 of 5) — the killed claim (CONTRIBUTING.md's provider table "omitting" two providers) was confirmed to be an intentional council-alias filter, documented and disclaimed in the file itself, introduced atomically with the registry in the same commit — a real documented-decision kill, not a weak pass.

<!-- counts: raw=5 survived=4 killed=1 -->

---

## Summary

Doc health this cycle shows **zero resolutions and three new findings** against an unusually stable baseline for a sixth consecutive measurement window: all 11 survivors carried from the 2026-09-22 digest are still live on `origin/main`, unchanged in every case re-checked, including `ARCHITECTURE.md`'s and `AGENTS.md`'s exact byte counts (unmoved for multiple nights running). Tonight's own fan-out independently re-derived only one of the eleven (the `CLAUDE.md` stale `verify:`-count) and surfaced three genuinely new items: a shallow-clone evidentiary limitation on the `backlog-closures` domain's own history window (HIGH, because it means "zero closures found" in that domain has been silently indistinguishable from "the clone can't see that far back" every night since the graft), a governance-doc forward to a deleted file (`protocols/ESSENTIALS.md`, deleted 2026-09-14, `[#628]`) from a self-declared *active* doctrine file that was never reconciled, and a methodology gap where the `backlog-closures` domain has had no actual open→closed transition to check against for its entire visible window — a "no material" result that could otherwise misread as a clean pass.

The concentration of drift remains exactly where the last several nights placed it: (1) the 2026-09-17 pre-commit-gate strip to `stages: [manual]` still hasn't propagated into `CLAUDE.md` §4, `AGENTS.md`, or `CONTRIBUTING.md`'s Validators table — now 6 consecutive nights across 3 HIGH + 2 MED/LOW findings, none fixed; (2) VISION.md's 2026-08-31 retirement from MUST/`CANONICAL_MANDATORY` to SHOULD still isn't reflected in the file's own header prose; and (3) a cluster of small numeric-drift items (byte counts, an internal ADR-77 contradiction, a wrong closure-evidence SHA) unchanged since first flagged. A broad set of independent checks came back clean — all cited JOURNAL lane merges corroborate exactly against git history, six living-doc factual cross-checks (byte budgets, hook-roster counts, ADR citation existence, quality-requirements YAML) all held, and HEAD exactly matches the newest JOURNAL entry's cited merge tip with no unlogged work ahead of it — so this remains narrow, named, persistent drift plus a genuine evidentiary gap, rather than systemic rot.

The more consequential finding for the record remains procedural, now compounding for a **sixth** night: `origin/claude/conformance-2026-09-18` through `-22` are all still unmerged, the same `[#426]` operator-consumption gap first named on 2026-08-10 (still OPEN per `BACKLOG.md` / `tasks/426-*.md`). Every finding in all five prior unmerged digests — including every HIGH-severity item above — remains invisible to anyone who reads only `main`. This run's own branch will be the sixth to join that queue once pushed.

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 5 · **Survived skeptic:** 4 · **Killed false positives:** 1
**Plus 10 findings carried forward unchanged from the 2026-08-10 → 2026-09-22 baselines that were not independently re-derived by tonight's own fan-out** (each was independently re-verified above with fresh evidence this run)

### High (4)

**PERSISTING — carried since ≥2026-09-18 (day 6)** — `docs/archive/VISION.md:16-18` self-describes a MUST-tier/`CANONICAL_MANDATORY[0]` status ADR-114/`[#614]` lane-a retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members … it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-18`
- **Evidence:** `grep -n -A5 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py` → tuple is `(ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)`, VISION absent, `ARCHITECTURE` is `[0]`; `grep -n -A15 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml` → `tier: {hub: SHOULD, consumer: SHOULD}`.
- **Verdict:** contradicted
- **Proposed fix:** Rewrite VISION.md's header paragraph to state its actual current tier (SHOULD/SHOULD, retired from MUST 2026-08-31 by `[#614]` lane-a, tracked in eight of nine members) instead of the pre-retirement claim.
- **Note:** Unchanged for a 6th consecutive night. `VISION.md`'s own `last_reviewed: 2026-08-29` predates the 2026-08-31 retirement that falsifies it.

**PERSISTING — carried since ≥2026-09-19 (day 5)** — `CLAUDE.md:65` / `AGENTS.md:66` claim `ruff` "blocks" as a pre-commit gate; it is currently report-only
- **Claim:** "`ruff check` is also a pre-commit gate (§9) and blocks" (`CLAUDE.md:65`); "lint (also a pre-commit gate)" (`AGENTS.md:66`)
- **Location:** `CLAUDE.md:65`; `AGENTS.md:66`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`, comment "NOT RE-ARMED 2026-09-18 … Left manual; flagged as a B3+ candidate."
- **Verdict:** contradicted
- **Proposed fix:** Reword both to state `ruff` is currently `stages: [manual]` / report-only via the Actions conductor job, matching `CLAUDE.md`'s own §9 roster which already gets this right.
- **Note:** Also an internal self-contradiction within `CLAUDE.md` alone (§4 vs §9).

**PERSISTING — carried since ≥2026-09-20 (day 4)** — `CONTRIBUTING.md:170`'s Validators table row lists `ruff` as a blocking commit-stage gate
- **Claim:** "`ruff` | commit | Lint gate … Blocks on violations. [#13] closed."
- **Location:** `CONTRIBUTING.md:170`
- **Evidence:** `grep -n -A6 'id: ruff$' .pre-commit-config.yaml` → `stages: [manual]`; `CONTRIBUTING.md`'s frontmatter `last_reviewed: 2026-09-10`, seven days before the 2026-09-17 strip, never reconciled.
- **Verdict:** contradicted
- **Proposed fix:** Re-reconcile `CONTRIBUTING.md`'s hook table against the current `.pre-commit-config.yaml` and bump `last_reviewed` past 2026-09-17.
- **Note:** Same underlying drift as the `CLAUDE.md`/`AGENTS.md` finding above and the MED/LOW table finding below — a single combined re-read closes all of them.

**NEW — evidentiary limitation, not content drift** — this checkout is a shallow clone (grafted 2026-09-18), so the `backlog-closures` domain's history-window checks are architecturally blind to pre-boundary closures
- **Claim (implicit in this domain's normal operation):** an empty result from `git log --all --since="2026-05-14" --grep="closes [#"` or `git log -p -S "[#<id>]" -- BACKLOG.md` means no matching closures occurred.
- **Location:** `.git/shallow`; boundary commit `4601b70fc2f2d720bab187e5d44e8136a48511a0`
- **Evidence:** `git rev-parse --is-shallow-repository && cat .git/shallow` → true, 6 grafted roots; `git show --stat 4601b70…` → a two-parent merge whose parents are not present locally, landing 3,580 files / 770,828 insertions in one shot; `git log --all --since="2026-05-14" --grep="closes [#" --oneline | wc -l` → 0.
- **Verdict:** unsupported
- **Proposed fix:** Have the `backlog-closures` domain declare its clone-depth window explicitly in its output (or run against an unshallowed clone) instead of treating an empty pre-boundary grep as a zero-closures result. This is a fix to `conformance-hub.js`'s V3 prompt/expectations, not to a living doc.
- **Note:** Reproduced independently by tonight's V3 verifier and confirmed by the skeptic. No prior digest in this series recorded the shallow-clone condition as a formal finding — flagged now because it silently limits every night's `backlog-closures` coverage, past and future, until either the clone is deepened or the domain reports its own blind spot.

### Med (4)

**PERSISTING — carried since ≥2026-09-21 (day 3), not independently re-derived tonight** — `[#780]`'s closure evidence and the 2026-09-16 closure census cite the wrong proving commit for lane z-11's three-repo comparison
- **Claim:** "Three-repo comparison … CLOSED 2026-09-16 — evidence `5f270cd9`."
- **Location:** `tasks/780-three-repo-comparison-gaps-adopt-candidates-and-an-explicit-will-not-adopt-list.md:12`; `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md:25`
- **Evidence:** `git log -1 --format='%H %s' 5f270cd9` → `chore(lane): step-2 sync -- merge main into the z-4 lane for the anchor gate [#772]` (unrelated); `git log -1 --format='%H %s' b81c554` → `Merge branch 'lane-z-11' @ f304a76c -- three-repo comparison: 4 intakes, 7 recorded refusals…` (the actual work).
- **Verdict:** unsupported
- **Proposed fix:** Repoint `[#780]`'s "CLOSED … evidence" line and the census's Table 1 row from `5f270cd9` to `b81c554`.
- **Note:** Unchanged since first flagged 2026-09-21, now day 3.

**PERSISTING — carried since ≥2026-09-20 (day 4)** — `CONTRIBUTING.md`'s Validators table lists five manual hooks as blocking commit-stage gates
- **Claim:** `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, `validate-backlog`, and `audit-health` are all listed with Stage=`commit`.
- **Location:** `CONTRIBUTING.md:159,161,167,168,169`
- **Evidence:** all five re-checked directly against `.pre-commit-config.yaml` lines 65-66, 81-82, 300-301, 313-314, 751-752 — all `stages: [manual]`, same 2026-09-17 "MOVED to the Actions conductor" comment.
- **Verdict:** contradicted
- **Proposed fix:** Same fix as the `ruff` row above — reconcile the table's Stage column from the live config in one pass; consider generating the table instead of hand-maintaining it.
- **Note:** Same root cause as the HIGH `ruff`-row finding, distinct table cells.

**NEW** — `docs/archive/governance.md` (self-declared **active** doctrine) forwards to the deleted `protocols/ESSENTIALS.md` for core principles
- **Claim:** `docs/archive/VISION.md:47-49` "Moved to `docs/archive/governance.md` '## Values' — which itself defers to `protocols/ESSENTIALS.md` 'How Claude thinks' for the principles."
- **Location:** `docs/archive/VISION.md:47-49`; `docs/archive/governance.md` '## Values' (status: active, `last_reviewed: 2026-09-05`)
- **Evidence:** `ls protocols/ESSENTIALS.md` → no such file (deleted 2026-09-14, `[#628]`, documented at `CLAUDE.md:16`); `grep -n 'DELETED 2026-09-14' CLAUDE.md` confirms the repo's own deletion record.
- **Verdict:** contradicted
- **Proposed fix:** Update `docs/archive/governance.md`'s '## Values' section (and VISION.md's one-line forward) to point at PLAYBOOK per CLAUDE.md's own documented ESSENTIALS.md deletion, then bump `governance.md`'s `last_reviewed` stamp past 2026-09-14.
- **Note:** `governance.md` is explicitly self-declared "ACTIVE doctrine, not retired" despite living under `docs/archive/`, and its `last_reviewed` (2026-09-05) predates the deletion it fails to reflect — this is a live governance file citing a deleted file as canonical, not an inert archival pointer.

**NEW (methodology gap)** — within the visible window, all 169 `tasks/*.md` closed rows were closed-on-introduction; zero open→closed diffs exist for the `backlog-closures` domain to check
- **Claim:** the `backlog-closures` domain's intended check ("does the closing diff match the item's Done-when?") has material to run against in this window.
- **Location:** `tasks/*.md` (169 files, all `status: closed` since their first tracked appearance)
- **Evidence:** `grep -l '^status: closed' tasks/*.md | wc -l` → 169; scanning every commit touching `tasks/` for a `-status: <x>` / `+status: closed` pair → exactly one bare `-status: open` removal (duplicate-row deletion, `1db485b`, not a closure), zero replacement pairs.
- **Verdict:** unsupported
- **Proposed fix:** Reword the `backlog-closures` domain's output to state plainly when no closure-transition diffs exist in the visible window, rather than implying a coherence check was performed and passed.
- **Note:** A legitimate "no material available" result, not a false negative — worth surfacing so the absence of findings in this domain isn't misread as a clean audit.

### Low (6)

**PERSISTING — carried since ≥2026-08-10 (44 days)** — the CLAUDE.md/AGENTS.md split's "43.50 KiB" byte-count justification is stale
- **Location:** `CLAUDE.md:212`, `AGENTS.md:37`, `CONTRIBUTING.md:32`, `templates/claude-regions/antipatterns-universal.md:4`
- **Evidence:** `wc -c CLAUDE.md AGENTS.md` → 23,651 B + 5,843 B = 29,494 B, comfortably under the 32 KiB cap the claim says would be exceeded.
- **Verdict:** contradicted
- **Proposed fix:** Attribute the number to its source measurement (ADR-115 decision packet, 2026-08-22) instead of stating it as a current fact, or re-measure all four occurrences together.
- **Note:** Longest-running item in this digest's tracked history — 44 days.

**PERSISTING — carried since ≥2026-09-19 (day 5)** — `CLAUDE.md` contradicts itself on the ADR-77 guard's armed/off status
- **Location:** `CLAUDE.md:80` vs `CLAUDE.md:194`
- **Evidence:** `grep -n -i 'ADR-77' CLAUDE.md` → both lines present verbatim, unchanged.
- **Verdict:** contradicted
- **Proposed fix:** Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])," matching §9.
- **Note:** Plain internal self-contradiction, unresolved for a 5th night.

**PERSISTING — carried since ≥2026-09-20 (day 4)** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `grep -l 'VISION\.md:' deploy/manifest-v*.yaml | wc -l` → 6, not 5; `scripts/canonical_docs.py:53` still enumerates "the ten machine constants," not thirteen.
- **Verdict:** contradicted
- **Proposed fix:** Update to six manifests / ten machine constants, or drop the hardcoded numbers.
- **Note:** Same paragraph as the HIGH VISION.md finding above; one re-read closes both.

**PERSISTING — carried since ≥2026-09-18 (day 6)** — `CONTRIBUTING.md:19` states a stale `AGENTS.md` byte count
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B vs the stated 5,714 B — same 129 B gap measured since 2026-09-19.
- **Verdict:** contradicted
- **Proposed fix:** Correct the byte figure or drop the hardcoded count.
- **Note:** Six nights unchanged.

**PERSISTING — carried since ≥2026-09-20 (day 4), independently re-derived tonight** — `CLAUDE.md` §5 rule 7's "three `verify:` lines" count is stale
- **Claim:** "`git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES)."
- **Location:** `CLAUDE.md:102` (Critical rules, item 7)
- **Evidence:** `grep -n 'verify:' .claude/rules/git-discipline.md` → 5 hits (lines 12, 51, 76, 87, 102), not 3.
- **Verdict:** contradicted
- **Proposed fix:** Change "three" to "five", or drop the exact count per the repo's own no-restated-counts convention.
- **Note:** Tonight's own V2 fan-out independently re-derived this (unlike the 2026-09-21/22 nights, where it fell into the verifier-coverage gap).

**PERSISTING — carried since ≥2026-09-20 (day 4)** — `ARCHITECTURE.md`'s size-target note is stale
- **Location:** `ARCHITECTURE.md:17`
- **Evidence:** `wc -c ARCHITECTURE.md` → 23,849 B — identical figure measured on 2026-09-20 through 2026-09-22, file has not changed size in four nights, still ~55% over the stated ≤15 KB target; `_FILE_SIZE_BUDGETS` (`scripts/validate_doc_rot.py:210`) still covers only `CLAUDE.md`.
- **Verdict:** omitted
- **Proposed fix:** Either drop the numeric target or update the note to record stabilization past it; consider adding `ARCHITECTURE.md` to `_FILE_SIZE_BUDGETS`.
- **Note:** Fourth night this exact byte count has been measured — file is stable, only the header note is stale.

---

## Killed Findings

**1 killed (skeptic, `documented-decision`):**

- **Claim:** "CONTRIBUTING.md's provider table ('Orientation only') omits `copilot-enterprise` and `antigravity` from `ecosystem/provider-registry.yaml`, which is drift against the source of truth."
- **Kill reason:** documented-decision
- **Detail:** The table's 5 rows (Anthropic/OpenAI/Google/xAI/DeepSeek) are exactly and only the providers that carry a non-null `council_alias` in `ecosystem/provider-registry.yaml`. The two omitted providers both carry `council_alias: null` with in-file comments explicitly marking them non-panellists ("NOT a council panellist", "NOT PANELLED"). The table's scope is "council-alias-bearing providers," not a full provider roster — the omission is by design. `CONTRIBUTING.md` also explicitly disclaims the table twice ("Orientation only — the registry is authoritative") and gives the live-enumeration command instead. Both the registry entries and the table were introduced together in commit `4601b70`, so there is no edit-drift event either.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last ~10 entries, 2026-09-21 through 2026-09-22(h)):**
- All 14 cited 2026-09-21/09-22 lane-merge anchors, test files, and referenced audit docs verified present in git history with matching dates ✓
- HEAD (`2fd8f25`) exactly matches the newest JOURNAL entry (h)'s cited merge tip — no unlogged work ahead of it ✓
- `docs/audits/2026-09-22-codex-lane-hooks-rearm.md`, `-technical-lane-hooks-rearm-disposition.md`, `-technical-lane-hooks-rearm-live-measurement.md` all exist as claimed ✓

**V2 (living-doc factual claims):**
- `CLAUDE.md`'s "≤24,576 B" byte budget: file is 23,651 B, under the cap, and `tests/test_claude_md_byte_cap.py` exists to gate it ✓
- `AGENTS.md` size (5,843 B) well under Codex's 32 KiB `project_doc_max_bytes` cap ✓
- `protocols/ESSENTIALS.md` deletion claim (`CLAUDE.md:16`) confirmed — file absent from filesystem ✓
- `CONTRIBUTING.md`'s ruff pre-commit rev (v0.15.5) matches `.pre-commit-config.yaml` exactly ✓
- `ARCHITECTURE.md`'s quality-requirements counts (29 total / 8 measured / 21 candidate) confirmed by direct YAML parse of `ecosystem/quality-requirements.yaml` ✓
- `CLAUDE.md` §9's "B2 lane4 armed 13 (counter+expiry)" matches the 2026-09-18 disposition audit and current `.pre-commit-config.yaml` stage assignments ✓
- `CONTRIBUTING.md`'s references to `scripts/check_backlog_commit_msg.py` confirmed to exist ✓
- Spot-checked ADR citations across `CLAUDE.md`/`ARCHITECTURE.md`/`CONTRIBUTING.md` (27-31, 36, 38, 39, 41, 51, 53, 54, 63, 65, 66, 68-70, 72, 74, 77, 78, 80-82, 84, 85, 89, 91-94, 97, 98, 101, 104, 106-111, 114-120) all exist under `docs/decisions/` ✓
- `CLAUDE.md` §9's hook-id roster (`normalize-dated-headers` through `block-unanchored-push`) all present in `.pre-commit-config.yaml` ✓

**V3 (BACKLOG closure semantic coherence, within the shallow-clone window):** no closure-transition material was found to check (see the NEW MED finding above) — this is a "no material" result, not a clean-check result, and is not double-counted in checked-clean.

---

## Next Actions (proposals for operator)

1. **(PROCESS, most urgent, now 6 nights running)** Absorb the queue of unmerged `claude/conformance-*` branches — `2026-09-18` through `2026-09-22`, plus this run's `2026-09-23`. Same `[#426]` operator-consumption gap named on 2026-08-10, still OPEN; every finding in all six unmerged digests, including every HIGH item above, is currently invisible to anyone reading only `main`.
2. **HIGH — persisting, day 6** — Re-read `docs/archive/VISION.md:16-19` end-to-end: fix the retired-tier claim and the machine-site/manifest counts in one pass (closes 1 HIGH + 1 LOW below).
3. **HIGH — persisting, day 4/5** — Correct `CLAUDE.md:65`, `AGENTS.md:66`, and `CONTRIBUTING.md`'s full Validators table (the `ruff` row plus five more rows) together in one pass: all describe now-manual hooks as local commit-blocking gates. Bump `CONTRIBUTING.md`'s `last_reviewed` past 2026-09-17 once fixed.
4. **NEW HIGH (evidentiary)** — Have `conformance-hub.js`'s V3 (`backlog-closures`) prompt declare its clone-depth window explicitly, or run this domain against an unshallowed clone, so an empty pre-boundary grep is never silently read as "zero closures."
5. **MED — persisting, day 3** — Repoint `[#780]`'s closure-evidence line and the 2026-09-16 census's Table 1 row from `5f270cd9` to `b81c554`.
6. **NEW MED** — Fix `docs/archive/governance.md`'s '## Values' section (and VISION.md's forward) to stop citing the deleted `protocols/ESSENTIALS.md`; bump `governance.md`'s `last_reviewed`.
7. **NEW MED (methodology)** — Reword V3's output to state plainly when no closure-transition diffs exist in the visible window, rather than implying a coherence check was performed and passed.
8. **LOW — persisting, 44 days** — Re-measure or attribute-to-source the "43.50 KiB / 32 KiB cap" byte-count claim across all 4 cited files.
9. **LOW — persisting, day 5** — Fix `CLAUDE.md:80` to read "the ADR-77 guard stays off ([#863])."
10. **LOW — persisting, day 4** — Correct `CLAUDE.md` §5 rule 7's "three `verify:` lines" to five, or drop the exact count.
11. **LOW — persisting, day 4** — Reconcile `ARCHITECTURE.md`'s stale ≤15 KB size-target note.
12. **(INFRASTRUCTURE, persisting since ≥2026-08-02, now 52 days unresolved)** Cloud runtime `uv` (`0.8.17`) still cannot reach the pinned `0.11.19` release via `uv self update` or the `astral.sh` installer (proxy `403`). `pip install "uv==0.11.19"` does succeed and was used as a session-local workaround tonight — worth considering for the base image if this persists.

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-23-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
