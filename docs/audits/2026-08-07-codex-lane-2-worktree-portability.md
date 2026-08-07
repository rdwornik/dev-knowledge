# Codex Review — lane-2-worktree-portability

**Date:** 2026-08-07
**Branch:** `worktree-lane-b-429-worktree-portability` (renamed at STOP; the review passes ran under the former name)
**HEAD:** `d7f2f7ff` (passes 1-2) · `9964110b` (pass 3) · `b3e9775f` (pass 4) · `6edd69f9` (pass 5) · `a27d30b6` (pass 6, CLEAN)
**Diff range:** `main..<the lane branch>`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (native `codex exec review --base main`)
**Model used:** `gpt-5.6-terra` (pinned; [#469])
**Review profile:** code
**Tally:** 0/7/0/0 (C/H/M/L)  ·  **final pass: CLEAN**
**Passes:** 6 · **Findings:** 8 · **Accepted:** 7 · **Refuted:** 1 · **Outstanding:** 0

---

## Why six passes, and what each one added

Each pass ran on the diff the previous pass's fix produced, and each returned something the
previous one had graded clean: pass 1 → F-1, pass 2 → F-2, pass 3 → F-3/F-4, pass 4 →
F-5/F-6, pass 5 → F-7/F-8, **pass 6 → nothing**. That is the argument for the batch's condition
3 being about a review *artifact* rather than a review *pass* — a single pass would have shipped
seven of these eight.

**One of the eight is REFUTED, and it is recorded as prominently as the accepted seven (F-4).**
A review artifact that only lists what the reviewer got right is not a record, it is agreement.

The lane's own suite could not have caught F-1 or F-2. Every test and every live run went
through the same entry point (F-1) and the same posture assumption (F-2), so they confirmed the
defects rather than caught them. A fresh data point for [#438] (review placement, not review
quality, is the variable) — and F-4 is the counterweight: an outside reader is also the source
of the one claim that did not survive being measured.

**Stopping rule, and how it terminated.** The rule from pass 3: a *design tension* gets
recorded as an accepted limit; a *defect with an exact fix* gets fixed; the loop stops when a
pass returns nothing that changes behaviour. Passes 4 and 5 each raised two of the latter and
none of the former, and the findings narrowed visibly as they went — entry point → execution
posture → apostrophes in paths → PEP 420 discovery. **Pass 6 returned no findings**, on the diff
produced by pass 5's fix, which is the termination condition rather than a decision to stop
looking. Verbatim: *"No critical or high-severity defects were identified in the changes
relative to the supplied merge base."* Nothing is outstanding, so nothing is handed to the
integrator as a deferred review item. (For scale: the [#436] refusal-gate arc took 10 passes.)

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

## F-5 [P1, pass 4] — a dotted package name would import its parent

`scripts/worktree_import_proof.py` — `find_spec("pkg.sub")` must IMPORT `pkg` to read its
`__path__` before it can look inside. A dotted name reaching the proof — from a setuptools
`include = ["pkg.sub*"]` or from `--packages` — would therefore execute child-repo code through
the very call chosen to avoid executing it, re-opening F-2 by the back door.

**Verdict: ACCEPTED.** Nothing is lost by resolving top-level only: the top-level package's
origin determines which checkout the whole subtree comes from, which is the entire question.

**Resolution:** `top_level()` applied at both discovery paths, plus an independent refusal
inside the generated test, so a dotted name cannot reach `find_spec` even if a future caller
bypasses discovery.

## F-6 [P1, pass 4] — the emitted PowerShell broke on an apostrophe in a path

`scripts/worktree_seed.py` — paths were interpolated into single-quoted PowerShell literals
unescaped. A path like `C:\Users\O'Brien\repo` closes the literal early: at best the emitted
block is a syntax error, at worst the tail is parsed as PowerShell.

**Verdict: ACCEPTED.** A path is not a safe string, and a provisioning block that a user with
an apostrophe in their profile name cannot run is broken for that user regardless of intent.

**Resolution:** `_ps_single_quote()` doubles embedded apostrophes, applied at the one place
paths become script text rather than trusted to each caller. Two tests: the helper directly,
and `_copy_block` end to end over a real worktree whose path contains an apostrophe — because
the regression is a NEW interpolation site added later without the escape.

## F-7 [P1, pass 5] — PEP 420 namespace packages were invisible to discovery

`scripts/worktree_import_proof.py` — the on-disk package predicate required `__init__.py`, so
a repo distributing a PEP 420 namespace package returned no declared packages and the CLI
answered NOT-APPLICABLE (exit 3).

**Verdict: ACCEPTED, with its severity stated honestly.** The failure mode is the mildest one
available — a *disclosed skip*, not a false pass, and exit 3 says in as many words that
nothing was proved. It is still a supported packaging style going unchecked by a tool whose
entire purpose is to work across a fleet it does not control, so it is fixed rather than
recorded as a limit.

**Resolution:** a directory counts when it ships modules at its top level or one level down.
The depth bound is deliberate — an unbounded `rglob` over a `node_modules`-shaped tree turns a
fast predicate into a slow one. The widening also has to stop somewhere, so
`test_a_directory_that_ships_no_python_is_not_a_package` pins the other edge: a data directory
sharing the distribution name is not a package, and counting it would put a name in the report
that no import could ever resolve.

## F-8 [P1, pass 5] — the same blind spot in the provisioning plan

`scripts/worktree_seed.py` — the twin predicate behind `env_bootstrap`, with a worse
consequence: a namespace-packaged repo derived `ENV_NONE`, so `--plan` told the lane no
per-checkout environment was needed and its worktree kept the shared interpreter. That is the
exact condition leg (b) exists to remove, reached by way of the advice meant to prevent it.

**Verdict: ACCEPTED**, same fix applied to the twin.

**And the duplication is now pinned.** The two modules carry their own copies of this
predicate deliberately — neither imports the other, so each stands alone — and F-7/F-8 are
what that costs: one defect, found twice, in two places that must agree. Rather than couple
them, `test_the_two_package_predicates_agree` asserts they return the same verdict across the
five shapes that distinguish them (regular, namespace, single module, data-only, absent), so
the next divergence is a test failure instead of a plan and a proof quietly disagreeing about
whether a repo has anything to check.

## Not raised by codex, found by the lane's own gates

Recorded here so the artifact is not read as the complete defect list for this diff.

- `scripts/worktree_import_proof.py:342` inherited platform newline translation —
  `test_every_text_write_in_scripts_pins_newline` (full-suite run). Fixed at `d7f2f7ff`.
- The read-only organ wrote `__pycache__/` into the tree it measured — caught by the test that
  asserts the claim (`git status --porcelain` on the target) rather than trusting the docstring.
  Fixed at `ae1abddd`.
- `resolve_interpreter` fell back to `sys.executable`, making the verdict partly a property of
  the calling seat. Found by running it live against ai-council. Fixed at `ae1abddd`.
