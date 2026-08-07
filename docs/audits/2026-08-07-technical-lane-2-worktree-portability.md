# Lane-2 — worktree provisioning made portable, and the import proof that measures it

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-07 · **Slug:** lane-2-worktree-portability
- **Row:** [#429] · **Batch:** 2, wave 1 · **Manifest:** `docs/audits/2026-08-07-technical-batch-2-manifest.md`
- **Branch:** `worktree-lane-b-429-worktree-portability` (renamed at STOP — see LB-1) · **Seat:** background CC (Opus 5)
- **Contract:** `LANE-2-429-portability.md`, frozen at boot
- **Proving satellite:** `ai-council` — the row's own named satellite, verified to carry no `.worktreeinclude`

> **Amendment — 2026-08-07, same session (in-file marker per CLAUDE.md §5 rule 3).** This file
> was first committed at `05d31b20`, before the contract-mandated terra review had run. Terra
> returned a P1 on each of five passes -- eight findings, seven real and one refuted; a sixth
> pass returned nothing, and §3's evidence was produced by the pre-fix organ — so the
> §3 transcripts and §4's defect list are amended to the final post-fix run, and §4 gains
> **D-3** through **D-10**. Nothing else changed. Recorded through the sanctioned in-file channel rather than by rewriting
> the commit, following the `2026-08-06-technical-batch1-verification` precedent: squashing it on
> an unpushed branch would have been tidier and would have left no trace that the artifact ever
> said otherwise — which is precisely the property an audit trail exists to deny itself.
>
> **The first P1, stated plainly, because it is the most interesting thing this lane found.** The proof
> ran its child as `python -m pytest`, which prepends the CWD to `sys.path`. The command a lane
> actually runs — `uv run --locked pytest`, i.e. the console script — does not. A **flat-layout**
> package therefore resolved out of the worktree purely because the proof's own entry point put
> it there. **The original §3 transcript contained the proof of its own defect and neither I nor
> the run noticed: `config` reported PASS in the very checkout whose `ai_council` was
> demonstrably coming from the primary.** A proof whose verdict depends on how the proof was
> launched is not a proof. Closed by running the child under `PYTHONSAFEPATH`, which makes `-m`
> resolve imports the way the console script does. **The second P1** — a Layer-2 validator
> executing sibling package code — is D-4 in §4.

---

## 1. What the row asked for, and what changed about the question

[#429] states two legs and one done-when:

> **(a)** a portable seed-manifest stated ONCE in the hub, not hand-copied per satellite …
> **(b)** a per-worktree venv so imports follow the checkout ·
> Done when: a satellite can provision a worktree AND prove by a runnable check that its
> pytest imports THAT worktree's source

**Leg (a)'s framing does not survive contact with its own named satellite, and that is the
lane's main finding.** `.worktreeinclude` is a list of untracked files to copy into a new
worktree. Measured against `ai-council`: it gitignores `.env` and `.claude/settings.local.json`
and has **neither on disk**, so its correct `.worktreeinclude` is **empty** — and an empty
manifest would still leave every ai-council worktree broken, because its provisioning need was
never an untracked file at all. It is an *environment*.

So "state the manifest once" cannot mean "ship a `.worktreeinclude` to every satellite". A seed
mechanism that models only the copy half cannot make a satellite provisionable. The manifest
built here models **both** halves, and `--plan` emits both. Leg (a) and leg (b) are not two
independent fixes; leg (b) is the part of provisioning that leg (a)'s stated shape could not
express.

## 2. What was built

| Organ | Leg | Posture |
|---|---|---|
| `scripts/worktree_seed.py` | (a) | read-only outside the hub; `--write` refuses any target but the hub's own `.worktreeinclude` |
| `scripts/worktree_import_proof.py` | (b) + done-when | read-only everywhere; writes only into the system temp dir |
| `tests/test_worktree_seed.py` (28) + `tests/test_worktree_import_proof.py` (37) | both | — |
| `.claude/commands/lane-boot.md` §3 / §6 | both | the adopt-native wiring |
| `.worktreeinclude` | (a) | now generated from the manifest, not hand-authored |

**Declared vs derived — the split is the portability property.** The *copy set* is declared
(hub-owned, closed, small; it is the only part a satellite could not compute for itself). The
*environment bootstrap* is **derived** from the target repo's own packaging files at call time:
`uv.lock` → `uv sync --locked`; a `[build-system]` with a package actually on disk → venv +
editable install; no importable package → nothing needed, stated as a real answer. A satellite
that adopts uv later changes its own answer with **no hub edit**. Declaring it per repo would
have recreated the hand-copied-per-satellite problem one layer up.

**Neither organ is wired into a gate.** Adoption-first, per the `/preflight` precedent. Whether
either should gate is a separate ruling; §7 records it as deferred rather than taken.

## 3. The done-when, discharged live on ai-council

Sequence run end-to-end against the finished code. `ai-council` had **no `.worktreeinclude`**
at any point, and the whole provisioning answer came from the hub.

**Step 1 — provision, and measure before remedying.** The failure the row describes,
reproduced by a runnable check rather than asserted:

```
checkout   : C:\Users\1028120\Documents\Dev\ai-council\.claude\worktrees\429-p2-recheck
interpreter: C:\Users\1028120\AppData\Local\Programs\Python\Launcher\py.EXE
venv       : NOT inside the checkout - no <root>/.venv; the ambient interpreter was used
pytest root: C:\Users\1028120\Documents\Dev\ai-council\.claude\worktrees\429-p2-recheck (matches the checkout)

  FAIL ai_council -> C:\Users\1028120\Documents\Dev\ai-council\src\ai_council\__init__.py
  FAIL config -> C:\Users\1028120\Documents\Dev\ai-council\config\__init__.py

FAIL - this checkout's pytest does NOT import this checkout's source.
```

Read the path lines together: pytest's rootdir is **the worktree**, and both packages resolved
to **the primary checkout**. That is the silent failure in one frame — the suite would have
reported green about code the lane never touched.

(Pre-D-3, this same run reported `config` as PASS; D-4 changed the resolution mechanism and left
both verdicts byte-identical. That line was the defect showing itself
inside its own evidence; see the amendment marker at the top.)

**Step 2 — the hub answers for a satellite it is not sitting in.**

```
$ python scripts/worktree_seed.py --plan <the ai-council worktree>
repo       : ai-council
1. Untracked files to seed from the primary
   .env  [not present - skip]
   .claude/settings.local.json  [not present - skip]
   Nothing to copy - this repo's worktree needs no untracked seed.
2. Per-checkout environment  [venv-editable]
     py -m venv .venv
     .venv\Scripts\python.exe -m pip install -e ".[dev]"
3. Verify the outcome - the step that makes 1 and 2 checkable
     python <hub>/scripts/worktree_import_proof.py --repo <the ai-council worktree>
```

"Nothing to copy" is the finding from §1, printed by the tool rather than argued.

**Step 3 — remedy applied verbatim from the plan, then re-measured.**

```
interpreter: …\429-p1-recheck\.venv\Scripts\python.exe
venv       : inside the checkout (.venv)
pytest root: …\429-p1-recheck (matches the checkout)

  PASS ai_council -> …\429-p1-recheck\src\ai_council\__init__.py
  PASS config -> …\429-p1-recheck\config\__init__.py

PASS - this checkout's pytest imports this checkout's source.
```

The D-3 fix strengthened the FAIL without weakening the PASS: **both** packages now resolve out
of the worktree, through the per-checkout install rather than through a path the proof injected.
That two-sided check — FAIL flips to PASS, and nothing that should FAIL still passes — is what
distinguishes a tightened check from a broken one.

**Step 4 — the satellite's real suite, in the worktree:** `939 tests collected` with
ai-council's repo-root checkout-guard conftest loading cleanly (it aborts collection on a
wrong-tree import, so a clean collection is independent corroboration from an organ this lane
did not write).

**Exit codes, verified as values, because a skip that greens is the failure class:** PASS `0` ·
FAIL `1` · NOT-APPLICABLE `3` (the hub itself, which ships no importable package — deliberately
**not** a PASS).

**No-leftovers round-trip.** Both proof worktrees were removed, pruned, their branches deleted,
and the `.claude/worktrees/` directory this lane created was removed. Verified after: `worktree
list` == primary only, `branch` == `main` only, `status --short` empty, directory absent.

## 4. Ten defects the work found in its own organs

None was found by reading the code. D-1 came from running it, D-2 from a test that asserted a
docstring claim instead of trusting it, and D-3 through D-10 from the five contract-mandated
review passes. D-1/D-2 are fixed in `ae1abddd`, D-3 in `d7f2f7ff`, D-4 in `9964110b`,
D-5/D-6 in `b3e9775f`, D-7/D-8 in `6edd69f9`, and D-9/D-10 in the commit carrying this
amendment. A **sixth** review pass on the resulting diff returned no findings, which is what
ended the loop — the review record is `docs/audits/2026-08-07-codex-lane-2-worktree-portability.md`,
tally 0/7/0/0, nothing outstanding. A seventh finding was **refuted**, not fixed —
see D-6 and the review artifact's F-4.

**That distribution is the finding underneath the findings.** Eight of ten came from an outside
reader and neither was reachable from inside: every test and every live run went through the
same entry point (D-3) and the same posture assumption (D-4), so the suite could confirm them
rather than catch them.

**D-1 — the verdict was partly about the caller.** `resolve_interpreter` fell back to
`sys.executable`. Invoked from the hub under `uv run`, that handed an unprovisioned ai-council
worktree the **hub's** interpreter and reported `ModuleNotFoundError` — a FAIL whose stated
cause was *"the package is missing"* when the actual finding is *"the package came from the
wrong checkout"*. A reader would have drawn the wrong conclusion from a technically-correct
failure. Fixed by stripping the caller's own prefix from `PATH` (and from the child's) and
trying `py` first: the Windows launcher lives outside every virtualenv, so it is the one name an
activated environment cannot shadow, and the system interpreter is where a shared editable
install actually sits. Only after this fix did the proof reproduce the row's failure at all.

**D-2 — the read-only organ was writing.** Importing the target's packages compiled them,
leaving `__pycache__/` in the tree being measured. Every fleet repo gitignores it, so it would
never have surfaced as dirt — which is precisely why it was worth suppressing rather than
tolerating. Found by the test that asserts the claim (`git status --porcelain` on the target)
instead of trusting the docstring.

**D-3 — the proof's own entry point manufactured a PASS (terra P1).** `python -m pytest`
prepends the CWD to `sys.path`; `uv run --locked pytest` — the console script, and the command
`/lane-boot` tells lanes to use — does not. So a flat-layout package resolved out of the
worktree because the proof put it there, not because the repo's environment did, and the proof
reported PASS about a package the real command would have taken from the primary's shared
install. The evidence was already sitting in §3 unread. Closed with `PYTHONSAFEPATH=1` on the
child, which makes `-m` resolve the way the console script does; re-verified on ai-council in
both directions (§3). **The generalisable form:** a check that reproduces a failure must
reproduce the *invocation*, not only the tool — matching `pytest` was not enough while the entry
point differed.

**D-4 — a Layer-2 validator was running child-repo code (terra P1, second pass).** The generated
test called `importlib.import_module`, which executes the target package's module body —
arbitrary sibling code with whatever import-time side effects it carries. That is a step beyond
anything else in `scripts/`, where hub tools shell out to `git` against a sibling and never to
the sibling's own code, and it sat directly against CLAUDE.md §5 rule 4 / ADR-28/36 while the
module's own docstring claimed read-only posture. Closed by resolving with
`importlib.util.find_spec` instead: it walks the same finders over the same `sys.path` an import
would and returns the origin it *would* have loaded, so the answer is identical and nothing
executes. Re-verified live on ai-council in both directions — **byte-identical verdicts** to the
D-3 run, which is what makes this a posture fix rather than a behaviour change. An AST test pins
it, because the regression is someone "simplifying" it back to `import_module` and that reads as
harmless.

**D-5 — the `--write` guard authorised by directory NAME (terra P1, third pass).** `--write`
refused any checkout whose primary directory was not named `.dev-knowledge` — which authorises a
clone at another path, a restored backup, or an unrelated repo that merely shares the name. A
refusal a stranger satisfies by renaming a folder is not a refusal. Closed with an identity check
against the checkout this script itself runs out of, keeping the name check behind it as a second
independent condition.

**D-6 — the read-only boundary, one half fixed and one half REFUTED (terra P1, third pass).**
The finding said collection loads the target's `conftest.py`, configuration and plugins. Measured:
the **conftest claim is false** — a sentinel appended to ai-council's root conftest never fired
across four live runs, because the collected test file lives in the system temp dir and conftest
discovery walks the *collected args'* ancestors. (The record already corroborated it: ai-council's
conftest RAISES on a wrong-tree import, and the wrong-tree run reported a clean FAIL rather than
aborting.) The **plugin half is true** and is closed with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. The
residual — the target's interpreter and pytest do run — is irreducible, since the row asks about
*its pytest*; it is now stated in the module docstring rather than left to be discovered. Full
adjudication: `docs/audits/2026-08-07-codex-lane-2-worktree-portability.md` F-4.

**D-7 — a dotted package name would import its parent (terra P1, fourth pass).** `find_spec("pkg.sub")` must IMPORT `pkg` to read its `__path__`, so a dotted name arriving from a setuptools `include` or from `--packages` would execute child-repo code through the very call chosen to avoid executing it — re-opening D-4 by the back door. Closed by reducing every name to its top-level segment at both discovery paths, plus an independent refusal inside the generated test. Nothing is lost: the top-level package's origin is what determines which checkout the subtree came from.

**D-8 — the emitted PowerShell broke on an apostrophe in a path (terra P1, fourth pass).** Paths were interpolated into single-quoted literals unescaped, so a checkout under a profile like `O'Brien` produced a block that will not run — at best a syntax error, at worst a tail parsed as PowerShell. Closed with an escape applied at the one place paths become script text, tested both directly and end to end over a real worktree whose path contains an apostrophe.

**D-9 / D-10 — PEP 420 namespace packages were invisible to BOTH organs (terra P1 ×2, fifth
pass).** The on-disk package predicate required `__init__.py`. In the proof that meant a
namespace-packaged repo answered NOT-APPLICABLE — a disclosed skip, the mildest failure mode
available. In the seed plan it was worse: the repo derived `ENV_NONE`, so `--plan` told the
lane no per-checkout environment was needed and its worktree kept the shared interpreter — the
exact condition leg (b) exists to remove, reached by way of the advice meant to prevent it.
Both closed by accepting a directory that ships modules at its top level or one level down;
`test_a_directory_that_ships_no_python_is_not_a_package` pins the far edge so a data directory
sharing the dist name is not counted. **One defect found twice is the cost of the deliberate
duplication** — the two modules carry their own predicates so neither imports the other — so
`test_the_two_package_predicates_agree` now makes the next divergence a test failure rather
than a plan and a proof quietly disagreeing.

**What D-3 says about review placement.** This is the [#438] thesis with a fresh data point:
the defect passed 51 tests and a live end-to-end run on the real satellite, because every one of
those ran through the same wrong entry point. Only an outside reader comparing the proof's
invocation against the documented one could see it. Condition 3 of the batch — a review artifact
per lane — is what caught it, and it caught something the suite structurally could not.

## 5. Findings for the batch, outside this lane's footprint

**LB-1 — the manifest's lane branch names are outside the enum it cites, and the lanes have
resolved that differently from each other.** `scripts/validate_branch_naming.py` compiles
`lane-[a-z]-\d+-<slug>` (a LETTER); the manifest states the grammar as
`worktree-lane-<n>-<id>-<slug>` (a DIGIT) and asserts "`validate_branch_naming.py` classifies
them". It does — as `unknown`, which is an explicit classification and not merely an absence:

```
BAD  worktree-lane-2-429-worktree-portability     unknown        'worktree-lane-…' that does not match lane-<letter>-<id>-<slug>
```

**Resolved in favour of the validator, following a sibling lane.** PLAYBOOK Ch8 does not state
the grammar itself — it delegates to that validator by name ("Naming grammar + prefix enum:
`scripts/validate_branch_naming.py`"), which makes the validator canonical and the manifest's
claim the drifted surface. Lane-3 had already reached the same conclusion independently and
renamed itself `worktree-lane-c-320-backup`, so conforming is also the in-batch precedent rather
than a unilateral call. This lane renamed `worktree-lane-2-…` → **`worktree-lane-b-…`** at STOP;
the enum now reports `all 8 branch name(s) conform`.

**Two things the integrator needs from this.** (1) The merge queue cannot be read off the
manifest's branch column — at least two of the three wave-1 branches are not named there.
(2) The manifest's grammar sentence is the surface to correct, not the branches; it is an
immutable `docs/audits/` artifact, so the correction belongs in the batch packet as a recorded
finding rather than as an edit. The R-1 exemption is unaffected either way: it keys on the
`worktree-lane-*` **prefix**, which every candidate name carries.

**LB-2 — the contract and the manifest disagreed on this lane's branch name.** The contract's
`Worktree + branch:` line said `worktree-lane-2-429-portability`; the manifest (committed at
dispatch) and the contract's own H1 both say `…-429-worktree-portability`. The slug was resolved
to the manifest — it is the committed arbitration surface and the contract's own title agrees
with it — and the lane index was later resolved to the enum per LB-1, giving
`worktree-lane-b-429-worktree-portability`. Recorded rather than silently absorbed, because a
lane renaming its own branch is exactly the act that should leave a trace. **Three surfaces
named this branch three ways**, which is the underlying finding: a lane booted from a contract,
a manifest, and a validator has no single place to read its own name from.

**LB-3 — PLAYBOOK Ch8 §2a "Manual-seed commands" is now the second-best path.** `/lane-boot` §3
points at the tool; the PLAYBOOK prose loop is hub-shaped and still correct for the hub. Not
edited: `protocols/PLAYBOOK.md` is [#505]'s footprint and the contract forbids re-scoping either
row.

**LB-4 — `AllocationRule.concurrent_prevention` stays `not-provided`.** `ecosystem/schema/
desired_state.py` marks widening it as "gated on [#429] delivering the organ", referring to
[#429]'s *second evidence* leg (ids on unmerged branches invisible to next-free scans). The
contract scopes this lane to legs (a) and (b) only, so that leg is untouched and the `Literal`
is unchanged.

## 6. Row status

**[#429] is not closed by this lane.** Its done-when is discharged and evidenced above, but a
row close is the operator's or the integrator's act, and `BACKLOG.md` is a shared generated
surface the manifest reserves for regeneration at integration. Reported as **ready to close on
the evidence in §3**.

## 7. Deferred decisions

1. **The manifest lives in code, not in `ecosystem/*.yaml`.** It follows
   `validate_branch_naming.py`, which holds the branch-prefix enum as a module constant for the
   same reason. An `ecosystem/` surface is the better long-run home; it acquires registry and
   parity obligations that collide with lane-1's exclusive ownership of
   `ecosystem/parity-surfaces.yaml` this batch. Deferred, not rejected.
2. **No `--check` pre-commit gate on `.worktreeinclude` drift.** The regen-and-diff exists and
   is tested; wiring it is a gate addition with fleet reach, and adoption-first is the standing
   precedent.
3. **No deploy-manifest carrier.** Shipping these organs to consumers means a v1.5.0 cut, which
   requires an operator release tag (ADR-91: CC does not tag). Out of proportion to one lane.
   Today a satellite is served by pointing the hub's tool at it, which is what the live proof
   in §3 did.
