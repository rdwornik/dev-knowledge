# Codex Review — lane-2-worktree-portability

**Date:** 2026-08-07
**Branch:** `worktree-lane-2-429-worktree-portability`
**HEAD:** `d7f2f7ff` (pass 1 + pass 2) → fix commit follows this artifact
**Diff range:** `main..worktree-lane-2-429-worktree-portability`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (native `codex exec review --base main`)
**Model used:** `gpt-5.6-terra` (pinned; [#469])
**Review profile:** code
**Tally:** 0/2/0/0 (C/H/M/L)
**Passes:** 2 · **Findings:** 2 · **Accepted:** 2 · **Rejected:** 0 · **Outstanding:** 0

---

## Why two passes, and why the second one matters

Pass 1 was run on the lane's three-commit diff and returned one P1. It was fixed, re-verified
live on the satellite, and committed at `d7f2f7ff`. Pass 2 was run on the *resulting* diff and
returned a **different** P1 — not a restatement, and not something pass 1 had graded clean. Both
are accepted. Recorded because a single-pass review would have shipped D-4, and the batch's
condition 3 says "a review artifact", not "a review pass".

The lane's own suite could not have caught either. Every test and every live run went through
the same entry point (F-1) and the same posture assumption (F-2), so they confirmed the defects
rather than caught them. This is a fresh data point for [#438] (review placement, not review
quality, is the variable).

---

## F-1 [P1, pass 1] — the proof's entry point manufactured a PASS

`scripts/worktree_import_proof.py` — the generated check ran as `python -m pytest`, which
prepends the CWD to `sys.path`. The command a lane actually runs — `uv run --locked pytest`,
the console script, the one `/lane-boot` prescribes — does not. A **flat-layout** package
therefore resolved out of the worktree because the proof put it there, and the proof reported
PASS about a package the real command would have taken from the shared editable install in the
primary checkout.

**Verdict: ACCEPTED — and it was already visible in the lane's own evidence.** The recorded
ai-council FAIL transcript reported `config` (flat layout) as PASS inside the very checkout
whose `ai_council` (src layout) was demonstrably resolving to the primary. The artifact printed
the contradiction; nobody read it.

**Resolution:** `PYTHONSAFEPATH=1` on the child, so `-m` resolves the way the console script
does. Re-verified live in both directions: the unprovisioned worktree now FAILs on both packages
(was one), the provisioned one still PASSes on both. Pinned by
`test_the_child_runs_under_safe_path`. Fixed at `d7f2f7ff`.

## F-2 [P1, pass 2] — a Layer-2 validator was running child-repo code

`scripts/worktree_import_proof.py` — the generated test called `importlib.import_module`, which
executes the target package's module body: arbitrary sibling code with whatever import-time side
effects it carries. That sits against CLAUDE.md §5 rule 4 / ADR-28/36 while the module's own
docstring claimed read-only posture, and it is a step beyond anything else in `scripts/`, where
hub tools shell out to `git` against a sibling and never to the sibling's own code.

**Verdict: ACCEPTED.** The alternative reading — that spawning the repo's pytest is already
"executing", so an import changes nothing — does not hold: the row's done-when *requires*
running the repo's pytest, and no reading of the invariant requires running the repo's
application code. The distinction is real and the fix is free.

**Resolution:** `importlib.util.find_spec` instead. It walks the same finders over the same
`sys.path` an import would and returns the origin it *would* have loaded, so the answer is
identical and nothing executes. Re-verified live on ai-council in both directions: verdicts
**byte-identical** to the F-1 run, which is what makes this a posture fix rather than a
behaviour change. Pinned on the AST by
`test_the_generated_proof_resolves_and_never_imports`, because the regression is someone
"simplifying" it back to `import_module` and that reads as harmless.

---

## Not raised by codex, found by the lane's own gates

Recorded here so the artifact is not read as the complete defect list for this diff.

- `scripts/worktree_import_proof.py:342` inherited platform newline translation —
  `test_every_text_write_in_scripts_pins_newline` (full-suite run). Fixed at `d7f2f7ff`.
- The read-only organ wrote `__pycache__/` into the tree it measured — caught by the test that
  asserts the claim (`git status --porcelain` on the target) rather than trusting the docstring.
  Fixed at `ae1abddd`.
- `resolve_interpreter` fell back to `sys.executable`, making the verdict partly a property of
  the calling seat. Found by running it live against ai-council. Fixed at `ae1abddd`.
