# Action Plan — 2026-05-25-corp-monorepo-session-sync

---

## Next session goal

Verify ADR-27 (safety-invariants) implementation status before any other work. Stage 3 verification confirmed that `src/corp/safety/onedrive.py` and `tests/safety/test_no_unguarded_writes.py` are absent — the ADR is merged but the code has not been written. Directive #1 must produce a written audit record before the session proceeds to any P1 BACKLOG item. If the implementation is confirmed missing, the session routes into foundation module implementation (PR 1 of the 4-PR plan); if somehow complete, proceed to directive #2. Directives #2–#6 follow in sequence only after directive #1 is closed.

---

## Action plan

**1. Audit ADR-27 implementation status** — Read `docs/decisions/ADR-27-safety-invariants.md` in full. Run `git ls-files src/corp/safety/` and `git ls-files tests/safety/`. Check whether `OneDriveSafetyError` is imported from `src/corp/safety/onedrive.py` or from `src/corp/cleanup/errors.py`. Check `deck_actions.py:104` write-intent caller. Write audit findings to `docs/audits/2026-05-25-adr27-status.md` with: verified-present items, verified-absent items, drift list, and recommended next PR. COMMIT. If implementation missing → route session into PR 1 (centralized `src/corp/safety/onedrive.py` foundation module); defer directives #2–#6 to next session.

**2. Resolve ADR namespace collision** — Read `CLAUDE.md §11`. Confirm that .dev-knowledge `ADR-27` and corp-monorepo `ADR-27` are distinct files with the same number. Draft a corp-local ADR numbering convention using `CMR-NN` prefix. Update corp-monorepo `CLAUDE.md §11` to note the CMR-NN convention and list active corp-local ADRs. Do not renumber existing ADRs. COMMIT on branch `docs/cmr-namespace`.

**3. Remove tier/scale frontmatter from all corp-monorepo files** — Run `grep -r "^tier:" .` and `grep -r "^scale:" .` from repo root. For each file with `tier:` or `scale:` frontmatter: remove those lines, preserve all other frontmatter fields, ensure `version`, `last_reviewed`, `owner`, and `status` are present (add if absent). COMMIT on branch `chore/tier-deprecation`. Run `grep -r "^tier:" .` again to verify zero matches before committing.

**4. Disambiguate ADR-34 vault underscore rule in `CLAUDE.md §4`** — Read `CLAUDE.md §4` (Conventions). Add a single clarifying sentence: Obsidian vault files referenced within corp-monorepo follow the underscore convention per ADR-34 Obsidian exception; all other corp-monorepo files use hyphens. Do not change any other content in §4. COMMIT on existing branch or `docs/adr34-disambig`.

**5. Draft scrum-master review authority ADR** — Create `docs/decisions/CMR-01-review-authority.md` (or next available CMR-NN number as determined in directive #2). ADR must specify: who has merge-gate authority on architectural changes, what the Codex `/review` requirement is for safety-critical and High-risk paths, and what constitutes an architectural change in corp-monorepo. Use corp-monorepo ADR template if present; otherwise use .dev-knowledge ADR template structure. COMMIT on branch `docs/cmr-review-authority`.

**6. Record README disposition in JOURNAL** — `corp-monorepo/README.md` was deleted or is under evaluation. Record the final disposition (retained, deleted, or deferred) as a JOURNAL entry with the rationale. Do not create, recreate, or modify README.md itself — only record the decision. COMMIT.

**7. DEFER the following** — Do not begin in this session: Phase 2 universalization rollout; hyphen migration (ADR-38 subitems 1 and 3); handoff folder format adoption across other repos; root hygiene; `renderer.py` drift fix and `deck_actions.py:104` caller fix (defer to ADR-27 implementation session).

---

## Hard Constraints

**1. Do not renumber existing ADRs** — existing `ADR-27-safety-invariants.md` keeps its filename; the CMR-NN prefix applies only to new corp-local ADRs going forward.

**2. Do not touch "OneDrive - Blue Yonder" paths, even read-only** — hard exclusion, no exceptions. If any path in a glob or grep result contains "OneDrive - Blue Yonder", skip it without reading.

**3. Do not write commit messages containing the literal string "OneDrive - Blue Yonder"** — the pre-commit hook blocks it. Use `git commit -F <msgfile>` with the message in a temp file instead.

**4. Do not skip Codex `/review` on safety-critical or architectural changes** — any change to `src/corp/safety/`, `src/corp/cleanup/`, or a new ADR must go through Codex `/review` before merge. The two-AI-reviewer pattern has caught real bugs; it is not optional overhead.

**5. Do not bypass `tach check`** — run `tach check` before any merge that touches module boundaries. New `src/corp/safety/` work is foundation layer; it must not import from interface or orchestration layers.

---

## Narrow scope rules

- Do not reference `PLAYBOOK.md`, `LESSONS.md`, or `~/.claude/skills/gotchas/gotchas.md` without first verifying those files exist in corp-monorepo (they do not; those are .dev-knowledge / user-level files).
- Do not omit JOURNAL entries — each directive that produces a commit must have a corresponding JOURNAL prepend with Did/Failed/Next.
- Do not start Phase 2 universalization or hyphen migration in the same session as directive #3 (tier-deprecation) — scope creep risk is high.
- Do not auto-merge architectural changes — always require explicit "merge confirmed" from Rob.
- Do not assume .dev-knowledge conventions (ESSENTIALS, PLAYBOOK, scope tags) are auto-loaded in corp-monorepo — verify each one against corp-monorepo `CLAUDE.md` before applying.

---

## Fallback contingencies

- **If directive #1 reveals ADR-27 implementation is partially present (some files exist, others absent):** Document exactly what is present and what is missing in `docs/audits/2026-05-25-adr27-status.md`. Do not attempt partial fixes mid-audit. Close the audit record first, then route to the appropriate PR.
- **If directive #1 confirms ADR-27 is fully absent:** Route the entire session into PR 1 of the 4-PR plan (foundation module `src/corp/safety/onedrive.py`). Defer directives #2–#6 to the next session. That is the correct outcome — safety invariants are P0.
- **If namespace collision is contested (directive #2):** Do not unilaterally assign CMR-NN prefix. Raise to AI Council or flag to Rob before modifying `CLAUDE.md §11`.
- **If Rob is unavailable for ADR-34 vault disambiguation (directive #4):** Do not modify any Obsidian vault references. Document the deferral in JOURNAL and skip directive #4 for this session.
- **If directive #1 takes the entire session:** Accept this. Do not compress audit work to make room for later directives. A thorough ADR-27 audit record is worth more than a rushed tier-deprecation pass.

---

## Success criteria

- `docs/audits/2026-05-25-adr27-status.md` exists and contains verified-present, verified-absent, and drift lists (directive #1).
- `grep -r "^tier:" . && grep -r "^scale:" .` returns zero matches across all corp-monorepo files (directive #3).
- corp-monorepo `CLAUDE.md §11` mentions CMR-NN convention (directive #2).
- corp-monorepo `CLAUDE.md §4` contains a sentence disambiguating Obsidian vault underscore exception (directive #4).
- `tach check` passes on every commit branch before merge.
- All commits are Conventional Commits format; working tree is clean at session end.
- JOURNAL has an entry for each completed directive.
- No regressions in `pytest -x --tb=short`.
