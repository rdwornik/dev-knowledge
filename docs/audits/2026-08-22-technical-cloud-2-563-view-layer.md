# `[#563]` Backlog.md view layer — the build artifact

> **CLOUD-2** (`claude/cloud-2-563-view-layer`), 2026-08-22. Repo-bound cloud lane on
> `.dev-knowledge` at revision `main` = `0360d6d`.
> **This artifact records a BUILD, not a trial and not a verdict.** `[#563]` carries verdict
> `ADOPT-VIEW-LAYER`, ruled 2026-08-19 and marked do-not-reopen; the design was consumed as
> given. Nothing here re-derives it. Source of record for the design:
> `docs/audits/2026-08-19-technical-backlogmd-trial.md`.

**Tally:** 0/5/4/1

---

## 1. What landed

Two added files, both in existing allowlisted homes (ADR-101 Rule C clean):

- `scripts/export_backlog_view.py` — the one-way exporter. A loose top-level module by design
  (mirrors `gen_audit_index.py` / `gen_claude_rosters.py`): no codemap node, no
  `ARCHITECTURE.md` regen on edit, confirmed by running the codemap check.
- `tests/test_export_backlog_view.py` — 37 tests in two tiers: tmp-tree unit tests that pin
  behaviour, and `live_repo`-marked fidelity tests that render THIS repo's 299-file `tasks/`
  tree and check it row for row.

Nothing else in the tree changed. Three shared-file needs are shipped as fenced diffs in §5
rather than edited here, per the lane's contract.

## 2. The Done-when clauses, discharged

`[#563]`'s row names four conditions. Each maps to a named test.

| Clause | How it is discharged | Standing assertion |
|---|---|---|
| writes the `Backlog.md` on-disk format directly from `tasks/` into a gitignored scratch dir | `export()` renders `<export-dir>/backlog/{config.yml,tasks/}` from `tasks/*.md`; default dir `.backlog-view/` | `test_the_project_level_is_where_backlogmd_looks_for_it` |
| re-exports on every invocation | every call wipes and re-renders; the result is a function of `tasks/` alone | `test_re_export_is_byte_identical`, `test_re_export_removes_a_stale_row`, `test_re_export_reflects_a_source_edit` |
| the export path is in `.gitignore`, with a test asserting nothing under it is tracked | the export root is **self-ignoring** — see §3 | `test_nothing_under_the_export_path_is_tracked` |
| `check_active_branches` and `remote_operations` are `false` | both, in both spellings — see §4 | `test_config_disables_branch_checks_and_remote_operations_in_both_spellings` |
| generated with `--agent-instructions none` | honoured structurally: a direct-write exporter has no code path that emits an instruction file | `test_no_instruction_file_is_ever_written` |
| a test asserts no gate, hook or script reads the export | greps the live enforcement surface for the export's own names | `test_no_gate_hook_or_script_reads_the_export` |

The brief's own extra clause — *tests cover generated-view fidelity to `tasks/` source* — is
`test_description_carries_the_source_body_byte_for_byte` (all 299 rows, byte-equal),
`test_every_untyped_clause_survives_verbatim_as_an_implementation_note` and
`test_every_done_when_clause_becomes_an_acceptance_box`. The latter two compare **round-trip
item lists**, not substrings, so a merged or reflowed clause fails rather than hiding inside a
longer match; both carry a coverage floor assertion so a corpus change cannot quietly make
them vacuous.

## 3. The one design decision this lane had to make

The row says *"the export path is in `.gitignore`"*, and this lane may not edit `.gitignore`
(shared file). Rather than ship a test that fails until an operator applies a diff, the
exporter writes a `.gitignore` containing `*` **at the export root, as the first file of every
export**. That ignores every file beneath it including itself, so:

- `git status` shows nothing — verified live, and asserted by the standing test;
- `git check-ignore` returns 0 for the first and last file of the export;
- nothing under the path can become tracked, with **no shared-file edit at all**;
- the same property holds for a sibling export dir outside the repo, which the trial named as
  the other sanctioned location.

The root-`.gitignore` entry is still shipped as a fenced diff (§5.1) as belt-and-braces and
because the row's literal wording names it. It is not load-bearing for the test.

**Why `.backlog-view/` and not `backlog/`:** the trial ruled `backlog/` must never land in the
repo, and ADR-101 Rule C would refuse the new top-level home. Nothing under `.backlog-view/`
is ever staged, so the hermetization gate never sees it either.

## 4. Measurements, made rather than carried

| Measurement | This tree, 2026-08-22 | Trial, 2026-08-19 |
|---|---|---|
| task files exported | 299 | 288 |
| status distribution | 190 open / 24 deferred / 81 closed / 3 retired / 1 superseded | 188 / 24 / 72 / 3 / 1 |
| export wall-clock | 0.19 s (0.6 ms/row) | 1.11 s (3.9 ms/row) |
| rows carrying clauses with no typed field | 279 | 266 |
| such clauses in total | 664 | 624 |
| longest emitted relative path | 122 chars | — |

Two of these need a word, because a number that disagrees with a ruled artifact is worth
explaining rather than quietly restating:

**The clause counts are reproduced, and reproducing them fixed the mapping.** The trial's
prototype source is not in the artifact, so the segmentation rule had to be re-derived. Two
candidate rules were measured against the live corpus: consuming `Done when:`, `refs`,
`serialize-group:` and `depends-on:` as typed gives 469 clauses across 264 rows; consuming
only `Done when:` and `refs` gives **664 across 279**, which scales from the trial's 624/266
at 288 rows almost exactly. The second rule was adopted on that evidence. It is also the more
lossless of the two: `serialize-group` and `depends-on` reach the view as typed fields *and*
their clause text still rides along verbatim.

**The export is ~6× faster than the prototype**, which is a measurement of this machine and
this implementation, not a claim about the prototype. The row's `~1.1 s` is not a target.

**MAX_PATH is not close.** The trial measured the CLI's 170-char title cliff as plain
MAX_PATH. The longest path this exporter emits is 122 characters relative to the project root,
so even from the trial's 74-char root the total is 196 — 64 under the 260 limit, and the slug
is truncated at 80 chars regardless because `id:` is authoritative.

**`config.yml` carries both spellings of the two flags, deliberately.** `[#563]` names them
snake_case and that wording is binding; the trial observed the live file using camelCase
(`checkActiveBranches`/`remoteOperations`). Unknown keys are inert, so emitting the pair
guarantees the mitigation binds whichever spelling the reader looks for. A snake_case-only
file would satisfy the row's letter while potentially leaving the ~2.8 s of git chatter the
flags exist to remove.

## 5. Shared-file needs — fenced diffs, not edits

### 5.1 `.gitignore` — belt-and-braces export-path entry

Not load-bearing (§3), but it matches the row's literal wording and costs nothing.

```diff
--- a/.gitignore
+++ b/.gitignore
@@
 # Personal scratch / temp work (unrelated to repo content)
 temp/
+
+# [#563] one-way Backlog.md view layer — disposable, regenerated per read, never committed.
+# BELT-AND-BRACES ONLY: scripts/export_backlog_view.py writes a `.gitignore` containing `*`
+# at the export root as the first file of every export, so the tree is already self-ignoring
+# with or without this entry (and so is a sibling export dir outside the repo).
+.backlog-view/
```

### 5.2 `protocols/STANDING_RULINGS.md` — N-2 gains its third landed site

`audit.py health` surfaced standing ruling **N-2** (`yaml.safe_load` frontmatter readers,
2026-08-03) during this lane. The exporter's first draft hand-rolled a regex frontmatter
reader — the exact class N-2 exists to end. It was migrated to `yaml.safe_load` rather than
diverged from silently (`pyyaml` is already a declared dev dependency). The register's
`landed` block should name the new site so the predicate checks it:

```diff
--- a/protocols/STANDING_RULINGS.md
+++ b/protocols/STANDING_RULINGS.md
@@ -1693,6 +1693,7 @@
 ```landed
 site: scripts/gen_intake_index.py | pattern: yaml\.safe_load
 site: scripts/gen_claude_rosters.py | pattern: yaml\.safe_load
+site: scripts/export_backlog_view.py | pattern: yaml\.safe_load
 ```
```

### 5.3 `ecosystem/doc-counts.md` — the `pytest_collected` claim moves 3372 → 3403

Measured, not estimated: `pytest --collect-only -q` reports **3403** with this lane's 31 tests
(the file's committed value is 3372; 3372 + 31 = 3403). **Deliberately not edited here.** The
value is a whole-tree function, so any concurrent lane that adds a test invalidates whatever
this lane would write — this is a collision file whose row is owed to the integrator, on the
v2.57 / v2.60 precedent. `doc_claims` is WARN-tier and the WARN is what keeps the debt visible.

Regenerate at integration rather than applying a hand diff:

```
python scripts/gen_doc_counts.py --write
```

## 6. Review — what ran, and what could not

**Terra could not run in this container, and no substitute is presented as terra.** The
`/codex-review` path needs the `codex` CLI plus the hub wrapper; this container has neither
(`which codex` → nothing; no `~/.claude/bin/`, no `~/.codex/`). A `gpt-5.6-terra` review of
this diff is therefore **owed and unrun** — it should be run pre-merge on a host that has the
wrapper. What ran instead, and is what the tally below counts:

1. **An adversarial code review of the staged diff at high effort**, which exercised the
   exporter against the live 299-file tree and cross-checked it against the trial artifact.
2. **The full test suite**, which caught a defect the review did not (§6.1, H-1).

### 6.1 Findings and dispositions — all fixed

| # | Sev | Finding | Disposition |
|---|---|---|---|
| H-1 | High | Every `write_text` in `scripts/` must pin `newline="\n"` — `tests/test_generator_newlines.py::test_every_text_write_in_scripts_pins_newline` was red. Windows text mode would have emitted CRLF and broken byte-comparison with the LF source. **Found by the suite, not the review.** | Fixed: all writes go through one `_write` helper that pins the newline. Regression: `test_every_write_pins_the_newline` |
| H-2 | High | Export layout omitted the `backlog/` project level, so `backlog browser` finds no project — the view was unopenable by the tool it exists to feed | Fixed: `PROJECT_SUBDIR`; `config.yml` and `tasks/` now sit under `<export-dir>/backlog/`. Regression: `test_the_project_level_is_where_backlogmd_looks_for_it` |
| H-3 | High | `test_nothing_under_the_export_path_is_tracked` passed **only because a prior manual export had left `.backlog-view/.gitignore` behind**. On a clean checkout nothing ignores the probe and `git check-ignore` returns 1 — a false green | Fixed: the test performs a real export at the shipped default path, then removes the directory if it created it (Critical Rule #9). Re-verified after `rm -rf .backlog-view` |
| H-4 | High | The governance grep `rglob`s `.claude/`, descending into `.claude/worktrees/<lane>/` full checkouts — each holds a second copy of the exporter, so the test reds whenever a parallel lane is live. A guard that misreports is worse than none | Fixed: `_SKIPPED_DIRS` excludes `.claude/worktrees`, `node_modules`, `.git`; a floor assertion keeps the sweep from becoming vacuous |
| H-5 | High | Multi-line clauses (4 live rows: `[#452]`, `[#480]`, `[#489]`, `[#498]`) rendered as one `- {note}`; continuations escaped the list, and a continuation opening `## ` would inject a heading that truncates `## Description` for every downstream reader | Fixed: `render_item`/`dedent_item` fold continuations into the item; the live fidelity tests now round-trip through `dedent_item`. Regression: `test_a_multi_line_clause_stays_inside_its_list_item` |
| M-1 | Medium | A mistyped `--tasks-dir` yielded 0 rows, still wiped the export dir, and exited 0 — a silent replacement of the view by nothing | Fixed: `load_tasks` refuses a missing dir or an empty result, and runs **before** the wipe. Regression: `test_an_empty_or_mistyped_source_is_refused_before_the_wipe` |
| M-2 | Medium | `.gitignore` was written after `mkdir` + marker, so an interrupted run left an unignored file dirtying `git status` — the exact failure the design exists to rule out | Fixed: the ignore rule is the first file written. Regression: `test_the_ignore_rule_is_the_first_file_written` |
| M-3 | Medium | `parse_frontmatter` searched the whole file `re.MULTILINE`, so a body line opening `depends-on:` would be read as frontmatter when the real key is absent, fabricating a `dependencies:` id | Fixed: reads are bounded to the frontmatter block (and the reader itself was then replaced — M-4) |
| M-4 | Medium | The hand-rolled regex frontmatter reader diverged from standing ruling **N-2**. Surfaced by `audit.py health`, not by the review | Fixed: migrated to `yaml.safe_load`. Register diff at §5.2 |
| L-1 | Low | The module docstring cited this artifact before it existed | Resolved by this file |

No Critical findings. Every High and Medium is fixed in the committed diff, each with a named
regression test; the mutation checks in §7 confirm those tests fail when the fix is reverted.

### 6.2 Honest limits, carried in the code

- `test_no_gate_hook_or_script_reads_the_export` greps for the export's own names (path,
  module, marker) — the real re-pointing risk. It cannot see a gate that shells out to the
  `backlog` CLI with a path assembled at runtime. Stated in the test's docstring.
- Acceptance boxes are **never pre-ticked**. `status:` carries state; Backlog.md computes
  completion against a status it recognises as terminal, and the five-value enum contains no
  such status (the trial's `Completion: 0%`). A tick would assert something the tool cannot
  mean.
- The exporter reads the **frontmatter**, not the body, because `derive_status` yields only
  open/deferred — reading the body would render all 85 terminal rows as `open`. Frontmatter is
  gate-verified against the body by `gen_task_tree --check` for every derivable key.

## 7. Gate evidence — hand-run, and why

**uv-pin caveat, declared.** `pyproject.toml` pins `required-version = "==0.11.19"`; this
container carries uv **0.8.17**, so every `uv run --locked` hook entry refuses before doing
anything (`error: Required uv version ==0.11.19 does not match the running version 0.8.17`).
No git hooks are installed in this container either (`.git/hooks/` holds only samples), so
`git commit` runs no gate. Every applicable gate was therefore **run by hand**, exactly as the
R4 precedent directs, against a hand-built venv: `/usr/bin/python3.12` + the `dev` dependency
group installed from PyPI (`pytest 9.1.1`, `ruff 0.15.5` — the exact pin — `pyyaml`, `click`,
`rich`, `pydantic`, `packaging`, `markdown-it-py`, `pytest-xdist`). The repo's own `python3` is
3.11.15, below the `requires-python = ">=3.12"` floor, so it was not used.

| Gate | Verdict |
|---|---|
| `ruff check` (0.15.5, the exact pin) | **PASS** — clean on both files |
| `pytest tests/test_export_backlog_view.py` | **PASS** — 37 passed |
| `codemap-freshness` (`scripts.codemap.cli check . --source-root scripts`) | **PASS** — the loose top-level module adds no node |
| `tests/test_generator_newlines.py` | **PASS** (was RED before H-1; see below) |
| `audit.py health` | rc=0, `DEGRADED` — **pre-existing**, and the same before this diff |
| full suite (`pytest -q`, 3403 collected) | **38 failed / 3354 passed** → after the H-1 fix, **37 failed**, which is exactly the baseline |
| `validate-hermetization` | n/a by inspection — both adds are in existing allowlisted homes (`scripts/`, `tests/`); this artifact's name conforms to the ADR-101 R3/R4 grammar (`YYYY-MM-DD-technical-<kebab-slug>.md`) |
| `backlog-id-on-close` / `backlog-filing-backpressure` | n/a — this commit removes no BACKLOG task line and adds no new task id |
| `block-commit-on-main` / `block-ff-push` / `block-unanchored-push` | n/a — committed on a session branch; this lane never pushes and never merges |
| spine-walking instruments (`validate_git_backlog` and kin) | **SKIPPED** per the lane's shallow guard — `git rev-parse --is-shallow-repository` is `true` |

**The baseline was measured, not assumed.** The 38 full-suite failures were re-run with this
lane's two files moved out of the tree: **37 failed**. Bisecting the tree-sensitive modules
both ways named the single difference —
`tests/test_generator_newlines.py::test_every_text_write_in_scripts_pins_newline`, finding H-1.
After the fix, the failing set is identical to the baseline: 17 `test_fleet_analytics` (pandas
absent — the `analytics` group is not installed), 5 `test_reverse_dep_oracle` + 1
`test_safe_remove` (Pyright / `node_modules` absent), 5 `test_audit`, 3
`test_telemetry_wiring`, and 6 singletons, all of them shallow-clone or missing-sibling-repo
artifacts of this container. **This lane introduces zero new failures.**

`audit.py health` reads `DEGRADED` for the same environmental reasons, including
`[!!] journal_spine_anchor: ... not a valid object name` — a truncated-history artifact of the
shallow clone, which is precisely what the lane's shallow guard anticipates. It exits 0, so the
`audit-health` gate does not block.

**Mutation checks — the tests were shown to fire, not merely to pass.** Six defects were
planted and each was caught by the intended assertion: truncating `## Description`
(fidelity test red), dropping a note (clause-survival red), removing the wipe (stale-row red),
writing outside the export dir (containment red), planting a `.backlog-view` reference in
`config/` (condition-3 red), and reverting the newline pin (`test_generator_newlines` red).
All were reverted; `git status` is clean of them.

## 8. Residuals

1. **A `gpt-5.6-terra` review of this diff is owed** — unrunnable in this container (§6). Run
   it pre-merge on a host carrying the wrapper.
2. **Three fenced diffs await an operator or the integrator** (§5): `.gitignore` (optional),
   `protocols/STANDING_RULINGS.md` N-2 (should land — it keeps the predicate honest), and
   `ecosystem/doc-counts.md` (regenerate at integration, do not hand-apply).
3. **No `[#563]` closure is proposed here.** This lane builds; the Tier-1 closure loop rules.
