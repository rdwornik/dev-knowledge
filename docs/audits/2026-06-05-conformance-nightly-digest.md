<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-05

**Date:** 2026-06-05
**Author:** Claude Code (claude-sonnet-4-6), operator Rob
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-05, confirmed unavailable).

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` (Explore subagent) | claude-sonnet-4-6 |

All five stages ran on `claude-sonnet-4-6` (the orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). This is the correct behavior for the fallback path — note for comparison with the prior run where Haiku 4.5 unexpectedly inherited.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-04-pilot81-hub-conformance-digest.md`
**Prior findings:** F1 (high) ARCHITECTURE.md HANDOFF_PROCESS v4.3.1 stub; F2 (med) BACKLOG.md #79 in-place strikethrough

| Status | Finding | Evidence |
|---|---|---|
| **RESOLVED** | F1 (high): ARCHITECTURE.md stale HANDOFF_PROCESS stamp v4.3.1 | Fixed by commit `d5753a8` — bumped references to v4.3.2 |
| **RESOLVED** | F2 (med): BACKLOG.md #79 in-place strikethrough stub | Fixed by commit `f88accb` / `052e311` — item removed per ADR-65 |
| **NEW** | S1 (med): ARCHITECTURE.md + CONTRIBUTING.md still reference HANDOFF_PROCESS v4.3.2 but actual file is now v4.4 | HANDOFF_PROCESS bumped to v4.4 in commit `1334110` (2026-06-04 23:13) — same recurrence class as F1 |

**Delta counts:** 2 resolved · 0 persisting · 1 new

---

## Summary

Documentation conformance remains strong. The skeptic killed 2 of 3 raw findings (kill-rate 67%), leaving 1 genuine survivor: ARCHITECTURE.md and CONTRIBUTING.md version-stamp references lag behind HANDOFF_PROCESS.md v4.4 (bumped 2026-06-04 22:00, stamps still claim v4.3.2). This is the same recurrence class as the prior F1 — the fix in `d5753a8` correctly updated to v4.3.2, but the subsequent v4.4 amendment to HANDOFF_PROCESS landed the same day, post-ARCHITECTURE.md edit. 28 items were verified clean across JOURNAL→git, living-doc claims, and backlog-closure coherence.

---

## Findings (PROPOSALS ONLY)

**Raw:** 3 · **Survived skeptic:** 1 · **Killed false positives:** 2

### High (0)

*(none)*

### Med (1)

**S1** — `living-docs` — ARCHITECTURE.md and CONTRIBUTING.md reference HANDOFF_PROCESS v4.3.2, but canonical file is v4.4

- **Location:** `ARCHITECTURE.md:336`, `ARCHITECTURE.md:402`; `CONTRIBUTING.md:169`
- **Evidence command:** `grep -E 'stamp.*4\.' /home/user/dev-knowledge/ARCHITECTURE.md /home/user/dev-knowledge/CONTRIBUTING.md && grep '^Version:' /home/user/dev-knowledge/protocols/HANDOFF_PROCESS.md`
- **Verdict:** contradicted
- **Proposed fix (proposal only):** Update ARCHITECTURE.md lines 336 and 402, and CONTRIBUTING.md line 169 to reference HANDOFF_PROCESS v4.4 and re-stamp `last_reviewed`
- **Skeptic note:** HANDOFF_PROCESS.md was bumped to v4.4 on 2026-06-04 23:13:07 per commit `1334110`. Both living docs were edited the same day but earlier (00:52 and 23:13 UTC respectively — ARCHITECTURE.md's last_reviewed predates the v4.4 commit). Genuine staleness: the canonical source moved but the cross-references were not updated.

### Low (0)

*(none)*

---

## Killed Findings

| Claim | Kill reason | Detail |
|---|---|---|
| #88 closure references evidence file at `corp-monorepo docs/audits/2026-06-04-graphify-pilot.md` not present in dev-knowledge repo | `true-but-irrelevant` | ADR-65 establishes git + JOURNAL as the technical and business records. Cross-repo evidence paths are not a conformance violation; outcome is documented in local handoff (04_RECENT.md) and JOURNAL. |
| C4 nightly-Action commits (57d9450, 70ff6b5) lack `closes [#id]` or `advances #id` tags | `documented-decision` | JOURNAL.md 2026-06-05 pre-handoff sweep explicitly states C4 is a "legitimate no-item class" distinct from #85's local track — operator-authorized exception. |

---

## Checked-and-Clean (28 items — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries):**
- 2026-06-05 session-2: Phase 2 consolidate claims about commits `e90a1fe` and `2bac2d2` verified in git history
- 2026-06-05 v44-wrap: Phase 2 consolidate bundle at `docs/handoffs/2026-06-05-dev-knowledge-v44-wrap/` verified in filesystem
- 2026-06-05 session: Phase 2 consolidate bundle at `docs/handoffs/2026-06-05-dev-knowledge-session/` verified in filesystem
- HANDOFF_PROCESS v4.4 amendment (A–F): v4.4 header present in `HANDOFF_PROCESS.md`, file separators present in bundles
- Pre-handoff sweep: #87 withdrawal, #83 note correction, #89/#90 addition verified in commit `1f22630`
- Phase C4 nightly triage Action: `.github/workflows/nightly-conformance-triage.yml` added in commit `57d9450`
- Phase C4 `surface_triage.ps1` verified in filesystem and commit `70ff6b5`
- Phase C3 model-routing re-probe verified in commits `f6c35cb` and `bdde839`
- PR #1 merge commit `205da14` exists with nightly conformance digest
- Nightly triage Action merged in commit `2842e52` (`feat/nightly-pr-manager`)
- Synthetic test PRs reverted (commits `75df9d9` and `3b4042f`) — cleanup confirmed
- CONTRIBUTING.md updates verified with hook-table sync (commit `d0cfe27`)
- Fleet health fail-soft landing verified in commit `d0cfe27`

**V2 (living-doc factual claims):**
- ARCHITECTURE.md: eight pre-commit hooks listed match `.pre-commit-config.yaml` (normalize-dated-headers, codemap-freshness, toc-freshness, toc-freshness-playbook, validate-backlog, audit-health, ruff, backlog-id-on-close)
- ARCHITECTURE.md: codemap two-node diagram claim — `scripts/codemap/` and `scripts/toc/` both exist as Python packages
- CONTRIBUTING.md: audit-health ships 12 self-conformance checks — verified against `ALL_CHECKS` registry in `audit.py`
- CONTRIBUTING.md: handoff bundle is 8-file structure (README + 01_ROLE through 07_ASK_BACK)
- CLAUDE.md: ruff version-pinned `>=0.15.5` enforced as pre-commit gate — verified in `.pre-commit-config.yaml`
- CLAUDE.md: freshness cadence with `last_reviewed` stamp and `audit.py` check #10 — verified in `audit.py` and CLAUDE.md §4
- All living docs exist: VISION.md, CLAUDE.md, ARCHITECTURE.md, CONTRIBUTING.md
- `protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md` exist
- `BACKLOG.md` exists
- Root `README.md` deleted per ADR-38 amendment A5 (2026-05-23) — confirmed absent
- `CHANGELOG.md` deleted per CLAUDE.md critical rule #8 — confirmed absent
- Ecosystem registry: 5 repos confirmed (`.dev-knowledge`, `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`)

**V3 (backlog-closure semantic coherence):**
- `5f327b2` closes [#88]: graphify REJECT verdict recorded with measurements; item promised pilot measurements + adopt/reject ruling — coherent
- `d5753a8` closes [#78]: consolidated docs-refresh pass with diffs to ARCHITECTURE + CLAUDE + `last_reviewed` re-stamped; item promised both files in one end-to-end re-read — coherent
- `052e311` closes [#79]: codemap grounding with outcome recorded; subsequent removal per ADR-65 rule — coherent

---

## Next Actions (proposals for operator)

1. Update `ARCHITECTURE.md` lines 336 and 402 and `CONTRIBUTING.md` line 169 to reference `HANDOFF_PROCESS v4.4`; re-stamp `last_reviewed` on both files after genuine end-to-end review.
2. Consider adding an `audit.py` check that cross-references `HANDOFF_PROCESS.md` version header against the version stamps in ARCHITECTURE.md and CONTRIBUTING.md — this is the third time this recurrence class has surfaced (#81 arc lesson).

---

## Safety Tripwire

`git status --porcelain` output at review completion (before this digest file was written):

```
(empty — clean working tree)
```

Only this digest file was written during the review. If any other tracked file appears in the porcelain output on the PR branch, that is a safety breach.

`git status --porcelain` output on this branch (post-digest write, pre-commit):

```
?? docs/audits/2026-06-05-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other changes.
