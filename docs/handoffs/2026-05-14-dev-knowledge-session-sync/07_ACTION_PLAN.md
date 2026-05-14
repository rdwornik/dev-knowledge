# Action Plan — .dev-knowledge (session-sync) 2026-05-14

<!-- scope: meta -->

---

## Next session goal

The next `.dev-knowledge` session should complete two objectives in sequence.

**First:** Validate the v3.3.1 handoff cycle empirically and capture the session lessons that were
identified but not yet committed. The new chat receiving this bundle is the first real test of
whether audience-aware Stage 2 text (per the seven rules in v3.3.1) closes the internalization gap.
Assessment happens during the new chat's first turns: does the articulation gate succeed on first
attempt? Does the new chat need additional document uploads? The five primary and three secondary
failure patterns observed during the recent extended session belong in LESSONS.md now.

**Second:** Begin PLAYBOOK content additions for ADRs 36, 37, 40, and 41 [Stream C P1,
methodology debt since 2026-04-30]. These are the highest-priority open Stream C items. PLAYBOOK
additions take priority over Audit tool P1 implementation because: PLAYBOOK is documentation-shaped
work (one file, additions to existing structure, low context-load per session), while Audit tool is
code-shaped work (multiple files, design decisions, dedicated session). ADR-36 codifies the audit
tool workflow — PLAYBOOK must reflect it before Audit tool implementation begins.

---

## Action plan

1. **Complete this handoff cycle.**
   Operator opens new claude.ai chat, uploads all 11 files from this folder, pastes `00_first-message.md`
   as first message. New chat completes articulation gate → operator types `role confirmed` → new chat
   presents receiver synthesis → operator confirms.
   Verification: articulation gate produces coherent 4-item output on first attempt; synthesis confirmed
   without correction; new chat does not need additional document uploads during first turns.

2. **Validate v3.3.1 empirically and capture session lessons.**
   Assess: (a) did the Stage 2 response exhibit audience awareness — were the seven gap patterns absent?
   (b) did the articulation gate in `00_first-message.md` trigger and produce a coherent articulation
   on first attempt? (c) did the operator need to upload any additional documents during the new
   session's first turns?
   Then generate a Claude Code prompt as downloadable `.md` (scale M, single commit on a feature branch)
   to append the five primary and three secondary observations from `06_STATE_OF_PLAY.md` ("Work in
   progress not yet captured" section) to LESSONS.md per ADR-29 format [scope tag required on each
   new entry]. Eight entries total.
   Verification: eight new LESSONS entries committed; CHANGELOG and JOURNAL entries; `pre-commit run
   --all-files` passes; merge via `--no-ff` after operator approval.

3. **Begin PLAYBOOK content additions for ADRs 36, 37, 40, 41** [Stream C P1].
   Generate a Claude Code prompt as downloadable `.md` (scale M). Read each ADR from
   `docs/decisions/`: ADR-36 (audit tool architecture and workflow), ADR-37 (two-phase handoff
   guidance with Current/Future State overlay), ADR-40 (tier transition procedures for repo scale
   changes), ADR-41 (BACKLOG grooming workflow with cross-session protocols). Draft a PLAYBOOK.md
   section for each ADR. Update PLAYBOOK header version and date. Scope-tag all new sections.
   Verification: `validate_scope_tags.py` passes; hybrid ceiling ≤25%; PLAYBOOK line count within
   reason; single commit; `BACKLOG.md` item marked [done].

4. **Address pre-existing test failure if still tracked in BACKLOG** [P2 priority].
   Bundle into a small session or schedule after PLAYBOOK additions.
   Verification: `pytest -x --tb=short` exits clean.

5. **If directive #1's articulation gate fails partially** — new chat cannot articulate from bundle,
   or paraphrases superficially without grounding — diagnose specifically: bundle insufficient (file
   missing or unreadable), `00_first-message.md` instruction unclear, or new chat ignored the gate.
   Refine v3.3.1 to v3.4 in a separate dedicated session. Documented escalation paths: grounded Q&A
   gate or simulation gate.

---

## Hard Constraints

- **Do NOT escalate to v3.4** until v3.3.1 empirical results are in. The audience-awareness rules
  need at least one full handoff cycle to assess before raising the articulation gate further.
- **Do NOT skip the articulation gate** in `00_first-message.md` even if the operator forgets to
  require it. The gate is the v3.3 mechanism whose efficacy under v3.3.1 audience-aware Stage 2 is
  being measured; skipping invalidates measurement.
- **Do NOT modify HANDOFF_FOLDER_TEMPLATE.md** (Stage 3 template) in this handoff cycle. v3.3.1
  scope was Stage 1 template only.
- **Do NOT capture session lessons as architectural ADRs** — these are observations of failure
  patterns and belong in LESSONS.md, not in `docs/decisions/`.
- **Do NOT begin Audit tool P1 implementation** in the same session as PLAYBOOK additions unless
  PLAYBOOK completes cleanly first — context-load risk.

---

## Narrow scope rules

- Do NOT generate cross-repo directives targeting ai-council, corp-monorepo, corp-ops, or
  corp-sca-time-automation from a `.dev-knowledge` session. Cross-repo work routes via routing
  artifacts per the Universal Self-Containment Rule.
- Do NOT combine PLAYBOOK additions with the test failure fix in a single commit — different concerns.
- Do NOT add ESSENTIALS.md sections without first verifying line count via `(Get-Content protocols/ESSENTIALS.md).Count` — current count is 323 lines; under-1-page constraint requires pruning before adding.
- Do NOT amend ADR-42 in this session's work. v3.3.1 is template/process-level.

---

## Fallback contingencies

- If Stage 3 bundle is insufficient (articulation gate flags a missing file or unreadable section):
  operator uploads the missing material once, note the gap in JOURNAL, refine v3.3.1 spec for next
  iteration.
- If articulation gate fails because new chat ignores or paraphrases superficially: diagnose — was
  the gate visible in `00_first-message.md`? Was operator-validation step skipped? Refine the
  instruction; do not just retry.
- If lessons capture surfaces additional observations beyond the eight identified: append them; do
  not recompute the list.
- If PLAYBOOK additions surface contradictions with existing methodology: stop, raise the
  contradiction for explicit operator decision; do not auto-resolve.

---

## Success criteria

Session is complete when:
- Articulation gate result observed and recorded in JOURNAL (pass or failure mode identified)
- Eight LESSONS entries appended and committed (if articulation gate passed and new chat executes)
- PLAYBOOK additions committed for ADRs 36, 37, 40, 41 with scope tags passing
- BACKLOG Stream C P1 items marked [done] for PLAYBOOK additions
- `validate_scope_tags.py` and `pre-commit run --all-files` passing
- CHANGELOG entry for session
- JOURNAL entry for session
