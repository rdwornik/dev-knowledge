<!-- scope: meta -->
# Conformance Rerun — Delta Digest vs 2026-06-03 Baseline

**Date:** 2026-06-04
**Author:** Claude Code (Opus 4.8 main loop), operator Rob
**Branch:** `docs/conformance-rerun`
**Backlog:** advances #81 (agentic-conformance arc) — tests the **recurring-review** mode
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.
**Run:** saved Dynamic Workflow `conformance-hub` (invoked as a saved artifact, script not regenerated), Run ID `wf_d044fa30-b08`, 5 agents, ~7m19s (438,996 ms).
**Baseline compared against:** `docs/audits/2026-06-04-pilot81-hub-conformance-digest.md` (the Pilot #81 v0 run launched 2026-06-03 — the "2026-06-03 baseline").

---

## Safety envelope (held end-to-end)

- **`Write`/`Edit` denied during the run** — session-scoped deny added to `.claude/settings.local.json` and **spot-checked active before launch** (a probe `Write` was denied; probe file absent afterward). Deny remained enforced through the run (and, due to session-level caching, even after removal — the digest itself was authored via the shell, not `Write`/`Edit`).
- **Scope locked** to `.dev-knowledge`; agents instructed read-only + no Bash-writes.
- **Post-run fleet tripwire:** `git status --porcelain` empty on all 5 repos (`.dev-knowledge`, `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`). **Zero writes occurred during the run.**
- **Actual-model check (from agent jsonl transcripts):** see "Recurring caveat" below.

---

## Delta vs baseline — RESOLVED / PERSISTING / NEW

Baseline had **2 survivors** (F1 high, F2 med) + 1 skeptic-killed. This rerun returned **3 survivors, 0 killed** (skeptic kill-rate 0/3).

### RESOLVED (baseline findings now clean — confirmed in verifier `checked_clean`)

| Baseline | What it was | Fixed by | Rerun evidence |
|---|---|---|---|
| **F1** (high) | `ARCHITECTURE.md:336,402` said HANDOFF_PROCESS "4.3.1 stable"; actual 4.3.2 | #78 / `f88accb` | V3 checked_clean: "#78 ARCHITECTURE F1 HANDOFF_PROCESS stamp updated 4.3.1→4.3.2"; V2: "ARCHITECTURE.md last_reviewed 2026-06-04" |
| **F2** (med) | `BACKLOG.md` #79 struck-through in-place vs ADR-65 "done items leave" | `fb24810` | V1 checked_clean: "#79 stub deletion verified: fb24810 removed struck-through #79 per ADR-65" |

Both baseline findings are **clean in live repo state.** The recurring-review mode worked: the two fixed items moved from *findings* to *checked_clean*.

### PERSISTING — same drift CLASS as F1, new locus (the F1 fix was incomplete)

| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | med | `CONTRIBUTING.md:133` STILL references HANDOFF_PROCESS "v4.3.1 *stable*"; actual is **v4.3.2, status live** | `head -12 protocols/HANDOFF_PROCESS.md && grep 'Status:' protocols/HANDOFF_PROCESS.md` |

The F1 remediation fixed `ARCHITECTURE.md` only; the **identical stale stamp in `CONTRIBUTING.md` was missed.** This is the headline value of the rerun: a targeted single-file fix left the same cross-file version-drift class live elsewhere.

### NEW

| # | Sev | Finding | Evidence |
|---|---|---|---|
| 2 | med | `CONTRIBUTING.md:98-105` validators table lists **6** pre-commit hooks; `.pre-commit-config.yaml` defines **8** (missing `toc-freshness`, `toc-freshness-playbook`, added `0d00028` 2026-05-30 / `ff8607c` 2026-06-03) | `grep '^      - id:' .pre-commit-config.yaml` |
| 3 | (skeptic: high) | Retrospective: closing commit `052e311` itself introduced the #79 in-place stub before `fb24810` corrected it | `git show 052e311:BACKLOG.md \| grep -A1 '[#79]'` |

**On finding #3:** this is a *historical* view of the already-RESOLVED F2 — the live tree is clean (fb24810). The forward-looking remediation (`validate_backlog` hardening to reject struck-through DONE lines) is **already backlogged as #83**. Not actionable on the current tree.

---

## Recurring-review-mode verdict

The mode **works as intended**: re-running the saved workflow against a moved-forward repo correctly (a) cleared the two fixed baseline findings into `checked_clean`, and (b) surfaced that one fix (F1) was incomplete — the same class lives at a new locus (`CONTRIBUTING.md`). Net actionable new drift this round: **findings #1 and #2 (both `CONTRIBUTING.md`, both med).**

## Recurring caveat — model routing (NOT new; confirmed persists)

Actual-model check from the 5 agent jsonl transcripts: **all 5 subagents ran on `claude-haiku-4-5`** — including V1/V2/V3 pinned to `claude-sonnet-4-6` and the skeptic/digest meant to inherit Opus. The script's `model:` param was not honored; every workflow subagent routed to Haiku 4.5. This matches the pilot-phase "Haiku-only routing probe verdict" (commits `90464ce`, `3bef14b`, `85d8e7e`) and is a known environment limitation, not a finding against the docs. Worth noting the run still produced 3 evidence-grounded, skeptic-survived findings on Haiku.

| Agent | Pinned/intended | Actual |
|---|---|---|
| V1 / V2 / V3 | `claude-sonnet-4-6` | `claude-haiku-4-5` |
| skeptic / digest | inherit Opus | `claude-haiku-4-5` |

---

## Next actions (proposals for operator triage — no action taken)

1. Sync `CONTRIBUTING.md:133` to HANDOFF_PROCESS **v4.3.2 / live** (finding #1) — and consider whether the F1-class (cross-file version-stamp drift) warrants a check, since per-file targeted fixes keep missing sibling references.
2. Add `toc-freshness` + `toc-freshness-playbook` rows to the `CONTRIBUTING.md` validators table (finding #2).
3. #83 already tracks the `validate_backlog` hardening that finding #3 motivates — no new item needed.

**Counts:** raw 3 → survived 3 → killed 0. Baseline F1/F2 both resolved. Net new actionable: 2 (both `CONTRIBUTING.md` drift).
