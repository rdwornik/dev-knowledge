<!-- scope: meta -->
# Pilot #81 v0 — Hub Conformance Review Digest (Dynamic Workflow)

**Date:** 2026-06-04 (run launched 2026-06-03 23:xx, completed 2026-06-04 — dated to completion per `YYYY-MM-DD-slug`)
**Author:** Claude Code (Opus 4.8), operator Rob
**Backlog:** advances #81 (the agentic-conformance arc); builds on Phase-0 (`docs/audits/2026-06-03-phase0-workflow-gates-findings.md`)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. Findings are proposals for operator triage.
**Run:** Dynamic Workflow `conformance-hub`, Run ID `wf_c962d194-014`, 5 agents, interactive (operator-watched via `/workflows`).

---

## What this run was

First real-conditions use of Dynamic Workflows: a **read-only conformance review of this repo's living documentation**, run as a workflow (3 verifiers fan out → 1 adversarial skeptic → 1 digest). It tests whether a workflow catches the **semantic** drift that `audit.py`'s 12 (syntactic/structural) checks and the pre-commit hooks cannot — at a false-positive rate worth the operator's attention.

**Safety posture (held end-to-end):** session-scoped `Write/Edit` deny rule (spot-checked active before the run — a throwaway subagent's write was denied, probe file absent), agents instructed read-only + no Bash-writes, scope locked to `.dev-knowledge`. **Post-run fleet tripwire: 5/5 repos `git status --porcelain` empty.** Zero writes occurred during the run; the only writes this session (this digest + JOURNAL) were made by the main session *after* the run, with deny rules restored.

---

## Findings

3 raw findings → **2 survived** the skeptic → **1 killed**. Both survivors verified against live repo state by the main session (not taken on agent narration).

| # | Sev | Domain | Finding | Evidence (verified) | Status |
|---|-----|--------|---------|---------------------|--------|
| F1 | **high** | living-docs | `ARCHITECTURE.md:336` and `:402` assert `HANDOFF_PROCESS.md` is "stamp **4.3.1**, status stable", but the file header reads `Version: **4.3.2**` (bumped 2026-06-03, commit `6f51aec`, ~2.5h after ARCHITECTURE.md's last edit) | `grep -n '4.3.1' ARCHITECTURE.md` → L336,402; `head -6 protocols/HANDOFF_PROCESS.md` → `Version: 4.3.2` | **verified real** |
| F2 | med | backlog-closures | `BACKLOG.md:124` (#79) is marked `~~struck~~ RESOLVED 2026-06-03` **in place** rather than removed; ADR-65 Decision 1 states done items **leave** the file and explicitly rejected in-file stubs | `sed -n '124p' BACKLOG.md` → struck-through entry present; `ADR-65 §Decision/§Alternatives` → "done items leave" + "one-line stubs in-file — rejected" | **verified contradicts ADR-65 as written; disposition is operator's call** |
| — | low | journal | JOURNAL "2 commits on `docs/playbook-toc`" vs git's 3 commits on the branch | `git log --oneline` on the merged branch | **killed by skeptic** (true-but-irrelevant — count phrasing/style, commits recorded correctly) |

**Note on F2:** the skeptic kept it citing ADR-65; the fact is correct (the in-place strikethrough form contradicts "done items leave"). Whether to **act** (delete the line) or **amend ADR-65** to sanction a transient "recently resolved" marker is a triage decision for the operator — the finding asserts the contradiction, not the remedy. Notably the `validate_backlog` hook did **not** flag it (the strikethrough form evades its done-task schema check), so F2 is net-new vs the hooks too.

---

## Pilot-evaluation block (the point of the exercise)

**(a) Net-new real findings vs `audit.py`'s 12 checks + the pre-commit hooks: 2**
1. **F1 (high)** — cross-file version-stamp drift. None of the 12 checks verify that one doc's reference to another doc's version stamp stays current; freshness check #10 only compares a file's own `last_reviewed` to its own mtime. Net-new.
2. **F2 (med)** — semantic done-item disposition. `validate_backlog` enforces the story-map *schema* but the struck-through-in-place form slips past it; no audit check evaluates "did this closure actually leave the file per ADR-65." Net-new.

**(b) False positives killed by the skeptic: 1** — the JOURNAL "2 vs 3 commits" item, correctly killed as true-but-irrelevant style/phrasing. (Skeptic kill-rate 1/3 = 33%.)

**(c) False positives that survived to the digest: 0 clear-cut.** Both survivors are factually grounded. F2 carries a *disposition* ambiguity (act vs. amend-ADR), not a factual one — flagged for operator judgment, not presented as settled.

**(d) Cost / time.**
- Wall time: **~10 min 14 s** (614,480 ms).
- Workflow output tokens: **~42.3k** (turn-shared `budget.spent()` went 49,591 → 91,917 across the run). **Under the ~80k target.**
- Gross `subagent_tokens` reported by the harness: **272,055** — this is the cache-inflated figure (input + cache-read dominate; per the known token-accounting gotcha, do not read this as real spend). The ~42.3k output delta is the meaningful number.

**(e) Saved workflow's shape.** `parallel([V1,V2,V3])` (barrier — skeptic needs all findings to dedup/cross-review) → 1 Opus skeptic (default-to-kill, consults `docs/decisions/`) → 1 Opus digest. Verifiers pinned `claude-sonnet-4-6`; skeptic/digest inherit Opus. Structured output throughout; `evidence_command` a **required** schema field; in-script post-skeptic filter drops any survivor lacking a state-based evidence command (the `/goal`-equivalent). Verifiers also emit a `checked_clean` list (38 items across the three domains) so absence of findings is informative.

---

## Checked-and-clean (so absence is informative)

The verifiers explicitly confirmed (sample of 38 checked-clean items):
- `HANDOFF_PROCESS.md` header **is** v4.3.2 (the drift is the *reference* in ARCHITECTURE.md, not the source).
- `audit.py` ships **12** checks (`python scripts/audit.py checks`).
- All 10 major merges in the last 40 commits have corresponding JOURNAL entries.
- **15** backlog items (#3, #13, #20, #24, #29, #31, #40, #44, #45, #46, #68, #69, #72, #73, #76, #77) correctly **left** the file on closure — #79 is the lone exception.
- Handoff bundle structure (8 files), pre-commit hook set, plugin-enabled state, ESSENTIALS↔PLAYBOOK summary relationship, deleted-files invariants (README/CHANGELOG/BACKLOG_ARCHIVE not recreated) — all confirmed.

Overall baseline doc-health is high; the two survivors are procedural-alignment gaps, not architectural drift.

---

## Saved-workflow record (operator decision, locked)

Per operator decision this session, **nothing workflow-related is committed to the repo.**
- **Saved (personal):** `C:\Users\1028120\.claude\workflows\conformance-hub` (rerunnable as a personal slash command; not a hub artifact).
- **Run-script copy (auto-persisted by the runtime):** `C:\Users\1028120\.claude\projects\C--Users-1028120-Documents-Dev--dev-knowledge\f68de088-0a41-422b-8cb7-efa3fc0cd13e\workflows\scripts\conformance-hub-wf_c962d194-014.js`.
- **Open R2 question (deferred to the ADR layer):** committing a saved workflow into the hub (`.claude/workflows/`) is the Layer-2 "never executes" boundary question from the #80 research note — a read-only conformance workflow is "a validator in new clothing," but whether it belongs as committed hub orchestration is **ADR/Council territory, not a unilateral call.** Codification (PLAYBOOK/ADR) is deliberately deferred until the feature proves out.

---

## Disposition

Findings are **proposals only**; fixing F1/F2 is a separate scoped session after operator triage. The operator applies the pre-registered kill criterion (**≥1 real net-new finding at a tolerable false-positive rate, or the workflow approach dies and the gates stay**) — this digest presents the evidence; it does not pronounce the verdict.
