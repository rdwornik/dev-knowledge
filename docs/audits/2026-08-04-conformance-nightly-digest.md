<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-04

**Date:** 2026-08-04
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-04; confirmed unavailable, consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-08-02-conformance-nightly-digest.md`
**Gap:** 2 days (2026-08-02 → 2026-08-04; no conformance digest was run on 2026-08-03)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING (upgraded MED→HIGH)** | prior S1 (MED): CONTRIBUTING.md §"Nightly outcome management" describes deleted Action as live | Today's skeptic upgrades to HIGH: ARCHITECTURE.md Ch6 warning is not an ADR-ratified accepted state. Persisting unfixed since 2026-07-31 (5 nights). |
| **PERSISTING (upgraded MED→HIGH)** | prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit | Today's skeptic upgrades to HIGH: gap has widened — last commit is now 2026-07-31 (6-day gap, up from 1-day). Persisting unfixed since 2026-07-31. |
| **NEW (HIGH)** | protocols/ESSENTIALS.md `last_reviewed: 2026-07-30` predates last commit 2026-07-31 | Prior K3 was killed as forward-dated (last commit was 2026-07-29 on 08-02). A new commit on 2026-07-31 flipped the stamp to backward-dated; now an A2 FAIL. |
| **NEW (MED)** | CONTRIBUTING.md Validators table lists 15 hooks; actual count is 17 | Two hooks added after CONTRIBUTING.md's last commit (2026-07-31): `check-seal-identity` ([#475]) and `block-unanchored-push` (ADR-85 §A5). |
| **NEW (MED)** | ARCHITECTURE.md:327 describes block_ff_push.py as "fail-soft to exit 0 on any git error" | ADR-85 amendment §A6 (2026-08-03) changed posture to fail-CLOSED (exit 2). ARCHITECTURE.md was last committed 2026-08-02 — one day before the amendment. |
| **NEW (MED)** | CONTRIBUTING.md:118 describes block-ff-push as "fail-soft" | Same root cause as ARCHITECTURE.md finding above. CONTRIBUTING.md predates the ADR-85 §A6 amendment. |
| **RESOLVED** | — | None. |
| **KILLED** | V1 LOW: terra finding count says "1C+5H" but commits total 1C+6H | true-but-irrelevant: all 7 fixes committed; count error in prose triggers no gate. |
| **KILLED** | V3 LOW: #458 Done-when requires PLAYBOOK re-read not performed | evidence-not-definitive: PLAYBOOK is not in _FRESHNESS_FILES; Done-when clause was miscalibrated against a mechanism that doesn't apply. |

**Delta counts:** 0 resolved · 2 persisting (upgraded) · 4 new · 2 killed
**Raw → survived → killed:** 8 → 6 → 2
**Skeptic kill-rate:** 25% (2 of 8 raw findings killed)

---

## Summary

Today's run surfaces the most significant single-night finding increase in recent history: 6 survivors (3 HIGH, 3 MED) up from 2 (both MED) on 2026-08-02. The increase is driven by two root causes. First, the ADR-85 amendment applied 2026-08-03 introduced a fail-CLOSED posture change to `block_ff_push.py` that neither ARCHITECTURE.md (last committed 2026-08-02) nor CONTRIBUTING.md (last committed 2026-07-31) reflects — producing two new MED contradictions. Second, ESSENTIALS.md received a commit on 2026-07-31 that advanced its last-commit date past its `last_reviewed: 2026-07-30` stamp, converting what was a killed forward-dated entry (K3, 08-02) into a backward-dated A2 FAIL. The two persisting findings (CONTRIBUTING.md dead Action, VISION.md backward-dated stamp) were both upgraded from MED to HIGH: the dead Action because no ADR formally accepts the stale state, and the VISION.md stamp because the gap has widened from 1 day to 6 days. The 25% kill-rate (2 of 8) is lower than the 78% seen on 08-02, reflecting that today's raw findings are mostly concrete, code-verifiable contradictions rather than the heuristic journal-vs-prose mismatches that typically inflate raw counts and fall to the skeptic.

<!-- counts: raw=8 survived=6 killed=2 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 8 · **Survived skeptic:** 6 · **Killed false positives:** 2

### High (3)

**S1** — VISION.md `last_reviewed: 2026-07-25` backward-dated vs last commit 2026-07-31 (A2 violation, widening gap)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git log --date=short --format='%cd' -- VISION.md | head -1` → `2026-07-26` (at 08-02 baseline); confirmed `2026-07-31` today — gap now 6 days.
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to on or after 2026-07-31.
- **Skeptic note:** VISION.md is in DEFAULT_FRESHNESS_FILES; audit check A2 FAIL fires. No ADR authorizes this gap. Persisting since 2026-07-31 (5 nights); upgraded HIGH because gap has widened and mitigation is absent.

**S2** — protocols/ESSENTIALS.md `last_reviewed: 2026-07-30` backward-dated vs last commit 2026-07-31 (A2 violation, NEW)
- **Claim:** protocols/ESSENTIALS.md was reviewed end-to-end on 2026-07-30 (frontmatter stamp).
- **Location:** `protocols/ESSENTIALS.md:2`
- **Evidence:** `git log --date=short --format='%cd' -- protocols/ESSENTIALS.md | head -1` → `2026-07-31`
- **Verdict:** contradicted
- **Proposed fix:** Re-read protocols/ESSENTIALS.md end-to-end and bump `last_reviewed` to on or after 2026-07-31.
- **Skeptic note:** ESSENTIALS.md is explicitly in DEFAULT_FRESHNESS_FILES. Previously killed (K3, 08-02) as forward-dated because last commit was 2026-07-29. A new commit on 2026-07-31 flipped the relationship. No ADR authorizes this gap.

**S3** — CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null || echo NOT_EXISTS` → `NOT_EXISTS`
- **Verdict:** contradicted
- **Proposed fix:** Rewrite CONTRIBUTING.md §"Nightly outcome management" (lines 128–176) to replace the present-tense Action description with a tombstone note pointing to ARCHITECTURE.md Ch6 for the live loop description.
- **Skeptic note:** `.github/` confirmed absent (deleted commit 82227f08, 2026-07-08, merged [#255]). ARCHITECTURE.md Ch6 warns against following CONTRIBUTING.md here but is a warning, not an ADR-ratified accepted state. Upgraded HIGH (from MED on 08-02) because no documented decision formally defers the fix. Persisting since 2026-07-31 (5 nights).

### Med (3)

**S4** — CONTRIBUTING.md Validators table lists 15 hooks; actual .pre-commit-config.yaml has 17 (omission, NEW)
- **Claim:** CONTRIBUTING.md Validators table reflects the complete pre-commit hook roster.
- **Location:** `CONTRIBUTING.md:100`
- **Evidence:** `grep -c '^ *- id:' /home/user/dev-knowledge/.pre-commit-config.yaml` → `17`
- **Verdict:** omitted
- **Proposed fix:** Add `check-seal-identity` and `block-unanchored-push` rows to the CONTRIBUTING.md Validators table to reflect the actual 17-hook roster.
- **Skeptic note:** Two hooks added after CONTRIBUTING.md's last commit (2026-07-31): `check-seal-identity` ([#475], wired 2026-08-02) and `block-unanchored-push` (ADR-85 §A5, added 2026-08-03). No ADR documents this omission as intentional.

**S5** — ARCHITECTURE.md:327 describes block_ff_push.py as "fail-soft to exit 0 on any git error" (contradicted by ADR-85 §A6, NEW)
- **Claim:** block_ff_push.py exits 0 (fail-soft) on internal git errors.
- **Location:** `ARCHITECTURE.md:327`
- **Evidence:** `grep -n 'exit 2\|fail CLOSED\|ADR-85' /home/user/dev-knowledge/scripts/block_ff_push.py | head -5`
- **Verdict:** contradicted
- **Proposed fix:** Update ARCHITECTURE.md organ map entry for block-ff-push to replace "fail-soft to exit 0 on any git error" with "fail-CLOSED (exit 2) on any internal error per ADR-85 amendment 2026-08-03 §A6"; also add block-unanchored-push to the organ map (currently absent).
- **Skeptic note:** block_ff_push.py line 228 explicitly reads `# ADR-85 amendment 2026-08-03 §A6: fail CLOSED` and returns 2. ARCHITECTURE.md was last committed 2026-08-02 — one day before the amendment applied. Contradiction is code-confirmed.

**S6** — CONTRIBUTING.md:118 describes block-ff-push as "fail-soft" (contradicted by ADR-85 §A6, NEW)
- **Claim:** CONTRIBUTING.md Validators table describes block-ff-push failure posture as "fail-soft".
- **Location:** `CONTRIBUTING.md:118`
- **Evidence:** `grep -n 'fail CLOSED\|return 2\|exit 2' /home/user/dev-knowledge/scripts/block_ff_push.py | head -5`
- **Verdict:** contradicted
- **Proposed fix:** Update CONTRIBUTING.md line 118 to replace "fail-soft" with "fail-CLOSED (exit 2 on internal error, per ADR-85 §A6 2026-08-03)".
- **Skeptic note:** Same root cause as S5 — ADR-85 §A6 amendment (2026-08-03) postdates CONTRIBUTING.md's last commit (2026-07-31). Both files carry the same stale description; both need separate fixes.

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — "Terra finding count says '1 CRITICAL and 5 HIGH' but commits total 1C+6H" (JOURNAL entries k, l)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** All 7 terra fixes are committed and accounted for in git history; the count error is in rolling summary prose only. No audit gate checks narrative accuracy of JOURNAL.md count sentences. The deliverable (fixes committed) is intact.

**K2** — "#458 Done-when requires PLAYBOOK freshness stamp to ride a genuine re-read, which the closing commit 9039d2d confirms was not performed"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** PLAYBOOK.md is not in `_FRESHNESS_FILES` and carries no `last_reviewed` stamp — only a `Last updated` touch-date. The Done-when secondary clause was written against the ARCHITECTURE.md freshness model, which audit.py explicitly does not apply to PLAYBOOK (noted inline). The clause is miscalibrated against a mechanism that doesn't exist for PLAYBOOK; the primary Done-when deliverable (note in PLAYBOOK Ch8 with witness cited) is fully met. Commit 9039d2d documents the limitation transparently. Identical kill rationale to K6 in the 2026-08-02 digest.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; entries (a)–(d) on 2026-08-04/2026-08-03, all within shallow-clone boundary):**
- Entry (a) 2026-08-04: SHAs 8d57c9b8, d0d58549, 68bf6ed8, 0cf327e all verified in git log with correct descriptions ✓
- Entry (a): ADR-104 anchor markers confirmed inserted (72 insertions, 0 deletions) ✓
- Entry (a): BACKLOG count 189→188 arithmetic confirmed ✓
- Entries (l)–(k): 14 SHA anchors across ARC 2+3 merge commits all verified ✓
- Entries (j)–(i): task files 481-*.md and 482-*.md both exist on disk ✓
- Entries (h)–(g): scripts/journal_anchor.py and scripts/block_unanchored_push.py both exist on disk ✓
- Entry (f): ADR-85 amendment confirmed append-only (179 insertions, 0 deletions) ✓
- Entry (e): ARC 0 commits (808ef911, 42ff1323) retroactively anchored by entry (e) — self-documented pattern, not omission ✓
- Entry (d): tasks/477–480 task files all exist on disk ✓
- BACKLOG arithmetic chain 184→188→189→188 internally consistent and matches current count ✓
- No significant merged work found in git history omitted from last-10 JOURNAL entries ✓

**V2 (living-doc factual claims):**
- VISION.md fleet count "nine git repos" — ecosystem/registry.md has exactly 9 rows ✓
- VISION.md eight child repo names match eight non-hub rows in ecosystem/registry.md ✓
- ARCHITECTURE.md `last_reviewed: 2026-08-02` — passes A2 gate ✓
- CLAUDE.md `last_reviewed: 2026-08-03` — passes A2 gate ✓
- CONTRIBUTING.md `last_reviewed: 2026-07-31` — passes A2 gate ✓
- ecosystem/doc-counts.md "39 registered checks" — matches ALL_CHECKS in scripts/audit.py ✓
- Pre-commit gate count 17 — matches `.pre-commit-config.yaml` exactly ✓
- ARCHITECTURE.md "five carriers" — exactly 5 `carrier_*.py` files in `deploy/` ✓
- tier1-lifecycle plugin enabled in `.claude/settings.json` ✓
- VISION.md audit.py subcommands 6 — all 6 confirmed as `@cli.command()` decorators ✓
- ESSENTIALS.md "audit check #7 retired" — `check_mermaid_theme_directive` marked RETIRED and absent from ALL_CHECKS ✓
- `.claude/commands/` (5 files) — matches generated `.claude/generated/commands-repo.md` enumeration ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-14 → 2026-08-04):**
- 23 closures verified semantically coherent: #472, #474, #475, #476, #473, #479, #455, #433, #459, #461, #462, #460, #469, #466, #467, #468, #471, #382, #435, #437, #439, #444, #386 ✓
- #472: ADR-104 fleet declaration anchor — 72 insertions, check_membership_agreement gains three anchor assertions ✓
- #479: principled SUPERSEDED — FR5 retired Stop hook enforcement premise; Done-when literally unsatisfiable ✓
- #455: principled SUPERSEDED — ADR-109 §2 retired registry.md as authoritative; checker's subject dissolved ✓

---

## Next Actions (proposals for operator)

1. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Session-end governance gates (backpressure, pre-commit hooks) remain non-functional. Blocks from prior digests.

2. **S1 (HIGH)** — Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to on or after 2026-07-31. The A2 canonical_freshness gate fires at every audit run; gap now 6 days. Five-night backlog.

3. **S2 (HIGH, NEW)** — Re-read protocols/ESSENTIALS.md end-to-end and bump `last_reviewed` from 2026-07-30 to on or after 2026-07-31. A2 FAIL; the last commit advanced the date past the stamp yesterday.

4. **S3 (HIGH)** — Rewrite CONTRIBUTING.md §"Nightly outcome management" (lines 128–176): replace present-tense Action description with a tombstone pointer to ARCHITECTURE.md Ch6. Five-night backlog; low-effort fix.

5. **S5+S6 (MED, NEW)** — Update ARCHITECTURE.md organ map (line 327) and CONTRIBUTING.md Validators table (line 118): replace "fail-soft" with "fail-CLOSED (exit 2, ADR-85 §A6 2026-08-03)". Also add `block-unanchored-push` to ARCHITECTURE.md Ch2 organ map (currently absent entirely).

6. **S4 (MED, NEW)** — Add `check-seal-identity` and `block-unanchored-push` rows to CONTRIBUTING.md Validators table to match the actual 17-hook roster.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-04-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
