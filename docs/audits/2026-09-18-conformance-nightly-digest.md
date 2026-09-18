<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-18

**Date:** 2026-09-18
**Author:** Claude Code (claude-sonnet-5), orchestrating the nightly conformance-hub run
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path: NATIVE Workflow launcher succeeded.** `.claude/workflows/conformance-hub.js` was launched via the `Workflow` tool (`name: "conformance-hub"`) and ran to completion in one pass — no spec-orchestration fallback was needed. This is a platform-state change worth recording for the re-probe: the 2026-08-09 run recorded the launcher as unavailable, and the 2026-08-10 run recorded it as invocable-but-faulting (`StructuredOutput retry cap exceeded` on all 3 verifiers, traced to a permission-handler bug). Tonight all 5 agents (3 verifiers + skeptic + digest) completed cleanly on the first attempt with no retries.

| Stage | Label | Model used | Tokens | Tool calls | Duration |
|---|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 90,451 | 9 | 92s |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 105,467 | 27 | 203s |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 78,029 | 25 | 121s |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 65,263 | 18 | 70s |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 52,384 | 1 | 31s |

Total: 391,594 subagent tokens, 80 tool calls, ~318s wall time across the 5-agent run.

**Known-advisory infra note (unrelated to doc conformance):** the session's Stop-hook backpressure fired throughout this run with `Required uv version ==0.11.19 does not match the running version 0.8.17`. This is the same systemic mismatch flagged in the 2026-08-10 digest's Next Actions #7, still unresolved 39 days later, and remains advisory-only per `CLAUDE.md` §9 ("Stop backpressure (advisory)") — not a doc-conformance finding, noted for operator awareness only.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-08-10-conformance-nightly-digest.md` (merged to `main`). This is the most recent digest carrying this pipeline's own schema (`-conformance-nightly-digest.md` naming, counts-marker contract, RESOLVED/PERSISTING/NEW-comparable findings). No `claude/conformance-*` branches are currently unmerged (`git branch -r --list "*conformance*"` returns empty; the unmerged-branch backlog the 08-10 digest flagged as [#426] appears to have been absorbed since). A later file, `docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md`, has a higher date but is a differently-scoped, differently-shaped artifact (a one-off `[#171]` dashboard review, no counts-marker contract, findings not comparable 1:1 to this pipeline's schema) and was **not** used as the delta baseline.
**Gap:** 39 days (2026-08-10 → 2026-09-18).

All 8 of 2026-08-10's carried/new findings were independently re-checked against current `origin/main` (`87638c8`) with fresh evidence commands:

| Status | Finding | Fresh evidence this run |
|---|---|---|
| **RESOLVED** | prior S1 (HIGH): `protocols/ESSENTIALS.md:123` instructed `/override [reason]` as the only session-end escape (stale since the ADR-85 §A2 retirement) | `ls protocols/ESSENTIALS.md` → no such file. `ESSENTIALS.md` was deleted 2026-09-14 (`[#628]`), per `CLAUDE.md`'s own header note ("its doctrine lives in PLAYBOOK; do not look for it"). The misinstruction cannot recur because its home file is gone. |
| **RESOLVED** | T1 (HIGH, historical, non-live at baseline): commit `cd38fb8` claimed to close `[#213] [#215] [#441]` without discharging them, self-corrected 18 min later by `a62d988` | No repo action was ever proposed beyond an annotation; already non-live at baseline time and remains so. Not carried forward as an open item. |
| **RESOLVED** | prior S2 (MED): ARCHITECTURE.md said "five carriers" at 4 locations against 6 live `carrier_*.py` files | `grep -n "five carrier" ARCHITECTURE.md` → no match. `ARCHITECTURE.md:573-578` now reads "the carrier set is **computed, not restated**: read the manifest's `carriers:` block" and cites the live count (six `implemented: true`) from `deploy/manifest-v*.yaml` instead of a hardcoded prose number — the whole class of drift this finding represented was designed out. |
| **RESOLVED (re-reviewed; see recurrence note below)** | prior S3 (MED): `VISION.md` `last_reviewed: 2026-07-25` predated its last commit by 11 days | `grep -n last_reviewed docs/archive/VISION.md` → `2026-08-29`, i.e. re-reviewed after the 08-10 finding. The specific stale stamp cited in the 08-10 digest is corrected. |
| **RESOLVED** | prior S4 (MED): `protocols/ESSENTIALS.md` `last_reviewed: 2026-07-30` predated its last commit by 6 days | Same as S1 — file deleted 2026-09-14, so its freshness stamp no longer exists to be stale. |
| **RESOLVED** | T2 (MED): `ARCHITECTURE.md:405` claimed `validate_doc_code_edge.py` was "live on 13 rules" (explicit enumeration) against an actual live count of 15 | `grep -n "live on 13 rules\|live on 15 rules\|rule-edge" ARCHITECTURE.md` → no match; `grep -n "validate_doc_code_edge" ARCHITECTURE.md` shows the section (lines 498-516) now describes the mechanism without a hardcoded rule count to drift. (Current live count is 16 per `grep -c '# DONE' ecosystem/doc-code-edge.yaml`, further confirming a static number would already be wrong again.) |
| **RESOLVED** | prior S5 (LOW): ARCHITECTURE.md's pre-commit gates paragraph omitted `block-unanchored-push` | `grep -n "block-unanchored" ARCHITECTURE.md` → 3 hits (lines 645, 651, 1005), now documented including its server-side counterpart status. |
| **RESOLVED** | T3 (LOW): `ARCHITECTURE.md:95` Purpose line said "ratified through ADR-109" against the file's own changelog naming ADR-110 | `grep -n "ratified through ADR"` and `grep -n "^\*\*Purpose"` → no match; the file no longer carries a single "Purpose: ratified through ADR-N" line in this form — superseded by restructuring, not by a targeted fix, but the specific false claim no longer exists on disk. |

**Recurrence note (not a formal finding — informational only, not run through tonight's verifier→skeptic pipeline):** `docs/archive/VISION.md`'s `last_reviewed: 2026-08-29` now predates its own last commit (`2026-09-13`, 15 days), the same *class* of staleness as the resolved prior-S3, on the same file, at a new file location (`docs/archive/VISION.md`, relocated from repo root per `CLAUDE.md` §5 item 5). Tonight's V2 verifier did independently catch two *different* VISION.md content defects at this same location (see NEW findings below) but did not separately flag the `last_reviewed` gap itself. Given a re-read is already the proposed fix for tonight's two VISION.md findings, one pass would close all three.

**NEW this cycle** (5 findings from tonight's independent V1/V2/V3 fan-out, all 5 survived the skeptic — see Findings below for full detail):

| Status | Finding | Severity |
|---|---|---|
| **NEW** | `docs/archive/VISION.md:16-19` still asserts MUST/`CANONICAL_MANDATORY[0]` status on all nine ADR-104 fleet members; the live registry retired it to `CANONICAL_RETIRED`/SHOULD on 2026-08-31 and the nine-member claim was itself refuted (tracked in eight) | HIGH |
| **NEW** | 2026-09-16 closure-census audit + `tasks/470-*.md` / `tasks/613-*.md` cite 15 "Proving SHA" values that do not exist as git objects anywhere in repo history | HIGH |
| **NEW** | `docs/archive/VISION.md:18-19` overstates its machine-site footprint ("thirteen machine constants plus five deploy manifests" vs actual eleven sites / six manifests) | MED |
| **NEW** | The synced anti-pattern text (CLAUDE.md, AGENTS.md, `templates/claude-regions/antipatterns-universal.md`, CONTRIBUTING.md) states a stale "43.50 KiB / 32 KiB cap" figure that no longer holds now that CLAUDE.md is byte-capped | MED |
| **NEW** | `CONTRIBUTING.md:19` states AGENTS.md is 5,714 B; current size is 5,843 B | LOW |

**Delta counts:** 8 resolved · 0 persisting · 5 new
**This run's own raw → survived → killed:** 5 → 5 → 0
**Skeptic kill-rate:** 0% (0 of 5 raw findings killed — every claim was independently re-verified against primary sources, including a `git cat-file -t` object-store lookup for the fabricated-SHA finding, before being kept)

---

## Summary

This pass raised 5 findings and the skeptic killed none (0% kill-rate) — every claim was independently re-verified against primary sources (direct file reads, byte counts, and `git cat-file -t` object lookups) and held up as genuine, unambiguous drift. All 8 items carried or newly raised in the 2026-08-10 baseline are now resolved: two by file deletion (`ESSENTIALS.md`, removing both the stale `/override` misinstruction and its own stale freshness stamp in one act), three by the repo *designing out* the drift class (carrier count and rule-edge count both moved from hardcoded prose to "computed, not restated" language pointing at the live source), one by a targeted freshness re-review, and two by document restructuring that removed the specific false claims (whether or not that restructuring was aimed at these findings specifically). Zero items are literally persisting.

Doc health this cycle is otherwise mixed. The always-on boot surfaces (`CLAUDE.md`, `AGENTS.md`, the generated command/ADR rosters) and the large majority of `JOURNAL.md`/`BACKLOG.md` provenance checked out clean — but `docs/archive/VISION.md` is stale on two independent content axes (its own retirement status and its machine-site counts) *and* has quietly drifted back into a stale `last_reviewed` stamp of the same class the prior baseline flagged and closed on a different file location, suggesting the freshness-cadence discipline around this specific file is fragile rather than fixed. Most seriously, a 2026-09-16 closure-census audit and two immutable task records cite 15 "Proving SHA" values that do not exist anywhere in the repository's git object store — meaning the provenance backing at least 15 CLOSED `BACKLOG.md` rows is currently unverifiable/fabricated, even though the underlying work for at least two of those rows (`#470`, `#613`) does genuinely exist under a different, uncited commit (`78823b0`). This is a real gap in exactly the audit trail `CLAUDE.md` §4 itself mandates ("resolve a locator before you act on it — a SHA you have not opened is a claim, not evidence"), baked into records the repo's own rules treat as immutable.

<!-- counts: raw=5 survived=5 killed=0 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 5 · **Survived skeptic:** 5 · **Killed false positives:** 0

### High (2)

**NEW** — `docs/archive/VISION.md:16-19` asserts a MUST-tier tracking status the live registry retired
- **Claim:** "It is a `MUST` on all nine ADR-104 fleet members ... it is `canonical_docs.CANONICAL_MANDATORY[0]`."
- **Location:** `docs/archive/VISION.md:16-19`
- **Evidence:** `sed -n '1,25p' docs/archive/VISION.md; sed -n '108,120p' scripts/canonical_docs.py; grep -n 'canonical-doc-vision' -A10 ecosystem/parity-surfaces.yaml`
- **Verdict:** contradicted
- **Proposed fix:** Update VISION.md's rationale block to reflect the 2026-08-31 retirement to `CANONICAL_RETIRED`/SHOULD tier and the eight-of-nine tracking figure, per `ecosystem/parity-surfaces.yaml`'s `canonical-doc-vision` row.
- **Note:** Skeptic directly re-read both cited files; the contradiction is exact, not a matter of interpretation. VISION.md's `last_reviewed` (2026-08-29) predates the 2026-08-31 retirement it fails to reflect — unpropagated drift, not a documented decision overriding the finding.

**NEW** — 15 "Proving SHA" values in a 2026-09-16 closure census and two task files do not exist in git
- **Claim:** Commit `0c120be` and `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md` cite specific "Proving SHA" values (e.g. `2812cd9d` for `#470`, `09fd7a00` for `#613`) as evidence that closed BACKLOG rows were "re-witnessed and closed."
- **Location:** `docs/audits/2026-09-16-technical-lane-ab-828-closure-census.md` (Table 1, "Proving SHA" column); `tasks/470-*.md`, `tasks/613-*.md`, and 13 other task files edited in commit `0c120be` (`#587 #591 #592 #596 #597 #600 #601 #605 #608 #626 #643 #653 #740`)
- **Evidence:** `for sha in 2812cd9d e806376e 8e832523 dd76e2b8 f8ae0f6d 6a4740ab b14306bc b043b9e1 79d5707b c52c5daa 09fd7a00 07e3adcb d30d1187 e73d4b84 f903a24; do git cat-file -t "$sha"; done` — every one prints `fatal: Not a valid object name`.
- **Verdict:** contradicted
- **Proposed fix:** File a correction audit that replaces the fabricated SHAs with the actual proving commit(s) (e.g. `78823b0` covers at least `#470`/`#613`'s underlying tests), or reopen the affected rows pending real evidence — the immutable audit and CLOSED annotations cannot be edited in place per `CLAUDE.md` §5 rule 3.
- **Note:** Skeptic independently re-ran `git cat-file -t` on all 15 SHAs; every one fails. The underlying work for at least `#470` (cp1252-encodable check-summary tests) and `#613` (routing-table agreement test) does genuinely exist, but was introduced by commit `78823b0`, not the cited SHAs — a real provenance failure in an immutable governance record, not explainable by any documented decision.

### Med (2)

**NEW** — `docs/archive/VISION.md:18-19` overstates its own machine-site footprint
- **Claim:** "thirteen machine constants plus five deploy manifests read its name or its `## H2` spine."
- **Location:** `docs/archive/VISION.md:18-19`
- **Evidence:** `sed -n '1,10p;50,70p' scripts/canonical_docs.py; grep -rl VISION deploy/*.yaml`
- **Verdict:** contradicted
- **Proposed fix:** Correct to "eleven machine sites (ten constants + one JS site) plus six deploy manifests," or drop the hardcoded numbers per the hub's own "never restate a count or roster in prose" convention (`CLAUDE.md` §4).
- **Note:** Both counts independently re-verified by direct read/grep; no documented decision changes these numbers — a miscount in VISION.md's prose.

**NEW** — The synced anti-pattern text's "43.50 KiB / 32 KiB cap" figure is stale
- **Claim:** "a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently," stated in present tense and duplicated verbatim in `CLAUDE.md:218`, `AGENTS.md:37`, `templates/claude-regions/antipatterns-universal.md:4`, and `CONTRIBUTING.md:32`.
- **Location:** `CLAUDE.md:218` (synced copies: `AGENTS.md:37`, `templates/claude-regions/antipatterns-universal.md:4`, `CONTRIBUTING.md:32`)
- **Evidence:** `wc -c CLAUDE.md AGENTS.md` → 24,571 B + 5,843 B = 30,414 B (29.70 KiB), under the 32 KiB cap; `grep -n '43.50 KiB' CLAUDE.md AGENTS.md templates/claude-regions/antipatterns-universal.md CONTRIBUTING.md`
- **Verdict:** contradicted
- **Proposed fix:** Re-measure and update the figures across all four synced copies (or reword to a relative/computed claim), now that `CLAUDE.md` is byte-capped to ≤24,576 B by `tests/test_claude_md_byte_cap.py`.
- **Note:** The 43.50 KiB figure traces to a one-time 2026-08-22 measurement (`docs/audits/2026-08-22-technical-intake-r1-decision-packet.md:45`, CLAUDE.md at 44,542 B then) that predates the later byte-cap reduction — the exact class of stale hardcoded number `CLAUDE.md` itself warns against, duplicated across 4 files via the hub-region sync mechanism.

### Low (1)

**NEW** — `CONTRIBUTING.md:19` states a stale AGENTS.md byte count
- **Claim:** "`AGENTS.md` — now exists" (added 2026-08-29, 5,714 B).
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B; `git log --oneline -5 -- AGENTS.md`
- **Verdict:** contradicted
- **Proposed fix:** Update the byte figure to match AGENTS.md's current size, or remove the hardcoded count per the hub's "never restate a count" convention.
- **Note:** AGENTS.md was last modified 2026-09-13, after CONTRIBUTING.md's 2026-09-10 `last_reviewed` stamp — expected-class drift, currently incorrect.

---

## Killed Findings

None. All 5 findings raised by tonight's V1/V2/V3 fan-out survived adversarial skeptic review (0% kill rate this cycle).

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries, 2026-09-17):**
- All 10 checked JOURNAL entries' anchor/merge commits exist in git log with matching subjects, bodies, and `--stat` file sets (entries q through z, all dated 2026-09-17) ✓
- `worktree-lane-aa-13-resource-lifecycle` branch confirmed absent both locally and on origin, consistent with a claimed teardown ✓
- Closure commit `0c120be2`'s message lists exactly the 25 `[#id]`s the JOURNAL claims closed, plus `[#828]`/`[#829]`/`[#830]` ✓
- SHALLOW-HISTORY GUARD: repo is shallow (boundary 2026-09-13, oldest visible commit `2d02727`); all 10 checked entries dated 2026-09-17, within available history — no corroboration blocked by truncation ✓
- Omission check: the single newest commit in `git log` (`87638c8`) is entry (z)'s own anchor/merge — no significant merged work sits above the newest JOURNAL entry unmentioned ✓

**V2 (living-doc factual claims):**
- CLAUDE.md's "≤200 lines... WARN-only" framing matches `scripts/validate_doc_rot.py`'s `_FILE_SIZE_BUDGETS` ✓
- CLAUDE.md's "≤24,576 B" byte cap is satisfied: actual size 24,571 B, under the cap per `tests/test_claude_md_byte_cap.py` ✓
- CONTRIBUTING.md's ruff pre-commit hook description (pinned rev `astral-sh/ruff-pre-commit @ v0.15.5`) matches `.pre-commit-config.yaml` and `pyproject.toml` ✓
- CLAUDE.md §7's repo-command roster (8 commands) matches the actual frontmatter of the 8 files under `.claude/commands/*.md` verbatim ✓
- CLAUDE.md §11's recent-ADR roster (ADR-115 Accepted, 116/117/118 Proposed, 119 Accepted) matches the Status lines in `docs/decisions/ADR-115..119-*.md`; 119 confirmed the highest-numbered ADR on disk ✓
- CLAUDE.md §9's local-vs-manual pre-commit hook split matches `.pre-commit-config.yaml` exactly (index-freshness + pre-push hooks local, rest `stages: [manual]`) ✓

**V3 (BACKLOG closure semantic coherence, commit `0c120be` and window):**
- BACKLOG closures `#744`, `#742`, `#743`, `#750`, `#751`, `#752`, `#765`, `#780`, `#784`, `#785` — all 10 "Proving SHA" values independently resolve to real commits, each consistent with the row's stated Done-when ✓ (contrast with the 15 fabricated SHAs in the same closure commit, flagged above — this run checked both populations, not just the defective one)

---

## Next Actions (proposals for operator)

1. **HIGH** — File a correction audit replacing the 15 fabricated "Proving SHA" values in the 2026-09-16 closure census (and `tasks/470-*.md`, `tasks/613-*.md`) with real proving commits (`78823b0` covers at least two), or reopen the affected rows pending real evidence.
2. **HIGH** — Re-read `docs/archive/VISION.md` end-to-end: fix the CANONICAL_RETIRED/SHOULD tracking-status claim and the machine-site/manifest counts in one pass (both MED findings below ride the same re-read), and bump `last_reviewed` past 2026-09-13 while there (closes the recurrence note above too).
3. **MED** — Re-measure and update the "43.50 KiB / 32 KiB" anti-pattern figure across all 4 synced copies (`CLAUDE.md`, `AGENTS.md`, `templates/claude-regions/antipatterns-universal.md`, `CONTRIBUTING.md`), or reword to a relative/computed claim.
4. **LOW** — Update `CONTRIBUTING.md:19`'s AGENTS.md byte figure (5,714 B → 5,843 B), or drop the hardcoded count.
5. **(INFRASTRUCTURE, persisting since ≥2026-08-02, still unresolved 39 nights later)** Upgrade cloud runtime `uv` to `==0.11.19`. Fires on every Stop-hook check.
6. **(PROCESS, positive signal)** The native `Workflow` launcher ran cleanly end-to-end tonight for the first time in this digest's recorded history. Worth one more confirming run before treating "native path" as the reliable default going forward.

---

## Safety Tripwire

`git status --porcelain` output at digest write time (before this file was staged):

```
?? docs/audits/2026-09-18-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. Safety check passes.
