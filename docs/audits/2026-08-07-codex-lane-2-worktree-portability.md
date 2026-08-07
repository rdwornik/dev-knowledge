# Codex Review — lane-2-worktree-portability

**Date:** 2026-08-07
**Branch:** `worktree-lane-2-429-worktree-portability`
**HEAD:** `d7f2f7ff` (passes 1-2) · `9964110b` (pass 3) → fix commit follows this artifact
**Diff range:** `main..worktree-lane-2-429-worktree-portability`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (native `codex exec review --base main`)
**Model used:** `gpt-5.6-terra` (pinned; [#469])
**Review profile:** code
**Tally:** 0/3/0/0 (C/H/M/L)
**Passes:** 3 · **Findings:** 4 · **Accepted:** 3 · **Refuted:** 1 · **Outstanding:** 0

---

## Why three passes, and what each one added

Each pass ran on the diff the previous pass's fix produced, and each returned something the
previous one had graded clean: pass 1 → F-1, pass 2 → F-2, pass 3 → F-3 and F-4. That is the
argument for the batch's condition 3 being about a review *artifact* rather than a review
*pass* — a single pass would have shipped three of these four.

**One of the four is REFUTED, and it is recorded as prominently as the accepted three (F-4).**
A review artifact that only lists what the reviewer got right is not a record, it is agreement.

The lane's own suite could not have caught F-1 or F-2. Every test and every live run went
through the same entry point (F-1) and the same posture assumption (F-2), so they confirmed the
defects rather than caught them. A fresh data point for [#438] (review placement, not review
quality, is the variable) — and F-4 is the counterweight: an outside reader is also the source
of the one claim that did not survive being measured.

**Stopping rule.** Passes converged on posture and boundary questions rather than on behaviour,
and pass 3's two findings were the first to include a refuted one. Pass 4 is the confirming run;
anything it raises that is a design tension rather than a defect is recorded as an accepted
limit rather than chased, per the [#436] 10-pass precedent.

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

## F-3 [P1, pass 3] — the write guard authorised by directory NAME

`scripts/worktree_seed.py` — `--write` refused any checkout whose primary directory was not
named `.dev-knowledge`. That authorises a clone at another path, a restored backup, or an
unrelated repo that merely shares the name. A refusal a stranger satisfies by renaming a folder
is not a refusal.

**Verdict: ACCEPTED, unqualified.** The binding question is narrower and has an exact answer:
`--write` may only rewrite the `.worktreeinclude` of the checkout **the script itself is running
out of**.

**Resolution:** an identity check against `_own_checkout()` (this file's own repo root), with
the name check retained behind it as a second independent condition rather than replaced by it.
Pinned by `test_write_refuses_a_lookalike_repo_that_merely_shares_the_hub_name`.

## F-4 [P1, pass 3] — "pytest loads the target's conftest.py": REFUTED in part, fixed in part

The finding claimed the proof "executes arbitrary child-repo code" because "pytest loads that
repo's configuration, `conftest.py`, and plugins during collection". Taken apart:

| Claim | Verdict | Basis |
|---|---|---|
| loads the target's `conftest.py` | **REFUTED** | sentinel probe, below |
| loads the target's configuration | **TRUE but not execution** | the ini is read as data via `-c` |
| autoloads installed plugins | **TRUE** | accepted and closed |

**The refutation, measured rather than argued.** A sentinel was appended to ai-council's root
`conftest.py` in a live worktree, writing a marker file if it ever ran. It **never fired**,
across four runs spanning both the FAIL and PASS directions. The collected test file lives in
the system temp directory, and conftest discovery walks the *collected args'* ancestors — which
never reach the repo. Independent corroboration was already in the record: ai-council's root
conftest **raises** on a wrong-tree import, and the wrong-tree run reported a clean FAIL instead
of aborting collection. Now a standing regression guard,
`test_the_targets_conftest_is_not_loaded`, because the property depends on where the generated
file is written and a future tidy-up could silently reverse it.

**The accepted half.** Entry-point plugin autoload is real, and is the one route by which
collecting a temp-dir file could still execute child-authored code. Closed with
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`; the generated proof needs no plugin. Re-verified live on
ai-council in both directions.

**The residual, disclosed rather than closed.** The proof does spawn the target's interpreter
and pytest. That is irreducible — the row asks whether *its pytest* imports the right source,
and no static read answers that. The remedy the finding proposed ("move this execution to the
target repo") would mean shipping the proof into every satellite, which is precisely the
hand-copied-per-satellite problem leg (a) exists to eliminate. The module docstring now states
the boundary explicitly: what runs is the target's interpreter and pytest, and nothing wider.

## Not raised by codex, found by the lane's own gates

Recorded here so the artifact is not read as the complete defect list for this diff.

- `scripts/worktree_import_proof.py:342` inherited platform newline translation —
  `test_every_text_write_in_scripts_pins_newline` (full-suite run). Fixed at `d7f2f7ff`.
- The read-only organ wrote `__pycache__/` into the tree it measured — caught by the test that
  asserts the claim (`git status --porcelain` on the target) rather than trusting the docstring.
  Fixed at `ae1abddd`.
- `resolve_interpreter` fell back to `sys.executable`, making the verdict partly a property of
  the calling seat. Found by running it live against ai-council. Fixed at `ae1abddd`.
