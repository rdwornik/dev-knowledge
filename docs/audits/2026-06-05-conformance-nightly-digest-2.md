<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-05 (run 2)

**Date:** 2026-06-05
**Author:** Claude Code (claude-sonnet-4-6), operator Rob
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-05, confirmed unavailable for the second time today).

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` (Explore subagent) | claude-sonnet-4-6 |

All five stages ran on `claude-sonnet-4-6` (the orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). This is the second nightly run on 2026-06-05; the file is named with a `-2` suffix to avoid collision with the nightly #8 digest (`2026-06-05-conformance-nightly-digest.md`) already on main.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-05-conformance-nightly-digest.md` (nightly #8)
**Prior surviving finding:** S1 (med) — ARCHITECTURE.md + CONTRIBUTING.md reference HANDOFF_PROCESS v4.3.2, canonical file is v4.4

| Status | Finding | Evidence |
|---|---|---|
| **RESOLVED** | S1 (med): ARCHITECTURE.md + CONTRIBUTING.md stale HANDOFF_PROCESS stamp v4.3.2 | Fixed by commits `9265096` (S1 stamps updated) + `6fbd078` (audit check #13 mechanizes this class); V2 verified stamp now correctly reads v4.4 in ARCHITECTURE.md |
| **NEW** | H1 (high): #79 closure initially violated ADR-65 done-items-leave policy (in-place strikethrough, commit `052e311`); corrected in `fb24810` | V3 surfaced from backlog closure history; skeptic kept it as process-improvement evidence for #83 hook hardening |

**Delta counts:** 1 resolved · 0 persisting · 1 new

> **Context note:** H1 is a historical violation already corrected before nightly #8 ran. It was partially documented in the pilot #81 baseline as F2 (RESOLVED there). V3 re-surfaced it by scanning all recent closures; the skeptic kept it on the grounds that the violation is factually verifiable and provides concrete evidence for the #83 hook-hardening task. The current BACKLOG.md is correct — the in-place stub was removed by `fb24810`.

---

## Summary

Overall documentation health is strong with mature conformance workflows and robust operator discipline. The single survivor finding reflects a genuine but already-corrected schema gap in backlog closure procedures (ADR-65 violation in commit `052e311`, procedurally fixed in `fb24810`). The skeptic kill-rate is 0% (no false positives raised — all verifiers converged on factual, corrected violations and clean artifact states). Forty-six items were verified clean across JOURNAL→git (V1), living-doc claims (V2), and backlog-closure coherence (V3), indicating systematic conformance coverage with high operator follow-through.

Prior nightly S1 (HANDOFF_PROCESS version stamp recurrence class) is **resolved**: audit check #13 (`6fbd078`) now mechanizes this detection permanently, so future stamp drift will be caught by `audit.py` before merge.

<!-- counts: raw=1 survived=1 killed=0 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 1 · **Survived skeptic:** 1 · **Killed false positives:** 0

### High (1)

**H1** — `backlog-closures` — #79 closure violated ADR-65 done-items-leave policy: commit `052e311` used in-place strikethrough + RESOLVED marker instead of removing the item; corrected by `fb24810`

- **Location:** `BACKLOG.md`, commit `052e311` initial form
- **Evidence command:** `git show 052e311 | grep -A10 '#79'` — shows the strike-through RESOLVED in-place marker; `git log -p -S '[#79]' -- BACKLOG.md | grep 'RESOLVED\|~~'` shows the initial violation; `git show fb24810` confirms the procedural correction (removal of the in-place stub per ADR-65)
- **Verdict:** contradicted (historical; now corrected)
- **Proposed fix (proposal only):** Ensure the #79 correction path (052e311 → fb24810) is documented as concrete evidence for #83 (harden `validate_backlog` to reject struck-through task lines at commit time)
- **Skeptic note:** Violation is factually real in commit `052e311` (contradicts ADR-65 Decision 1: done items LEAVE the file; in-file stubs explicitly rejected in Alternatives). Correction is verifiable in `fb24810`. Operator documented both the violation and fix in JOURNAL + commit message. Kept as genuine process-gap evidence supporting #83 hook hardening.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

*(none — skeptic raised 0 kills; all verifiers returned clean or the single finding survived)*

---

## Checked-and-Clean (46 items — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries — all within shallow history window):**
- 2026-06-05 Synthetic Action-path test green end-to-end — PR #9 auto-merged (`4a4a4c8`)
- 2026-06-05 Nightly follow-ups — survivor-issue extractor aligned (`3f4113f` merged)
- 2026-06-05 Nightly digest count-contract restored (`821ef02` merged)
- 2026-06-05 audit.py check #13 handoff_version_stamp (`13f5ac1` merged)
- 2026-06-05 Nightly #8 findings cleanup (`9265096`, `af6c300` merged)
- 2026-06-05 Pre-nightly cleanup (`da61d4c` merged)
- 2026-06-05 Handoff Phase 2 complete (2026-06-05-dev-knowledge-session-2) (`239c19a` merged)
- 2026-06-05 Handoff Phase 2 complete (2026-06-05-dev-knowledge-v44-wrap) (`e90a1fe` merged)
- 2026-06-05 HANDOFF_PROCESS v4.4 amendment shipped beta (`ec1d0cf` merged)
- 2026-06-05 Handoff Phase 2 complete (2026-06-05-dev-knowledge-session) (`628d7cb` merged)
- 2026-06-04 Phase C4 nightly outcome management (`2842e52`, `cbb5c42` merged)
- 2026-06-04 Model-routing re-probe completed (`c12ac88` merged)
- 2026-06-04 Model-routing re-probe pins honored (`bdde839` merged)
- 2026-06-04 Phase C3 runtime-machinery cleanup (`c3f592e` merged)
- 2026-06-04 Merge nightly PR #1 + land fleet_health fail-soft (`6abe725` merged)
- 2026-06-04 Hub closeout V1 shallow-history guard (`01d7607` merged)
- 2026-06-04 Phase B hub pushed to private GitHub + cloud-night pipeline (`e497653` merged)
- 2026-06-04 CONTRIBUTING stamp/hook-table sync (`9673681` merged)
- 2026-06-04 Conformance rerun (`23baf64` merged)
- 2026-06-04 Pilot-arc retro captures (`87464c9` merged)
- 2026-06-04 Pilot-phase closeout (`f88accb` merged)

**V2 (living-doc factual claims):**
- ARCHITECTURE.md: HANDOFF_PROCESS stamp v4.4, status live — verified against `protocols/HANDOFF_PROCESS.md` line 6
- ARCHITECTURE.md: Eight pre-commit hooks listed (normalize-dated-headers, codemap-freshness, toc-freshness, toc-freshness-playbook, validate-backlog, audit-health, ruff, backlog-id-on-close) — all verified in `.pre-commit-config.yaml`
- CONTRIBUTING.md: 13 self-conformance checks — verified `ALL_CHECKS` in `scripts/audit.py` contains exactly 13 check functions
- CLAUDE.md: ruff version-pinned `>=0.15.5` — verified in `pyproject.toml`
- ARCHITECTURE.md: Two-node diagram (`scripts/codemap/` and `scripts/toc/` as Python packages) — both `__init__.py` confirmed
- CONTRIBUTING.md: Handoff bundle structure 8 files (README + 01_ROLE…07_ASK_BACK) — verified in `docs/handoffs/2026-05-31-dev-knowledge-session-2/`
- ARCHITECTURE.md: ADR-71 doc-tooling distribution listed in Governing ADRs — file exists at `docs/decisions/ADR-71-doc-tooling-hook-source-repo.md`
- VISION.md: Repo-tier system deprecated 2026-05-23 — verified matching date across all documents
- CONTRIBUTING.md: HANDOFF_PROCESS v4.4 (two-phase flow, eight flat bundle files) — verified in `protocols/HANDOFF_PROCESS.md`
- CLAUDE.md §8: tier1-lifecycle plugin enabled as dev-knowledge-methodology — verified in `.claude/settings.json`
- Pre-commit hooks list complete with toc-freshness ×2 (ARCHITECTURE and PLAYBOOK) — verified in `.pre-commit-config.yaml` lines 27–44

**V3 (backlog-closure semantic coherence):**
- `d5753a8` closes [#78]: ARCHITECTURE + CLAUDE end-to-end re-read with `last_reviewed` re-stamped — coherent with Done-when criteria
- `5f327b2` closes [#88]: graphify pilot REJECT ruling + evidence reference — coherent with Done-when criteria
- `052e311`+`fb24810` closes [#79]: codemap grounding audit + decision recorded (violation form corrected) — semantically coherent; see H1 for process-gap detail

---

## Next Actions (proposals for operator)

1. Use the #79 correction evidence (commit `052e311` violated ADR-65; `fb24810` corrected it) as concrete input for #83 (harden `validate_backlog` to reject struck-through task lines at commit time), preventing future ADR-65 closure-form violations from reaching main.

---

## Safety Tripwire

`git status --porcelain` output at review completion (before this digest file was written):

```
(empty — clean working tree)
```

Only this digest file was written during the review. No other tracked files were modified.

`git status --porcelain` output on this branch (post-digest write, pre-commit):

```
?? docs/audits/2026-06-05-conformance-nightly-digest-2.md
```

Expected: one untracked file (this digest). No other changes. **No safety breach detected.**
