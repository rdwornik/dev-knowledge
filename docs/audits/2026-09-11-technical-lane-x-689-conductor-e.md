# Lane `lane-x-689-conductor-e` — end-of-lane artifact

**Consumers:** `[#689]` · `[#669]` · `[#692]` · `[#716]` · `[#717]` · ADR-101 · intake #93

**Lane:** `lane-x-689-conductor-e` (batch X wave 1, slot X1-2) · branch
`worktree-lane-x-689-conductor-e` · mode `execute`, effort `high`, model `opus` ·
contract `docs/audits/2026-09-11-technical-batch-x-launch-contracts/LANE-x-689-conductor-e.md`

**Immutable artifact** (ADR-101 / CLAUDE.md §5 rule 3). Supersede with a new file; never edit
in place.

---

## 1 · What changed

Five commits, on `worktree-lane-x-689-conductor-e`, each one gate-clean:

```
6b55f177  docs  the carried AX clauses and the three live §7 verdicts, written into [#689]
8b028a0b  feat  the `· phase:` clause and its closed enum, RED-first
e7381b49  feat  the Actions runner, the phase gate, and the required-check ruleset
35f54acb  feat  the SessionStart surface and the AX3-2 floor declaration
<this>    docs  this artifact
```

Files added:

```
.github/workflows/conductor.yml                  253 lines   the runner
scripts/conductor.py                             ~560 lines  the phase table, the gate,
                                                             the §6 numbers, the boot surface
deploy/conductor-required-checks.ruleset.json      26 lines   the ruleset, as a pure payload
tests/test_conductor.py                           35 tests    the RED-first witnesses
```

Files changed:

```
scripts/validate_backlog.py          the `· phase:` clause, its closed enum, phase_census
tests/test_validate_backlog.py       7 more witnesses (15 collected)
tasks/689-...md                      the carried clauses, the §7 verdicts, the footprint,
                                     and the first live `· phase: build`
.claude/settings.json                one appended SessionStart entry
deploy/manifest-v1.5.0.yaml          carrier `conductor` + 2 components (AX3-2)
.claude/methodology-roster.md         regenerated (driven by the manifest edit)
ecosystem/doc-counts.md              regenerated (the collected-test count moved twice)
```

### The three build legs of §8

**Leg 2 — `phase:` field + validator.** A BODY clause, `· phase: <stage>`, not a frontmatter
key. `gen_task_tree.py` DERIVES frontmatter from the body and `find_incoherences` refuses a
file whose frontmatter disagrees with it, so a hand-added frontmatter key would be overwritten
or refused; making it a derived key means editing `render_task_file` and re-rendering all 456
task files. The body clause is also the only shape `validate_backlog` can see — since `[#589]`
it reads the reassembled body, never the frontmatter — and it matches the three machine-read
clauses already in use (`· depends-on:`, `· serialize-group:`, `· review_date=`).

The enum is the operator's own delivery spine, carried verbatim from the header of
`to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md`: intake, task, build, review, merge, docs,
deploy, telemetry, archive. Order is pinned by a test, because the gate reads the index to
answer "which stage comes next".

**Absence is legal**, for two measured reasons rather than as a soft default: a mandatory
clause would demand a mass edit of all 311 live rows, and it would break
`tests/test_validate_backlog_twin_parity.py` — this validator is the ADR-78 plugin floor twin,
the shared fixtures carry no phase clause, and the twin has no phase check, so the hub would
invent findings the twin cannot produce. Adoption is therefore MEASURED, by the `unphased`
bucket, not mandated. Baseline: **1 of 311 rows phased** (`[#689]` itself, at `build`).

**Leg 1 — `conductor.yml` + ruleset.** The workflow carries §4's four triggers verbatim. The
phase table is NOT in it: §4 says the phase table is "the only custom content", and a gate
written in workflow shell is a gate no local test can exercise, so the process lives in
`scripts/conductor.py` and the workflow is a runner. Six jobs: `pytest`, `ruff`, `seal`,
`terra`, `phase-gate`, `metrics` (the last two in one job).

The gate has real teeth on three stages and states its reason on the other six. `archive`
FAILS a row whose body is still live in `tasks/`; `intake` FAILS a row citing no
`docs/intake/` file or citing one that does not exist; `task` FAILS a row with no body file.
The other six print why no committed artefact distinguishes them — the `window_metrics`
NOT-COMPUTED-with-a-reason discipline applied to a gate. An anti-gap test asserts every enum
member sits in one bucket or the other, and it earned its keep on the first run by catching
`merge`, which was silently in neither.

**Leg 3 — the SessionStart hook.** `scripts/conductor.py session-start`, wired as a fifth
SessionStart entry. A subcommand rather than a new script: one organ, one test file, one wiring
surface. Live on this tree: `runs: none readable` (correct — the workflow is not on `main`
yet), `phase gate: 0 FAIL, 1 of 311 rows phased`, `awaits your word: nothing from the phase
gate`. `process-list` now reports **159 processes / 120 triggered** (was 158 / 119), so the new
organ is registered AND triggered rather than an orphan.

### AX3-2 / AX4-1

Carrier `conductor` (order 9) plus components `conductor-workflow` and
`conductor-required-checks`, both `waivable: false` — which is what AX4-1's `floor: MUST`
means in this schema. `release_lint --version v1.5.0`: **0 FAIL, 1 WARN, 7 pass**, the WARN
being the pre-existing `C2-tag` state the manifest header predicts.

DECLARATION-ONLY (`implemented: false`), on the `editor-config` / `boot-inversion` precedent,
because `to-browser/RATIFICATION-2026-09-11.md` rules *"No harness deployment to corp-monorepo
until batch X's waves are done"*. A write-through carrier today would execute a deployment the
operator deferred.

The **AX4-1 parity-registry row is NOT written by this lane**, deliberately: AX4-1 names
`decision_coverage` (X1-1) as the clause's owner, and AX12-1 bars a lane from editing a surface
another row owns. The disposition is recorded in `[#689]`'s body; the registry row is owed by
X1-1 and is item 5 of §4 below.

---

## 2 · §7's three preconditions — the verdicts, read live at `0be08b3c`

**P1 · GitHub plan + required checks — PASS.** `gh api user` returns `plan: pro`
(`private_repos: 9999`). `gh api repos/rdwornik/dev-knowledge/rulesets` returns `[]` at HTTP
200, not the 403 `to-cc/AMEND-CONDUCTOR-DECISION-001.md` §1 measured on Free.

D2's locator in the row and in the batch manifest is **stale, and is resolved rather than
amended**: the 1,097 B duplicate both cite as `to-browser/RATIFICATION-2026-09-10 (1).md` no
longer exists under that name. The same 1,097 B file is now
`to-browser/RATIFICATION-2026-09-10-architect.md` and carries D2 unchanged — *"D2 · GitHub Pro
— YES (~$4/month, account rdwornik) … Purpose: required checks as the merge gate for conductor
E (GitHub Actions)"*. Same byte count, same D-numbering. The 4,332 B
`to-browser/RATIFICATION-2026-09-10.md` still lists GitHub Pro under NOT RATIFIED, exactly as
the row says.

**P2 · Actions minutes quota — PASS.** The endpoint the amendment used
(`users/{u}/settings/billing/actions`) is now HTTP 410. `users/rdwornik/settings/billing/usage`
reports **1,192 Actions minutes for September 2026**, all on `dev-knowledge`, `netAmount` 0 —
against Pro's 3,000/month, 1,808 of headroom.

**P3 · `/install-github-app` on the hub repo — NOT MET, and it gates no leg of this
Done-contract.** `gh api repos/rdwornik/dev-knowledge/actions/secrets` returns an EMPTY list
and `actions/workflows` lists only `report-only-wall.yml` plus the Codespaces prebuild, so the
app has never been installed here. This is not a refuted premise:
AMEND-CONDUCTOR-DECISION-001 §1 already recorded it as *"not yet reported"*. What it gates is
§4's LANE-EXECUTOR leg (`claude-code-action` reading a task file and opening the PR). §8's
build is *"1. `conductor.yml` + ruleset. 2. `phase:` field + validator. 3. SessionStart
hook"* — none of the three names the app, and all three are built here with zero dependency on
it. It is an interactive operator act no lane can perform, so it is item 1 of §4 below rather
than a PAUSE against a leg it does not block.

---

## 3 · The findings — what the lane could not decide, and why

### F1 · Arming required checks on `main` and this repo's landing protocol are mutually exclusive

**This is the decision E's gate leg still owes, and it is the most important line in this
artifact.**

A ruleset's `required_status_checks` rule refuses a direct push whose head commit has no
passing checks. A `--no-ff` merge commit created locally does not exist server-side before the
push, so its checks cannot have run. CLAUDE.md §4, core-invariant #5 and the `block-ff-push`
pre-push hook mandate exactly that local merge. So arming the ruleset against this repo as it
lands today refuses **every** push to `main`, permanently.

Either landing moves to PRs — which is what §4's `pull_request` trigger and its
`claude-code-action` executor both already presuppose — or the gate leg stays report-only.
E's RUNNER leg does not depend on the choice. E's GATE leg IS the choice. It is a functional
question about how the operator lands work, so under ADR-108 §A it is his, not the architect's
and not a lane's.

The ruleset therefore ships as a file at `enforcement: disabled`: applying it is reversible and
inert, and enabling it is one explicit flip. Three further reasons it is not armed live:
AX3-2 makes it a floor component in the deploy manifest, and a manifest ships files rather
than live GitHub state; `.github/workflows/report-only-wall.yml` declares arming a required
check *"a separate, ADR-owing decision on a different plan"* and **no such ADR exists** (only
ADR-101 and ADR-30 mention rulesets or required checks, and neither arms one); and it is
outward-facing live state on the operator's account.

### F2 · The repo is PUBLIC, and three surfaces say it is private

`gh api repos/rdwornik/dev-knowledge` returns `private: false, visibility: public`. Against
that:

- `to-cc/AMEND-CONDUCTOR-DECISION-001.md` §2 declines the public-repo option — *"Public repo:
  no — private, personal"*
- `.github/workflows/report-only-wall.yml` — *"the repo is private on the Free tier, so
  required checks are unavailable"*
- `ecosystem/fleet-shape-spec.yaml`, the `.github` root-allowlist provenance comment —
  *"Report-only (private repo, Free tier), so no gate lives there"*

Reported, not acted on: visibility is the operator's, and Pro makes P1 PASS either way. But
it is the premise under two committed governance claims, and the second of those is the
sentence that has kept `.github/` gate-free.

### F3 · `terra` is a job and cannot be a required check

The Done-contract names four required checks — pytest, ruff, seal, terra. The first three run
and are in the ruleset. `terra` is a job (§4: *"Codex review becomes a job, never a paste"*)
but is deliberately absent from the required set: this repo has **no Actions secrets at all**,
so no provider credential exists, and a required check that can never pass bricks the branch.
The job reports the gap rather than faking a verdict, and a test pins the asymmetry so it is
not later rediscovered as a bug. **3 of 4 contexts armable.** Arming the fourth is two
operator acts: add the credential, then add the context.

### F4 · §5's deletion list yields nine countable organs against a target of ≥ 10

`conductor.py metrics` enumerates §5 as `SECTION_5_ORGANS`, because "organs deleted from the §5
list — target ≥ 10" is uncountable until the list is enumerated. Twelve items; **nine are files
this hub can probe, three are not**: the four `win-tooling` dispatch verbs (a child repo
ADR-28/36 bars Layer 2 from reading), and the dispatcher and integrator SEATS (roles, not
files). So the target **cannot be scored from this repo alone** — it needs the win-tooling
count taken where it lives, or a restatement. Baseline today: **0 of 9 deleted.** Every
non-None probe is asserted to resolve, so a phantom deletion cannot inflate the number.

### F5 · §6's revert condition is not evaluable, and number 1's denominator is the reason

§6: *"If 1 and 3 do not fall, revert to B."* `conductor.py metrics` answers whether that can be
evaluated at all. Today: **NO**.

Number 1 is "phase transitions without operator action ÷ all transitions". The numerator is
real and countable (conductor.yml runs). **The denominator is not instrumented and cannot be
closed from this side**: an operator-performed phase transition leaves no committed record
anywhere. So the ratio §6 asks for is unavailable, and the honest report says so rather than
printing a percentage over a guessed denominator. Number 2 is NOT COMPUTED structurally — no
operator-time clock exists here and corp-monorepo is a child repo. Number 3 IS computed:
**211 pastes in the last 7 days**, in `H:\My Drive\CLAUDE PROMPT DIR\to-cc`, against a target
of `< 5`. The directory is always printed — the E-29 lesson made mechanical, because two live
values of `CLAUDE_PROMPTS_DIR` exist on this machine and a count from an unnamed directory is
an honest instrument returning a confidently wrong answer. Number 5 (the fifth number
AMEND-CONDUCTOR-DECISION-001 §3 added) is computed alongside: 1,192 minutes this month.

### F6 · `pull_request` is vacuous today

Present because §4 names it. The wall's header records why it cannot fire: *"the repo merges
locally with --no-ff and pushes, so a PR-triggered organ would never fire — the `[#255]`
vacuity that retired the last `.github/` organ."* It goes live the day F1 is decided toward
PRs, and not before.

### F7 · Three wave-1 lanes write `.claude/settings.json`, and none declares a serialize-group

The batch manifest's disjointness argument (§"`[#727]` folded into X1-5") compares `[#727]`
against `[#664]` and concludes they are file-disjoint. That pair is disjoint. The **set** is
not:

- **X1-2 / `[#689]`** (this lane) — appends one entry to `hooks.SessionStart[0].hooks`
- **X1-5 / `[#727]`**, riding in `LANE-x-664-delivery-spine` — that contract's Done-contract
  clause 2 says `[#727]` *"touches `.claude/settings.json`"* and adds a `PreToolUse`
  deny-and-point hook
- **W-2′ / `[#684]`** (`LANE-w-684-pretooluse-guard-root-prime`) — Done-contract clause 1 owes
  *"A SessionStart check verifies interpreter + guard script"*, and hardens the existing
  `PreToolUse` prompts-guard; both live in `.claude/settings.json`, though the contract does
  not name the file

`derive_serialize_group` returns `None` for every one of them, which is exactly why the
dispatcher's check bound nothing — fifteen other rows carry `· serialize-group: settings-json`
and these three do not. **This lane and W-2′ both touch the SessionStart array**, so that is
the direct conflict. Mitigation taken here: the edit is a single object appended at the END of
the array, the most conflict-tolerant shape available. It does not prevent the conflict; it
makes it trivial to resolve by keeping both entries.

`deploy/manifest-v1.5.0.yaml` is a second, smaller instance: this lane and
`LANE-x-734-retire-stage` both write it. **A manifest conflict must not be resolved by
regenerating anything** — regenerating a conflicted manifest absorbs the conflict markers into
the output.

---

## 4 · Open items — what this lane hands on

1. **`/install-github-app` on the hub repo** — the one operator act this lane needs and cannot
   perform (interactive OAuth). It gates §4's `claude-code-action` lane-executor leg only, not
   anything built here. **This lane's single operator ask.**
2. **F1 — the landing-protocol decision.** PRs, or the gate leg stays report-only. Functional
   question, ADR-108 §A, the operator's. Whichever way it goes, the ADR
   `report-only-wall.yml` says is owed for arming a required check is still owed.
3. **F2 — repo visibility.** The operator may want to know the repo is public, given he
   declined "public repo" as an option on 2026-09-09. Three committed surfaces need correcting
   either way; none is corrected by this lane, because they are not its footprint.
4. **F3 — the terra credential**, then the `terra` context in the ruleset.
5. **AX4-1's parity-registry row** for the two conductor surfaces — owed by X1-1
   (`decision_coverage`), which AX4-1 names as the clause's owner. Reported here rather than
   written, per AX12-1.
6. **F4 — the ≥ 10 target** needs the win-tooling count taken where it lives, or a
   restatement. `[#734]`'s retire-stage lane is the likeliest place the four dispatch verbs
   actually get deleted.
7. **§6 number 1's denominator** — nothing records an operator-performed phase transition.
   `[#669]`'s transition machine is where that record would come from, which is another reason
   the two rows sit in sequence rather than in one lane.
8. **`ecosystem/organ-index.md` is stale by one row** (`SessionStart: conductor.py`). Left for
   the integrator, who is gate-of-record and regenerates once at the merge (Q1). The
   single-hook bypass was declared in commit `35f54acb`'s body.
9. **`[#717]`** (no `-Model` on the contract gate's dispatch grammar) is untouched and still
   open; this lane's declared and dispatched models agree by construction, so the mismatch
   could not bite it.

Not done, and out of footprint by design: no merge, no push to `main`, no JOURNAL entry (P-1,
the integrator's surface), no index regeneration beyond the two the gates named as their own
fixes.

---

## 5 · Deviations from the frozen contract, each with its reason

1. **`argparse`, not Click**, against Done-contract clause 3's "Click for a CLI where one is
   warranted". Two subcommands and three flags do not warrant it, and repo conventions win:
   every read-only reporter in `scripts/` uses argparse (`window_metrics`, `graph_queries`,
   `file_purpose_graph`), while Click is used where a command group with options earns it
   (`validate_hermetization`, `deploy/release_lint`).
2. **The §6 instrument landed in step 3's commit, not step 4's.** It is the same module as the
   phase gate, and splitting one file across two commits to match the step numbering would
   have left a half-written module in the tree.
3. **The step-0 sync merged local `main`, not `origin/main`.** Local `main` was SEVEN commits
   ahead of `origin/main` — the batch X manifest merge and the six frozen wave-1 contracts,
   this lane's own included. Merging `origin/main` would have been a no-op against a base
   missing this lane's own contract. Exactly the `[#716]` hazard step 0 names.
4. **P3 was recorded as NOT MET and the lane continued**, where step 1 says "If any
   precondition fails, PAUSE with the fact". The fact is disclosed here and in commit
   `6b55f177`; the continuation is argued in §2 above — P3 gates a leg outside this
   Done-contract, was already recorded as unreported by the amendment the contract cites, and
   is an act no lane can perform, so a PAUSE would have delivered nothing and still left the
   operator the same act. Flagged as a deviation rather than presented as compliance.
5. **`ecosystem/organ-index.md` left stale** under a declared `SKIP=organ-index-freshness`,
   per the contract's own "No index regeneration" and its "a lane declares its single-hook
   bypass in the commit body".
6. **CLAUDE.md not edited.** §9's header calls itself "a roster, not a manual" and points at
   the generated organ index, which carries the new row; its "SessionStart surfacing" phrase
   already covers four hooks and now a fifth. The file has 746 bytes of headroom under a hard
   24,576 B cap and is one of the eight A2-gated canonical docs, where an edit demands a
   `last_reviewed` re-stamp that cannot be expressed same-day.

---

## 6 · Verification

```
pytest (targeted)   66 passed   tests/test_validate_backlog.py + twin parity
pytest (targeted)   35 passed   tests/test_conductor.py
pytest (full)       see §7 below
ruff check          clean on every file this lane touched
release_lint        v1.5.0 — 0 FAIL, 1 WARN (pre-existing C2-tag), 7 pass
hermetization       rc=0 with all four adds staged (.github/workflows and deploy/ are both
                    admitted Rule-C homes; .github/rulesets would NOT have been, which is why
                    the ruleset lives in deploy/)
graph               task-coverage OK · orphan-census OK · process-list OK, 159/120 (was 158/119)
validate_backlog    OK, 311 tasks; "phase census — build (1); unphased (310)"
gen_task_tree       --check ok (BACKLOG.md projection byte-unchanged throughout)
```

RED-first witnesses (ADR-108 §B) are quoted in the bodies of `8b028a0b` (5 failed, 1 passed)
and `e7381b49` (2 failed, 26 passed — one a real gap in `conductor.py`, one a test defect).

## 7 · Full-suite result

```
uv run --locked pytest -q --tb=short      58 failed, 5733 passed, 11 skipped in 2132.29s
```

**Two of the 58 are attributable to this lane, and neither is a regression.** The rest are
pre-existing or context artifacts, verified below rather than assumed. The comparison base is
`docs/audits/2026-09-11-technical-w278-ship-gate-baseline.md`, which recorded **33 failed /
5682 passed / 8 skipped** for the full suite taken IN A WORKTREE on the same day, and whose
own "Honest limit" section states that worktree-context failure counts are inflated and not
comparable to a primary-checkout number.

### Attributable to this lane

1. **`test_generate_organ_index.py::test_live_committed_index_is_the_generated_bytes`** —
   DELIBERATE. `ecosystem/organ-index.md` is stale by exactly one row,
   `SessionStart: conductor.py`. This contract's "What NOT to do" reserves index regeneration
   for the integrator, who is gate-of-record and regenerates once at the merge (Q1); the
   single-hook bypass was declared in `35f54acb`'s body. It goes green at integration.
2. **`test_floor_mechanisms.py::test_pre_existing_components_are_untouched_by_the_mechanism_reader`**
   — the test asserts `len(plain) == 21`. **Measured at the merge base `0be08b3c`: 20. It was
   ALREADY RED before this lane touched anything.** At HEAD it is 22, because the two AX3-2
   components landed. So this lane moved the number without causing the failure, and did not
   fix it: re-pinning the assertion to 22 would rubber-stamp a stale count-pin in a test this
   lane does not own, on a manifest that legitimately grows. Left red, reported here.

### Not attributable — verified, not assumed

- **15 × `tests/test_fleet_analytics.py` — `ModuleNotFoundError: No module named 'pandas'`.**
  This run did not pass `--group analytics`; the recorded baseline did. Environment, not tree.
  58 − 15 = 43 comparable failures.
- **`test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar`
  (`88956 < 72000`).** `git diff 0be08b3c..HEAD -- BACKLOG.md` is EMPTY — this lane did not
  change one byte of the view, and it was already 16,956 B over the bar on arrival. The row
  edits moved only the body, and the projection carries id + band + title + pointer, none of
  which changed.
- **`test_normalize_headers.py` × 4, `test_toc.py`, `test_stale_worktrees.py`** — the
  documented worktree artifact. `_SKIP_PARTS` contains `worktrees`, every path in this
  checkout contains that segment, so the live-corpus glob resolves to zero files and the
  tests fail their own plausibility floor ("corpus implausibly small (0)"). Named in the
  baseline's own "Honest limit" section.
- **`test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`**
  — **PASSES when re-run with `-n 0`.** An xdist artifact: an identity assertion on a
  spec-derived constant, which separate workers cannot satisfy.
- **`test_graph_spine.py::test_the_disposition_register_names_no_file_that_is_gone`** — names
  `.claude/commands/override.md`, which `orphan-census` reported as a NOTE on this lane's
  FIRST run, before any edit.
- **`test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers`**
  — false-strips `2026-07-07-allowlist-v1.ps1`, `2026-07-08-emptygrant-v2.ps1` and four
  others. None of the six strings is in anything this lane wrote.
- **`test_gen_north_star.py::test_the_committed_view_is_current`** — the stale diff is
  47 → 77 open rows in scope and three more count blocks; `689` does not appear in it. Many
  rows filed on `main`, none of them this lane's.
- **`test_gen_handoff.py` × 4, `test_handoff_modes.py`, `test_governance_health.py`,
  `test_enforcement_coverage.py`, `test_preflight_freeze_predicates.py`,
  `test_routing_agreement.py`, `test_reverse_dep_oracle.py`, `test_v6_frozen_contract.py`** —
  handoff-bundle probe counts, intake rendering, the pre-push anchor organ's discrimination,
  freeze predicates, the routing table, the reverse-dep oracle and the v6 contract. Three
  were re-run serially and fail for reasons visibly unrelated to this footprint (probe counts
  15 vs 13; "intakes live: resolved but rendered unavailable"; "pre-push organ REFUSED an
  anchored push too"). **The remaining ones were attributed by footprint rather than
  re-measured individually — this is where the evidence stops.** None of them can reach any
  of the eleven files this lane changed.

### The honest headline

`pytest` is NOT green on this tree, and it was not green at the merge base either. What this
lane can claim, and does: **every test covering its own footprint passes** — 66 in
`test_validate_backlog.py` plus the twin-parity pair, 35 in `test_conductor.py`, `ruff` clean,
`release_lint` 0 FAIL. Of the two suite failures this lane's diff touches, one is a declared
deferral to the integrator and one was already red before the lane started. Claiming "pytest
green" against Done-contract clause 3 would be false, so it is not claimed.
