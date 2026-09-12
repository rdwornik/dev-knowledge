# Lane x-675 merge cost — end-of-lane packet · 2026-09-12

**Seat:** lane `lane-x-675-merge-cost` · **Batch:** X, wave 2 · **Row:** `[#675]`
**Branch:** `worktree-lane-x-675-merge-cost` · **Base:** `ec18875e` · **Tip:** `50d633f3`
**Status:** **SIX COMMITS LANDED. NOT MERGED — commit-and-STOP, integration is the
integrator's act.**

**carried-by:** `docs/audits/2026-09-12-technical-lane-x-675-merge-cost-packet.md`

**Consumers:** `[#675]` (the row this lane implements) · `[#689]` (owed a proposed diff, §4.1) ·
`[#664]` (owed a proposed diff, §4.2)

---

## 1. THE HEADLINE NUMBER, AND IT IS NOT A NUMBER

Target 3.6 asks for **median merge under 30 minutes, MEASURED — a median over a real run of
merges, reported as a number with its spread against the baseline.**

**The measured answer is: UNDEFINED. Not zero, not "under 30", not met.**

```
merge minutes: NO RECEIPTS. The median is undefined, not zero -- logs/MERGE-RECEIPTS.jsonl
holds no closed merge receipt yet. (2 receipt(s) of another kind EXCLUDED -- a median over
mixed arcs answers a different question than target 3.6 asked, and answers it flatteringly)
```

**A lane seat cannot merge.** The contract's own "What NOT to do" forbids it: *"No merges, no
pushes to `main`, no touching another lane's branch — commit-and-STOP."* So the instrument that
target 3.6 requires was built, is wired into `/lane-integrate`, and **has no merge to measure
from this seat.** The first real datum is owed by the next integration run.

**This is reported as a NOT-MET target rather than dressed up**, and the tool is built so that
it cannot be dressed up: `median` excludes non-merge receipts by name and says it did, because a
ledger mixing merges with cheaper arcs answers a different question under target 3.6's name.
That refusal was added *because* the only receipt this lane could take was a cheaper arc — the
tool caught its author reaching for the flattering number.

### 1.1 What WAS measured, labelled as what it is

**One itemised arc receipt** (`logs/MERGE-RECEIPTS.jsonl`, `kind=arc`, excluded from the merge
median):

```
 0.02 min  [ceremony] lint                ok
 0.50 min  [ceremony] regen               ok
 0.03 min  [ceremony] regen-organ         ok
 0.02 min  [tests   ] targeted            FAILED rc=2
14.36 min  [tests   ] targeted-retry      FAILED rc=1     <- OOM-killed
 0.16 min  [tests   ] targeted-code       ok
 3.61 min  [tests   ] targeted-livetree   ok
 WALL 18.69 min = 18.15 tests + 0.54 residual ceremony     concurrent_seats=4
```

and the receipt closes by naming its own blind spot — `UNRECORDED required step(s): handback,
merge, suite, teardown` — so 18.69 min is explicitly **not** a merge figure.

**A second arc receipt** (`lane-x-675-step-7`) closes at **0.03 min over one FAILED step**, and
it is kept rather than tidied because it records a real defect *of this seat's own making*: the
step ran `pytest` with `impacted_tests select`'s prose output — `# FULL SUITE -- the selector
declined to narrow` — passed through as if it were a file list. **The 111-minute suite run was
therefore taken OUTSIDE the receipt** (§6.1), after four in-receipt attempts were OOM-killed, so
that receipt's `suite` step is genuinely unrecorded and says so. The module offers no way to
enter a duration by hand — it is a stopwatch, and a stopwatch that accepts typed-in numbers is a
spreadsheet — so the honest record is an unrecorded step plus the measurement reported here.

**Six commit-to-commit intervals**, with spread, and they are **wall time containing design,
build and verification — NOT merge ceremony**, so they are not target 3.6's number either:

```
n=6   median 21.6 min   range 7.3 .. 57.1   mean 27.3
quartiles 13.7 / 21.6 / 39.2
each: 7.3, 44.0, 57.1, 24.8, 18.3, 12.1
```

The trend inside them is the only speed claim this packet makes, and it is a claim about
*method*, not about the merge: **57.1 → 24.8 → 18.3 → 12.1** across the last four, because each
gate was verified locally before the commit was attempted rather than discovered by a bounced
commit.

### 1.2 Against the baseline, with the baseline's own spread

Clause 2's frozen baseline, transcribed not recomputed:

> **84 min wall = 11.3 targeted tests + 72.7 residual ceremony (itemised views ~90 and ~63,
> nothing measured today).**

**The parenthesis is part of it.** The two itemised views disagree with each other and with the
wall figure, and nothing was measured on the day it was frozen. Any improvement stated against
it inherits that uncertainty, so **no improvement is stated here.** `merge_receipt median`
prints the baseline's spread beside every median it ever reports, structurally, so a future
number cannot be quoted without it.

**One baseline component is now known to be non-constant** (§3.1): `11.3 targeted tests` is not
a property of how much code changed.

---

## 2. WHAT CHANGED

Six commits, `ec18875e..50d633f3`.

| Commit | Clause / target | What landed |
|---|---|---|
| `76c036f3` | clause 1 (AX25-2) | `scripts/dispatch_conformance.py` + witness — fence, location, model, base in **one** assertion. RED-first, proven RED against the live verb's `:285` refusal |
| `5d3e4001` | clause 2 | `[#675]`'s Done-when leg replaced with the frozen baseline, transcribed with its parenthesis |
| `f903a24f` | clause 1 green + refusal leg | The **writer** moved, not the reader; `dispatch-conformance` pre-commit hook refuses a seam left red |
| `b64f454e` | target 3.1 | `scripts/merge_receipt.py` — per-step minutes, a stopwatch not an orchestrator |
| `0c0c2088` | target 3.4 | `file-collision`, a sixth STEP-0 refusal; **fires on the live batch** |
| `efc9dba2` | target 3.2 (half) | `scripts/actions_verdict.py` — the integrator READS the Actions result, attributed |
| `50d633f3` | targets 3.3, 3.5 | Review raced against the suite, handed a pre-assembled packet |

### 2.1 Clause 1 — which side of the seam moved, and why

**The writer moved. Not one line of the retiring PowerShell verb was touched**, so AX25-4's
bound is satisfied by construction. `Assert-ClaudeCommand`'s refusal at `Invoke-Dispatch.ps1:285`
— *"this script never runs an arbitrary command from a contract file"* — is a deliberate safety
property; widening it would have made every `## Dispatch` block an arbitrary-execution surface to
buy one form's convenience.

**The probe caught a defect in its own fix**, which is the argument for having built it. The
first green run used `<PROMPTS_DIR>`, the interactive shape's prose placeholder. The reader
substitutes exactly one literal, `$env:CLAUDE_PROMPTS_DIR`, so that token would have ridden
through into a real session's prompt: the verb resolves, the dry run prints a plausible line, and
the lane boots unable to find its own contract.

### 2.2 Targets delivered

| Target | State | Evidence |
|---|---|---|
| 3.1 per-step minutes into the receipt | **DONE** | `merge_receipt.py`, wired into `/lane-integrate`; one itemised arc receipt (§1.1) |
| 3.2 Actions suite + index regen, integrator READING it | **HALF DONE** | Reading: `actions_verdict.py`, wired as a step and checklist row 2b. Index regeneration: **NOT DONE**, §4.1 |
| 3.3 Codex reviews in parallel | **DONE (mechanism + wiring)** | `merge_receipt race`, wired as suite‖review. Limit: §3.4 |
| 3.4 dispatcher refuses same-file lanes | **DONE** | `seat_refusals.file-collision`, STEP-0, fires on the live batch |
| 3.5 review/triage handed pre-assembled inputs, NOT cut | **DONE** | `review_packet.py`; no `--brief`/`--summary`/`--max-files`, each absence tested |
| 3.6 median merge under 30 min, MEASURED | **NOT MET — UNDEFINED** | §1. Instrument built and wired; no merge available to a lane seat |

---

## 3. WHAT THE MEASUREMENT FOUND

Every item here was measured during the lane, not reasoned about.

### 3.1 The targeted-test bucket is NON-ADDITIVE — one prose line multiplied it by ~56

`impacted_tests.py select` answers each half of a diff cheaply and the combination explosively:

```
scripts/merge_receipt.py             alone -> 1 file
tests/test_merge_receipt.py          alone -> 1 file
.claude/commands/lane-integrate.md   alone -> 0 files, emits `-m live_repo`
all three together                         -> 56 explicit paths
```

`1 + 1 + 0 = 56`. The two selection modes do not compose: a prose change alone is answered with
a **marker expression**, and the moment any source path joins it the live-tree tests are
materialised as **paths**. `--explain` attributes the expansion to the `[live-tree-doc]` rule.

**Consequence for the baseline:** `11.3 targeted tests` is not a function of how much code
changed. It is a function of whether a diff happens to touch prose and code in the same commit —
which the tree-coherence gates actively **force**, since a new organ must move its generated
surfaces in the same commit.

### 3.2 Contention is a hard ceiling on what a lane can verify, not a footnote

Measured mid-lane: **2,072 MB free of 28,330 MB**, the remainder held by peer seats' python
processes, with `concurrent_seats=4` recorded automatically into the receipt.

**The targeted selection for a three-file diff could not be run on this machine at all.**
OOM-killed at `-n 6`, then again at `-n 2`; it completed only decomposed and serial. A fourth
kill took a commit's own hook run. **14.36 minutes were spent producing no verdict** — and the
receipt recorded that as a *failed* step, which is the whole argument for itemisation: in a
single wall number those minutes are indistinguishable from minutes that bought a passing suite.

**Then the FULL suite was OOM-killed too — four times: `-n 6`, `-n 2`, `-n 0` serial, and a
12-file chunking.** Free memory was measured at **2,574–2,971 MB of 28,330 MB with only two
python processes alive**, so the pressure is the concurrent *sessions* themselves, not their test
runs.

**The fifth shape worked, and which shape it was is the finding.** Run as **31 serial chunks of
6 test files, each chunk a fresh process**, the whole suite completed: 69 failed, 6139 passed, 11
skipped, 111.1 min cumulative (§6.1). Nothing was skipped and no test file was dropped — chunking
bounds *peak* memory to one chunk without touching coverage. So the honest form of this finding is
narrower than the one this section first recorded, and the correction matters:

> **`pytest` green is verifiable at this batch width — but only in a shape no one asks for, and
> at ~111 minutes.** What the contention actually destroys is not the suite's runnability; it is
> the suite's runnability *in the single command the process prescribes*. `uv run --locked pytest`
> is OOM-killed; the same tests in 31 processes are not.

**This is the part of merge cost that no process change can reach — with one exception this lane
can name.** Targets 3.1–3.5 make the merge legible and move work off the critical path; none of
them creates memory. At four seats the integrator's *"full suite run once on the merged result"* —
refuse-to-finish row 2 — is the step most likely to be unrunnable exactly when the batch is
widest. **The exception is target 3.2:** a suite that runs on Actions does not compete with four
local seats for 28 GB at all, which is a second, independent reason for that target beyond the one
the row gives.

**A caveat the chunking imposes, stated rather than buried:** 31 processes are not one process,
and *which tests share a process* is observable — 5 of the 69 failures depend on exactly that
(§6.1). A chunked run establishes each test file's verdict; it does not establish the verdict of
one 6,219-test process. Both were measured here, and the 5 that differ are traced to their cause.

### 3.3 The Actions suite is RED on `main`, and nobody reads it

The row says *"a green run nobody reads is not a gate"*. The live state is worse. The three most
recent `conductor.yml` runs on `main` all concluded **failure** (`pytest` fails; `ruff`, `seal`,
`phase-gate`, `terra` pass), **every one was already printed at SessionStart**, and every merge
proceeded.

That measurement forced the design: a gate refusing any non-green run would refuse every merge in
this repo today, and a gate that refuses everything is turned off inside a window. Hence the
differential — `REGRESSED` / `PRE-EXISTING` / fixed / `UNATTRIBUTED` — **all exiting non-zero**,
`PRE-EXISTING` included, because this merge did not cause those failures and must still never be
recorded as green.

### 3.4 One new pre-commit hook moved THREE generated surfaces

Adding `dispatch-conformance` bounced a commit and required regenerating `ecosystem/doc-counts.md`
(two claims: `pytest_collected` and `precommit_hook_count`), `ecosystem/organ-index.md`, and the
persisted FPG-1 store. **The marginal cost of one gate is three regenerations plus a bounced
commit** — and it is also why target 3.4's refusal cannot see derived-surface collisions: two
lanes declaring *different* sources that regenerate one index collide in fact and not in
declaration.

### 3.5 A superseded contract on the transport collides with its own replacement

Globbing `LANE-x-*.md` returns 13 contracts and one collision — `deploy/manifest-v1.5.0.yaml`
between `LANE-x-734-retire-stage` and `LANE-x-734-retire-stage-2` — and `git worktree list` shows
only the **second** provisioned. The first is a superseded re-cut nobody deleted. So a dispatcher
feeding the collision refusal a **glob** would be refused for a lane it was never going to fire.

Not re-solved here: `[#630]`'s `freeze_manifest_contract_agreement` already owns whether the
contract set is the right set. The dependency is **stated** in three places rather than
duplicated, and carried as a test.

### 3.6 A vacuous test, caught by mutation

`test_EVERY_changed_file_is_listed_and_the_list_is_NEVER_truncated` **passed** against a
deliberate `changed_files[:50]` truncation. The fixture's 400 files were all *undeclared*, so
every path also appeared in the declared-vs-actual section and a whole-document `in` check could
not see the list shrink. **A test that cannot fail is worse than no test, because it is
counted.** Fixed by slicing the section under its own heading, plus a complement test for the
case the vacuous version could never distinguish.

This is `[#675]`'s own filed defect, found inside the work that answers it: a check returning a
plausible result because the discriminating field — *which section* a path appeared in — was
absent from what it looked at. Five further mutations were run against `merge_receipt.py`; each
failed exactly one test.

### 3.7 A gate whose remedy cannot be followed

`graph-task-coverage` refused a staged `.gitignore` for having no `implements` edge from an open
row. Its remedy — *"name this file in the row's body, or name the row `[#id]` in this file"* — is
**unsatisfiable in both directions**: `file_purpose_graph._REL_PATH_RE` requires at least one `/`
in a path, so **no root-level dotfile can ever carry that edge**. Both halves were tried and both
failed. Every commit staging a root-level dotfile is refused with an instruction that cannot be
followed.

The `.gitignore` change was withdrawn on its own merits anyway (§3.8), so this lane is not
blocked by it — but the defect is live for the next lane that stages one.

### 3.8 A design that changed because of a gate

The in-flight receipt scratch was going to be gitignored. It is now deliberately **not**: `close`
removes it on the normal path, so the only case an ignore rule would affect is the abandoned one
— where that file is the sole record a merge died half-way. Hiding it would make an integrator's
tree read clean over exactly the case worth seeing.

---

## 4. PROPOSED DIFFS — not applied, and why

### 4.1 `[#689]` — the `index-regen` job (target 3.2's other half)

Target 3.2 asks for the full suite **and index regeneration** on Actions. The suite is there; the
regeneration is not, so a green run covers one half. `actions_verdict` reports that gap and the
notice **retires itself** when such a job appears.

**Not applied because this lane's own target 3.4 forbids it.** Measured with
`seat_refusals.declared_footprint`, the function this lane shipped:

```
LANE-x-689-conductor-e.md  ->  .github/workflows/conductor.yml
LANE-x-675-merge-cost.md   ->  docs/audits/2026-09-12-technical-batch-x2-manifest.md
```

`[#689]` declares that file; this lane does not. Writing it would be exactly the collision target
3.4 exists to refuse, in the same commit range that built the refusal. The contract offered a
class-(b) escalation here; it was not needed, because the mechanism this lane built answered it.

**Proposed**, for `[#689]` to apply — a job named `index-regen` (the id `actions_verdict.
INDEX_REGEN_JOB` already looks for), running each generator with `--check` rather than `--write`,
since a gate that edits the tree is not a gate:

```yaml
  index-regen:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: astral-sh/setup-uv@v5
        with: { version: "0.11.19" }
      - run: uv sync --locked
      - name: every generated index is current
        run: |
          set -e
          uv run --locked python scripts/gen_task_tree.py --check
          uv run --locked python scripts/gen_audit_index.py --check
          uv run --locked python scripts/generate_organ_index.py --check
          uv run --locked python scripts/gen_doc_counts.py --check
          uv run --locked python scripts/gen_claude_rosters.py --check
```

**Honest note for whoever applies it:** `docs/audits/README.md` is `merge=ours`-pinned and is
therefore **stale by construction after every merge**, so `gen_audit_index.py --check` will fail
on `main` until the integrator's own once-per-batch regeneration lands. Either sequence that
regeneration before the push or leave `gen_audit_index` out of this job. That interaction is why
this diff is proposed rather than applied blind.

### 4.2 `[#664]` — command files are not wiring surfaces

**Three organs from one lane** — `merge_receipt.py`, `actions_verdict.py`, `review_packet.py` —
are all genuinely adopted by `.claude/commands/lane-integrate.md` and all three read as orphans,
because the `[#664]` wiring surfaces are `.pre-commit-config.yaml`, `.claude/settings.json`, the
plugin `hooks.json`, the scheduled task and the CI workflows — and a **command file is none of
them**. So every operator-invoked organ in this repo reads as an orphan by construction, whatever
its real adoption.

One such row is a curiosity; three from a single lane is the shape of a gap. Each carries a
reasoned `ORPHAN_DISPOSITIONS` entry naming this as the cause and `[#664]` as the owner — the
rows delete by that decision, not by a lane.

**Proposed:** add `.claude/commands/*.md` to the wiring-surface set in `file_purpose_graph.py`,
contributing `triggers` edges from a command file to each `scripts/*.py` it invokes. **Not
applied from here** because it changes what `graph-orphan-census` refuses repo-wide, from a lane
contracted on merge cost — the same overrun AX25-4 bounds on clause 1.

A pre-commit trigger was considered and **rejected on the merits** for all three, not merely as
out of scope: a stopwatch has nothing to gate; an Actions verdict reads a run for a merge SHA
that does not exist at commit time; a review packet assembles over a merge range and a lane
contract that do not exist at commit time in the lane being reviewed.

### 4.3 `graph-task-coverage`'s unsatisfiable remedy (§3.7)

**Proposed:** either admit root-level paths in `_REL_PATH_RE`, or exempt root-level dotfiles from
`graph-task-coverage` with a reason. **Not applied**: widening that regex changes edge extraction
repo-wide, and the exemption register is explicitly for surfaces that *cannot carry* an ownership
claim (generated files, whole-row records) — `.gitignore` is neither, so adding it would be the
paper suppression that register's own docstring warns against. This needs a ruling, not a lane.

---

## 5. OPEN ITEMS

1. **Target 3.6 is UNMET and owes one measurement.** The next `/lane-integrate` run produces the
   first real merge receipt. Until then the median is undefined, and the tool says so.
2. **Target 3.2's index-regeneration half** — §4.1, owned by `[#689]`.
3. **Three orphan dispositions** — §4.2, owned by `[#664]`'s wiring-surface list.
4. **`graph-task-coverage`'s unsatisfiable remedy** — §4.3, needs a ruling.
5. **The Actions suite is RED on `main`** (§3.3). Not this lane's to fix, and now readable:
   `actions_verdict.py --sha <merge> --baseline <first parent>` names which jobs are
   pre-existing.
6. **`impacted_tests` non-additivity** (§3.1) — reported, unowned. It sets the size of the
   baseline's `targeted tests` bucket, so it is on `[#675]`'s critical path even though it is not
   in this lane's footprint.
7. **Contention** (§3.2). Four concurrent seats OOM-kill `uv run --locked pytest` in every
   whole-suite shape tried — `-n 6`, `-n 2`, `-n 0`, and 12-file chunks. It completes only as 31
   serial 6-file chunks, at ~111 min. This is a fact about batch width vs machine, and ADR-110's
   ceiling is stated in coordination cost rather than memory.
8. **The full suite is 69-RED on this tree before any lane touches it** (§6.1), so
   refuse-to-finish row 2 currently hands the integrator a 69-failure wall to read. **Unowned and
   not filed by this lane** — filing a row is the operator's act and a `kill-candidates:` line
   would be owed. Two sub-findings are cheap and separable:
   - **17 of the 69 are one missing optional dependency** — `pandas`, absent from the locked
     environment, failing all of `tests/test_fleet_analytics.py`. Either the dependency is
     declared or those tests are skipped on its absence; silently red is the one option that
     teaches nothing.
   - **`test_gen_handoff.py` shadows the real `audit` module** with a stub written to a temp
     directory, which REDs 5 tests in `test_gen_handoff_preflight.py` / `test_gen_intake_tree.py`
     whenever they share a process with it. They pass alone. This is why the suite's verdict
     depends on how it is chunked.

## 6. THE SUITE VERDICT

### 6.1 How it was obtained, and why that is stated

```
185 test files, run as 31 serial chunks of 6, each chunk a fresh process
69 failed, 6139 passed, 11 skipped
cumulative wall 6665.6s = 111.1 min
ATTRIBUTABLE TO THIS LANE: 0 of 69
```

**Every one of the 69 was attributed, and none is this lane's.** Two mechanisms, both measured,
neither assumed:

- **64 of 69 reproduce at the lane base.** The lane's twenty tracked paths were stepped back to
  `ec18875e` in place, the 69 ids re-run there, and the tree restored unconditionally — the
  paired-baseline method §6.2 already used, and *not* `git stash`, which is shared with the
  concurrent seats. Result at the base: **64 failed, 5 passed**.
- **The remaining 5 are order-dependent, and the order is not this diff's.** They **pass at HEAD
  when run alone** (`5 passed in 9.55s`). Re-running chunk 14's exact six-file composition at
  HEAD reproduces the original failure set exactly (10 failed, 336 passed), and the errors name
  the cause outright: `module 'audit' has no attribute 'check_intake_tree_coherence'` /
  `_HUB_ONLY_FRESHNESS_FILES`, with `audit` resolving out of a **temp directory** —
  `test_gen_handoff.py`'s stub shadowing the real module for every test collected after it in the
  same process. Neither attribute has anything to do with this lane; the shadowing is a
  pre-existing test-isolation defect that surfaces whenever those files share a process.

**It was run in 31 serial chunks because four whole-suite attempts were OOM-killed** — `-n 6`,
`-n 2`, `-n 0` serial, and a 12-file chunking — with free memory measured at 2,574–2,971 MB of
28,330 MB under four concurrent seats (§3.2). **Chunking changes peak memory, never coverage:**
every test file is run exactly once, and the chunk boundaries are `ls tests/test_*.py | sort`
sliced six at a time. A serial run is not a weaker verdict — it executes the same tests — but it
is a *slower* one, and it is recorded as serial so its duration is never compared against a
parallel baseline.

**The chunking is also what made the 5 order-dependent failures visible at all**, and that cuts
both ways: a chunked run is not identical to a single-process run, because which tests share a
process is exactly what these 5 depend on. The honest statement is that this run establishes
each test file's verdict, not the verdict of one 6,219-test process — and that the difference
showed up as 5 tests, all traced.

### 6.1.1 What the suite verdict actually says about merge cost

**The full suite is 69-RED on `main` before this lane touches it, and 17 of those 69 are one
missing optional dependency** (`ModuleNotFoundError: No module named 'pandas'`, all in
`tests/test_fleet_analytics.py`). That is the same finding as §3.3 from the other end: refuse-to-
finish row 2 asks the integrator to run the full suite on the merged result, and on this tree
that instruction returns a 69-failure wall whose signal-to-noise is low enough that nobody reads
it — which is precisely how a real regression would pass unnoticed.

**This is a target-3.2 argument, not an aside.** Moving the suite to Actions *and reading the
result attributed against a baseline* — which `scripts/actions_verdict.py` now does, with
`PRE-EXISTING` as a distinct state from `REGRESSED` — is the only shape in which a 69-red suite
is still a usable gate.

### 6.2 Pre-existing REDs — attributed, reported, NOT fixed

**All 69 are attributed in §6.1 by the two mechanisms stated there.** This section keeps the
per-test detail for the ones examined individually, because a count is not an attribution and
the table is what a reviewer can check. None was fixed: a lane does not repair `main`'s REDs
inside its own diff, and doing so would have put work outside the declared footprint.

The largest clusters, named so the 69 is not an opaque number:

| Cluster | n | Attribution |
|---|---|---|
| `test_fleet_analytics.py` | 17 | `ModuleNotFoundError: No module named 'pandas'` — an optional dependency absent from the locked environment. Environmental; reproduces at the base |
| `test_governance_health.py` | 7 | Reproduces at the base |
| `test_gen_handoff.py` | 5 | Reproduces at the base; also the *source* of the 5 order-dependent failures (§6.1) |
| `test_funnel_lifecycle.py` | 4 | Live-tree legs; `check_funnel_lifecycle` is SHIP-tier by declaration and leg a1 FAILs on live `main` **by design** |
| `test_normalize_headers.py` | 4 | Corpus-wide legs; reproduces at the base |
| `test_gen_intake_tree.py` | 4 | The order-dependent set — passes alone at HEAD (§6.1) |

The four examined in full before the whole-suite run, kept for their detail:

| Test | Attribution |
|---|---|
| `test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger` | Names **only** `scripts/worktree_seed.py`, dispositioned AND triggered via `.claude/settings.json`. Re-measured with all three of this lane's dispositions in place: unchanged. Owner `[#664]` |
| `test_canonical_docs.py::test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date` | Reproduces identically at HEAD. Date-driven (PLAYBOOK stamped 2026-09-08, read 2026-09-12) |
| `test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival` | Same |
| `test_v6_frozen_contract.py::test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped` | `verify_handoff_probes` CLI flags; untouched by this diff |

**One test fixture WAS repaired**, because it blocked the very property covering this lane's
change: `test_the_SIX_FROZEN_BATCH_X_CONTRACTS_still_pass_after_the_widening` asserted a
hard-coded `== 6` against a directory grown to 8, so it failed on its own arithmetic *before*
reaching the property — leaving the checker's regression guard off during exactly the change it
guards. The count is now a lower bound.

---

## 7. WHAT THIS LANE DID NOT DO

- **No merges, no pushes to `main`, no other lane's branch touched.** Commit-and-STOP.
- **No JOURNAL entry** — the integrator's surface (`STANDING_RULINGS.md` P-1).
- **No index regeneration beyond the generated surfaces its own diff moved**, each regenerated
  with its declared generator and staged with the commit that moved it. **No single-hook bypass
  was used at any point**; no `--no-verify`.
- **No work on the retiring PowerShell verb** beyond clause 1's test (AX25-4).
- **The 30-minute target was NOT reached by cutting review or triage.** `review_packet.py` has no
  flag that could shorten a review, and `race` records every job's verdict and fails if any job
  failed.
- **No median was reported without its spread** — including the one that could not be computed,
  which is reported as undefined rather than omitted.
