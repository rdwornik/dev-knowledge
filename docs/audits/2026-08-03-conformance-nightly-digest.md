<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-03

**Date:** 2026-08-03
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-03; confirmed unavailable, consistent with all prior nightly runs.)

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
**Gap:** 1 day (2026-08-02 → 2026-08-03)

| Status | Prior ID | Finding | Notes |
|---|---|---|---|
| **PERSISTING (escalated MED→HIGH)** | S1 | CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live | 4th consecutive nightly digest unfixed. Skeptic elevated severity to HIGH: no ADR covers permanent deferral; present-tense prose is actively misleading. |
| **PERSISTING (escalated MED→HIGH)** | S2 | VISION.md `last_reviewed: 2026-07-25` predates last commit | Gap now 2 days (last commit 2026-07-27 vs prior digest's 2026-07-26 measurement). Unfixed since 2026-07-31. Skeptic elevated to HIGH: definitive A2 canonical_freshness FAIL at every audit run. |
| **NEW** | — | #476 premature closure: name-only lane presence vs required blob check | Post-closure fix (0e27f308) landed 16 minutes after merge, naming the hole explicitly. |
| **NEW** | — | #471 premature closure: non-recursive glob missed scripts/toc/cli.py | Post-closure fix (13d9cc1) landed 26 minutes after merge, naming the non-recursive gap explicitly. |
| **OUT OF SCOPE (scrolled)** | — | Prior journal entry (t) broken SHA ee76c412 | Entry (t) remains beyond the 10-entry review window. Not re-verified. |

**Delta counts:** 0 resolved · 2 persisting (escalated) · 2 new · 0 killed-from-prior
**Raw → survived → killed:** 7 → 4 → 3
**Skeptic kill-rate:** 43% (3 of 7 raw findings killed — lower than prior nights' 78%, reflecting stronger evidence in new backlog-closure findings)

---

## Summary

Documentation conformance has deteriorated relative to the prior baseline. The two MED findings that persisted through last night were each escalated to HIGH: CONTRIBUTING.md's present-tense description of a GitHub Action retired on 2026-07-08 has now gone four consecutive nightly digests without correction, and VISION.md's backward-dated `last_reviewed` stamp (2026-07-25, vs last commit 2026-07-27) constitutes a live A2 canonical_freshness gate failure at every audit run. Two new MED-severity backlog-closure findings emerged: closures #476 and #471 were each followed within 30 minutes by commits explicitly naming a hole in the closure's own implementation — the closure's behavioral guarantees were not fully satisfied at merge time. The 43% skeptic kill-rate reflects that the raw findings this run were stronger than prior nights'; the three kills were an opinion (journal omission of a one-file mechanical pin), an evidence-not-definitive (interpretive Done-when gap for #467), and a true-but-irrelevant (#458 freshness clause for a file not in `_FRESHNESS_FILES`). V1 verified 25+ SHA anchors across 10 journal entries with no contradictions; V2 confirmed 12 factual living-doc claims clean; V3 verified 18 closures as semantically coherent.

<!-- counts: raw=7 survived=4 killed=3 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 4 · **Killed false positives:** 3

### High (2)

**S1** — CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (.github/workflows/nightly-conformance-triage.yml) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls /home/user/dev-knowledge/.github 2>/dev/null && echo EXISTS || echo NOT_EXISTS` → `NOT_EXISTS`
- **Verdict:** contradicted
- **Proposed fix:** Replace §"Nightly outcome management" present-tense GitHub Action description with a tombstone note pointing to ARCHITECTURE.md Ch6, citing the 2026-07-08 retirement commit 82227f08.
- **Skeptic note:** No `.github/` directory exists; the file cannot exist. CONTRIBUTING.md uses present-tense "handles the morning" for a workflow that was deleted 26 days ago. No ADR permanently exempts this section from correction. Elevated to HIGH: 4th consecutive nightly run with no fix; ARCHITECTURE.md Ch6 provides in-repo correction but does not excuse the stale prose.

**S2** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-07-27 (A2 violation)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git -C /home/user/dev-knowledge log --date=short --format='%cd' -- VISION.md | head -1` → `2026-07-27`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to a date on or after 2026-07-27; the A2 canonical_freshness gate fires at every audit run.
- **Skeptic note:** Stamp (2026-07-25) is now 2 days before the last commit (2026-07-27) — gap widened from yesterday's measurement. Exact backward-dated A2 canonical_freshness FAIL; VISION.md is in `_FRESHNESS_FILES`. No ADR exempts it. Elevated to HIGH: unfixed since 2026-07-31.

### Med (2)

**S3** — #476 premature closure: name-only lane-presence check when blob identity was required
- **Claim:** #476 closure was complete at merge time: the lane-presence check was a blob-identity check, so a file present by name but with different content would still flag.
- **Location:** `d3264ff6` (closure commit 2026-08-02 18:58) / `0e27f308` (post-closure fix 2026-08-02 19:14)
- **Evidence:** `git show 0e27f308762dc02025f1031a9c09c3b709c952cf | grep -E 'Repairs a hole|name-only|blobs|name check'`
- **Verdict:** contradicted
- **Proposed fix:** Open a new backlog row recording the premature closure of #476 and the Done-when gap; the closure commit's third clause ("a daily absent from the lane still flags") was not satisfied at merge time.
- **Skeptic note:** Post-closure fix (0e27f308) states "Repairs a hole in [#476]'s own implementation" — `_on_lane()` matched via `ls-tree --name-only`, excusing any file whose name appeared regardless of content. The Done-when required blob-identity comparison. Fix arrived 16 minutes post-closure; no new backlog row opened.

**S4** — #471 premature closure: non-recursive glob missed scripts/toc/cli.py
- **Claim:** #471 Done-when "every text-mode write in scripts/ pins newline" was fully met at closure time; AST sweep returned ZERO offenders.
- **Location:** `af6fa93f` (closure commit 2026-08-01 13:51) / `13d9cc1` (post-closure fix 2026-08-01 14:17)
- **Evidence:** `git show 13d9cc1669483bf6e86e4aaf01db9503860b9087 | grep -E 'claim|11 sites|recursive|NON-RECURSIVE|cli.py'`
- **Verdict:** contradicted
- **Proposed fix:** Open a new backlog row recording the premature closure of #471; the non-recursive glob used at closure time left scripts/toc/cli.py unpatched, contradicting the closure's ZERO-offenders claim.
- **Skeptic note:** Post-closure fix (13d9cc1) states `_write_sites()` used `_SCRIPTS.glob('*.py')` which is NON-RECURSIVE, missing `scripts/toc/cli.py:50`. Fix adds `rglob` and a regression test pinning the recursion. Arrived 26 minutes post-closure; no new backlog row opened.

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — "Entry (d) Changes section omits commit 5d1c71f (ecosystem/doc-counts.md re-pin 2181→2182)"
- **Kill reason:** `opinion`
- **Kill detail:** No protocol (CONTRIBUTING.md, PLAYBOOK.md, or any ADR) requires journal Changes blocks to enumerate every commit in the covered range. The commit is a one-file mechanical re-pin (1 insertion, 1 deletion) that arrived between entries (d) and (e); the journal conventions impose no obligation to retroactively list it. Identical kill pattern to prior digest's K-series.

**K2** — "#467 Done-when is satisfied: a ruling records repomix declined for all surfaces, or the code-context trial ran"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The closure records code-context as DEFERRED ("until a review-lane consumer shows real pain"), not declined, and the trial was not run. Whether a recorded deferral ruling satisfies Done-when branch A ("declined for all surfaces") is an interpretive question the evidence alone cannot definitively resolve. The closure commit is transparent about its basis and explicitly guards against misreading. The adversarial standard requires the evidence_command to definitively prove a conformance problem; here it shows an interpretive gap at most.

**K3** — "#458 Done-when is fully met: the PLAYBOOK freshness stamp rides a genuine re-read"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** PLAYBOOK.md is not in `_FRESHNESS_FILES` (confirmed against audit.py, which documents the 8 gated files: VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, docs/handoffs/README, ESSENTIALS, SESSION_SETUP, AI_COUNCIL_PROCESS). The freshness-re-read clause is mechanically unenforced and carries no canonical_freshness gate. The closure commit is explicitly transparent: "NO end-to-end re-read of all 3,995 lines was performed and none is claimed." Primary deliverable (PLAYBOOK Ch8 rule with witness cited) was delivered. Same kill rationale as prior digest K6.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; entries (a)–(f) 2026-08-02, entries (c)–(f) 2026-08-01):**
- Entry (f) SHAs 087d967f ([#475] seal-identity gate), bc0c2ada ([#474] write-guard) — both confirmed ✓
- Entry (f) new files scripts/check_seal_identity.py and tests/test_check_seal_identity.py — both on disk ✓
- Entry (e) SHA 55733ea4 (lane union commit, automation/fleet-audit branch) — confirmed after fetch ✓
- Entry (e) SHA 24882f8c (conformance absorption, claude/conformance-2026-08-02) — confirmed ✓
- Entry (d) SHA 0e27f308 (blob-not-name backpressure fix) — confirmed ✓
- Entry (c) SHAs 27c82d40 ([#473]), 40bad185 ([#474]/[#475] filing), 64693e25 (doc_rot trim), ae173251 ([#476] fix) — all confirmed ✓
- Entry (b) SHA 0f5738be (handoff suffix-sibling resolution) — confirmed ✓
- Entry (a) SHA 6a116157 (night batch), four morning merge SHAs (56f82aaf, 7cdebe05, 1aef11f3, 2335a9e6) — all confirmed ✓
- 25+ SHA anchors checked across 10 entries; no fabricated or absent SHA; no significant unmentioned work ✓

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-08-02` — passes A2 gate (last commit also 2026-08-02) ✓
- CONTRIBUTING.md `last_reviewed: 2026-07-31` — passes A2 gate (last commit 2026-07-30) ✓
- ESSENTIALS.md `last_reviewed: 2026-07-30` — passes A2 gate (last commit 2026-07-29) ✓
- ARCHITECTURE.md audit check count 38 — matches `ALL_CHECKS` in scripts/audit.py exactly ✓
- VISION.md fleet count "nine git repos" — ecosystem/registry.md has exactly 9 data rows ✓
- ARCHITECTURE.md "five carriers" — exactly 5 `carrier_*.py` files in `deploy/` ✓
- CLAUDE.md §8 skills: `.claude/skills/` holds exactly `verify` + `check-against-spec` ✓
- CLAUDE.md §9 ruff pin v0.15.5 — matches `.pre-commit-config.yaml` rev ✓
- CLAUDE.md §9 pre-commit hook roster (16 hooks) — matches `.pre-commit-config.yaml` exactly ✓
- CLAUDE.md §11 ADR-105 through ADR-109 — all 5 files exist on disk ✓
- ecosystem/doc-counts.md pre-commit gate count (16) — matches actual `.pre-commit-config.yaml` ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-14 → 2026-08-03):**
- 18 closures verified semantically coherent: #474, #475, #473, #459, #461, #462, #460, #469, #382, #466, #471 (substantive clauses), #437, #439, #444, #435, #436, #386, #35/#41/#367/#370 (grooming) ✓
- #476 and #471 listed above in findings (S3, S4) — verified with post-closure evidence ✗

---

## Next Actions (proposals for operator)

1. **(HIGH, 4th night — overdue)** **S1:** Update CONTRIBUTING.md §"Nightly outcome management": replace present-tense GitHub Action description with a tombstone pointer to ARCHITECTURE.md Ch6. Low-effort, one-section rewrite. Evidence command: `ls /home/user/dev-knowledge/.github 2>/dev/null && echo EXISTS || echo NOT_EXISTS`

2. **(HIGH, persistent A2 fail)** **S2:** Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to on or after 2026-07-27. The A2 gate fires on every audit run. Five-day backlog; stamp gap now 2 days. Evidence command: `git -C /home/user/dev-knowledge log --date=short --format='%cd' -- VISION.md | head -1`

3. **(MED, new)** **S3:** Open a new BACKLOG row for [#476] premature closure: the Done-when's third clause (blob-identity check) was not met at closure time; fix 0e27f308 arrived 16 minutes later. Evidence command: `git show 0e27f308762dc02025f1031a9c09c3b709c952cf | grep -E 'Repairs a hole|name-only|blobs|name check'`

4. **(MED, new)** **S4:** Open a new BACKLOG row for [#471] premature closure: non-recursive glob at closure time left scripts/toc/cli.py unpatched; fix 13d9cc1 arrived 26 minutes later. Evidence command: `git show 13d9cc1669483bf6e86e4aaf01db9503860b9087 | grep -E 'claim|11 sites|recursive|NON-RECURSIVE|cli.py'`

5. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate (session-end backpressure, pre-commit hooks) fails with version mismatch 0.8.17. Blocks from prior digests.

6. **(OUT OF SCOPE — needs manual verify)** Prior journal entry (t) broken SHA `ee76c412` remains beyond the 10-entry review window. Operator should manually verify whether it was corrected.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-03-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
