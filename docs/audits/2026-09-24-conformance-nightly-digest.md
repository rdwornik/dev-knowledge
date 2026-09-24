<!-- scope: meta -->
# Nightly Conformance Digest — 2026-09-24

**Date:** 2026-09-24
**Author:** Claude Code (claude-sonnet-5), native Workflow launcher
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** Native `Workflow` launcher was attempted first (`.claude/workflows/conformance-hub.js` via the Workflow tool, name `"conformance-hub"`), per the nightly re-probe instruction. **It succeeded end to end this time** — a change from the 2026-08-10 run, which recorded the launcher as invocable but faulting on a `StructuredOutput`/permission-handler bug across all three Stage-1 verifiers, and from earlier runs (2026-08-03 through 2026-08-09) that recorded it as not enabled in the cloud runtime at all. Tonight all 5 agents completed with zero errors, zero empty results, and no fallback to spec-orchestration was needed.

| Stage | Label | Model actually used | Duration | Tokens |
|---|---|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-5 | 70s | 76,184 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-5 | 297s | 129,351 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-5 | 200s | 119,034 |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-5 | 131s | 69,616 |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-5 | 28s | 51,563 |

**Platform re-probe signal for the operator:** the script's phase metadata names Opus for Stage 2 (skeptic) and Stage 3 (digest) — those `agent()` calls carry no explicit `model` override in `conformance-hub.js`, so they ran on the session default (claude-sonnet-5) rather than Opus. This is the same behavior as the script's literal code (only the three Stage-1 `agent()` calls pin `model: 'claude-sonnet-5'` explicitly; Stage 2/3 do not pin a model at all), so it is not a bug — just worth flagging since the `phases` metadata's parenthetical ("Opus") no longer describes what actually runs, if that was ever the intent. Total run: 5/5 agents done, 0 errors, 0 empty results, 87 tool calls, 445,748 subagent tokens, ~461s wall time.

---

## Delta vs Prior Baseline

**Prior digest used for delta:** `docs/audits/2026-08-10-conformance-nightly-digest.md` — the most recent conformance-nightly digest found under `docs/audits/`. **Gap: 45 days** (2026-08-10 → 2026-09-24). No `claude/conformance-*` branches remain open (`git branch -a` shows none), consistent with the per-repo git-discipline rule that an absorbed conformance branch deletes at its own merge — so the 45-day gap reflects no *nightly runs* recorded under `docs/audits/`, not an absorption backlog like the one `[#426]` diagnosed on 2026-08-10.

All 8 of 2026-08-10's findings (5 carried + 3 new that cycle) were checked against current `origin/main` (`aca2385`):

| Status | 2026-08-10 finding | This run's evidence |
|---|---|---|
| **RESOLVED** | HIGH — carried S1: `protocols/ESSENTIALS.md:123` told agents `/override [reason]` was the only session-end escape (stale since ADR-85 §A2, 2026-08-03) | `ls protocols/ESSENTIALS.md` → **file does not exist**. CLAUDE.md's own header confirms: "`protocols/ESSENTIALS.md` was **deleted 2026-09-14** (`[#628]`) — its doctrine lives in PLAYBOOK." The one remaining `/override [reason]` mention, in `protocols/DEFINITION_OF_DONE.md:49`, is itself explicitly flagged inline: "**BOTH CLAUSES ARE SUPERSEDED; do not act on this line.**" — correctly handled, not a live defect. |
| **RESOLVED** (historical, not recurring) | HIGH — T1: commit `cd38fb8` claimed to close `[#213] [#215] [#441]` without discharging them | Was explicitly logged as a one-time historical event, self-corrected 18 minutes later in the same session (commit `a62d988`) — not a standing claim that could "persist." Tonight's independent V3 fan-out (different window, 2026-09-03 → HEAD) found no analogous false-closure claim in the current window. |
| **RESOLVED** (moot — structural rewrite) | MED — carried S2: `ARCHITECTURE.md` said "five carriers" at 4 locations against six `carrier_*.py` files | `grep -n "five carrier" ARCHITECTURE.md` → no output. `ls deploy/carrier_*.py \| wc -l` → still 6. The passage no longer exists in this form — subsumed by the 2026-09-18 "BUILD MODE cut" (110,357 B → current 23,849 B) that tonight's own killed finding independently documents. |
| **NOT INDEPENDENTLY RE-VERIFIED this cycle** (status: superseded, folded into tonight's related finding) | MED — carried S3: `VISION.md` `last_reviewed: 2026-07-25` predated its last commit (11-day gap at 2026-08-10) | File relocated `docs/archive/VISION.md` ([#614] lane-e-5, 2026-09-01), `status: superseded`, `last_reviewed` now `2026-08-29`; last commit touching the file `2026-09-18` (20-day gap, unconfirmed whether content or incidental). Tonight's V2 fan-out did examine this file and surfaced a **different, related** issue (see New findings below: the file's own "why still here" rationale is stale against the [#614] retirement) rather than re-checking the bare freshness stamp — so this line item is folded into today's finding rather than independently carried forward. |
| **RESOLVED** (file deleted) | MED — carried S4: `protocols/ESSENTIALS.md` `last_reviewed: 2026-07-30` predated its last commit | Moot — file deleted 2026-09-14 (see S1 above). |
| **RESOLVED** (moot — structural rewrite) | MED — T2: `ARCHITECTURE.md:405` claimed `validate_doc_code_edge.py` was "live on 13 rules" (actual 15) | `grep -n "rule-edge\|live on 1[0-9] rules" ARCHITECTURE.md` → no output. The enumeration itself no longer exists in the post-BUILD-MODE-cut file. |
| **RESOLVED** (moot — structural rewrite) | LOW — carried S5: `ARCHITECTURE.md` pre-commit gates paragraph omitted `block-unanchored-push` | `grep -n "block-unanchored\|pre-push" ARCHITECTURE.md` → no output; the old enumerated hooks paragraph this finding pointed at no longer exists in the cut file. |
| **RESOLVED** (moot — structural rewrite) | LOW — T3: `ARCHITECTURE.md:95` Purpose line said "ratified through ADR-109" against the file's own ADR-110 changelog entry | `grep -n "ratified through ADR-1" ARCHITECTURE.md` → no output; the Purpose-line phrasing this finding cited no longer exists. |

**Delta counts:** 8 resolved (6 via the 2026-09-14/09-18 structural cuts, 1 via explicit file deletion, 1 historical/non-recurring) · 0 persisting · 0 not-independently-re-verified as a carried item (folded into a new finding instead) · **5 new** (this cycle's own survivors)

**This run's own raw → survived → killed:** 6 → 5 → 1
**Skeptic kill-rate:** 17% (1 of 6) — the killed finding (ARCHITECTURE.md's historical "BUILD MODE cut... was 110,357 B; target ≤15 KB" line) was ruled true-but-irrelevant: it is past-tense cut provenance, not a live, tested size invariant (no `tests/test_architecture_md_byte_cap.py` equivalent exists, unlike CLAUDE.md's gated `≤24,576 B`).

---

## Summary

The prior baseline's entire findings set — all 8 items from 2026-08-10, including the operationally risky HIGH-severity `/override` misinstruction — is now moot, mostly as a side effect of two large structural events since: `protocols/ESSENTIALS.md`'s deletion (2026-09-14, `[#628]`) and `ARCHITECTURE.md`'s "BUILD MODE cut" (2026-09-18, ~110 KB → ~23.8 KB). No line-by-line fix was applied to most of these; they were swept away by the surrounding rewrite. That is a favorable outcome for the specific claims, but it also means this cycle cannot confirm any of the 2026-08-10 findings were *deliberately* corrected versus incidentally removed — worth the operator's awareness if similar large cuts happen again, since a doc-claim could equally be re-introduced by a future rewrite without anyone re-checking it.

Tonight's own independent V1/V2/V3 fan-out found the doc-health picture is otherwise narrow: V1 (JOURNAL vs git) and V3 (BACKLOG closure coherence) came back **fully clean** — zero findings across 54 checked commit anchors, all 15 recent merges, and a careful backlog-window analysis that correctly recognized several non-issues (Wave-4b lane rows staying `status: open` by design, a disclosed backlog-filing deferral, a branch-sync commit's `+status: closed` lines being pre-existing history becoming visible rather than new closures). All 6 raw findings came from V2 (living-doc claims), and after the skeptic killed 1 as irrelevant, 5 survived: 2 HIGH, 2 MED, 1 LOW. The two HIGH findings are both "prose fell behind a decision" cases — `docs/archive/VISION.md`'s own "why still here" rationale still asserting the pre-[#614] MUST/`CANONICAL_MANDATORY[0]` status that was retired to SHOULD/`CANONICAL_RETIRED` on 2026-08-31, and `CLAUDE.md:102`'s restated count of `git-discipline.md`'s `verify:` lines (claims three, live file has five) — the latter a direct instance of the anti-pattern CLAUDE.md's own conventions section warns against ("Never restate a count or roster in prose"). The two MED findings are both instances of the same root cause: `CLAUDE.md` §4 and `CONTRIBUTING.md`'s validators table both assert `ruff` (and, in CONTRIBUTING.md's case, `audit-health` and several other hooks) "blocks" at commit, but the 2026-09-17 hook-role move put them at `stages: [manual]`, not yet re-armed. The LOW finding is a small hardcoded byte count in CONTRIBUTING.md drifting from the live file by 129 bytes.

The systemic `uv` infrastructure mismatch flagged in the 2026-08-10 digest's Next Actions (cloud runtime version vs the pinned `==0.11.19`) also continues: it fired on every Stop-hook check during this session, unresolved at least 45 nights later.

<!-- counts: raw=6 survived=5 killed=1 -->

---

## Findings (PROPOSALS ONLY)

**This run's raw:** 6 · **Survived skeptic:** 5 · **Killed false positives:** 1

### High (2)

**NEW** — `docs/archive/VISION.md:17-18` still claims the file "is a MUST on all nine ADR-104 fleet members" and "is `canonical_docs.CANONICAL_MANDATORY[0]`", but `[#614]` lane-a retired it to SHOULD / `CANONICAL_RETIRED` on 2026-08-31
- **Claim:** VISION.md's own "why this file is still here" rationale asserts present-tense MUST status and `CANONICAL_MANDATORY[0]` membership.
- **Location:** `docs/archive/VISION.md:17-18`
- **Evidence:** `grep -n -A6 'id: canonical-doc-vision' ecosystem/parity-surfaces.yaml` → tier `{hub: SHOULD, consumer: SHOULD}`, reason string "VISION.md — RETIRED from the fleet-wide MUST set 2026-08-31 ([#614] lane-a)". `grep -n -A2 'CANONICAL_MANDATORY: tuple' scripts/canonical_docs.py` → `(ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS)`, VISION absent (index 0 is ARCHITECTURE). `grep -n 'CANONICAL_RETIRED: tuple' scripts/canonical_docs.py` → VISION lives there instead.
- **Verdict:** contradicted
- **Proposed fix:** Update VISION.md's rationale paragraph to reflect the 2026-08-31 retirement to SHOULD/`CANONICAL_RETIRED`, replacing the MUST/`CANONICAL_MANDATORY[0]` justification with the current retained-for-machine-constants rationale.
- **Note:** ADR-114 (2026-08-29), which VISION.md itself cites, recorded the tier as MUST at the time the claim was written — so it was true when `last_reviewed` was stamped. The decision that invalidated it (`[#614]` lane-a, 2 days later) is what changed; the doc never caught up. Not excused by a documented decision — the decision is precisely the disproof.

**NEW** — `CLAUDE.md:102` (§5 rule 7) says `git-discipline.md` carries "three `verify:` lines plus two standing operator orders"; the live file has five `verify:` lines and a third, unnamed operator-order section
- **Claim:** "`git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES)"
- **Location:** `CLAUDE.md:102`
- **Evidence:** `grep -n 'verify:' .claude/rules/git-discipline.md` → 5 matches (lines 12, 51, 76, 87, 102). `grep -n '^###' .claude/rules/git-discipline.md` → a third order-shaped section, "THE HANDOFF MERGE IS ATOMIC WITH TEARDOWN" (line 54), not named by the claim.
- **Verdict:** contradicted
- **Proposed fix:** Correct the count to five `verify:` lines and name all three operator-order sections, or drop the itemized count entirely per the repo's own "never restate a count or roster in prose" rule (§4).
- **Note:** This is a direct instance of the anti-pattern CLAUDE.md's own §4 conventions section warns against.

### Med (2)

**NEW** — `CLAUDE.md:65` (§4 Linting) states `ruff check` "is also a pre-commit gate (§9) and blocks"; the live hook is `stages: [manual]`
- **Claim:** "`uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks"
- **Location:** `CLAUDE.md:65`
- **Evidence:** `grep -n -A4 '  - id: ruff' .pre-commit-config.yaml` → `stages: [manual]`, with a comment recording the hook was moved to the Actions conductor 2026-09-17 and not re-armed in the B2 lane4 hook-role review.
- **Verdict:** contradicted
- **Proposed fix:** Update the Linting line to note `ruff` currently runs `stages: [manual]` (moved to the conductor 2026-09-17, not re-armed) and does not block a plain `git commit` today — consistent with CLAUDE.md's own §9 preamble, which already says "rest `stages: [manual]`".
- **Note:** An internal inconsistency within the same file: §9's preamble already states the correct current condition; §4 has simply not been updated to match.

**NEW** — `CONTRIBUTING.md`'s validators table lists `ruff` and `audit-health` (plus several other rows) as `Stage: commit`, blocking; several are actually `stages: [manual]` since the 2026-09-17 hook-role move
- **Claim:** Validators table rows for `ruff` ("Blocks on violations") and `audit-health` ("FAIL-level findings block the commit") both claim Stage: commit.
- **Location:** `CONTRIBUTING.md:169-170` (Validators table)
- **Evidence:** `grep -n -A3 '  - id: ruff' .pre-commit-config.yaml` and same for `audit-health` → both `stages: [manual]`; `grep -n 'health: DEGRADED' docs/audits/2026-09-18-technical-b2-lane4-hook-role-review.md` confirms `audit-health` is additionally recorded as currently broken. The same table's rows for `normalize-dated-headers`, `toc-freshness-playbook`, `check-seal-identity`, and `validate-backlog` are also confirmed `stages: [manual]` live, so the drift is fleet-wide across the table, not a one-off.
- **Verdict:** contradicted
- **Proposed fix:** Add a manual-stage / conductor-report-only caveat to the affected rows, or regenerate the table from `.pre-commit-config.yaml` so it can't drift again; `CONTRIBUTING.md`'s `last_reviewed` (2026-09-10) predates the 2026-09-17 hook-role move by a week.
- **Note:** Same root cause as the CLAUDE.md finding above (the 2026-09-17 hook-role move), surfacing in a second document.

### Low (1)

**NEW** — `CONTRIBUTING.md:19` states `AGENTS.md` was "added 2026-08-29, 5,714 B"; current file is 5,843 B
- **Claim:** "the file a cross-vendor agent would conventionally read at the repo root — `AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"
- **Location:** `CONTRIBUTING.md:19`
- **Evidence:** `wc -c AGENTS.md` → 5,843 B, not 5,714 B. (This clone is shallow, history for `AGENTS.md` only reaches back to 2026-09-18, so whether 5,714 B was accurate at the original 2026-08-29 add commit can't be independently confirmed here — but the number no longer matches the file's current, live state, which is what a reader would check it against.)
- **Verdict:** unsupported
- **Proposed fix:** Drop the hardcoded byte count from CONTRIBUTING.md prose per the repo's own "never restate a count in prose" rule, or replace it with a pointer to a live `wc -c AGENTS.md` check.
- **Note:** Severity is low because the drift is small (129 B) and the file is expected to change incrementally; still the same restated-count anti-pattern as the CLAUDE.md HIGH finding above.

---

## Killed Findings

**1 killed** (of 6 raw) — 17% kill rate.

**Claim:** `ARCHITECTURE.md`'s "BUILD MODE cut (2026-09-18, B2 lane 1): was 110,357 B; target ≤15 KB" is contradicted because the file is now 23,849 B, ~59% over target.
**Kill reason:** true-but-irrelevant
**Kill detail:** The sentence is past-tense provenance for a dated one-time cut ("was X; target Y. Removed: …"), not an ongoing invariant claim about the file's current size. Unlike CLAUDE.md's explicit gated budget ("≤24,576 B, gated by `tests/test_claude_md_byte_cap.py`"), no test enforces an ARCHITECTURE.md byte cap (confirmed: only `test_claude_md_byte_cap.py` and `test_agents_md_byte_cap.py` exist under `tests/`). A living doc growing after a historical reduction pass is expected and not itself a documented rule violation.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries, 2026-09-22 (f) through 2026-09-24 (b)):**
- All 54 distinct commit SHAs cited across the window exist in git log with matching subject lines ✓
- All 15 merge commits in `git log --merges -20` map 1:1 onto merges narrated across the last 10 JOURNAL entries; no extra unlogged merge sits between the oldest covered entry and HEAD ✓
- HEAD (`aca2385`) equals the newest JOURNAL entry (2026-09-24 (b)) — nothing merged into main postdates the JOURNAL's last entry ✓
- Shallow-history boundary: repo history starts 2026-09-18 (`f3eba9b`); all cited SHAs fall within available history, none out-of-scope ✓
- Repair/refusal histories are accurately narrated where they occur (e.g. 2026-09-23 (b)'s handback-organ repair correctly describes a never-on-main commit as such; 2026-09-22 (g)'s two-repair rebuild) ✓

**V2 (living-doc factual claims — `docs/archive/VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`; `protocols/PLAYBOOK.md` out of scope per the domain spec):**
- ARCHITECTURE.md's quality-requirements block ("v1.0.0, 29 requirement(s), 8 measured, 21 candidate") matches a live count of `ecosystem/quality-requirements.yaml` ✓
- ARCHITECTURE.md's Codemap block (2 orphan modules, no dependency edges) matches a live regen ✓
- ARCHITECTURE.md's organ-map "8 classes" claim matches `ecosystem/organ-index.md`'s 8 `## ` headers ✓
- CLAUDE.md's byte-cap claim ("≤24,576 B") holds — live file is 23,651 B ✓
- CLAUDE.md/ARCHITECTURE.md's `reconciled_with: handoff-process@7.1.0` stamp matches `protocols/HANDOFF_PROCESS.md`'s stated version ✓
- CLAUDE.md §11's ADR roster (116–120) matches the highest-numbered ADR on disk ✓
- CLAUDE.md/ARCHITECTURE.md's "B2 lane4 armed 13" figure matches the B2 lane4 audit's own table and live hook stage assignments ✓
- ~14 cross-referenced file paths spot-checked across ARCHITECTURE.md/CONTRIBUTING.md all exist on disk; CONTRIBUTING.md's ruff pinned-rev claim (`v0.15.5`) matches `.pre-commit-config.yaml` and `pyproject.toml` ✓

**V3 (BACKLOG closure semantic coherence, 2026-09-03 → HEAD — the actual ~3-week window; the task text's literal `--since=2026-05-14` was a stale/miscalculated date, correctly identified and worked around rather than followed blindly):**
- Zero non-merge commits in the window flipped any `tasks/*.md` `status:` from `open`/`deferred` to `closed` — verified by pairing every `-status:`/`+status:` diff hunk across all 25 non-merge commits touching `tasks/*.md` ✓
- The literal instruction's `git log --all --since=... --grep="closes \[#"` convention returns zero matches in this repo; the real closing convention is a bare `[#id]` tag enforced by the `backlog-id-on-close` hook — confirmed not violated ✓
- The one commit introducing many `+status: closed` lines in-window (`beae756e`, a branch-merge/sync commit) is pre-existing off-window history becoming visible, not an authored closure event ✓
- Wave-4b lane rows `#956`–`#962` correctly remain `status: open` despite "landed"/"merged" JOURNAL language, consistent with each row's own "close nothing" Done-when step — not a coherence defect ✓
- The 2026-09-24 memory-admission-gate lane landing with no BACKLOG row of its own is a disclosed, intentional filing deferral per its own audit doc, not an omission ✓

---

## Next Actions (proposals for operator)

1. **HIGH** — Update `docs/archive/VISION.md`'s "why this file is still here" rationale (lines 17-18) to reflect the 2026-08-31 `[#614]` retirement to SHOULD/`CANONICAL_RETIRED`.
2. **HIGH** — Correct `CLAUDE.md:102`'s `git-discipline.md` tally to five `verify:` lines and name the third operator-order section, or drop the itemized count.
3. **MED** — Revise `CLAUDE.md:65`'s Linting line to reflect `ruff`'s current `stages: [manual]` status (moved to the conductor 2026-09-17, not re-armed).
4. **MED** — Revise `CONTRIBUTING.md`'s validators table (`ruff`, `audit-health`, and the other now-manual rows) to match live `.pre-commit-config.yaml` stage assignments, ideally by generating the table rather than hand-authoring it.
5. **LOW** — Drop or refresh the hardcoded `AGENTS.md` byte count at `CONTRIBUTING.md:19` (currently 5,843 B, not 5,714 B).
6. **(PROCESS observation, not a finding)** — All 8 of the 2026-08-10 baseline's findings were resolved as a side effect of two large structural changes (the `ESSENTIALS.md` deletion and the `ARCHITECTURE.md` BUILD MODE cut) rather than by individually verified fixes. Worth the operator's awareness that a future large rewrite could just as easily silently reintroduce a stale claim as remove one — this digest's delta section could not distinguish "deliberately fixed" from "incidentally removed" for 6 of the 8 baseline items.
7. **(INFRASTRUCTURE, persisting since ≥2026-08-02)** — Upgrade cloud runtime `uv` to `==0.11.19`. Fired on every Stop-hook check this session; still unresolved at least 45 nights later.
8. **(PLATFORM, notable but not a doc finding)** — Tonight is the first fully-successful native `Workflow` launcher run recorded in this digest series (prior runs: unavailable, or available-but-faulting). Also note the skeptic/digest stages ran on `claude-sonnet-5`, not the Opus the script's `phases` metadata parenthetical implies — `conformance-hub.js`'s Stage 2/3 `agent()` calls carry no explicit model pin, so they inherit the session default. Neither is a doc-conformance defect; flagged here purely as the platform re-probe record this section exists to capture.

---

## Safety Tripwire

`git status --porcelain` output at digest write time, on branch `claude/conformance-2026-09-24`:

```
?? docs/audits/2026-09-24-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. ✓ Safety check passes.
