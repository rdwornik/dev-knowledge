# Lane close — `lane-v-000-seal-rules-rerun` (batch V, V-3)

> **End-of-lane artifact.** The lane commits and STOPs here; integration is the integrator's
> act. Two clauses are NOT discharged and both are named below rather than rounded up.

## 1 · The done-contract, clause by clause

| # | clause | verdict |
|---|---|---|
| 1 | seal WAIVE count **336 → N, with N PRINTED** | **MET** — `N = 204`, printed in `docs/audits/2026-09-09-technical-seal-rerun-fleet.md` §1 and in the `c5109ce0` commit subject. Consumer-facing residue **67**. |
| 2 | the re-run is **witnessed post-V-2 merge**, recording the merge SHA | **NOT MET** — §4. There is no merge SHA. Run against this lane's HEAD `471d3ce0`. |
| 3 | English · hyphen-only names · logging over print · Click where warranted · `pytest` green | **MET** — §5. |

## 2 · What the lane did

**The two rules, identified from a property rather than a list.** §A.4 names their count and
their character — *hub-local* — and never their identifiers. The fleet report's own sentence
names them: *"the rule that works produces the actionable findings; the two that do not
produce the waivers."* **Rule B** (audit-filename grammar) and **Rule C** (home allowlist).

**Proven, not asserted.** Driven through the live rule functions over all nine ratified
members, the measurement reproduced the predecessor's 348 items exactly and split Rule B
into `class 194 / casing 39` — classes B2 and B1 to the item. Re-classifying the twelve
non-WAIVE items attributes the 336 as **A 28 / B 233 / C 75**.

**The defect in one sentence.** Both rule functions were pure functions of a path string
with **no repo identity**, so there was no seam through which the repo under test could
declare its own class vocabulary or its own homes. One bug wearing two rules.

**The fix.** Each rule splits along a seam the spec had already written down and no organ
read: Rule B's date-shape and R4-casing legs travel while its class enum is repo-local
(`audit_class_enum_scope: repo-local`); Rule C's `docs/` genre-tree rule travels while its
home tuple is repo-local (*"never with the hub's tuple"*). A repo declares its local halves
in its own `.methodology.yaml` under `shape_profile:`. `<allowed-home>/archive` also became
one grammar rule instead of six literals. **The hub's verdicts did not move** — every rule
function defaults to `HUB_PROFILE`.

**The result.** 336 → **204**, of which 137 are the hub's own ADR-101 §6 grandfathered
filenames the prospective gate never inspects. **Rule C's waiver residue is zero** and it
keeps both of its genuine findings. Read-only was measured per repo, not claimed: a
`git status --porcelain` stamp before and after each seal, all nine byte-identical.

## 3 · THE STOP — three rules produce WAIVEs, not two

Step 2 required a stop and a naming if more than two rules were implicated. **The
measurement implicates three.** Rule A produces **28** of the 336 (classes D/I/P/N/F/U).

The fix stayed at two on three checkable grounds: this lane's footprint names two; Rule A
already produces 9 of the fleet's 11 RELOCATEs, so it is not the rule §A.4 describes; and
**every one of Rule A's 28 is fixed by a data line in `ecosystem/fleet-shape-spec.yaml`,
which is V-2's footprint and pinned OUT of this lane.** `N` was never going to be zero, and
the residue has an owner rather than a silence.

## 4 · Done-clause 2 — the debt, and why it was not papered over

V-2 (`lane-v-000-shape-spec-clauses`) committed-and-STOPped at `6b6ab678`; the integrator
has not merged it, and `origin/main` is still `33bcb0bd`. **The witness required by clause 2
does not exist and this lane did not manufacture one.**

**The wait was implemented as code, twice, and the machine killed it twice** — a bounded
poll on the `origin/main` ref surface at 120 s and then at 300 s, each terminated by the OS
in a low-memory event with five lane sessions on the box. Rather than end a third turn on a
peer wait, steps 3–5 were taken on two **measured** facts:

1. **V-2 changes none of the three rule inputs this seal reads.** Every deletion in its spec
   diff is confined to `required_docs.asserted_by` and `python_layout`'s `asserted_by` /
   `unasserted_reason`. `root_allowlist`, `genre_folders`, `home_grammar.patterns` and
   `naming_grammar.audit_class_enum` are byte-identical. Its `kinds:` / `declared_kinds:`
   addition feeds its own new reader, not Rule C's tuple.
2. **This lane's patch applies cleanly to V-2's finished blob** — all eleven exact-string
   edits matched uniquely against its 624-line version, read out of the shared object
   database into scratch, with V-2's branch, its worktree and this tree untouched.

So the number should be invariant across the merge, and **neither fact is a substitute for
the witness.** The integrator's re-witness is one command per repo
(`validate_hermetization.py report <repo-root>`), and if the merged run is not 204 the
merged run is right.

## 5 · Verification

**Targeted tests** — the lane's diff touches `scripts/validate_hermetization.py` plus its
importers and its new test file, so the targeted set is those seven modules. The full suite
runs once, at integration ([#528]).

```
tests/test_seal_repo_profile.py · test_validate_hermetization.py · test_fleet_shape_spec.py
tests/test_canonical_docs.py · test_batch_manifest.py · test_e2e_consumer_lifecycle.py
tests/test_check_derived_copies.py
    246 passed, 1 failed, 1 skipped
```

The single failure is `test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival`
and it is **PRE-EXISTING** — confirmed by running it against the unpatched base before the
fix was applied, not diagnosed after the fact. It belongs to the 28-RED batch baseline at
`08c35b9c`. **This lane adds zero new REDs to its targeted set.**

`ruff check` clean on both changed files. `ecosystem/doc-counts.md` regenerated in-lane
(5390 → 5421, exactly the 31 tests added), because `doc-counts-pytest-freshness` is a
blocking commit gate and cannot be deferred.

**RED-first (ADR-108 §B):** the witness is commit `47cf6c25` — 24 failing, 7 passing, before
any build code.

**Reviewer tally (batch gate D3, AMEND-002).**

```
reviewer   codex exec review -m gpt-5.6-terra --base main
model      gpt-5.6-terra -- VERIFIED, not merely requested: the review subagent's own
           session log records `gpt-5.6-terra` and no other model, so this is not the
           silent-model-swap class R-6 names
passes     1
verdict    CLEAN -- "No critical or high-confidence runtime issues were identified in
           the diff."
```

One pass rather than a loop, and the stopping rule is satisfied rather than skipped: the
`terra` loop's rule is *stop when a pass returns nothing*, and there was no fix to produce a
second diff to review.

## 6 · Residue discovered, with owners — none of it silently absorbed

- **Rule A's 28 WAIVEs** — `ecosystem/fleet-shape-spec.yaml` data lines: `INSTALL.md` and the
  standard Python root files into `root_allowlist.files`, a repo-kind axis for the domain
  directories, an ADR-59 clause for the two dot-prefix cases. **Owner: V-2's footprint, then
  the operator's Sitting-3 list.**
- **39 R4-casing items are a consumer's declaration act, not a hub defect** — corp's 11 are
  already declared in its `.methodology.yaml`; demo-prep's 28 are the same class pending the
  same act. **Owner: the operator's list.**
- **`deploy/manifest-v1.5.0.yaml` carries a pending mechanism whose blocker this lane just
  made false, and whose drift probe cannot see it.** `floor-seal-report` states
  *"MEASURED 2026-09-07: `scripts/validate_hermetization.py` has NO report mode … there is
  nothing for a carrier to ship"*. There is now: `seal_repo()` and the `report` sub-command.
  Its `drift.hub` probe looks for the literal **`--report`**, and this lane shipped a Click
  **sub-command**, so the probe would report the mechanism still absent. Surfaced by the
  terra pass. **The manifest is outside this lane's footprint and was not edited. Owner:
  unassigned — this is the finding to file.**
- **The escalated transcripts row is answered as SHAPE and untouched as CONTENT.** Under the
  fixed rule `corp-monorepo/docs/decisions/transcripts/` is in-shape, because below a
  sanctioned genre depth is the repo's own structure. Whether corp should keep 28
  transcripts is a content ruling the seal was never the right instrument for, and it stays
  the operator's.

## 7 · What this lane did NOT do

- **No seal list ruled** — the verbs stay the operator's, at Sitting 3.
- **No waiver added.** A waiver that hides a rule defect is the defect.
- **No write, move or deletion in any consumer repo** — nine repos read with `git ls-files`,
  and the read-only claim is stamped per repo rather than asserted.
- **No widening past two rules** — the third was named and stopped on, not fixed.
- **No edit to `ecosystem/fleet-shape-spec.yaml`** — V-2's footprint.
- **No merge, no push to `main`, no touch of another lane's branch.** V-2's blob was READ
  out of the shared object database; its branch and worktree were not modified.
- **No JOURNAL entry** — the integrator's surface (`STANDING_RULINGS.md` P-1).
- **No `BACKLOG.md` edit** — the batch gate reserves it for V-4; this is the no-row lane.
- **No index regeneration** — `docs/audits/README.md` and `ecosystem/organ-index.md` are the
  integrator's, once, on the merged result ([#590]).

## 8 · Commits

```
afb50de4  docs(seal)  the attribution measurement + THE STOP
47cf6c25  test(seal)  RED-first witness -- 24 failing, 7 passing
e80fc0cc  test(seal)  assert the hub instance by vocabulary, not directory name
471d3ce0  fix(seal)   the repo seam -- fleet half travels, local half does not
c5109ce0  docs(seal)  the re-run -- WAIVE 336 -> N = 204
<this>    docs(seal)  this lane close
```

---

**Lane:** `lane-v-000-seal-rules-rerun` · batch V, V-3 · substrate local · mode execute
**Closed:** 2026-09-09 · working tree clean · `git stash list` empty
**Base:** `33bcb0bd` · **run against:** `471d3ce0` · **V-2 merge SHA:** none — owed, §4
