# Batch-4 prep — evidence sheets, footprint map, contract skeletons

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** batch-4-prep-evidence
- **Seat:** CC (Opus 5, effort high), lane C, worktree `.claude/worktrees/batch4-prep`, branch
  `worktree-batch4-prep`, cut from `main` @ `12ef9c91`
- **Purpose:** carry the research half of batch-4's GO, so the GO is a decision and not a
  research session. Per-candidate evidence · a file-disjointness map the lane decomposition can
  be cut from · contract skeletons · copy-ready recording blocks.
- **Posture: READ-ONLY.** Nothing born, nothing closed, no row / intake / ADR / BACKLOG edited.
  This report is the lane's only write. **Every judgment below is a RECOMMENDATION, never a
  ruling** — labelled as such at each site.

## Run conditions — what this lane could and could not verify

- Hub worktree on the operator's host, full history. `uv run --locked` used for every script
  invocation (STANDING_RULINGS D4 — a bare `python` inside a lane reads the PRIMARY checkout).
- **No test run.** This lane changed no code, so the suite was not exercised; the standing
  `test_routine_consumers_live_backlog_governs_exactly_one_row` RED is unchanged and untouched.
  No test result is claimed anywhere below.
- **Row state is read from `tasks/*.md` frontmatter, never from `BACKLOG.md`** — 253 files with
  frontmatter, **170 `status: open`**, independently reproduced here and matching the
  `2026-08-10-technical-satisfied-row-census.md` figure.
- **GitHub Actions run history is NOT readable from this seat.** Where a claim depends on
  whether a workflow job has actually executed since a given commit, it is marked UNCERTAIN and
  is not resolved by inference.
- Filename verified against both consuming parsers before writing:
  `validate_hermetization.classify()` → `None` (clean), `rule_a_violation()` → `None`, and the
  path does **not** match `batch_manifest.MANIFEST_GLOB` (`docs/audits/*-batch-*-manifest.md`)
  — so this report cannot be mistaken for a batch manifest and grants no ADR-110 exemption.

---

## 1. Evidence sheets

### Sheet A — `[#270]` Operator-load gauge (P1/M)

**Frontmatter, verbatim** (`tasks/270-operator-load-gauge.md:1-10`):

```
id: "[#270]"
title: "Operator-load gauge"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
```

**No `serialize-group`. No `depends-on`. No `DEFER` peg.**

**Done-when, verbatim:** *"Done when: the `[load]` line renders in the SessionStart digest from
live counts AND the CSV appends per run AND the ex-ante metric + kill criterion are recorded in
the closing commit"*

**Current evidence lines.**

- **Idle 34 days**, confirmed. The only two commits touching the task file are `9bd0d719`
  (2026-07-27, the `tasks/` tree generation) and `5c8a9d6d` (2026-07-28, the ADR-107 STEP-3
  flip — a 175-file mechanical provenance re-stamp whose own message says *"No row closed."*).
  Last **meaningful** touch is `6a5115d4` (2026-07-07), pre-flip, in `BACKLOG.md`. The Fable
  adversarial review reached the same figure independently
  (`2026-08-10-verification-fable-adversarial-plan-review.md:60-63`).
- **Build target exists and is unmodified:** `scripts/fleet_health.py` (525 lines) carries no
  `[load]` section — `grep load` returns only `_load_state_yaml` / `load_all_states`.
- **`logs/OPERATOR-LOAD.csv` is NOT in `.gitignore`.** The ignore file carries the sibling
  ephemera (`logs/PROPOSALS-*.md:26`, `logs/FLEET-HEALTH.md:30`, `logs/FLEET-ANALYTICS.md:49`,
  `logs/COHERENCE-NUDGE.log:73`) but no `OPERATOR-LOAD` line. **A build owes a `.gitignore`
  edit** or the CSV lands as tracked churn on every session start.
- The row's five funnel counts each have a live producer already in the repo (nightly-triage
  Issues, `propose_closures.py` proposals, `ecosystem/disposition-register.yaml`,
  ARCHITECT-REVIEW-PENDING markers, open BACKLOG by priority) — this is aggregation, not new
  measurement.

**Serialize-group membership:** none declared on `[#270]` itself. Its two `depends-on`
dependents split: `[#348]` carries `serialize-group: settings-json`, `[#271]` carries none.

**Dependency edges — the three dependents, each verified in-row.**

| Row | Edge | Site | Status / size |
|---|---|---|---|
| `[#271]` Nightly proposal loop | `depends-on: "#270"` | `tasks/271-*:9` | open, P3/L |
| `[#348]` Backlog grooming as a standing routine | `depends-on: "#270"` | `tasks/348-*:10` | open, P3/S |
| `[#117]` Evaluate prompt/agent-based hooks | `DEFER — peg: #270` (body, not frontmatter) | `tasks/117-*:13` | **deferred**, P3/S |

Also referencing but not gated: `[#322]`, `[#391]`, `[#419]` (*"`#270` gauge…"* in its
kill-candidates clause), `[#424]`.

**Interaction worth the architect's eye:** `[#424]` asserts that `depends-on` gates are INERT
because `_DEPID_RE` requires a `#`. **Both `[#270]` dependents write `"#270"` WITH the hash**,
so they are the shape the parser does read — `[#424]`'s defect does not blunt this chain. That
is a fact about these two rows, not a disposition of `[#424]`.

**Testability verdict: MECHANICAL (2 of 3 legs) + CONVERTIBLE (1).** Leg 1 (`[load]` renders
from live counts) and leg 2 (CSV appends per run) are directly testable. Leg 3 (*"the ex-ante
metric + kill criterion are recorded in the closing commit"*) is checkable by reading one commit
message — mechanically greppable if the closing commit is required to carry a named token.

---

### Sheet B — `[#514]` Two rival `LANE_BRANCH_RE` constants (P1/M) — the merge-queue wedge

**Frontmatter, verbatim** (`tasks/514-*.md:1-10`):

```
id: "[#514]"
title: "Two rival `LANE_BRANCH_RE` constants ship in one repo"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
```

**No `serialize-group`. No `depends-on`.**

**Done-when, verbatim:** *"Done when: provisioning refuses an off-enum lane name, one clean batch
runs under it, and exactly ONE definition remains"*

**The regex pair, re-measured this session (not carried from the review).**

| Constant | Site | Pattern |
|---|---|---|
| strict | `scripts/validate_branch_naming.py:85` | `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$` |
| loose | `scripts/batch_manifest.py:91` | `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$` |

The loose one is documented in-file as *"A REFINEMENT of `worktree-<name>` (Ch8), so it needs no
new prefix-enum ruling to exist"* — i.e. it was authored deliberately, not by accident, which is
why the reconciliation is a decision and not a cleanup.

**`LANE_PREFIXES` is a separate and currently-healthy surface:** `validate_branch_naming.py:75`
holds `("worktree-", "epic/", "claude/", "automation/")`, cardinality 4, matching all in-repo
prose (see Sheet D-adjacent `[#508]`, §5 block 3). **The `[#514]` split is about the lane-BRANCH
grammar, not the prefix enum** — two different constants, easily conflated.

**The ADR-110 interaction, stated precisely.**

- `exempt()` (`batch_manifest.py:251-268`) requires **both** an open committed manifest **and** a
  `LANE_BRANCH_RE` (loose) match on the merged-branch name.
- ADR-110 §1 item 5 declares *"Lane/branch-prefix enum — validator-checked naming"* as one of the
  five artifacts; §2 parameterizes lane count at N (drilled 3, designed 4–10).
- **A `claude/<slug>` cloud lane matches NEITHER regex.** `classify()` routes it to
  `KIND_CLOUD_LANE`, which is a *conforming* kind — so it passes branch-name validation while
  being structurally incapable of exemption. This is why the ADR-110 exemption granted the
  2026-08-09 night batch nothing, as `JOURNAL.md` 2026-08-10 (b) item 1 records at the time.
- **Live datapoint from this very lane:** this session's branch is `worktree-batch4-prep`, which
  matches neither lane regex and classifies `KIND_WORKTREE`. A non-batch worktree is correctly
  outside both — the split does not mis-classify ordinary worktrees, only lane-shaped ones.

**THE SEQUENCE IS THE ROW'S OWN LOAD-BEARING CLAUSE and must survive into any contract:** enforce
at provisioning FIRST (classify `git branch --show-current`, BLOCK on `KIND_UNKNOWN` under the
`worktree-lane-` prefix), and ONLY THEN delete the loose regex. Step 2 before step 1 makes 9 of 10
historical lane merges non-exempt — a merge-queue outage. **A contract that lists these as two
steps without marking the order load-bearing has already lost the row's point.**

**Dependency edges:** none in frontmatter. Prose neighbours, each of which **disclaims** ownership
of the split (so `[#514]`'s `kill-candidates: none` is earned):

- `[#510]` P2/M — *"Scope the R-1 exemption to the lanes its manifest enumerates"*. **Same file,
  `scripts/batch_manifest.py`.** Its Done-when wants `exempt()` keyed to a declared lane ROSTER
  rather than branch shape; `[#514]` wants one grammar. **These two rows cannot run in parallel
  lanes** — see §3.
- `[#508]` P3/S — the prefix-enum cardinality claim, a different surface.
- `[#505]` P1/M — batch-protocol encoding, the parent artifact set.

**Testability verdict: MECHANICAL, with one empirical leg.** Leg 1 (provisioning refuses an
off-enum name) and leg 3 (exactly one definition remains — a two-file grep) are directly testable.
Leg 2 (*"one clean batch runs under it"*) is an **empirical** predicate: it cannot be discharged
by a test run, only by an actual batch. **RECOMMENDATION:** if batch 4 takes this row, leg 2 is
naturally discharged by batch 4 itself only if the fix lands *before* the batch integrates —
otherwise the row cannot close in the same batch that builds it, and the contract should say so.

---

### Sheet C — `[#502]` mutmut mutation-testing evaluation (P3/M) — the substrate question

**Frontmatter, verbatim** (`tasks/502-*.md:1-11`):

```
id: "[#502]"
title: "mutmut 3.7.0 mutation-testing evaluation — CI-hosted"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: environment
generates: BACKLOG.md
```

**Done-when, verbatim:** *"Done when: a scoped pilot runs on CI, the `uv run --locked` question is
answered from a real run, and the result is a recorded ADOPT/REJECT with measured divergence"*

**THE ROW'S NARRATIVE IS STALE ON TWO LOAD-BEARING PREMISES. This is the sheet's principal
finding, and it changes the row's size.**

1. **"BLOCKED ON `[#501]` — until that wall exists there is nowhere to host the eval."**
   `[#501]` is `status: closed`, and the wall exists:
   `.github/workflows/report-only-wall.yml`, landed `67e5518c` (2026-08-06). It carries a
   dedicated `mutation-pilot` job (`:225-303`), gated since `e62c412a`/LA-4 to
   `workflow_dispatch` OR a push that touched the pilot's own subject.
2. **"`mutmut` under `uv run --locked` is NOT VERIFIED, the one remaining unknown."** The
   workflow's own comment at `:261-265` states the opposite and says why:
   *"`--with` keeps mutmut EPHEMERAL … `--locked` still asserts the project lockfile is current,
   so the contract's 'under uv run --locked' holds. **This composition was exercised live before
   being written here, not assumed.**"* The invocation is `uv run --locked --with mutmut==3.7.0
   mutmut run` (`:266`).

**What else is already built.** `pyproject.toml:52-91` carries a scoped `[tool.mutmut]` block:
`source_paths = ["scripts"]`, `only_mutate = ["*fleet_analytics.py"]`,
`pytest_add_cli_args_test_selection = ["tests/test_fleet_analytics.py"]`, and
`pytest_add_cli_args = ["-n", "0"]`. The key names are recorded as verified against mutmut 3.7.0's
own `configuration.py`, not assumed. The calibration case named by the workflow exists:
`tests/test_fleet_analytics.py:144-146`, `test_canonical_path_survives_a_cycle`, asserting
`in {"a","b"}` where the correctness assertion is `== "b"` — the mutant that flips *which* node is
returned should survive, and that survivor is the pilot's whole verdict.

**The one recorded run, and its measured failure.** `pyproject.toml:87-88` records CI run
`31127625224`, job `mutation-pilot`: *"`mutmut exit: 1` with all 84 mutants reported `not
checked`, i.e. a pilot that measures nothing while looking green."* Cause: `-p no:xdist` also
unloads the `-n` option that `addopts` supplies. Fixed at `27c37ae3` (2026-08-06) by switching to
`-n 0`.

**UNCERTAIN, and not resolved by inference: has the pilot run since `27c37ae3`?** The `if` gate
means it fires only on `workflow_dispatch` or a push touching `scripts/fleet_analytics.py` /
`tests/test_fleet_analytics.py` / `pyproject.toml`. No in-repo artifact records a post-fix run,
and Actions history is not readable from this seat. **This is the single fact that decides whether
`[#502]` is a 10-minute close or a real lane.**

**Serialize-group:** `environment` — shared with every other row that touches the locked
toolchain. No other subject in this batch carries it.

**Dependency edges:** `refs #501` (closed), `refs #392` (the pilot-slice evidence — the
`fleet_analytics` rename-alias defect, open, P3/S). `[#507]` also refs `#501` (the fourth
report-only leg) — a sibling on the same workflow file.

**Testability verdict: MECHANICAL (legs 1–2) + PROSE (leg 3).** *"a scoped pilot runs on CI"* and
*"the `uv run --locked` question is answered from a real run"* are artifact-checkable. *"a
recorded ADOPT/REJECT with measured divergence"* is a judgment; it is convertible to mechanical
only if the row names where the verdict is recorded (an ADR, a `docs/audits/` file, or the row's
own close commit).

**RECOMMENDATION (not a ruling):** re-read `[#502]`'s size before scheduling it. If a
`workflow_dispatch` produces a checked-mutant report, the remaining work is *read the survivor
list, write the verdict* — S-sized, and its row text needs a correction pass regardless, because
two of its stated premises are false at HEAD.

---

### Sheet D — the `kill-candidates:` refusal-check candidate (3b-3) — NO ROW EXISTS

**There is no `tasks/` file for this.** This sheet describes the gap so the architect can decide
whether it earns a birth. Searched and rejected as owners: `[#440]` (tamper-evident `tasks/` id
ledger — the *record*, not the filing gate), `[#488]` (a ranking function), `[#487]`
(closure-proposal consumption — the close side), `[#519]` (the two-edit close path). **None owns
the quality of the commit-msg filing gate.**

**The mechanism as built** — `scripts/check_backlog_filing.py`, 116 lines, wired as the
`backlog-filing-backpressure` commit-msg hook. Its whole acceptance predicate is one regex
(`:35`):

```
_KILL_RE = re.compile(r"^kill-candidates:\s*(none\b.*|.*#\d+.*)$", re.M | re.I)
```

**Four refusal gaps, each read off that line rather than inferred:**

1. **The reason is optional in code and mandatory in doctrine.** `PLAYBOOK.md:3812` requires
   *"`kill-candidates: none — <reason>`"*. The regex accepts `none` followed by `.*`, so a bare
   `kill-candidates: none` with no reason at all passes.
2. **No existence check.** `.*#\d+.*` matches any digit string. `kill-candidates: #999999`
   passes; there is no lookup against `tasks/`.
3. **No liveness check.** Naming an already-`closed` id satisfies the gate identically to naming
   an open one — the backpressure is discharged by proposing the removal of something already
   removed.
4. **Any prose containing a `#id` on that line passes.** The alternation's second branch is
   `.*#\d+.*`, so `kill-candidates: supersedes #241` satisfies it without proposing anything.

(Known and already-recorded: the line must be **flush-left** — `re.M` anchors it. That is a
usage gotcha, not a refusal gap, and is not counted above.)

**Measured usage — the case that the gate is a formality.**

| Population | Total | `none` form | Names an id |
|---|---|---|---|
| Commit messages since 2026-06-01 | 350 | **331 (94.6%)** | 19 (5.4%) |
| `tasks/*.md` rows carrying the field | 171 of 254 | **165 (96.5%)** | 6 (3.5%) |

**Counter-evidence, recorded because it refutes the strong form of the finding.** The mechanism
has produced a real disposition at least once: `[#489]` was filed carrying
`kill-candidates: #218`, and the 2026-08-05 architect ruling re-scoped `[#218]` in place and
retired `[#489]` — the retirement note in `tasks/489-*.md` says so and cites
`docs/audits/2026-08-05-technical-night-batch-morning-report.md` §6.1. **So the honest claim is
"used as a formality in ~96% of filings", not "never works".** A refusal check should be scoped
to make the `none` branch cost something, not to abolish it.

**Serialize-group:** n/a (no row). The natural label is `gates`, which `[#508]` already carries.

**Testability verdict: MECHANICAL.** Every gap above is a regex-plus-lookup change with a
directly pinnable test (a message that passes today and must FAIL after).

---

### Sheet E — the ARC-6 carry-forward defect (evidence on `[#310]` + JOURNAL 2026-08-10 (c))

**Owning row's frontmatter, verbatim** (`tasks/310-*.md:1-11`):

```
id: "[#310]"
title: "Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: handoff
generates: BACKLOG.md
```

**`status: deferred`, peg `post-Wave-1`. This row is not open** — a batch-4 lane taking it must
un-defer it first, which is an operator act.

**`[#310]`'s Done-when, verbatim:** *"Done when: a sanctioned cold-annotation surface is defined
AND the 07-05 architect bundle is recorded as-cold on it (no rendered bundle file edited, no
retrospective fabricated)"* — **this Done-when does NOT cover the carry-forward defect.** The
defect is attached to the row as a second instance; it is not in the row's contract.

**The defect, from repo state.**

- `gen_handoff.py --allow-suffix` (`:278-300`, `_resolve_bundle_dir`; render tokens rebuilt at
  `:757-766`) writes a fresh `-2` / `-3` sibling with **FILL-IN regions re-rendered EMPTY**. The
  flag exists to prevent a worse failure — `:289` records that silent suffixing was rejected
  because a prior run *"wrote into"* an existing bundle *"reproduced with real data loss"*.
- On 2026-08-10 the `-2` sibling nearly shipped four unfilled regions minus its predecessor's
  residual. It was **refused** by `residual_completeness` (`86078062`), which is the gate working.
- **The gate catches only the EMPTY case.** `validate_residual_completeness.py:25-33` states its
  own limit: *"It asserts only *placeholder-replaced*, never *value-present*. A by-reference fill
  that names no verdict, count, or sha PASSES (pinned by `test_by_reference_fill_passes`)."* A
  region refilled with **thinner** content therefore passes.
- **Nothing names a re-cut's predecessor sibling or carries its payloads.** That is the unowned
  half, recorded on `[#310]` rather than birthed, per the ARC-6 instruction.

**Ownership already adjudicated — do not re-search.** JOURNAL 2026-08-10 (c) records that
`[#422]` was checked and **rejected** as owner (its subject is cold framing prose surviving a
FILLED flip — a missing detector after a *fold*, a different mechanism), and that `[#511]`,
`[#399]`, `[#298]`, `[#404]`, `[#353]`, `[#365]`, `[#366]` were each read and none owns it.

**Serialize-group:** `handoff` — shared with `[#390]` (Sheet-adjacent, §5 block 2), `[#404]`,
`[#422]`, `[#298]`, `[#350]`.

**Testability verdict: CONVERTIBLE.** *"A `-N` sibling carries its predecessor's payloads"* is
mechanical only once "carries" is defined. Two phrasings that would be:
(a) *a `-N` sibling whose FILL-IN region is byte-shorter than the same region in its immediate
predecessor FAILs unless the commit declares the reduction*; (b) *`gen_handoff --allow-suffix`
refuses unless `--carry-from <predecessor>` is passed*. **(b) is the cheaper and more honest
predicate** — it moves the check to the generator, where the predecessor is known, instead of
asking a validator to infer intent from byte counts. **RECOMMENDATION only.**

---

### Sheet F — the ARC-7 §6-item-3 site (`CLAUDE.md:109` + carrier)

**No row.** This is a knowingly-left-standing residual, declared in the file it lives in.

**The two sites, byte-identical, verified this session:**

| Site | Line | Text |
|---|---|---|
| `CLAUDE.md` | `:109` | `3. Read most recent handoff if continuing prior session` |
| `templates/claude-regions/session-start-protocol.md` | `:4` | *(same line)* |

They are byte-coupled by `tests/test_boundary_headers.py:266-279`
(`test_hub_region_bodies_still_byte_match_the_templates`), which reads
`templates/claude-regions/`. **Source-of-truth order is carrier first, then `CLAUDE.md`** — the
order ARC-7 used and the order the coupling test enforces.

**The fixed sibling, for the exact phrasing to mirror.** `templates/claude-regions/first-read.md:5`
now reads: *"The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what
`audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`,
`check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than
one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule."*

**Standing declaration.** `CLAUDE.md:224` (§12 v2.55) states the residual in terms:
*"A SECOND SITE IS KNOWINGLY LEFT STANDING — §6 item 3 still reads 'Read most recent handoff'; it
lives in a different hub region (`session-start-protocol`) and the operator scoped this act to
one line, so it is filed rather than widened."* JOURNAL 2026-08-10 (d) says the same and calls it
*"a real residual"* that *"should not be read as complete coverage of the phrase."*

**Gate coupling — the reason this is not a one-line edit.** Touching `CLAUDE.md` puts
`last_reviewed` before the file's last edit, which reds `canonical_freshness` (A2) and **wedges
the `audit-health` pre-commit gate**. Discharging it requires a genuine full-file end-to-end
re-read plus a §12 entry and an L10 version bump — ARC-7 did exactly this and recorded the cost.
**Any lane taking this item is buying a CLAUDE.md re-read, not a line edit.**

**UNCERTAIN — consumer copies.** The `session-start-protocol` region is an `owner=hub` region;
whether consumer repos (`ai-council`, `corp-monorepo`, …) carry a deployed copy of *this*
region, and how many, was **not** verified — no sibling repo is resolvable from this worktree.
Marked UNCERTAIN in the footprint map rather than assumed either way.

**Testability verdict: MECHANICAL, cheaply.** A `doc_claims`-shaped assertion — *"no boot-region
line contains the phrase `most recent handoff` without naming `_select_active_bundle`"* — is a
grep with a test that flips one site. The byte-match test then guards the carrier↔`CLAUDE.md`
pair for free.

---

## 2. Feature-class candidate search (F24-2)

**Method.** All 170 open rows enumerated from `tasks/` frontmatter and read by theme. Two
mechanical screens, then judgment:

- **Screen 1 — the repo's own "new-feature epic" definition.** `check_backlog_filing.py:40`
  (`_LBAND_RE`) treats `[P1-3][L]` as the new-feature-epic band. **Five open rows are L-sized:**
  `[#244]` P2/L, `[#271]` P3/L, `[#383]` P2/L, `[#43]` P3/L, `[#487]` P2/L.
- **Screen 2 — intake-cited rows** (the ADR-98 requirements spine, which is where feature work
  enters): **24 open rows** cite an intake.

**Verdict: NOT zero — but the finding is close to it in substance, and it is a quota finding.**

Of the 170 open rows, the overwhelming majority are **governance repair** (a gate that does not
fire, a doc that contradicts code, a ruling not recorded) — 59 in `[E2] Enforced governance`
alone. This is structural, not accidental: `CLAUDE.md` §5 rule 4 makes this Layer 2, which never
executes, so a "feature" here can only ever be a new *validator, generator, or surface*. The
census reached the same shape from the other direction: **78% of open Done-whens are prose
predicates** with no path at all.

**Top 3 candidates, ranked (RECOMMENDATION — not a ruling).**

| # | Row | Why it fits "feature-class" |
|---|---|---|
| 1 | **`[#270]` Operator-load gauge** (P1/M, `[E7]`) | The most feature-shaped row in the open set and the only P1 among them: it produces a **new artifact a human reads** (a `[load]` section in the SessionStart digest) plus a new time-series (`logs/OPERATOR-LOAD.csv`). It is aggregation over five producers that already exist, so the risk is low and the output is immediately visible. It also unblocks three rows. |
| 2 | **`[#132]` Organ-index generator** (P2/M, `[E2]`) | Emits a genuinely new document — `docs/ORGAN-INDEX.md` — on the established codemap/toc generator+freshness-hook pattern, and absorbs `[#248]`. Its stated purpose, *"kills 'operator-as-registry'"*, is a capability the operator currently supplies from memory. Confirmed still unbuilt: the census records *"the generator emits `docs/ORGAN-INDEX.md`" → file does not exist*. |
| 3 | **`[#171]` Conformance dashboard at `ecosystem/conformance.md`** (P3/M, `[E6]`) | Same shape as #2 — a read-only validator generating and committing a new human-facing surface (ADR-86/ADR-80). **UN-DEFERRED 2026-08-09**, peg met, and it un-blocks the `[#169]`/`[#322]` chain. Confirmed unbuilt: the census records the named file does not exist. |

**Runners-up, named so the architect can substitute rather than re-search:** `[#488]` (a ranking
function the backlog has never had — but its own Done-when makes leg (a) a *research* lane whose
output is ruling input, so it is not a build); `[#412]` (subagent/workflow routing + fan-out —
explicitly *"Filing only, zero build"*); `[#329]` (VS Code ownership visualization — consumer-facing).

**`[#490]`-class (a green signal that measures a subset).** `[#490]` itself is **closed**
(`status: closed`, parity-surfaces reached 9/9 at 2026-08-07). Its live successor is
**`[#383]` Execution waves per surface** (P2/L, `[E9]`), whose Done-when is unusually mechanical
for this repo — three named, runnable clauses over 8 enumerated rows at
`ecosystem/parity-surfaces.yaml:834-899`, with clause (c) requiring the operator to have read
them. **1 of 6 waves is executed**; `serialize-group: architecture`.

**Consumer-repo work — the cohort is real and is the batch's blind spot.** 17 open rows in
`[E6]`, plus `[#413]`, `[#371]`, `[#464]`, `[#340]`, `[#430]`. **The census's own §4 finding
binds here:** 27 open rows have an off-repo predicate and are *"testable from the operator's
machine"* but not from cloud — which is exactly the highest-yield untested cohort and exactly the
cohort a cloud lane cannot take. **RECOMMENDATION: any consumer-repo row in batch 4 must be a
LOCAL worktree lane, never a `claude/<slug>` cloud lane.**

---

## 3. Footprint & disjointness map

**Subject keys:** **A** `[#270]` · **B** `[#514]` · **C** `[#502]` · **D** 3b-3 kill-candidates
refusal check · **E** ARC-6 carry-forward · **F** ARC-7 §6 item 3.

### 3.1 Per-subject plausible footprint

Files a fix would plausibly touch. **UNCERTAIN** marks a file whose involvement depends on a
design choice not yet made — treat every UNCERTAIN as an OVERLAP until the architect resolves it.

**A — `[#270]`**
- `scripts/fleet_health.py` · `tests/test_fleet_health.py` · `.gitignore` (the missing
  `logs/OPERATOR-LOAD.csv` line)
- `ARCHITECTURE.md` — **7** `fleet_health` mentions; Ch2 organ map / Ch6 verification mesh
- `ecosystem/doc-counts.md` — regenerate if tests are added (`gen_doc_counts.py --write`)
- **UNCERTAIN:** `CLAUDE.md` §9 (the SessionStart surfacing row names `fleet_health.py`) — only
  if the digest's declared contents change in a way the roster line states
- **UNCERTAIN:** `ecosystem/disposition-register.yaml` — only if the gauge reads it live rather
  than counting it
- close-time: `tasks/270-*.md`, `BACKLOG.md`, `tasks/manifest.json`

**B — `[#514]`**
- `scripts/validate_branch_naming.py` · `scripts/batch_manifest.py` ·
  `tests/test_validate_branch_naming.py` · `tests/test_batch_manifest.py`
- `.claude/commands/lane-boot.md` (the provisioning refusal is a boot-step change)
- `protocols/PLAYBOOK.md` **Ch8** (batch protocol) · `docs/decisions/ADR-110-*.md`
  (append-only amendment marker if the exemption's shape moves)
- `ecosystem/doc-counts.md` (tests added)
- **UNCERTAIN:** a new `scripts/` module if the provisioning guard is not folded into
  `validate_branch_naming.py`
- close-time: `tasks/514-*.md`, `BACKLOG.md`, `tasks/manifest.json`

**C — `[#502]`**
- `pyproject.toml` (`[tool.mutmut]`) · `.github/workflows/report-only-wall.yml` (the
  `mutation-pilot` job's `if` gate — `:223-224` says *"UNGATE WHEN `[#502]` LANDS ITS VERDICT"*)
- a `docs/audits/` verdict file (new; needs a filename verified against the class enum)
- **UNCERTAIN:** `tests/test_fleet_analytics.py` — only if the verdict is *strengthen the
  assertions*, which is the likely ADOPT consequence
- **UNCERTAIN:** `uv.lock` — the `--with` composition is deliberately ephemeral, so an ADOPT that
  promotes mutmut to a dependency group would churn it
- close-time: `tasks/502-*.md`, `BACKLOG.md`, `tasks/manifest.json`

**D — 3b-3**
- `scripts/check_backlog_filing.py` · `tests/test_check_backlog_filing.py`
- `protocols/PLAYBOOK.md` **§10** (the filing-backpressure doctrine paragraph, `:3812`)
- `CLAUDE.md` §9 (`backlog-filing-backpressure` roster row states the gate's behaviour)
- `ARCHITECTURE.md` — **1** mention (Ch2 gate list)
- `ecosystem/doc-counts.md` (tests added)
- birth-time: a **new** `tasks/NNN-*.md`, `BACKLOG.md`, `tasks/manifest.json`

**E — ARC-6 carry-forward**
- `scripts/gen_handoff.py` (878 lines — `_resolve_bundle_dir` `:278-300`, render `:757-766`) ·
  `scripts/validate_residual_completeness.py` (214 lines) ·
  `tests/test_gen_handoff.py` · `tests/test_residual_completeness.py`
- `protocols/HANDOFF_PROCESS.md` (spec — a version bump trips `coherence-nudge` and the
  `reconciled_versions` check) · `docs/handoffs/README.md` (**freshness-gated**)
- `ARCHITECTURE.md` — **4** `residual_completeness` mentions
- `ecosystem/doc-counts.md` (tests added)
- row-time: `tasks/310-*.md` (**and an un-defer, which is an operator act**) **or** a new row

**F — ARC-7 §6 item 3**
- `templates/claude-regions/session-start-protocol.md` (carrier — edit FIRST)
- `CLAUDE.md` (§6 region + a §12 entry + `last_reviewed` re-stamp + L10 version bump)
- `tests/test_boundary_headers.py` — **read-only**: it passes automatically once both sides match
- **UNCERTAIN:** consumer-repo `CLAUDE.md` copies of the `session-start-protocol` region — not
  resolvable from this worktree

### 3.2 The overlap that is not pairwise — read this before the matrix

**`BACKLOG.md` and `tasks/manifest.json` are GENERATED from `tasks/` by `gen_task_tree.py`**
(`:4` — *"THE DERIVATION RUNS TREE → FILE. `tasks/` is the SOURCE OF TRUTH"*). Any lane that
**closes or births a row** regenerates both. **Consequence: no two lanes in this batch are truly
file-disjoint if both touch a row.** `ecosystem/doc-counts.md` behaves the same way for any lane
that adds tests (it carries `tests: 2721 collected`).

This is not a reason to serialize — it is a reason to **name the resolution rule in every
contract**. The repo already has the precedent and it worked: at ARC-5 (`19aca464`)
`docs/audits/README.md` conflicted exactly as predicted and was **resolved by regeneration, never
by hand** (`gen_audit_index.py --write`, then `--check` exit 0, then a grep proving zero conflict
markers reached the staged blob).

**RECOMMENDATION (not a ruling): every batch-4 lane contract carries the same clause —**
*"`BACKLOG.md`, `tasks/manifest.json` and `ecosystem/doc-counts.md` are generated. On any
conflict, regenerate; never hand-merge. Verify with `--check` exit 0 and a conflict-marker grep
before staging."* These three files are then excluded from the disjointness question by
construction, and the matrix below reads them out.

### 3.3 Pairwise disjointness matrix

Generated files (§3.2) are excluded throughout. `DISJOINT` = no shared file. `OVERLAP(f)` = shared
file `f`. `UNCERTAIN` = the overlap depends on an unmade design choice.

| | A `[#270]` | B `[#514]` | C `[#502]` | D 3b-3 | E ARC-6 | F ARC-7 |
|---|---|---|---|---|---|---|
| **A** | — | DISJOINT | DISJOINT | **OVERLAP** `ARCHITECTURE.md`; **UNCERTAIN** `CLAUDE.md` §9 | **OVERLAP** `ARCHITECTURE.md` | **UNCERTAIN** `CLAUDE.md` |
| **B** | DISJOINT | — | DISJOINT | **OVERLAP** `protocols/PLAYBOOK.md` (Ch8 vs §10) | DISJOINT | DISJOINT |
| **C** | DISJOINT | DISJOINT | — | DISJOINT | DISJOINT | DISJOINT |
| **D** | see above | see above | DISJOINT | — | **OVERLAP** `ARCHITECTURE.md` | **OVERLAP** `CLAUDE.md` (§9 vs §6) |
| **E** | see above | DISJOINT | DISJOINT | see above | — | DISJOINT *(but see gate note)* |
| **F** | see above | DISJOINT | DISJOINT | see above | DISJOINT *(gate note)* | — |

**Notes the matrix cannot carry.**

1. **`ARCHITECTURE.md` is the batch's busiest shared file** — A (7 mentions), E (4), D (1). Three
   of six subjects plausibly edit it, and the Fable review found it carries **14 checkably-FALSE
   claims** with ≥3 already false when `8f09c12d` stamped a genuine review on 2026-08-08. **A lane
   editing `ARCHITECTURE.md` inherits that stamp problem.** RECOMMENDATION: at most ONE lane in
   batch 4 may edit `ARCHITECTURE.md`, or the file is declared out of scope for all lanes and the
   owed rows are collected by the integrator.
2. **`CLAUDE.md` is the second — and it is worse, because it is freshness-gated.** D (§9 roster
   row) and F (§6 region) are a **hard OVERLAP**: both force a `last_reviewed` re-stamp on the
   same file, and `canonical_freshness` A2 wedges `audit-health` — which is a **pre-commit** gate,
   so it blocks even the commit explaining it. **D and F cannot be separate lanes.**
3. **`protocols/PLAYBOOK.md` — B (Ch8) and D (§10).** Different sections of one 3800+-line file,
   so git will usually merge them cleanly, but the `toc-freshness-playbook` pre-commit hook fires
   on both. Marked OVERLAP rather than DISJOINT deliberately: *"different sections"* is exactly
   the reasoning that produces a race.
4. **E–F gate note (not a file overlap).** Both edit a `canonical_freshness`-gated file — E
   touches `docs/handoffs/README.md`, F touches `CLAUDE.md`. Different files, so they merge; but
   both owe a **genuine re-read**, and neither can discharge the other's.
5. **`[#510]` is the missing seventh subject and it collides with B.** `[#510]` (P2/M, open)
   re-keys `exempt()` in `scripts/batch_manifest.py` — **the same function `[#514]` deletes a
   regex from.** They are `OVERLAP(scripts/batch_manifest.py)` at function granularity. **If both
   are in batch 4 they are ONE lane.** RECOMMENDATION: run `[#514]` first and alone; `[#510]`'s
   roster keying is a strictly easier problem once one grammar exists.
6. **C is the cleanest lane in the set** — `pyproject.toml` + one workflow file + one new audit,
   overlapping nothing. It is also the one whose *size is unknown* (Sheet C's UNCERTAIN).

### 3.4 Decomposition the matrix supports (RECOMMENDATION — not a ruling)

A four-lane cut with no OVERLAP cell inside any lane:

- **Lane 1 — B `[#514]`** (+ `[#510]` folded in if the architect wants the roster keying, since
  it is the same file). P1, the merge-queue wedge, and the sequencing clause is load-bearing.
- **Lane 2 — C `[#502]`**. Fully disjoint. **Contract step 1 is a `workflow_dispatch`** — its
  size is not knowable before that.
- **Lane 3 — D + F together** (they share `CLAUDE.md`; splitting them creates the wedge). One
  lane owns the `CLAUDE.md` re-read and both edits.
- **Lane 4 — A `[#270]`** *or* **E ARC-6**, not both — they share `ARCHITECTURE.md`. **A is the
  RECOMMENDATION**: it is the only P1 of the two, it is 34 days idle, it unblocks three rows, and
  E's owning row is `deferred` and needs an operator un-defer before a lane can take it.

---

## Appendix 1 — Contract skeletons

**These are DRAFTS for the architect, not dispatchable artifacts.** None is frozen; each needs the
architect's Done-when before it becomes a contract. Decision-budget stubs follow the V-2 shape
(escalate on (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) fork classes with no
standing ruling; everything else decided per contract defaults and reported in the end packet).

### Skeleton A — `[#270]` Operator-load gauge

**Purpose.** Build the gating first element of any Tier-2 nightly layer: a `[load]` funnel-count
section in the existing `fleet_health.py` SessionStart digest, plus a gitignored per-run CSV. Its
ex-ante success metric and pre-registered kill criterion ARE the contract.

**Candidate Done-when (mechanically testable phrasing).**
1. `scripts/fleet_health.py` emits a `[load]` block carrying all five funnel counts, each derived
   from a live producer — pinned by a test that seeds each producer and asserts the rendered count.
2. `logs/OPERATOR-LOAD.csv` gains exactly one row per digest run, header-stable — pinned by a test
   asserting append-not-overwrite across two runs.
3. `.gitignore` carries `logs/OPERATOR-LOAD.csv` — pinned by asserting `git status --porcelain` is
   clean after a run.
4. The closing commit message carries a line matching `^load-gauge-metric:` and one matching
   `^load-gauge-kill-criterion:`. *(Converts the row's prose leg into a greppable one. **Needs the
   architect's word** — it adds a commit-message convention.)*

**Steps outline.** (1) Read `fleet_health.py`'s digest assembly and the five producers; state
which are already read and which are new I/O. (2) Write the failing tests first. (3) Implement
the `[load]` block. (4) CSV append + `.gitignore`. (5) Regenerate `ecosystem/doc-counts.md`.
(6) `ARCHITECTURE.md` Ch2/Ch6 row **only if** the architect assigns `ARCHITECTURE.md` to this
lane. (7) Full suite + `audit.py health` + ship-gate; commit-and-STOP.

**Decision-budget stubs.** ESCALATE: whether the closing-commit token convention (leg 4) is
adopted; whether this lane owns `ARCHITECTURE.md`; whether the CSV is gitignored or tracked (the
row says gitignored — a contradiction with a durability requirement would be a (b) conflict).
DECIDE-AND-REPORT: column set and ordering; where in the digest the block renders; whether a
producer that errors renders `n/a` or omits the row.

### Skeleton B — `[#514]` Reconcile the rival `LANE_BRANCH_RE` constants

**Purpose.** Two constants with the same name and different grammars mean both organs cannot be
enforced. Reconcile to one — **in the row's stated order**, because the reverse order is a
merge-queue outage.

**Candidate Done-when.**
1. **Step 1 first:** provisioning refuses an off-enum lane name — `/lane-boot` (or the validator
   it calls) classifies `git branch --show-current` and BLOCKs on `KIND_UNKNOWN` under the
   `worktree-lane-` prefix. Pinned by a test asserting refusal on `worktree-lane-foo` and pass on
   `worktree-lane-a-514-lane-regex`.
2. **Step 2 only after step 1:** `scripts/batch_manifest.py` imports the strict constant;
   `grep -c "LANE_BRANCH_RE *=" scripts/` returns **1**. Pinned by a test asserting the two
   modules resolve to the *same object*.
3. One clean batch runs under the reconciled pair. **Empirical, not a test** — the contract must
   say which batch discharges it, and if that batch is batch 4 itself, the fix must land before
   integration or the row cannot close in-batch.

**Steps outline.** (1) Re-measure the disagreement on real merged lane branches and record the
count in the packet. (2) Build and test the provisioning refusal. (3) `/lane-boot` step-1 text.
(4) Only then collapse the constants; run `tests/test_batch_manifest.py` and
`tests/test_validate_branch_naming.py`. (5) PLAYBOOK Ch8 + an ADR-110 append-only amendment marker
if the exemption's shape moved. (6) Suite + gates; commit-and-STOP.

**Decision-budget stubs.** ESCALATE: whether `[#510]`'s roster keying folds into this lane (same
file); whether ADR-110 needs an amendment marker (an ADR touch is (a)); how leg 3 is discharged.
DECIDE-AND-REPORT: which module owns the surviving constant; whether the provisioning guard is a
new script or a `validate_branch_naming.py` mode; the refusal's exit code.

### Skeleton C — `[#502]` mutmut pilot verdict

**Purpose.** Answer the assertion-quality question with a real run. **Step 1 is a measurement,
not a build** — the row's two stated blockers are false at HEAD (Sheet C), and the lane's first
act is to find out whether anything remains to build.

**Candidate Done-when.**
1. A `mutation-pilot` run **after `27c37ae3`** exists and its report shows mutants actually
   *checked* (not the 84-`not checked` shape). Artifact-checkable.
2. The `uv run --locked --with mutmut==3.7.0` composition is confirmed from that run's log.
3. A `docs/audits/YYYY-MM-DD-technical-<slug>.md` records **ADOPT or REJECT**, names the survivor
   list, and states whether the calibration case
   (`test_canonical_path_survives_a_cycle`, `in {"a","b"}` vs `== "b"`) produced a survivor.
4. **Either** the workflow's `mutation-pilot` gate is widened (ADOPT) **or** the job is deleted
   (REJECT) — the workflow's own `:223-224` demands one or the other.
5. `tasks/502-*.md`'s two stale premises are corrected **whatever the verdict**.

**Steps outline.** (1) `workflow_dispatch` the pilot. (2) Read the survivors against the
calibration case. (3) Write the verdict audit (filename verified against the class enum first).
(4) Execute leg 4. (5) Correct the row. (6) Commit-and-STOP.

**Decision-budget stubs.** ESCALATE: ADOPT/REJECT itself — this is a standing-tool decision, an
operator call; whether an ADOPT promotes mutmut into a dependency group (`uv.lock` churn, and the
`--with` ephemerality was a deliberate choice). DECIDE-AND-REPORT: the verdict audit's slug;
whether a REJECT deletes the `[tool.mutmut]` block or leaves it inert-with-reason.

### Skeleton D — the `kill-candidates:` refusal check (3b-3)

**Purpose.** The filing-backpressure gate accepts a `none` line with no reason, a `#id` that does
not exist, and a `#id` that is already closed. 94.6% of filings take the `none` branch. Make the
escape cost something without abolishing it.

**Candidate Done-when.**
1. `check_backlog_filing.py` BLOCKs a message whose `kill-candidates:` line is the bare `none`
   form with no reason — pinned by a test that flips one character.
2. It BLOCKs a line naming a `#id` with **no file** in `tasks/` — pinned by a test using a
   fabricated id.
3. It BLOCKs (or WARNs — **architect's call, see budget**) a line naming an id whose frontmatter
   `status` is terminal.
4. `PLAYBOOK.md` §10 and the `CLAUDE.md` §9 roster row state the gate's *actual* predicate.
5. **No existing in-repo commit-message convention is retroactively invalidated** — verified by
   replaying the last 50 `kill-candidates:` lines through the new predicate and reporting how many
   would now block.

**Steps outline.** (1) Birth the row (carries its own `kill-candidates:` line — the gate applies
to its own filing). (2) Write the failing tests. (3) Extend the predicate. (4) Run leg 5 and put
the number in the packet **before** deciding leg 3's severity. (5) Doc sites. (6) Regenerate
`ecosystem/doc-counts.md`. (7) Suite + gates; commit-and-STOP.

**Decision-budget stubs.** ESCALATE: whether this earns a row at all (**it has none today**);
BLOCK vs WARN for leg 3 — a BLOCK on a closed-id reference is a real behaviour change for a
100%-of-filings gate; whether a minimum reason length is imposed (a (c) fork class — no standing
ruling on prose-quality gates). DECIDE-AND-REPORT: exact error text; whether the existence lookup
reads `tasks/` or `tasks/manifest.json`.

### Skeleton E — the ARC-6 carry-forward defect

**Purpose.** `--allow-suffix` re-renders FILL-IN regions empty and `residual_completeness` catches
only the empty case, so a `-N` sibling can ship thinner than its predecessor and pass. Nothing
names a re-cut's predecessor or carries its payloads.

**Candidate Done-when.** *(Two rival phrasings — the architect picks ONE.)*

- **(b), RECOMMENDED:** `gen_handoff --allow-suffix` REFUSES unless the predecessor is named
  (`--carry-from <dir>` or equivalent), and the named predecessor's filled regions are carried
  into the new sibling. Pinned by a test that runs `--allow-suffix` without the flag and asserts
  refusal, and one that runs it with the flag and asserts payload carry.
- **(a):** `validate_residual_completeness` FAILs when a `-N` sibling's region is byte-shorter
  than the same region in its immediate predecessor unless the commit declares the reduction.
  *(Cheaper to state, harder to live with — "shorter" is not "thinner".)*

**Steps outline.** (1) **Confirm the row's status.** `[#310]` is `deferred`; an un-defer is an
operator act — the lane STOPs if it is not already done. (2) Reproduce the re-cut on a scratch
slug and record the exact loss. (3) Failing test. (4) Implement the chosen phrasing.
(5) `HANDOFF_PROCESS.md` (**version bump → `coherence-nudge` + `reconciled_versions`**).
(6) Regenerate `ecosystem/doc-counts.md`. (7) Suite + gates; commit-and-STOP.

**Decision-budget stubs.** ESCALATE: (a) vs (b); whether this rides `[#310]` (whose Done-when does
NOT cover it) or earns its own row; the `HANDOFF_PROCESS` version bump (a spec touch).
DECIDE-AND-REPORT: the flag's name; whether refusal is hard or `--force`-able.

### Skeleton F — the ARC-7 §6-item-3 site

**Purpose.** `CLAUDE.md` §6 item 3 and its carrier still say *"Read most recent handoff"* — the
phrase §1 item 3 was fixed for. Declared standing at `CLAUDE.md:224`.

**Candidate Done-when.**
1. `templates/claude-regions/session-start-protocol.md` item 3 names the live predicate
   (`_select_active_bundle`, newest by **git add-date**), mirroring `first-read.md:5`.
2. `CLAUDE.md` §6 matches it byte-for-byte —
   `tests/test_boundary_headers.py::test_hub_region_bodies_still_byte_match_the_templates` passes.
3. `grep -c "most recent handoff"` over `CLAUDE.md` + `templates/claude-regions/` returns **0**
   outside §12's historical narrative.
4. `CLAUDE.md` carries a §12 entry, an L10 version bump, and a `last_reviewed` re-stamp **backed
   by a genuine end-to-end re-read** — never a stamp-around.
5. **RECOMMENDED, needs the architect's word:** a `doc_claims`-shaped check pins leg 3 so the
   phrase cannot reappear.

**Steps outline.** (1) Carrier FIRST. (2) `CLAUDE.md` region. (3) Genuine twelve-section re-read
(this is the lane's real cost, not the edit). (4) §12 + L10 + `last_reviewed`. (5) Confirm
`silent_rule_ratchet` is unmoved — **add no `must|shall|never` token**; the budget stood at
440 ≤ 441 after ARC-7. (6) Suite + gates; commit-and-STOP.

**Decision-budget stubs.** ESCALATE: whether leg 5's check is in scope (new machinery, and ARC-7
deliberately shipped *"a reference to an existing predicate, not new machinery"*); whether
consumer copies are in scope (**UNCERTAIN** — unresolvable from a hub worktree, and core-invariant
#6 bars a unilateral global edit if `~/.claude` is implicated). DECIDE-AND-REPORT: the exact
wording, given it must mirror `first-read.md` without adding a normative keyword.

---

## Appendix 2 — Recording paste-blocks

**Every block below is a DRAFT and applies ONLY under the corresponding checklist ruling.** None
is a ruling; none has been written anywhere. Each is copy-ready for the primary's post-ruling
recording pass. Dates left as `2026-08-10` — change if the ruling lands later.

### Block 1 — `[#241]` cardinality-free re-phrase

> **DRAFT — applies only under the corresponding checklist ruling** (census "Needs a ruling" #3:
> *"`[#241]` — re-scope or re-write?"*). The row tests *"each of the **6**"* against a live
> population of **20** `warn-undeclared` ids in `ecosystem/disposition-register.yaml`. This
> re-phrase removes the cardinality so the predicate cannot silently expire again.

Replace the Done-when clause in `tasks/241-undeclared-edge-groom.md` with:

```
· Done when: every id the `undeclared_edges` ship-gate leg surfaces is either declared
(`reconciled_with`) or recorded permanent-defer-with-reason, and each such id's disposition
entry retires or is re-annotated — the predicate reads the live surfaced set, never a fixed
count
```

Commit message (the row is edited, not closed or born — no `kill-candidates:` line is owed, and
`backlog-id-on-close` does not fire because no task line is removed):

```
docs(backlog): [#241] re-phrase the Done-when cardinality-free — "the 6" expired at 20

The row was written against 6 tier-1 candidates the `undeclared_edges` leg surfaced on its
first live run. `ecosystem/disposition-register.yaml` now carries 20 `warn-undeclared` ids;
ARC-4 landed the 20th at `201191f0`. A Done-when that names a count silently expires when the
count moves (census 2026-08-10 §4), so the predicate now reads the live surfaced set.

Scope: phrasing only. No id declared, no disposition retired, no status change.
Ruling: <ruling locator>
```

**Watch:** the row is `serialize-group: coherence`; `validate_doc_rot.scan_backlog_accretion`
WARNs at ≥3 full `YYYY-MM-DD` dates AND >700 chars, **or** >1200 chars — keep the edit net-neutral
in length and add no third full date.

### Block 2 — `[#390]` cell fix + version-bump note

> **DRAFT — applies only under the corresponding checklist ruling** (census "Needs a ruling" #1:
> *"Is `[#390]`'s clause 2 a build or a correction?"*). Clause 1 is **already MET** —
> `docs/decisions/ADR-87-*.md:113` carries `## Amendment — 2026-08-08: the population boundary on
> model/effort`, landed `f633e063`. Only clause 2 is live.

The edit, `templates/prompt-template.md:68`:

```
| Effort | `<low | medium | high>` |
```
→
```
| Effort | `<low | medium | high | xhigh>` |
```

**The enum comes from `:126` of the same file** — *"Effort is a CLOSED enum — `{low | medium |
high | xhigh}`"* — so this is a document made self-consistent, not a new decision. `:82` records
that `max` sits outside dispatch routing and is deliberately excluded.

Commit message:

```
fix(template): [#390] clause 2 — the Effort cell matches the enum its own file declares

`templates/prompt-template.md:68` offered three rungs while `:126` of the same file declares
`{low | medium | high | xhigh}` as a CLOSED enum and `:82` places `max` outside dispatch
routing. One file, three cardinalities (census 2026-08-10 §2). Fixed to `:126`'s ruled form.

VERSION-BUMP NOTE: `templates/prompt-template.md` is a registered `_SPEC_REGISTRY` spec, so a
content edit trips the `coherence-nudge` forgotten-version-bump path. Ruled <BUMP | NO-BUMP>
by <ruling locator>: <reason>.

Clause 1 was already discharged at `f633e063` (ADR-87 amendment 2026-08-08).
```

**Watch:** `coherence-nudge` is **non-blocking** (always exit 0) and logs to
`logs/COHERENCE-NUDGE.log`; the `reconciled_versions` audit check is the durable signal. If the
ruling is BUMP, the bump and the cell fix ride the **same** commit or the nudge fires on the gap.

### Block 3 — `[#508]` deliberately-unmechanized register line

> **DRAFT — applies only under the corresponding checklist ruling** (census "Needs a ruling" #2:
> *"`[#508]` — take the ruling branch?"*). The row's Done-when is an explicit OR, and this block
> executes the **ruling** branch. **State of the world when written:** the drift is currently
> ABSENT — `validate_branch_naming.py:75` holds four members and both in-repo prose sites say
> four. The row exists because agreement reached by hand decays.

Register line for `protocols/STANDING_RULINGS.md`:

```
- **B<n> (2026-08-10) — the lane-prefix enum's cardinality stays UNMECHANIZED, deliberately.**
  `validate_branch_naming.LANE_PREFIXES` is the checkable surface; four prose sites state the
  cardinality in words — `CLAUDE.md` §4, `CONTRIBUTING.md`, the hub carrier
  `templates/claude-regions/conventions-commit-branch.md`, and global
  `~/.claude/rules/core-invariants.md` §5. **One of the four lives outside this repo**, so any
  in-repo mechanism covers three of four at best and would report GREEN while the global rule
  disagreed — a check whose green is narrower than its subject is worse than no check, because
  it reads as coverage. The enum's own governing clause already supplies the real control: a
  new member enters ONLY via a recorded ruling (this register), which is a human gate on the
  one event that can create the drift. Witnessed instance — `automation/` entered the code and
  the B5 register while all four sites still said "three" (repaired 2026-08-07, CLAUDE.md §12
  v2.52/v2.53) — was caught by a human spot-check and closed in one day. **Revisit if:** the
  global site is hub-owned (`[#289]`), at which point a four-of-four check becomes possible and
  this ruling expires. Discharges `[#508]`'s Done-when ruling branch. Ruled: <ruling locator>.
```

Commit message:

```
docs(rulings): [#508] the lane-prefix enum cardinality stays deliberately unmechanized

Takes the row's OWN Done-when ruling branch: "or a ruling records it deliberately unmechanized
with its reason". Reason recorded at STANDING_RULINGS B<n>: one of the four prose sites is
`~/.claude/rules/core-invariants.md` §5, outside this repo, so an in-repo check covers 3 of 4
and its green would be narrower than its subject.

The underlying drift is ABSENT at HEAD — LANE_PREFIXES cardinality 4 (`validate_branch_naming.py:75`),
`CLAUDE.md` §4 and `CONTRIBUTING.md` both say four. Nothing is being papered over.

Expiry named: revisit if [#289] hub-owns the global rule.
Closes [#508]
```

**Watch:** closing the row is a **two-file act** — set `status:` in `tasks/508-*.md` **and**
regenerate (`gen_task_tree.py`), then confirm the row leaves `BACKLOG.md`. The commit-msg hook
`backlog-id-on-close` requires the bracketed `[#508]` form, not a bare `#508`.

### Block 4 — the K-4 supersession-pointer register line

> **DRAFT — applies only under the corresponding checklist ruling**
> (`2026-08-10-technical-decision-sheet-verification.md` "Needs a ruling" #2: whether the
> superseded decision sheet earns a supersession pointer, given it is immutable and its K-4 row
> still reads as a kill recommendation). **The substantive call is already made and is NOT
> reopened here:** `9a7ffcb4` ruled `[#310]` stays open, and K-4's rationale was REFUTED at
> `9fc1a8b4` (2026-07-21) — the escape premise is false; `validate_residual_completeness.py:33-35`
> is prospective-only and grandfathers the 07-05 bundle (8 `(fill:` live). This block only
> records that the *sheet* is superseded on that row.

Register line for `protocols/STANDING_RULINGS.md`:

```
- **B<n> (2026-08-10) — `docs/audits/2026-08-09-technical-decision-sheet.md` is SUPERSEDED on
  its K-4 row; the file is not edited.** The sheet recommends *"KILL `[#310]` via its own escape
  clause"* on the premise that `#292`'s closure satisfies the escape. **That premise was refuted
  on 2026-07-21 at `9fc1a8b4`, seven weeks before the sheet was written** — the closure fact is
  true, the escape inference is false, and `validate_residual_completeness.py:33-35` is
  prospective-only, so the 07-05 bundle stays grandfathered with 8 `(fill:` markers live.
  `9a7ffcb4` ruled the row STAYS OPEN. Audits are immutable (CLAUDE.md §5 rule 3), so the sheet
  is not corrected in place; this register entry is the supersession pointer, and it is the
  surface a reader hits before acting on that row. The refutation's full working:
  `docs/audits/2026-08-10-technical-decision-sheet-verification.md` §1 and §3. **Nothing else in
  the sheet is superseded** — K-1/K-2/K-3 hold. Ruled: <ruling locator>.
```

Commit message:

```
docs(rulings): supersession pointer for the 2026-08-09 decision sheet's K-4 row

The sheet's K-4 kill rationale rests on a premise refuted at `9fc1a8b4` (2026-07-21), seven
weeks before the sheet was written; `9a7ffcb4` already ruled [#310] stays open. Audits are
immutable, so the sheet is untouched and the pointer lives in the ruling register — where a
reader meets it before acting on the row.

Scope: K-4 only. K-1/K-2/K-3 are unaffected. No row status changes; [#310] stays as ruled.
kill-candidates: none — this records a supersession, it files nothing
```

**Watch:** do **not** edit `docs/audits/2026-08-09-technical-decision-sheet.md`. The
`block_immutable_edits.py` `PreToolUse` guard is fail-closed on transcripts; audits are immutable
by CLAUDE.md §5 rule 3 whether or not a guard catches the specific path.

---

## Packet

**Sheets:** 6 of 6 done — `[#270]` (+3 dependents named and verified in-row) · `[#514]` (with the
`LANE_BRANCH_RE`/ADR-110 interaction measured from the regex pair, not carried) · `[#502]` · the
3b-3 kill-candidates gap (no row; gap described with four measured refusal holes and the
counter-evidence that the mechanism has worked once) · the ARC-6 carry-forward defect · the ARC-7
§6-item-3 site.

**Matrix:** 6×6 pairwise, generated files factored out and named separately. **4 OVERLAP cells, 2
UNCERTAIN cells, 9 DISJOINT.** The load-bearing findings are that `BACKLOG.md` /
`tasks/manifest.json` / `ecosystem/doc-counts.md` make **no** two row-touching lanes truly
disjoint (resolve-by-regeneration is the precedent, ARC-5 `19aca464`), that **D and F cannot be
separate lanes** (both re-stamp `CLAUDE.md`, and `canonical_freshness` wedges a **pre-commit**
gate), and that **`[#510]` collides with `[#514]` inside `scripts/batch_manifest.py`**.

**Skeletons:** 6 — one per sheet, each with a purpose, a mechanically-phrased candidate Done-when,
a steps outline, and V-2 decision-budget stubs.

**Feature-class verdict (F24-2):** **not zero, but thin, and the thinness is the finding.** Top 3:
`[#270]` · `[#132]` · `[#171]`. Mechanical anchors: 5 open rows in the `[P1-3][L]` new-feature-epic
band the repo's own hook defines; 24 open rows cite an intake; 78% of open Done-whens are prose
predicates (census §4). The `[#490]`-class successor is `[#383]` (P2/L, 1 of 6 waves executed).
Consumer-repo work is a real 17+-row cohort and is the census's highest-yield untested cohort —
**and it cannot be run from a cloud lane.**

**Batched questions for the architect** (none blocked this lane; each is a GO-day input):

1. **`[#502]` — has the `mutation-pilot` job run since `27c37ae3`?** Not answerable from this
   seat. It decides whether the row is a 10-minute close or a lane, and it is the only UNCERTAIN
   in this report that changes a scheduling decision.
2. **Does any batch-4 lane own `ARCHITECTURE.md`?** Three of six subjects plausibly edit it, and
   the file carries 14 checkably-FALSE claims under a current review stamp (Fable High #1). A
   blanket "no lane edits `ARCHITECTURE.md`" is the cleanest cut if the re-read is not in scope.
3. **`[#514]` leg 3 — which batch discharges *"one clean batch runs under it"*?** If it is batch 4,
   the fix must land before integration or the row cannot close in-batch.
4. **Does 3b-3 earn a birth?** It has no row. Filing one costs a `kill-candidates:` line on its
   own filing commit — which is the gate under review.
5. **`[#310]` is `deferred` (peg `post-Wave-1`).** Any lane taking the ARC-6 carry-forward needs
   an un-defer first, and the defect is **not** inside `[#310]`'s Done-when.

**Posture at STOP:** read-only honoured. Nothing born, nothing closed, no row / intake / ADR /
`BACKLOG.md` edited; no merge, no push, no `SKIP=`, no `--no-verify`. This report and the
regenerated `docs/audits/README.md` index line are the lane's only writes. No JOURNAL entry — a
batch lane never journals; the integrator does.
