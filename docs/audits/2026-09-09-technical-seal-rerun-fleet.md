# Seal re-run after the two-rule fix — 336 WAIVEs become 204, and 67 of them are a consumer's

> **Step 4 of lane `lane-v-000-seal-rules-rerun` (batch V, V-3).** DECLARE-REVIEWS §A.4
> ruled that the two hub-local seal rules are fixed *before* the operator is asked to rule a
> list, and predicted the result would be *"tens, not hundreds"*. This is the re-run that
> tests the prediction. **N is the closure, not an adjective, so N is printed.**
>
> **Read-only, and measured rather than claimed.** Each repository's
> `git status --porcelain` was captured immediately before and immediately after its seal
> and compared; all nine are byte-identical. The only commands touching a repo other than
> the hub are `git ls-files`, `git rev-parse` and that `status` stamp.

## 1 · The number

```
before:  348 out-of-pattern items  ->  RELOCATE 11 / RETIRE 0 / WAIVE 336 / ESCALATED 1
after:   215 out-of-pattern items  ->  WAIVE N = 204, non-WAIVE 11

  N = 204          336 - 204 = 132 waivers withdrawn by fixing two rules
  of which 137     ADR-101 section 6 grandfathered filenames at the HUB, which the live
                   prospective gate has never inspected and never will
  CONSUMER-facing WAIVE residue = 67
```

**67 is the number §A.4's prediction was about** — the list the operator is eventually
brought. It is tens, not hundreds, and it is the honest figure because the 137 are not a
consumer's problem and were never going to reach an operator's list (§3).

## 2 · The measurement

Driven through `validate_hermetization.seal_repo()` — the API this lane added, so the
re-run is the module's own grain rather than a rebuilt harness. Rule A per ITEM, Rule B per
FILE, Rule C per distinct HOME, short-circuit A→B→C.

```
repo                       head      branch                          trk  items    A    B    C   clean?
.dev-knowledge             471d3ce0  worktree-lane-v-000-seal-…     3065    137    0  137    0      YES
ai-council                 7a3c057   main                            254      4    4    0    0      YES
corp-monorepo              37b8aa1   main                            821     14    3   11    0      YES
corp-ops                   3bde930   main                             60      4    4    0    0      YES
corp-sca-time-automation   3661b3a   feature/tenrox-loader            75      6    5    0    1      YES
demo-prep                  1f7c35c   feat/leadership-template-deck   883     36    8   28    0      YES
life-architect             7688b76   main                             45      5    5    0    0      YES
terminal-setup             d8a7b61   main                              3      2    2    0    0      YES
win-tooling                61120b7   feat/prompts-dir-user-scope-…   178      7    6    0    1      YES
                                                                    ----   ----  ---  ---  ---
                                                                    5384    215   37  176    2
```

`clean?` is the read-only proof, per repo: `status --porcelain` before == after.

**Re-run command** — one call per repo, and the module now carries it:

```
uv run --locked python scripts/validate_hermetization.py report <repo-root>
```

## 3 · Where the 132 went, and where the 204 sit

```
rule    before   after   what moved
-----   ------   -----   ---------------------------------------------------------------
B         233     176    the CLASS-ENUM leg stopped travelling: 194 -> 0 at consumers.
                         The 39 R4-CASING refusals REMAIN -- casing is a fleet clause.
                         The 137 at the hub remain and are section 6 grandfathered.
C          75       2    the HOME TUPLE stopped travelling: 72 -> 0. The 2 that remain
                         are `docs/` homes, which is Rule C's FLEET leg working.
A          28      28    unchanged, and unchanged deliberately -- see section 5.
      -------  ------
          336     204
```

**The 204, itemized to the last one:**

```
.dev-knowledge             B: 137 files            ADR-101 section 6, grandfathered
demo-prep                  B: 28 files             R4 casing -- declaration PENDING
corp-monorepo              B: 11 files             R4 casing -- ALREADY DECLARED (audit-casing-r4)
                                                   ---- 176 Rule B
ai-council                 A: INSTALL.md, conftest.py, council_inbox
corp-monorepo              A: INSTALL.md, tach.toml
corp-ops                   A: INSTALL.md, assets, tools
corp-sca-time-automation   A: assets, data, pytest.ini, requirements.txt
demo-prep                  A: SOURCES.md, brand, examples, generators, knowledge, output, pipeline
life-architect             A: OPEN-QUESTIONS.md, dimensions, seed
terminal-setup             A: huvix-custom.omp.json, setup.ps1
win-tooling                A: INSTALL.md, config.yaml, conftest.py, tools
                                                   ---- 28 Rule A
```

**Rule C's residue is zero.** Its two surviving items — `corp-sca-time-automation/docs/`
and `win-tooling/docs/` — are both RELOCATEs the predecessor already verdicted, not
waivers. The rule that produced 75 waivers now produces none and keeps both of its
genuine findings.

**The escalated item is discharged as a SHAPE question and untouched as a CONTENT one.**
`corp-monorepo/docs/decisions/transcripts/` was the report's one ESCALATED row, filed
because no standing ruling says whether the hub's 2026-07-22 transcript deletion was
hub-scoped or fleet-scoped. Under the fixed rule the path is in-shape: below a sanctioned
genre, depth is the repo's own structure. **That answers the seal's question and not the
operator's.** Whether corp should keep 28 transcripts is a content ruling the seal was
never the right instrument for, and it is still open.

## 4 · What actually changed in the rules

Each rule split along a seam the spec had already written down and no organ read:

| rule | FLEET leg — travels | REPO-LOCAL leg — declared, or not applied |
|---|---|---|
| **B** | the `YYYY-MM-DD-` date shape · the R4 casing rule | the audit class enum (`audit_class_enum_scope: repo-local`) |
| **C** | the `docs/` genre-tree rule — `docs` is not a home | the home tuple — *"never with the hub's tuple"* |

A repo declares its repo-local halves in its own `.methodology.yaml` under
`shape_profile:`. A repo that declares nothing gets the fleet legs and neither local leg.
The repo that carries the spec is the spec's own instance, which keeps the hub governed
without restating the enum in a second file. `<allowed-home>/archive` also became a grammar
rule rather than six literals.

**The hub's own verdicts did not move.** Every rule function defaults to `HUB_PROFILE`;
`.dev-knowledge`'s row is 137 before and 137 after, and Rule C still admits every tracked
path in the live repo.

## 5 · What this re-run does NOT close — named, not left silent

- **Rule A's 28 are untouched, by contract.** The step-2 measurement STOPped on the fact
  that three rules produce WAIVEs, not two, and named Rule A's 28. Every one of them is
  fixed by a **data line in `ecosystem/fleet-shape-spec.yaml`** — `INSTALL.md` and the
  standard Python root files into `root_allowlist.files`, a repo-kind axis for the domain
  directories, an ADR-59 clause for the two dot-prefix cases. That file is **V-2's
  footprint and pinned OUT of this lane.**
- **39 R4-casing items are a consumer's declaration, not a hub defect.** corp's 11 are
  already declared in its own `.methodology.yaml`; demo-prep's 28 are the same class
  pending the same act.
- **The hub's 137 are an artifact of RETROSPECTIVE mode.** `seal_repo()` reads every
  tracked path; the pre-commit gate reads only staged ADDs. They are in this count because
  the 336 was measured the same way and the two numbers have to be commensurable.
- **No seal list is ruled here.** The verbs stay the operator's, at Sitting 3.
- **`docs/audits/README.md` is NOT regenerated** — the integrator is gate-of-record
  ([#590]).

## 6 · Done-clause 2 is NOT discharged — the debt, stated plainly

The contract requires the re-run be **witnessed post-V-2 merge**, recording the merge SHA
it ran against. **There is no such SHA.** V-2 (`lane-v-000-shape-spec-clauses`) has
committed-and-STOPped at `6b6ab678`, and the integrator has not merged it: `origin/main` is
still `33bcb0bd`. This run was made against this lane's own HEAD, **`471d3ce0`**.

**Two measured facts say the number is invariant across that merge, and neither is a
substitute for the witness:**

1. V-2 changes **none of the three rule inputs this seal reads**. Every deletion in its
   spec diff is confined to `required_docs.asserted_by` and `python_layout`'s
   `asserted_by` / `unasserted_reason`; `root_allowlist`, `genre_folders`,
   `home_grammar.patterns` and `naming_grammar.audit_class_enum` are byte-identical. Its
   `kinds:` / `declared_kinds:` addition feeds its own new reader, not Rule C's tuple.
2. This lane's patch applies cleanly to V-2's finished blob — all eleven exact-string edits
   matched uniquely against its 624-line version, read out of the shared object database
   into scratch with V-2's branch, its worktree and this tree untouched.

**The witness is owed and is one command.** After the integrator merges V-2, re-run
section 2 on the merged result and record that merge SHA. If the number is not 204, this
file is wrong and the merged run is right.

---

**Lane:** `lane-v-000-seal-rules-rerun` · batch V, V-3 · substrate local
**Measured:** 2026-09-09 against `471d3ce0` (`worktree-lane-v-000-seal-rules-rerun`)
**Writes in any consumer repo:** none — proven per repo by a `status --porcelain` stamp
taken before and after each seal
