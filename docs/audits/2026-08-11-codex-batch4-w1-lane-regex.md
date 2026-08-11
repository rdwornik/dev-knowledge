# Codex Review — batch4-w1-lane-regex

**Date:** 2026-08-11
**Branch:** `worktree-lane-a-514-lane-regex`
**HEAD:** `b412ba7d`
**Diff range:** `main..worktree-lane-a-514-lane-regex`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

The two rival LANE_BRANCH_RE constants collapsed to one imported strict constant. Verify: (1) the collapse is a TIGHTENING with no shape newly admitted; (2) the by-NAME import of validate_branch_naming introduces no shadow/import-order hazard that could silently yield a wrong regex rather than a loud failure; (3) the four new tests actually pin the collapse and cannot pass with the loose rival restored; (4) the HONEST LIMITS rewrite is accurate about what is and is not now scoped, especially that roster scoping ([#510]) remains OPEN; (5) the CLAUDE.md/carrier edit is byte-identical across both sites.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/batch_manifest.py:117

**What:** The by-name import can consume a preloaded/shadowed `validate_branch_naming` module; the identity test compares against that same cached module and cannot detect it.  
**Why:** A wrong regex could silently control exemption decisions instead of producing the claimed loud failure.  
**Fix direction:** Verify the imported module resolves to this file’s sibling `validate_branch_naming.py`, and add a preloaded-shadow regression test.

## MEDIUM

(none)

## LOW

(none)

The strict regex is a proper subset of the former loose regex; the added grammar, merge, and end-to-end tests fail if the loose local rival is restored. `tasks/manifest.json` matches the generated `BACKLOG.md` hash, and the CLAUDE carrier text is byte-identical to its in-document site.

---

## Disposition (CC, 2026-08-11)

**HIGH `scripts/batch_manifest.py:117` — CONFIRMED and FIXED, not dispositioned.**

Reproduced before touching anything, per the read-the-body-not-the-band rule (PLAYBOOK §16): a
standalone probe preloaded a shadow `validate_branch_naming` exporting the LOOSE regex, then
imported `batch_manifest`. Result — `identity assertion passes: True`, `grammar actually in
force: ^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`, `worktree-lane-wave-closures` matching. The
finding is exactly right, and the false claim was mine: the step-1 comment asserted the identity
test would catch a shadow, when both it and the module resolve through the same `sys.modules`
entry.

**Fix, both legs the finding names.** (1) `batch_manifest` now checks PROVENANCE at import — the
resolved `validate_branch_naming` must be its own sibling — and raises `ImportError` otherwise,
which `audit.py`'s FR6 `except` renders as a `journal_spine_anchor` FAIL rather than a silent
pass. (2) `test_a_preloaded_shadow_of_the_enum_module_is_REFUSED_at_import` pins it, in a
SUBPROCESS so the shadow cannot poison later tests in the worker. Negative control run: with the
guard disabled the test REDs reporting `IDENTITY_HOLDS` / `LOOSE_IN_FORCE`, i.e. the defect
itself. The misleading comment is rewritten to say what is true and why the earlier argument was
wrong.

**Honest limit on this artifact.** One clean-except-F1 pass is one pass. The terra loop rule is
that each re-run tends to find what the last graded clean, so the CRITICAL/MEDIUM/LOW `(none)`
bands are weak evidence, not proof — a re-run after this fix has NOT been performed.
