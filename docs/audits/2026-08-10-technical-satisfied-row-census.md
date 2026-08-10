# Satisfied-row census — which open rows recent work has already discharged

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** satisfied-row-census
- **Seat:** CC (Opus 5), CLOUD lane N-A, branch `claude/night-batch-cloud-lanes-a4mpkp`
- **Purpose:** test every open row's Done-when against live state, so closes can be adjudicated
  from evidence instead of built.
- **Posture:** read-only. **Nothing closed, nothing born, no row edited.** Evidence only; the
  architect adjudicates.

## Run conditions — hand-run, not gate-passed

Cloud container, conditions as recorded in `[#453]` and confirmed rather than rediscovered:

- `uv 0.8.17` in container vs `pyproject.toml:25 required-version = "==0.11.19"` → every
  `uv run --locked` hook entry refuses. **No pre-commit gate fired for this report.**
- `.git/hooks/` holds only `*.sample` → nothing armed.
- `pytest` is not importable in the container → **no test was executed**; test *existence* is
  reported as existence, never as passing.
- Clone arrived shallow; `git fetch --unshallow` ran before any history claim (4777 commits).
- `audit.py health` is structurally unpassable in a cloud clone (`operational_ok` counts
  resolvable sibling repos; `ls ..` shows none) — not run, not claimed.

Filename verified against both parsers that consume `docs/audits/` before writing:
`validate_hermetization.classify()` returns `None` (clean) for this path, and
`gen_audit_index.py` parses its `YYYY-MM-DD-` prefix and reads the `# ` title above.

## Method, and its honest coverage limit

Source of truth is `tasks/*.md` frontmatter read directly — **never** the generated
`BACKLOG.md`. 255 files, 254 with frontmatter (`tasks/README.md` is the tree's own doc),
**170 `status: open`** — the figure the brief carries, independently reproduced here.

All 170 Done-when clauses parsed cleanly. Rows were then screened mechanically and a subset
deep-tested clause by clause against live state.

**Coverage limit, stated plainly:** ~22 rows were deep-tested with per-clause evidence. The
remaining ~148 carry a mechanical screen verdict only. **A "0 SATISFIED" headline below is a
claim about the tested subset, not about all 170 rows.** The untested remainder is where a
second pass should go, and §5 names the highest-yield cohort.

Prioritisation was as the brief directed: 503 commits landed on `main` since 2026-08-01;
**53 of the 170 open rows cite a path inside that footprint**, and those were tested first.

---

## 1. SATISFIED — every clause demonstrably met

**Zero, within the deep-tested subset.**

This is the census's principal finding and it is a negative one. The hypothesis behind this
lane — that batch 3 shipped ten lanes of change and nobody asked what it discharged — does
**not** hold for the rows most likely to have been discharged. The rows whose footprint
intersects recent work were not silently completed; they were *advanced*, leaving one or two
clauses live. Those are §2.

The practical consequence for the under-100 target: **this lane does not deliver free closes.**
It delivers a short list of rows that are one small act from closing, which is a different and
weaker instrument than the brief hoped for.

## 2. PARTIALLY SATISFIED — ordered by smallest remaining act

### `[#390]` P2/S — resolve the ADR-87 effort-ownership contradiction, then true up the template

Two clauses. **The first is now met and was not when the row was written.**

- Clause 1 — *"ADR-87 carries the resolution"* — **MET.**
  `docs/decisions/ADR-87-*.md:113` carries `## Amendment — 2026-08-08: the population boundary
  on model/effort`, landed at `f633e063` (2026-08-08, *"docs(adr-87): population boundary on
  model/effort — architect states the boot tier"*). It resolves exactly the contradiction the
  row names, and does so as an append-only amendment section — the form the row itself
  prescribes ("resolve there via an append-only amendment marker").
- Clause 2 — *"the template matches it"* — **NOT MET**, and the row's stated defect is still
  live verbatim. `templates/prompt-template.md:68` still renders
  `| Effort | `<low | medium | high>` |`.

  The template is now additionally **self-inconsistent**, which the row did not anticipate:
  `:126` declares *"Effort is a CLOSED enum — `{low | medium | high | xhigh}`"* while `:68`
  offers three rungs, and `:82` says *"`max` sits outside dispatch routing"*. One file, three
  cardinalities.

**Smallest remaining act:** edit one table cell at `templates/prompt-template.md:68` to the
enum already declared at `:126` of the same file. No ruling required — `:126` is the ruled
form; `:68` is stale against its own document.

### `[#508]` P3/S — couple the lane-prefix enum's cardinality to its prose

Done-when is an OR: *"a check FAILs when cardinality and in-repo prose disagree (pinned by a
test that flips one), **or** a ruling records it deliberately unmechanized with its reason."*

- **The underlying drift is currently absent.** `scripts/validate_branch_naming.py:75` holds
  `LANE_PREFIXES = ("worktree-", "epic/", "claude/", "automation/")` — cardinality 4 — and both
  prose sites now say four (`CLAUDE.md:60`, `CONTRIBUTING.md:27`). Prose and code agree today.
- **Neither Done-when branch is met.** Agreement-by-hand is not a check, and no ruling records
  the divergence as deliberately unmechanized. The row exists precisely because agreement
  achieved by hand decays — as CLAUDE.md §12 v2.52 records, this enum already spent a night
  asserting "three" while the validator accepted four.

**Smallest remaining act:** the ruling branch — one recorded line choosing unmechanized-with-
reason — is smaller than the test branch and is fully within the architect's gift.

### `[#317]` P2/M — default-parallel test invocation

Three clauses.

- *"verify cadence parallel by default"* — **MET.** `pyproject.toml:79` records
  `[tool.pytest.ini_options] addopts is -n auto (parallel by default since 2026-08-06)`, and
  `pytest-xdist>=3.8` is a declared dependency (`:30`).
- *"the `not slow` run completes under 60s (measured time recorded at build)"* — **NOT
  ESTABLISHED.** No measurement located in the tracked record. Not testable here in any case:
  pytest is not installed in this container.
- *"serial-nightly preserved"* — **NOT ESTABLISHED** from repo state alone.

**Smallest remaining act:** one timed `not slow` run on a machine with the toolchain, its
number written down. Cannot be done from cloud.

### `[#505]` P1/M — batch-protocol encoding

The highest-priority row in the tested subset. Five clauses; three are met.

- *"hygiene WARN … validator-checked"* — **MET.** `scripts/audit.py:1214`,
  `"""[#505] batch hygiene — WARN on a linked worktree no live batch owns (ADR-110 §1 item 4)."""`
- *"branch-prefix enum … validator-checked"* — **MET.** `scripts/validate_branch_naming.py:75`
  plus `tests/test_validate_branch_naming.py` (exists; **not executed** — see run conditions).
- *"the refuse-to-finish checklist is mechanical"* — **MET.**
  `.claude/commands/lane-integrate.md:50`, `## 3. The refuse-to-finish checklist`.
- *"a fresh seat runs a full batch from repo artifacts alone"* — **FALSIFIED, and falsified
  again tonight.** A prior audit already recorded this:
  `docs/audits/2026-08-06-technical-batch1-verification.md:177-179` — *"Clause 1 … is falsified
  by the … delivered as prompts, not committed artifacts"* — restated at
  `docs/audits/2026-08-07-technical-batch-2-manifest.md:146`. **Tonight is a third instance:**
  this batch reached three cloud lanes as a pasted prompt, and the brief says so in its own
  first line (*"a cloud session cannot see the operator's local prompts directory"*).
- *"batch-1 executes under it with exactly 2 operator touches"* — **UNDETERMINED.** No
  operator-touch count located in `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`.

**Smallest remaining act:** none is small. Clause 1 needs the contract committed as a repo
artifact rather than pasted — which is the same defect three consecutive batches have hit.

### `[#241]` P2/S — undeclared-edge groom

Done-when speaks of *"each of the **6**"*. `ecosystem/disposition-register.yaml` now carries
**20** `warn-undeclared` ids. The population the row was written against has more than tripled;
ARC-4 landed the 20th disposition at `201191f0`. Whether the original 6 are among the
dispositioned 20 is true in substance, but the row's second clause (*"its disposition entry
retires or is re-annotated"*) is not met — the entries stand.

**Smallest remaining act:** re-scope the row's cardinality before testing it again — see §4,
this is also a phrasing finding.

## 3. NOT SATISFIED

**Count: 11 of the deep-tested subset**, each with a Done-when clause demonstrably unmet.
No further detail, per the brief. For the record, the mechanically decisive ones:

| Row | The clause that fails | Evidence |
|---|---|---|
| `[#132]` | *"the generator emits `docs/ORGAN-INDEX.md`"* | file does not exist |
| `[#171]` | names `ecosystem/conformance.md` | file does not exist |
| `[#486]` | names `desired_state_report.py` at that path | not at the cited path |
| `[#269]` | *"header repointed to ADR-100"* | `docs/audits/README.md:5` still points at `[#212]`; shape is month-grouped, not count-tiered |
| `[#285]` | *"PLAYBOOK … carries a `last_reviewed` stamp … in `_FRESHNESS_FILES`"* | `protocols/PLAYBOOK.md` has **no frontmatter at all**; `scripts/audit.py:286` lists only SESSION_SETUP, AI_COUNCIL_PROCESS, DEFINITION_OF_DONE — and `:280` records PLAYBOOK as explicitly DEFERRED |
| `[#334]` | *"the legacy `ruff` alias is gone"* | `.pre-commit-config.yaml:195` still `- id: ruff` |
| `[#369]` | *"the hook is registered … doc-counts reflects 16 gates"* | no `boundary_headers` entry in `.pre-commit-config.yaml`; `ecosystem/doc-counts.md:15` says **17** gates, not 16 |
| `[#365]` | *"the row moves to `coverage_scope:`"* | `residual_completeness` still in the exempt block, `ecosystem/doc-code-edge.yaml:161` |
| `[#422]`, `[#511]`, `[#358]` | cited path/posture unmet | screened; see §5 |

## 4. UNTESTABLE — the Done-when is not mechanically checkable as written

This is a finding about phrasing, not about the work.

- **Off-repo predicate — 27 rows.** The Done-when resolves against consumer repos
  (`ai-council`, `corp-monorepo`) or fleet state: `[#123] [#244] [#267] [#276] [#293] [#324]
  [#327] [#331] [#332] [#340] [#343] [#351] [#371] [#383] [#391] [#401]` and 11 more. These are
  untestable **from a cloud clone specifically** — `ls ..` shows no sibling repos. They are
  testable from the operator's machine. Recording the distinction matters: this is a *runtime*
  limit, not a phrasing defect.
- **Drifted cardinality — `[#241]`.** "each of the 6" against a live population of 20. A
  Done-when that names a count silently expires when the count moves.
- **Drifted locator — `[#360]`.** The row names `protocols/DEFINITION_OF_DONE.md:106-109` as
  "expired in place"; lines 104-112 today hold the *"BACKLOG — gated, advisory (interim, v1)"*
  block, whose own text says it is *"promoted to a hard block when the traceability-spine ADR
  lands"*. Whether that is the intended referent cannot be established from the row. **A
  Done-when pinned to `file:line` in a living document is not mechanically checkable** — the
  line moved, and nothing detected it.
- **Prose predicate — 132 rows.** Their Done-when cites no path at all ("the shape is decided",
  "the divergence is recorded with a reason", "a ruling records…"). These are checkable only by
  a human reading a judgment, which is legitimate for ruling-shaped rows but means **78% of the
  open set cannot be mechanically tested for satisfaction.** That is the structural reason a
  satisfied-row hunt cannot be automated, and the reason this census could not cover all 170.

## 5. Where a second pass should go

The 53 rows intersecting the post-08-01 footprint were the right cohort and are now largely
tested. The untested remainder splits into: the 27 off-repo rows (testable on the operator's
machine, *not* from cloud — highest yield, and blocked only by runtime), and the prose-predicate
bulk (needs an adjudicator, not a script).

`[#506]` deserves the architect's eye here: its Done-when is *"a ranked evidence sheet covers
the full open set with per-id last-touch and closing-merge cross-check, the architect records
live / dead / awaiting-ruling for each id, and the closes land per ADR-65."* **This report is a
partial down-payment on that row's first clause and does not discharge it** — coverage is a
subset, and the architect's per-id record and the closes are both still owed.

## Needs a ruling

1. **Is `[#390]`'s clause 2 a build or a correction?** `templates/prompt-template.md:68`
   contradicts `:126` of its own file. Fixing one table cell to match the enum the same document
   already declares needs no ruling in my reading — but the template is a registered
   `_SPEC_REGISTRY` spec, so an edit trips the coherence-nudge version machinery. Rule whether
   this is a drive-by correction or owed a version bump.
2. **`[#508]` — take the ruling branch?** Its Done-when explicitly offers "a ruling records it
   deliberately unmechanized with its reason". That branch is one line and closes a P3 today.
   The alternative is building a check for an enum that currently agrees.
3. **`[#241]` — re-scope or re-write?** The row tests "the 6" against a population of 20. It
   cannot be adjudicated as written. Re-peg to the live count, or re-phrase to a predicate that
   does not name a cardinality.
4. **`[#360]` — what is the referent?** The `file:line` locator has drifted. I could not
   establish which text the row means. Needs the author's intent, not more searching.
5. **Does `[#505]` clause 1 stay in the row?** It has now been falsified three times
   (batch 1, batch 2, and tonight), each time by the same cause: contracts arrive as pasted
   prompts rather than committed artifacts. Either the clause is the point of the row and stays,
   or the batch protocol accepts pasted dispatch and the clause is struck. A P1 that fails the
   same way three running is not being tested — it is being re-observed.
6. **Is a 0-SATISFIED result acceptable evidence to change the strategy?** The lane was
   commissioned on the hypothesis that satisfied rows exist in quantity. Within the cohort most
   likely to contain them, none did. If that holds on a second pass, neither kills nor satisfied-
   row harvesting closes the gap to under-100, and the 71 closes have to come from somewhere
   else. **That is a strategy question, and it is the most important thing this lane found.**
