<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-13

**Date:** 2026-06-13
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-13, confirmed unavailable. Consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-06-12-conformance-nightly-digest.md`
**Prior surviving findings:** 5 (F2 med, F3 high, F4 med, F5 med, F7 high)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | F2 (med): ARCHITECTURE.md frontmatter/inline timestamp mismatch | Skeptic killed as `documented-decision`: `Last updated: 2026-06-07` annotates the six-chapter rewrite content date; `last_reviewed: 2026-06-12` tracks review date — two different purposes per design |
| **RESOLVED** | F4 (med): merge commit 0ee6c3d `closes [#147]` pattern | V3 clean pass: e56375f properly removes #147 from BACKLOG.md; pattern resolved |
| **RESOLVED** | F5 (med): merge commit 5193de5 `closes [#11]` pattern | V3 clean pass: 88ab795 properly removes #11 from BACKLOG.md; pattern resolved |
| **RESOLVED** | F7 (high, process note): #79 inline RESOLVED notation | V3 clean pass: fb24810 removed the inline resolved stub per ADR-65; historical process note, no current breach |
| **PERSISTING** | F3 → S3 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/verify/` confirmed present; claim directly contradicted; persisting from 2026-06-12 and 2026-06-11 |
| **NEW (skeptic-borderline)** | S1 (high): JOURNAL.md entry cites SHA f578ac4 (May 2026, absent from git) | Skeptic kept; however this SHA predates the shallow-clone boundary (~2026-06-03) — per the shallow-history guard this is out-of-scope; operator should assess |
| **NEW (skeptic-borderline)** | S2 (high): JOURNAL.md entry cites SHA 818a1c6 (May 2026, absent from git) | Same as S1 — shallow-boundary concern applies; operator should assess |

**Delta counts:** 4 resolved · 1 persisting · 2 new (both skeptic-borderline)
**Skeptic kill-rate:** 63% (5 of 8 raw findings killed)

---

## Summary

Strong progress since the 2026-06-12 baseline: 4 of 5 prior findings resolved. The F4/F5 merge-commit closure-placement findings (historical process notes) are fully resolved with proper BACKLOG removals confirmed. F7 (#79 inline RESOLVED) was previously noted as self-corrected and V3 confirms fb24810 cleaned it properly. F2 (ARCHITECTURE.md timestamp mismatch) was killed by the skeptic as a documented-decision: the inline `Last updated: 2026-06-07` annotates the six-chapter rewrite date and is intentionally distinct from the `last_reviewed` frontmatter stamp — a reasonable kill.

One finding persists: CLAUDE.md §8 "No repo-level skills directory exists yet" (S3/F3) has been contradicted for 3+ days. `.claude/skills/verify/` exists with `SKILL.md` and `verify.py`. This is a simple one-line fix.

Two new findings survived the skeptic (S1, S2) but carry a skeptic-borderline flag: they reference commit SHAs from May 2026 JOURNAL entries. V1 read from the bottom of the newest-first JOURNAL (old entries) instead of the top (recent entries), causing a methodological confusion. The SHAs in question (f578ac4, 818a1c6) predate the shallow-clone boundary (~2026-06-03), meaning the shallow-history guard marks them as out-of-scope. The skeptic kept them on the grounds that they represent "real drift" even in a shallow clone, but this conflicts with the guard's explicit instruction. Operator judgment call: if these May 2026 JOURNAL entries are considered in-scope, they warrant investigation; if the shallow-history guard takes precedence, they should be dismissed.

The skeptic kill-rate of 63% (5/8) is higher than yesterday's 29% (2/7), reflecting that most V1 findings were methodological artifacts and the V2 count finding was verified correct by the skeptic.

---

## Findings (PROPOSALS ONLY)

**Raw:** 8 · **Survived skeptic:** 3 · **Killed false positives:** 5

<!-- counts: raw=8 survived=3 killed=5 -->

### High (3)

**S3** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from F3; 3rd consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory. Remove the "No repo-level skills directory exists yet" claim.

**S1** — JOURNAL entry cites non-resolvable SHA f578ac4 *(NEW; skeptic-borderline — see note)*
- **Claim:** 2026-05-09 JOURNAL entry states "Added Strategic emphasis section to VISION.md" with commit f578ac4
- **Location:** JOURNAL.md:3190 (old entry near bottom of newest-first file)
- **Evidence:** `git cat-file -t f578ac4 2>&1`
- **Verdict:** contradicted
- **Note:** SHA predates shallow-clone boundary (~2026-06-03). Shallow-history guard marks this out-of-scope. Skeptic kept on grounds of "real drift," but the guard's explicit rule is that pre-boundary SHAs are not findings. Operator should decide if pre-boundary JOURNAL entries are in scope for this review.
- **Proposed fix:** If in-scope: investigate whether f578ac4 existed in a prior git history (force push, rebase, or hallucinated SHA) and correct the JOURNAL entry if the SHA is confirmed hallucinated.

**S2** — JOURNAL entry cites non-resolvable SHA 818a1c6 *(NEW; skeptic-borderline — same caveat as S1)*
- **Claim:** 2026-05-09 JOURNAL entry states "Committed ai-council audit-sync execution evidence" with commit 818a1c6
- **Location:** JOURNAL.md:3188 (old entry near bottom of newest-first file)
- **Evidence:** `git cat-file -t 818a1c6 2>&1`
- **Verdict:** contradicted
- **Note:** Same shallow-boundary caveat as S1.
- **Proposed fix:** Same remediation path as S1 — investigate origin of SHA reference.

### Med (0)

*(none — all prior med findings resolved or killed)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — SHA e428a5e (2026-05-11 JOURNAL entry)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** SHA from 2026-05-11, outside shallow-clone boundary (~2026-06-03). Cannot distinguish "SHA never existed" from "SHA predates shallow clone." Shallow-history guard explicitly marks these out-of-scope.

**K2** — JOURNAL 180+ commits omitted from 2026-05-11 entry
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** V1 read from the bottom (oldest) section of the newest-first JOURNAL. The June 2026 entries ARE present at the top. The apparent "omission" is a verifier methodology error, not a real conformance gap.

**K3** — 2026-05-11 entry as "final state" with June sessions missing
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Same root cause as K2. The verifier read old entries and concluded new entries were absent — they are not. 2026-06-12 entries confirmed at lines 22-100 of JOURNAL.md.

**K4** — ARCHITECTURE.md "18 registered checks" count
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Skeptic re-ran `grep -c 'def check_' scripts/audit.py` and confirmed 18 check functions. V2 over-counted by including non-ALL_CHECKS functions. The 2026-06-12 baseline had this as checked-clean; it remains correct.

**K5** — ARCHITECTURE.md frontmatter/inline timestamp mismatch (F2 from prior baseline)
- **Kill reason:** `documented-decision`
- **Kill detail:** The inline `Last updated: 2026-06-07` annotates the six-chapter rewrite content date; `last_reviewed: 2026-06-12` tracks the review/re-read date per CLAUDE.md §4. Two timestamps serve distinct, documented purposes. Not a contradiction.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, checked newest entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-12 entry: #149 flip bundle work — top-of-file entries confirmed present
- 2026-06-12 handoff canonical runbook session — JOURNAL entries verified
- V1 methodology note: agent read from bottom (old entries) rather than top (new entries); new entries confirmed present by skeptic

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-06-12` frontmatter — verified
- ARCHITECTURE.md pre-commit gates count (8) — matches `.pre-commit-config.yaml`
- ARCHITECTURE.md "18 registered checks" in ALL_CHECKS — verified correct (18 functions in list)
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in `.pre-commit-config.yaml`
- CLAUDE.md §11: ADR-76 through ADR-80 exist in `docs/decisions/` — verified
- `.claude/commands/` contains `save.md`, `handoff.md`, `changelog-review.md` — verified
- VISION.md tier system deprecated 2026-05-23 per ADR-38 — correct
- CONTRIBUTING.md pre-commit hooks table — matches `.pre-commit-config.yaml`
- ESSENTIALS.md structural claims — correct

**V3 (backlog-closure semantic coherence, since 2026-05-24):**
- Closures #149, #151, #160, #148, #124, #25 (v5 flip arc) — all semantically coherent
- Closure #11 (88ab795) — item removed from BACKLOG.md; coherent
- Closure #147 (e56375f) — item removed from BACKLOG.md; coherent
- #79 inline-RESOLVED cleanup (fb24810) — item removal confirmed per ADR-65
- BACKLOG.md validate_backlog gate — passing

---

## Next Actions (proposals for operator)

1. **S3 (high, persisting 3 nights)** — Update CLAUDE.md §8: change "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" to document `.claude/skills/verify/` (the verify skill, added by #104). Simple one-line fix; this has appeared in every nightly since 2026-06-11.
2. **S1 + S2 (high, skeptic-borderline — operator judgment call)** — If pre-2026-06-03 JOURNAL entries are considered in scope: investigate whether SHAs f578ac4 and 818a1c6 existed (possible rebase/force-push history loss or LLM-hallucinated SHAs from old sessions). If shallow-history guard takes precedence, dismiss these findings.
3. **Process note** — V1 verifier read from the bottom of the newest-first JOURNAL (old entries) instead of the top. The spec prompt instructs "last 10 entries" but a newest-first file's most-recent entries are at the top. Consider clarifying the V1 prompt to say "read the FIRST 10 entries (the most recent, which appear at the TOP of the newest-first file)" to avoid this recurrence.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-13-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
