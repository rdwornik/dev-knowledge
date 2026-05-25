# State of Play — 2026-05-25-dev-knowledge-session-sync

<!-- scope: hybrid -->

Current State per ADR-37 [session-boundary protocol]. Source: Stage 2 architect
REALITY + RATIONALE answers, reconciled and verified against repo state at
Stage 3. Relative dates converted to absolute against the 2026-05-25 Stage 1
anchor.

## Current state

- **HEAD at Stage 3:** `2b29329490acfa3484e1a9807845f31d3922ae9a`
- **Branch:** `docs/handoff-stage1-2026-05-25-dev-knowledge`
- **Working tree:** clean apart from this handoff's own generated files
- **Tests:** `pytest` → 72 passed (Stage 3 verified 2026-05-25)
- **Stage 1 pinned HEAD:** `328ded75b3a64b4191fca1fe418374671a120a14` (ancestor of
  Stage 3 HEAD — drift check passed)

## What was completed in the recent session arc (2026-05-23 → 2026-05-25)

- **Repo-tier system fully deprecated.** Task-sizing Scale S/M/L is preserved as
  an orthogonal authoring aid. The `ARCHITECTURE.md` mandate was universalized
  across all repos regardless of size; `README.md` was deprecated from the
  baseline; a root-hygiene convention was added (`.env.example` no-create policy;
  dot-prefix-where-supported); the audit tool was unified to a governance-docs-only
  baseline check.
- **Self-audit completed against the amended standards** — 15 findings fixed,
  including operator-flagged tier residue in `ARCHITECTURE.md`, a live "Project
  Scale Tiers" section in `ESSENTIALS.md` that sat past a naive grep's hit-cap,
  and an `[L+M]` tag caught only by a post-remediation tag-specific re-grep.
- **BACKLOG audit completed** (~48 entries categorized). It surfaced bookkeeping
  lag: four items closed in repo reality were still marked "open" in BACKLOG,
  caught only by a live-state check (not by commit-name matching).
- **Handoff-process audit residuals resolved.** The medium/low findings from the
  relevant audit were closed; the multi-file bundle structure was preserved; the
  `_in_progress/` → `in-progress/` directory rename landed; residual `CHANGELOG`
  references were struck from the Stage 3 procedure per ADR-49 [past-recording
  consolidation].
- **Workspace combo iterated to a stable state** — multi-root with dated-artifact
  aliases at the bottom; `explorer.sortOrder: default` + `sortOrderReverse: true` +
  `compactFolders: false`; six canonical-file workspace tasks added
  (`open-vision`, `open-journal`, `open-backlog`, `open-architecture`,
  `open-lessons`, `open-claude-md`).

## Decisions locked this session

- **The 11→N handoff-bundle consolidation was rejected on a broken premise, and
  deferred rather than deliberated.** The proposal's file-map named source files
  that do not exist in the repo; verification against a live bundle showed the
  real inventory includes the VISION/PLAYBOOK/ESSENTIALS invariant copies plus the
  `01_manifest.json` SHA-256 manifest — none of which the map mentioned.
  Mechanically executing it would have silently dropped those, which is materially
  the ADR-45 direction that was rolled back. The operator chose "audit fixes only"
  and flagged the substantive consolidation question for proper deliberation.
- **ADR-45's `Supersedes: ADR-42` claim was withdrawn.** ADR-45's v4
  mechanical-gates rewrite was explored and rolled back the same night; a design
  that did not stick cannot supersede ADR-42. The fix struck the supersession
  header (strikethrough, preserving the record), annotated the References line,
  and added an Amendment 2026-05-25. ADR-42 v3 + amendments remains the live
  convention.
- **The audit residuals were split from the consolidation into a separate scope.**
  The residual findings were each audit-endorsed, "< 10 lines", structure-preserving
  hygiene against the protocol's v3.0 → v3.3.3 evolution (low risk). Consolidation
  had no audit endorsement and no reality-based design (high architectural impact,
  Council-deliberation territory). Splitting kept the safe work immediately
  executable while fencing the architectural work for deliberation.

## Open decision threads (need an operator call before related work proceeds)

- **Handoff-bundle structural scope (11→N).** Genuinely open — there are real
  token-cost and ceremony-decay concerns — but the answer requires AI Council
  deliberation grounded in the real bundle inventory plus an explicit decision on
  whether to re-open ADR-45. Not routine refactoring. (See `07_ACTION_PLAN.md`
  action 1 and Hard Constraint 1.)
- **ADR-45** needs no further action *unless* consolidation is pursued, which
  would re-open it.

## Risk carried into the next session: the verification-miss pattern

The recent arc produced N=7 verification-miss instances (architect-witnessed):
factual claims about ADR contents the cited ADR did not state; a hallucinated
file-mapping table in a substantive refactor prompt; a missed file-existence check
(a "frontmatter mechanism" proposed where the system actually uses a Registry);
claims about merge state contradicted by the repo log; a CHANGELOG-mandate line
inserted into proposed user preferences while ADR-49 retirement was being codified.
The pattern is recorded in `LESSONS.md`, but the mechanism is behavioral, not
knowledge: confidence is itself a signal to verify harder. The next session should
treat any substantive prompt about existing-system state as requiring a mandatory
pre-flight pass (read live files end-to-end + cited ADRs in full) before design.
This is encoded as Narrow-scope rule 3 and Hard Constraints in `07_ACTION_PLAN.md`.

## Deferred items (BACKLOG references — not duplicated here)

Read the live `BACKLOG.md` for full entries. Most relevant to this repo:
- **[P1] Codify scrum-master review authority pattern** — N=3 grounding; unblocked.
- **[P1] Sacred-files maintenance enforcement.**
- **[P1] Council decisions management consolidation** — contradiction detection +
  ownership model + retrievable index.
- **[P2] Lessons activation P1**, **ESSENTIALS cheat-sheet additions**, **Hooks
  audit + consolidation**, **Skills universalization**.
- **[P3] CLAUDE.md §4 stale-test fix**, **SESSION_SETUP.md:209 CHANGELOG strike**,
  **ADR relationship/supersession graph**, **PLAYBOOK codifications from the
  2026-05-19 posture audit**, **ADR-39/ADR-41 grouped amendments**.
- **New (to capture, action 4):** remote + nightly batch on schedule; Chinese
  model adoption (GLM, Kimi K2); continuous token optimization.

## Stage 3 verification summary

The architect provided witnessed claims; Stage 3 classified them:

- **Verified against repo state:**
  - ADR-45 `Supersedes: ADR-42` withdrawal — confirmed: strikethrough at
    `ADR-45-handoff-architecture-v4.md:7` + Amendment/Decision block (~:391-397).
  - `protocols/SESSION_SETUP.md:209` "append JOURNAL + CHANGELOG" drift — confirmed
    present (in a Stage 3 procedure bullet). Action 5 target valid.
  - `CLAUDE.md` §4 stale known-failing test
    (`test_audit_run_passes_structural_checks_on_synthetic_repo`) — confirmed at
    `CLAUDE.md:43`; suite is green (72 passed), so the note is stale. Action 5
    target valid.
  - Unmerged branches `docs/audit-ai-council-2026-05-23-deep`,
    `docs/audit-corp-monorepo-2026-05-23-deep`, and
    `chore/workspace-sort-default-2026-05-24` — confirmed to exist (`git branch`).
- **Unverifiable from repo (preserved as-is):** conversation-history claims —
  the N=7 verification-miss count, the N=3 scrum-master grounding, the
  operator-stated future items, and the "operator chose audit-fixes-only" framing.
- **Architect-flagged inferences (preserved with flag):** "audit reports already
  exist on main"; "SessionStop hook absent"; "N=3 grounding reached"; "user-instructions
  update affects future chats only".
- **Stage 3 clarifications / soft flags:**
  - The architect repeatedly refers to a **"12-file bundle."** That is the
    *cross-repo* count. **This bundle is a self-handoff (target = `.dev-knowledge`),
    so it is 11 manifest-tracked files** — `02b_ECOSYSTEM_VISION.md` is correctly
    omitted (it would duplicate `02_VISION.md`). The invariant-copies + manifest
    principle the architect describes is intact; only the count differs by one.
  - The architect cited "six medium findings closed"; the repo log shows the
    residual fixes landed as **five** commits (M-1, M-2, M-3, M-5, M-6) plus the
    `in-progress` rename (L-3 was a LOW). Count is approximate; the substance
    (residuals resolved, structure preserved) is verified.
