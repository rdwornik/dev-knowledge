<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-02

**Date:** 2026-08-02
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-02; confirmed unavailable, consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-08-01-conformance-nightly-digest.md`
**Gap:** 1 day (2026-08-01 → 2026-08-02)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | prior S4 (MED): terminal-setup absent from ecosystem/registry.md | Fixed — commit 12e51c0 added terminal-setup row; V2 verified registry.md now has exactly 9 rows matching VISION.md's fleet count. |
| **OUT OF SCOPE** | prior S1 (MED): JOURNAL entry (t) cites broken SHA ee76c412 | Entry (t) scrolled beyond the 10-entry review window as new entries were prepended. Not re-verified today — not confirmed resolved. |
| **PERSISTING (downgraded)** | prior S3 (HIGH → MED): CONTRIBUTING.md Nightly outcome management describes dead Action as live | Skeptic downgraded from HIGH to MED: ARCHITECTURE.md Ch6 provides an authoritative in-repo correction that mitigates operational impact, but the stale prose persists. Today's S1. |
| **PERSISTING (downgraded)** | prior S2 (HIGH → MED): VISION.md `last_reviewed: 2026-07-25` predates last commit 2026-07-26 | Skeptic downgraded from HIGH to MED on same grounds as prior survival: backward-dated A2 violation, unfixed since 2026-07-31. Today's S2. |
| **NEW survivors** | — | None. |

**Delta counts:** 1 resolved · 1 out-of-scope · 2 persisting (downgraded) · 0 new
**Raw → survived → killed:** 9 → 2 → 7
**Skeptic kill-rate:** 78% (7 of 9 raw findings killed)

---

## Summary

Overall doc health continues to improve incrementally. The terminal-setup registry gap (prior S4, persisting three nights) was resolved by commit 12e51c0, and V3 verified 20 backlog closures as semantically coherent. The 78% skeptic kill-rate reflects effective filtering: four low-severity findings killed (two forward-dated stamps as evidence-not-definitive, one byte-count imprecision as true-but-irrelevant, one journal branch-hygiene snapshot claim as evidence-not-definitive), and three backlog-closure findings killed (one commit subject ambiguity with no harmful effect, one unmeetable Done-when conjunct transparently documented, one architect-ratified closure per ADR-108 §A).

Two medium-severity findings persist. CONTRIBUTING.md's "Nightly outcome management" section continues to describe the retired `.github/workflows/nightly-conformance-triage.yml` in present tense — flagged every nightly digest since 2026-07-31 with no fix; severity held at MED because ARCHITECTURE.md Ch6 provides an in-repo correction. VISION.md's `last_reviewed: 2026-07-25` stamp predates its last commit (2026-07-26) — a genuine backward-dated A2 canonical_freshness violation also persisting since 2026-07-31. The systemic uv infrastructure finding (cloud runtime 0.8.17 vs required 0.11.19) continues to block all session-end governance gates; noted as infrastructure context, not a doc-conformance finding.

<!-- counts: raw=9 survived=2 killed=7 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 9 · **Survived skeptic:** 2 · **Killed false positives:** 7

### High (0)

*(No high-severity findings survived the skeptic.)*

### Med (2)

**S1** — CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (.github/workflows/nightly-conformance-triage.yml) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls /home/user/dev-knowledge/.github 2>/dev/null && echo EXISTS || echo MISSING` → `MISSING`
- **Verdict:** contradicted
- **Proposed fix:** Rewrite CONTRIBUTING.md §"Nightly outcome management" (lines 132–155) to match ARCHITECTURE.md Ch6's documented retired-Action state; replace present-tense workflow description with a pointer to ARCHITECTURE.md Ch6 for the live loop description.
- **Skeptic note:** `.github/` directory confirmed MISSING; deleted at commit 82227f08 (2026-07-08). ARCHITECTURE.md lines 776–780 acknowledges the staleness and explicitly warns against following CONTRIBUTING.md here — a documented deferral, not a ratified decision to leave it wrong. Severity MED (not HIGH): ARCHITECTURE.md Ch6 provides the authoritative correction in-repo, mitigating operational impact. Persisting unfixed since 2026-07-31.

**S2** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-07-26 (A2 violation)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git -C /home/user/dev-knowledge log --date=short --format='%cd' -- VISION.md | head -1` → `2026-07-26`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to a date on or after 2026-07-26.
- **Skeptic note:** Stamp (2026-07-25) is BEFORE the last commit (2026-07-26) — exact backward-dated condition that triggers the canonical_freshness A2 gate failure. No ADR or documented decision covers leaving this backward-dated. Persisting unfixed since 2026-07-31.

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — "origin now holds exactly main + automation/fleet-audit, no worktrees, no feature or backup refs" (JOURNAL.md:29)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The evidence command (`git branch -a` run on 2026-08-02) proves the CURRENT branch state, not the state when JOURNAL entry (f) was written on 2026-08-01 EOD. A journal entry is a historical snapshot of what was true at write time; a branch disappearing after the entry was made does not contradict what the entry recorded.

**K2** — "PASTE_THIS 46,051 bytes (under the 65,000 budget)" (JOURNAL.md:53)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Actual file is 46,052 bytes — a one-byte discrepancy. The material conformance claim (file is under the 65,000-byte budget) is unambiguously true at either figure. No check or gate depends on the exact byte count matching the journal log.

**K3** — "ESSENTIALS.md frontmatter `last_reviewed: 2026-07-30` — stamp is forward-dated vs last commit 2026-07-29" (protocols/ESSENTIALS.md:2)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Stamp (2026-07-30) is LATER than the last commit (2026-07-29T14:31:30+02:00). Forward-dated stamps do NOT fail the canonical_freshness A2 gate — only backward-dated stamps fail. Same pattern as K4/K5/K6 from 2026-08-01 digest.

**K4** — "CLAUDE.md frontmatter `last_reviewed: 2026-07-31` — stamp is forward-dated vs last commit 2026-07-30" (CLAUDE.md:2)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Stamp (2026-07-31) is LATER than the last commit (2026-07-30T22:32:12+02:00). Forward-dated stamp; does not fail the canonical_freshness A2 gate. Identical kill rationale to K3.

**K5** — "Merge commit 31c8071 emits 'closes [#465]' in subject but #465 is still open — only leg 1 of 4 Done-when clauses delivered" (31c8071)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The commit subject reads "closes [#459] [#461], [#465] leg 1: ..." — the [#465] reference appears after a comma with "leg 1" qualifier, not a clean "closes [#465]" token. No harmful effect materialized: BACKLOG.md row at line 266 confirmed still present and task file status is open. The body's "row stays OPEN" clarification is unambiguous. Ambiguous phrasing that caused no closure is a style concern, not a conformance failure.

**K6** — "Commit 9039d2d closes [#458] but Done-when 'PLAYBOOK freshness stamp rides a genuine re-read' was not met" (9039d2d)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** PLAYBOOK.md is NOT in `_FRESHNESS_FILES` (audit.py:248 documents the 8 gated files; PLAYBOOK absent by design) and carries no `last_reviewed` stamp. The freshness-stamp Done-when conjunct was drafted assuming a stamp mechanism that does not apply to PLAYBOOK.md. The actual substantive deliverable (note in Ch8 with witness cited) was delivered. Acknowledged non-performance of a structurally unmeetable conjunct, fully documented in the commit, is not a closure defect.

**K7** — "Commit a42e5fc closes [#370] but Done-when 'marker/template/test work...ruled into row or follow-on' not met in literal sense" (a42e5fc)
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-108 §A explicitly vests the architect with authority to make the call, record it, and rely on revertability. Commit body documents the Done-when is self-referential (names no deliverable), prior refusals were on evidence grounds (d66aef63, 4911f009), and the non-blocking follow-up is recorded in JOURNAL. Architect-ratified closure within ADR-108 §A authority.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; entries (f)–(v), all within shallow-clone boundary):**
- Entry (f) SHA anchors 31c80714, 3c050b15, 16ebdeb0, 80dd54d6 — all verified in git log with correct descriptions ✓
- Entry (f) BACKLOG.md task count 186 — confirmed by grep count ✓
- Entry (f) handoff bundle `docs/handoffs/2026-08-01-dev-knowledge-architect-2/` with all 5 files — confirmed on disk ✓
- Entry (e) SHA anchors 6786318, 80e743aa, 0216acb7, bf373b13 — all verified in git log ✓
- Entry (d) all 6 post-reword SHAs (d48ebd65, c7c2905c, 95e86721, 12e51c06, 8e285499, 8f81b48f) — all verified ✓
- Entry (c) SHA anchors 61496aca, e4d3a920, f049e3a2, 812ee192 — all verified ✓
- Entry (b) SHA anchors acb26d38, af6fa93f, 9039d2d0, 8636e565, bdd7f8aa, 6b158858, cae18323, 13d9cc16 — all verified ✓
- Entry (a) SHA anchors c7af2c03, 3aab4d28, c5507f50 — all verified ✓
- Entries (y)–(v): SHA anchors 9a75777, 597c81a, 1afd957, 5fc6b8ab, a489402f, 626c51bb, f4c3503f, ede6fc5a — all verified ✓
- 50+ SHA anchors checked across 10 entries; no significant unattributed merged work found ✓

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-08-01` — passes A2 gate ✓
- VISION.md fleet count "nine git repos" — ecosystem/registry.md has exactly 9 rows ✓
- Pre-commit hook count 15 — matches `.pre-commit-config.yaml` exactly ✓
- Audit check count 38 — matches `ALL_CHECKS` in `scripts/audit.py` exactly ✓
- CLAUDE.md §8 skills: `.claude/skills/` holds exactly `verify` + `check-against-spec` ✓
- ARCHITECTURE.md "five carriers" — exactly 5 `carrier_*.py` files in `deploy/` ✓
- CLAUDE.md §9 ruff pin v0.15.5 — matches `.pre-commit-config.yaml` rev ✓
- CLAUDE.md §9 pre-commit hook roster (15 hooks) — matches `.pre-commit-config.yaml` set ✓
- ESSENTIALS.md "audit check #7 retired" — `check_mermaid_theme_directive` marked RETIRED in audit.py and absent from `ALL_CHECKS` ✓
- `.claude/commands/` (5 files) — matches generated `.claude/generated/commands-repo.md` enumeration ✓
- ARCHITECTURE.md "six chapters" — six ##-level chapter sections confirmed ✓
- VISION.md audit.py subcommands 6 — all 6 confirmed as `@cli.command()` decorators ✓
- tier1-lifecycle plugin enabled in `.claude/settings.json` ✓
- ADR-109 referenced in ARCHITECTURE.md exists on disk ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-12 → 2026-08-02):**
- 20 closures verified semantically coherent: #459, #461, #462, #460, #469, #466, #467, #468, #471, #382, #35, #41, #367, #435, #437, #439, #444, #386, #434, #436 ✓
- #462: terminal-setup added to registry.md; check_membership_agreement (ALL_CHECKS 37→38) confirmed ✓
- #382: ADR-109 accepted, schema v1 committed at ecosystem/schema/ — both Done-when clauses met ✓
- #437: shared helper `closure_ids/strip_quoted_contexts` authored once, byte-identical plugin twin; 110 tests green ✓

---

## Next Actions (proposals for operator)

1. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (session-end backpressure, pre-commit hooks fail with version mismatch). Blocks from prior digests.

2. **S2 (MED)** — Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to on or after 2026-07-26. The A2 canonical_freshness gate fires at every audit run. Four-day backlog.

3. **S1 (MED)** — Update CONTRIBUTING.md §"Nightly outcome management": replace present-tense GitHub Action description with a tombstone pointer to ARCHITECTURE.md Ch6. Four-day backlog; low-effort fix.

4. **(OUT OF SCOPE — needs manual verify)** Prior S1: JOURNAL.md entry (t) broken SHA anchor `ee76c412` has scrolled beyond the 10-entry review window. Operator should manually verify whether it was corrected (re-entry rewrite) or remains a broken reference at JOURNAL.md:257.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-02-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
