# Codex Review — lane-f-521-syspath-substrate

**Date:** 2026-08-11
**Branch:** `worktree-lane-f-521-syspath-substrate`
**HEAD:** `04dd9b39` (both passes reviewed the same HEAD — no fix landed between them, because nothing needed fixing)
**Diff range:** `main..worktree-lane-f-521-syspath-substrate`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/0/0/0 <!-- Critical/High/Medium/Low — CONFIRMED findings, cumulative across the 2-pass loop. Pass 1 produced one HIGH; it was REFUTED by reproduction, not fixed, so counting it would report a defect that does not exist. It is recorded in full below rather than erased — the lane-e precedent counts findings that reproduced; this one did not. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Passes:** 2 (pass 2 re-run against the same diff carrying pass 1's finding and its refutation, with an instruction to attack the refutation or find something new)

> **Why this review exists.** `[#521]` is a `sys.path` substrate change. The W-521 lane contract
> makes a terra review request mandatory for it — *"sys.path/substrate work is code-impact by
> definition"* — regardless of how small the diff reads.

---

## Focus (frozen acceptance constraints, both passes)

1. **Config correctness.** Can any of the 74 top-level module names the two new roots expose shadow
   a stdlib module, an installed distribution, or a test module? Can any import now resolve to a
   *different module object* than before — the `scripts.gitenv` vs bare `gitenv` dual-identity class
   that broke `tests/test_gitenv.py` at `c94e7fdb`? Both the repo root and `scripts/` are importable
   now, which is exactly the layout that produced that defect.
2. **Deletion correctness.** Any deletion leaving a dangling `if`/`try` body; any file where the
   insert was load-bearing for a reason `pythonpath` does not cover (a subprocess spawn, a fixture
   that mutates `sys.path`, an import before pytest configures the path); any `os`/`sys` removal
   where the name is used dynamically and ruff's static analysis was wrong.
3. **Vacuity.** Is any test now passing for a new and wrong reason — especially tests asserting on
   `sys.path` contents, module identity, or import layout?
4. **The deliberate exclusion.** `tests/test_batch_manifest.py` keeps 2 inserts (live in another
   lane) — does that inconsistency create a real hazard?
5. **The residual left alone.** The 18 `scripts/` + 6 `deploy/` inserts are untouched by design —
   does anything here make them newly redundant or newly broken?
6. `tests/test_enforcement_coverage.py:389` (the f-string generating subprocess source) survived
   intact, and the line-anchored regex could not have caught it.

---

## Findings

## CRITICAL

(none, either pass)

## HIGH

(none confirmed)

### Pass 1 — `scripts/batch_manifest.py:91` — REFUTED, not fixed

**What the reviewer reported:** *"lane-anchor exemption was broadened to off-grammar branches — the
local regex again accepts any `worktree-lane-*` shape … the regression tests that prevented this
were deleted."*

**Verdict: REFUTED by reproduction.** Two commands, both run on this branch before pass 2 was
dispatched, both returning EMPTY:

```
git diff --stat main...worktree-lane-f-521-syspath-substrate -- scripts/ deploy/
git diff main...worktree-lane-f-521-syspath-substrate -- tests/ \
  | grep '^-' | grep -v '^---' | grep -vE '^-[ \t]*(sys\.path\.insert\(|import (os|sys)$)'
```

The first shows this branch touches **zero** files under `scripts/` or `deploy/`, so
`batch_manifest.py:91` is untouched pre-existing code rather than a change in this diff. The second
shows **every** deleted line in `tests/` is either a `sys.path.insert(` line or a bare `import os` /
`import sys` — zero test functions, zero assertions, zero regression tests were deleted. The
diffstat reconciles exactly: 72 files, 174 deletions = 75 inserts + 99 orphaned imports.

**What the reviewer actually found** is the live, known, still-OPEN row **`[#510]`** — *"Scope the
R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today"* — whose
row text describes this same condition in the same words. It pre-exists this branch, it is batch-4
lane W1's deliverable, and this lane does not touch it. **Recorded rather than deleted** because a
reviewer reporting an unrelated repo-state defect as a property of the diff is itself worth knowing;
and because a reader who sees only the clean pass 2 would not know the loop had a false positive in
it. It is not evidence against `[#510]`, which needs none — it is already open and already owned.

**Disposition:** no change made. Pass 2 was given the finding, the two reproduction commands, and an
instruction to attack the refutation or find something new.

## MEDIUM

(none, either pass)

## LOW

(none, either pass)

---

## Loop record

| Pass | HEAD reviewed | Findings | Outcome |
|---|---|---|---|
| 1 | `04dd9b39` | 1 HIGH | **refuted** by reproduction (see above); no fix, no change |
| 2 | `04dd9b39` | none | **clean pass** — refutation accepted, loop terminated |

Pass 2 reviewed the same HEAD deliberately. In the usual loop each pass attacks the previous pass's
*fix*; here there was no fix to attack, because the finding described code the diff does not
contain. Re-running against an unchanged tree is the correct control for that case: it asks whether
the finding survives once the reviewer knows the true diff shape. It did not.

---

## What the lane verified itself, independent of this review

Stated because a review artifact carrying a clean pass and nothing else invites the reader to treat
the clean pass as the whole assurance. It is not — these are the lane's own measurements:

- **Shadowing, the hazard a new `sys.path` root actually carries.** Of the 74 top-level module names
  `scripts/` and `deploy/` expose, **zero** shadow a stdlib module (`sys.stdlib_module_names`) and
  **zero** shadow a module already resolvable by `importlib.util.find_spec`. Measured before the
  config line landed, not after.
- **Isolated per-file collection**, one process per file, all 101 test files:
  0/101 pre-rollout · 0/101 config-only · **0/101 post-rollout** · **68/101** with the roots narrowed
  back to `["."]`. The last figure is the negative control that makes the third mean something, and
  it reproduces the `[#502]` measurement's 67/99 on a tree three days newer.
- **`ruff check`** — 99 F401, all `os`/`sys`, all inside `tests/`, all fixed by `ruff check --fix`;
  clean before and clean after, so all 99 are attributable to this change.
- **Full suite**, both sides, quoted in the closing commit and in the JOURNAL entry.

**Honest limit of this artifact.** The reviewer ran read-only over a diff. It did not execute the
suite, did not run the isolated probe, and its one finding was about code outside the diff. Every
measurement in the section above is the lane's own, run in this worktree under `uv run --locked`;
the review's contribution here is a clean second opinion on the diff, not the proof.
