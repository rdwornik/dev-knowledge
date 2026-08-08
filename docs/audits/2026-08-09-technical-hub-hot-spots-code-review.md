# Structural code review — the hub's hot spots (NIGHT LANE N4)

**Date:** 2026-08-09
**Branch:** `claude/new-session-ljw038`
**HEAD:** `9e4b294c` (base = `origin/main`; this branch adds only this artifact)
**Scope:** `scripts/audit.py` · `scripts/gitenv.py` + consumers · the handoff engine · the validator family · `deploy/` carriers · the generators
**Mode:** structural review, read-only — **no code, config, or test was changed**
**Tally:** 0/3/5/4 <!-- Critical/High/Medium/Low, counted from §2. Machine-readable per `audit._REVIEW_TALLY_RE`. -->

**Review profile:** code
**Reviewer lane:** **NOT REACHABLE — no reviewer lane ran.** See §0.
**Orchestration:** opus main thread (every severity judgment, every ranking); six sonnet retrieval subagents (structural facts + locators only, one module family each; none assigned severity).

---

## 0. Reviewer lane — not reachable, not simulated

**No codex or terra review was run, and none is reported below.** Measured in this runtime:

- `which codex` / `which terra` → not found; no reviewer binary on `PATH` (`compgen -c | grep -iE '^(codex|terra|gemini|aider)'` → empty).
- No reviewer credentials in the environment (`env | grep -icE 'OPENAI|CODEX|TERRA|XAI|GROK'` → 0).
- Outbound reviewer endpoints unreachable: `curl --max-time 8 https://api.openai.com/v1/models` → `000`.

The repo's `codex/` directory holds `AGENTS.md` (the reviewer's *config*, deployed by
`deploy/carrier_globalconfig.py`), not a runnable lane. Every "terra pass-N" commit in today's
history was produced from the operator's local runtime, not from a cloud container like this one.

This artifact is therefore **deliberately not titled `# Codex Review`** — that title is
`audit._REVIEW_TITLE_RE`'s marker for a reviewer-lane artifact, and claiming it here would
manufacture exactly the unfalsifiable evidence `check_review_artifact_coverage` exists to prevent
(`scripts/audit.py:4022-4028`). The tally below is a **first-party** tally.

## 1. What this runtime could and could not execute — read this before trusting a negative

The gate mesh **did not run here**, so no finding below is backed by a gate result:

- `uv` is `0.8.17`; `pyproject.toml [tool.uv]` pins `required-version = "==0.11.19"` (ADR-106).
  **Every** hook entry and the CI legs invoke `uv run --locked`, so all of them fail with a
  version error before doing any work. `uv run --locked python -c "print('ok')"` → refused.
- System Python is 3.11.15 against a `.python-version` of `3.12.10`, and lacks `click`/`pytest`
  — `import audit` fails at `scripts/audit.py:48`.
- `.git/hooks/pre-commit` and `.git/hooks/pre-push` do not exist in this container (fresh clone,
  `arm_hooks.py` never ran).

So: **`pytest` did not run, `audit.py health` did not run, no hook fired.** Findings are static
analysis plus *targeted empirical reproduction* using system `git` 2.43.0 and system Python —
where I reproduced something, I say so and give the observation. This is an environment fact, not
a repo defect; CI pins uv correctly and even greps `pyproject.toml` to assert the pin has not
moved (`.github/workflows/report-only-wall.yml:105-106`). It is, however, the exact class
**[#453]** ("Cloud night-run runbook — the container gaps that silently degrade an unattended
session") was opened for, and it is now measured rather than suspected.

---

## 2. Findings

### F1 · HIGH · `scripts/audit.py:2998-3004` — `_git` runs unscrubbed, and it feeds the ratchet gate's baseline read

`_git` passes `cwd=str(repo_path)` and **no `env=`**, while the same file imports `gitenv` at
module level (`scripts/audit.py:62-65`) and already aliases `_git_location_env` at
`scripts/audit.py:1952`. The scrub is present in the file and simply not applied here.

**Reproduced, not theorised.** Two temp repos, `GIT_DIR` pointed at A:

```
GIT_DIR=A/.git git -C B rev-parse --show-toplevel   ->  .../B      (the LABEL says B)
GIT_DIR=A/.git git -C B log -1 --format=%s          ->  "A root"   (the ANSWER is from A)
```

That is precisely `gitenv.py`'s stated failure mode — "reads the PARENT's repo while labelling the
answer with the target's id" — now confirmed on this git.

**How the variable actually arrives** (also measured, git 2.43.0). In a *primary* checkout, hooks
see `GIT_DIR=[]` — the vector is inert. In a **linked worktree** it is exported, absolute:

```
worktree pre-commit hook sees:
  GIT_DIR=[/…/A/.git/worktrees/A-wt]  GIT_INDEX_FILE=[/…/A/.git/worktrees/A-wt/index]
```

This repo runs its lanes in worktrees (`worktree-lane-*`, `worktree_seed.py`, `EnterWorktree`), so
every commit- and push-time organ firing inside a lane runs with an inherited absolute `GIT_DIR`.

**What breaks in practice.** Six call sites, all of which pass an explicit `repo_path` and claim
their answer is about it:

- `scripts/audit.py:3064`, `:3072`, `:3078` — `_ref_baseline_state` reads
  `ecosystem/silent-rule-baseline.yaml` from the ref. Under an inherited `GIT_DIR` the baseline is
  read from the **wrong repo**, so `check_silent_rule_ratchet` compares a live measurement against
  a foreign baseline. The whole point of `_target_baseline_state`'s careful `unresolved`/`absent`/
  `invalid`/`valid` lattice (`scripts/audit.py:3007-3053`) is that an indeterminate baseline must
  block — but a *confidently wrong* baseline reads as `valid` and sails through.
- `scripts/audit.py:2971-2972` — `_index_worktree_divergence` reports dirtiness for the wrong tree.
- `scripts/audit.py:1048` — `_git_commit_epoch` dates the wrong commit, feeding
  `check_stale_worktrees`.

**Smallest correct fix.** One line: add `env=_gitenv.scrubbed_git_env()` to the `subprocess.run` at
`scripts/audit.py:3001`. The comment block at `scripts/audit.py:1945-1949` enumerates both where the
scrub fires *and* the one path deliberately exempted (`_commit_routine_outputs`, which sets
`GIT_INDEX_FILE` on purpose). `_git` appears in **neither** list — this is an omission, not a
sanctioned exemption.

**Ownership: UNOWNED.** `[#396]` (extract `gitenv.py`) and `[#512]` (scrub `batch_manifest._git`)
are both **closed**; neither covered this helper.

### F2 · HIGH · Two `LANE_BRANCH_RE` constants, same name, different grammar — they disagree on 8 of 11 real merged lane branches

- `scripts/batch_manifest.py:91` — `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`
- `scripts/validate_branch_naming.py:85` — `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`

Same identifier, no import relationship, each file defines its own. The second's acceptance set is
a strict subset of the first's. **Measured against the actual merged branch names in this repo's
history:**

```
branch (real, from git log --merges)          batch_manifest   validate_branch_naming
worktree-lane-280-315-carriers                lane             unknown
worktree-lane-290-floor-teeth                 lane             unknown
worktree-lane-502-pythonpath-measure          lane             unknown
worktree-lane-506-groom-sheet                 lane             unknown
worktree-lane-archival-audit                  lane             unknown
worktree-lane-e-gitenv-scrub                  lane             unknown
worktree-lane-intakes-28-29                   lane             unknown
worktree-lane-wave-closures                   lane             unknown
worktree-lane-a-490-parity-manifest           lane             batch-lane
worktree-lane-b-429-worktree-portability      lane             batch-lane
worktree-lane-c-320-backup                    lane             batch-lane

DISAGREE on 8 of 11.
```

**What breaks in practice.** `batch_manifest.is_lane_merge` (`:251-254`) feeds `exempt()`
(`:257-268`), which feeds `audit.check_journal_spine_anchor` — so the **loose** regex grants the
ADR-85 anchoring exemption to branches the naming validator classifies `unknown` (and
`validate_branch_naming.classify` routes them there *deliberately*, `:186-189`, with a test named
`test_worktree_lane_prefix_with_a_broken_grammar_is_not_waved_through_as_a_plain_worktree`).
Meanwhile `/lane-boot` runs `validate_branch_naming.py --lane …` (`.claude/commands/lane-boot.md:25`)
and exits 1 on the shape 8 of 11 real lanes actually used. Both organs cannot be enforced; the
branch names in history are evidence that the strict one is being bypassed in practice.

**Smallest correct fix.** Not a code fix first — a ruling on which grammar is canonical (§8). Once
ruled, the code change is that one module imports the other's constant so a single definition
exists.

**Ownership: UNOWNED.** `[#508]` ("Couple the lane-prefix enum's cardinality to its prose") is
adjacent but covers *prose-vs-code cardinality*, not this code-vs-code grammar split.

### F3 · HIGH · `deploy/carrier_globalconfig.py:179-195` — the only carrier that writes outside a repo is the one with no path containment

```python
def _target_path(self, target: Any) -> Path:
    name = (target or {}).get("target_filename", DEFAULT_TARGET_NAME)
    return self.user_config_base / name            # :179-181  — unvalidated
...
    tpath.parent.mkdir(parents=True, exist_ok=True)  # :194 — "~/.codex/ — a user dir"
    tpath.write_bytes(source)                        # :195
```

`target_filename` comes straight from the manifest and is joined to `user_config_base` (`~/.codex`)
with no `_safe_rel`, no `_contained`, no `.resolve()` check. A value of `../../.bashrc` writes hub
bytes into the user's home tree. Today's containment fix (commit `295f359`) landed in
`carrier_docs.py` **only**.

Note also `deploy/carrier_globalconfig.py:80` *looks* like a guard and is not: the
`.resolve().relative_to(_HUB_ROOT)` is wrapped in `try/except ValueError` purely to decide whether
to attempt `git show HEAD:<rel>`, and on `ValueError` it falls through to
`source_path.read_bytes()` at `:92` — reading the out-of-tree path anyway.

**Severity note.** The manifest is hub-authored, so this is not attacker-controlled today. It is
rated HIGH on blast radius, not on likelihood: it is the only unguarded write in the tree whose
destination is the user's **home directory** rather than a repo.

**Smallest correct fix.** Reuse the guard that already exists and is already tested — call
`carrier_docs._safe_rel` + `_contained` against `user_config_base`. **Ownership: UNOWNED.**

### F4 · MEDIUM · The containment fix is correct but not generalized — three sibling carriers take manifest paths with no guard and no tests

First, the contract's question, answered: **the fix does resolve symlinks and Windows
trailing-dot/space forms, on BOTH legs.** Verified:

- `deploy/carrier_docs.py:118-134` `_contained` calls `.resolve()` on base and joined path and
  tests `is_relative_to` — so symlinks are followed and Win32 normalization applies.
- SOURCE leg guarded at `:158` (`_hub_text`); DEST leg at `:179`, `:207`, `:245`, and again at
  `:253` — a deliberate **re-check after `mkdir(parents=True)`** at `:249`, because that is the one
  moment the carrier changes what the path resolves to. Both re-checks precede `write_text` at `:254`.
- `deploy/carrier_docs.py:83-115` `_safe_rel` additionally rejects trailing-dot/space components
  lexically (`part.rstrip(" .")`) and tests absoluteness on **both** path flavors.
- Tests are real and adversarial: `tests/test_deploy_docs.py:196`, `:212`, `:223`, `:243` cover
  `..` traversal, Win32 trailing-dot aliasing, a symlinked destination parent, and a symlinked hub
  source — asserting both the raise *and* `assert not (outside / …).exists()`.

That is a well-built guard. The finding is that it is **local to one carrier**:

- `deploy/carrier_floor.py:852-856` — `_floor_path`/`_sidecar_path` join manifest values to
  `repo_root` with no validation; written at `:684-685` (`_write_lf`).
- `deploy/carrier_precommit.py:839-840` — `_config_path` likewise; written at `:616`/`:622`.
- plus F3's `carrier_globalconfig`.

Zero containment tests exist for any of the three (`tests/test_deploy_floor.py`,
`test_deploy_precommit.py`, `test_deploy_globalconfig.py` contain no `symlink`/`absolute`/`..`
cases; each pins its target dict to the default literal and never varies it).

One reserved-name gap applies to all four: nothing anywhere in `deploy/` checks Windows reserved
device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`).

**Smallest correct fix.** Extract `_safe_rel` + `_contained` to a shared `deploy/pathguard.py` and
call it from the other three carriers. **Ownership: UNOWNED** (`[#485]`, "a shared LF-enforcing
write helper", is the adjacent row and the natural place to land a shared write+guard seam).

### F5 · MEDIUM · `scripts/gen_handoff.py:186-224` is a fifth, independent copy of the git-env scrub that [#396] did not consolidate

`gitenv.py:10-18` states it is "the ONE definition" and names four consumers. `gen_handoff.py`
is not among them and never imports it — it carries its own 17-name `_GIT_LOCATION_ENV_FALLBACK`
(`:186-192`), its own `_GIT_LOCATION_ENV_CACHE` (`:193`), its own `_git_location_env()`
(`:196-209`), and its own inline scrub dict-comprehension (`:218`). Its comment at `:185` still
reads "Mirrors audit.py `_git_location_env`, the established precedent" — written before the
extraction and not updated by it.

**What breaks in practice.** Nothing today: the 17 names are the same strings, so the two agree.
This is rated MEDIUM as a **latent drift edge**, not a live wrong answer — and it is the exact
shape `[#396]` was opened to remove ("the shape where one copy gets a fix and the others rot"),
sitting in the very module whose RM-8 open-batch refusal `gitenv.py`'s docstring cites as the
motivating live failure.

**Smallest correct fix.** Replace `:186-209` with the same by-path load `batch_manifest.py:79-82`
already uses, and point `_git_status` at `_gitenv.scrubbed_git_env()`. Keep `_git_status` itself —
its ok/stdout split is load-bearing (`:170-177`). **Ownership: UNOWNED** (`[#396]` closed).

### F6 · MEDIUM · `scripts/audit.py:3001` — `text=True` with no `encoding=`/`errors=`; `UnicodeDecodeError` escapes the function's own handler

Same function as F1. `_git` catches `(OSError, subprocess.SubprocessError)`; `UnicodeDecodeError`
is a `ValueError` and is caught by neither.

**Reproduced.** A repo containing a filename with an invalid UTF-8 byte, running `_git`'s exact
subprocess shape:

```
core.quotePath=true   -> no raise, stdout='"bad\351name.txt"\n'   (git escapes it)
core.quotePath=false  -> !! ESCAPES audit's handler: UnicodeDecodeError:
                         'utf-8' codec can't decode byte 0xe9 in position 3
```

**What breaks in practice.** `audit.py health` — the blocking `audit-health` pre-commit gate — dies
with a traceback instead of returning a Finding, so the commit is refused with a crash rather than
a verdict. Rated MEDIUM rather than HIGH because it is conditional on `core.quotePath=false`, which
is not git's default (though it is a common setting for people who want readable UTF-8 filenames).

This is a known, ratified class in this very file: `scripts/audit.py:1153-1156` documents
`errors="replace"` as "not decoration (terra HIGH, 2026-08-07)" for exactly this reason, and every
other git call in `audit.py` carries `encoding="utf-8", errors="replace"`. `_git` is the one that
was missed.

**Smallest correct fix.** Add `encoding="utf-8", errors="replace"` at `:3001` — the same one-line
edit as F1, in the same call. **Ownership: UNOWNED.**

### F7 · MEDIUM · Two freshness hooks do not watch their own generator

Verified mechanically against the live `files:` patterns:

```
roster-freshness           deploy/manifest-v1.4.0.yaml          MATCH
                           .claude/methodology-roster.md        MATCH
                           scripts/gen_methodology_roster.py    NO MATCH
claude-rosters-freshness   .claude/commands/save.md             MATCH
                           docs/decisions/ADR-99-x.md           MATCH
                           .claude/generated/commands-repo.md   MATCH
                           scripts/gen_claude_rosters.py        NO MATCH
audit-index-freshness      scripts/gen_audit_index.py           MATCH   <- sibling does it right
intake-index-freshness     scripts/gen_intake_index.py          MATCH   <- sibling does it right
```

**What breaks in practice.** A commit that changes only the generator's rendering logic does not
trigger that generator's own regen-and-diff gate, so the committed artifact silently goes stale
until some unrelated input happens to change. The two sibling hooks include their generator, so
this is an inconsistency, not a design choice.

**Smallest correct fix.** Append `|^scripts/gen_methodology_roster\.py$` and
`|^scripts/gen_claude_rosters\.py$` to the two `files:` regexes in `.pre-commit-config.yaml`
(lines 53 and 65). **Ownership: UNOWNED.**

### F8 · MEDIUM · The general case behind the intake finding: `ecosystem/index.yaml` is generated and guarded by nothing

The contract asked for the general case; here it is, ordered worst-first.

- **`ecosystem/index.yaml` — fully unguarded.** Generated wholesale by `audit.py::regenerate_index`
  (`scripts/audit.py:4433-4448`) via `audit.py registry update` (`:4837`, whose argument is
  `click.Choice(["update"])` — update only). There is **no `--check` mode to hook**, no pre-commit
  hook, and no `ALL_CHECKS` leg. No dedicated test file either.
- **`templates/child-methodology-floor.sha256` — unguarded on the hub.** No hook; `generate_floor.py
  check` validates the rendered floor's binding rules but never diffs against the committed sidecar;
  `check_floor_integrity` returns NOT-APPLICABLE on the hub by construction
  (`scripts/audit.py:1576-1579` — the hub is the floor *source* and carries no floor).
- **`ecosystem/doc-counts.md` — no hook, and its audit check cannot fail.** `check_doc_claims` is
  WARN-only by design (`scripts/validate_doc_claims.py:37-38`), so drift is surfaced and never blocked.
- **`docs/intake/manifest.json`** — the case the contract cited, and the *mildest* one: it has no
  dedicated pre-commit hook, but it **is** guarded by `check_intake_tree_coherence`
  (`scripts/audit.py:3337`) under `audit-health` (`always_run: true`), which is blocking. Two
  carriers, one *pre-commit* hook — but not one unguarded carrier.

**Smallest correct fix.** For `ecosystem/index.yaml`, add a `check` action to `cmd_registry`'s
`click.Choice` and either a hook or an `ALL_CHECKS` leg. **Ownership: PARTIAL** — `[#369]` ("Wire
`boundary_headers.py --check` into pre-commit") is another instance of the same class and
`[#132]`/`[#269]` are adjacent; nothing owns `ecosystem/index.yaml` itself.

### F9 · LOW · `scripts/audit.py:2977` splits git output on whitespace, shredding filenames containing spaces

```python
divergent = sorted(set(unstaged.stdout.split()) | set(untracked.stdout.split()))
```

`git diff --name-only` is newline-separated. Confirmed: `"my file.md\nother.md\n".split()` →
`['file.md', 'my', 'other.md']`.

**What breaks in practice.** The pass/fail verdict survives (a non-empty set stays non-empty), so
the gate still fires correctly. The *evidence it prints* names files that do not exist, which is
what a human then tries to act on. **Fix:** `.splitlines()`. **Ownership: UNOWNED.**

### F10 · LOW · `scripts/validate_onboarding_rulings.py` is reachable by no gate and no command

Not in `ALL_CHECKS`, not in `.pre-commit-config.yaml`, not referenced by any file in
`.claude/commands/`. Only the test suite exercises it. Its own docstring says so explicitly ("NOT
an `audit.py` `ALL_CHECKS` member and is wired into no blocking gate"), so this is
**deliberate-but-inert** rather than an accident — recorded here because an inert validator is
indistinguishable from a passing one until someone checks. **Ownership: UNOWNED.**

### F11 · LOW · The validator family has no shared module, and three copies of one rule disagree

Measured across the 12 validators:

- **Repo-root discovery: 8 byte-identical copies** of `_SCRIPTS_DIR = Path(__file__).resolve().parent`
  / `_REPO_ROOT = _SCRIPTS_DIR.parent` (`validate_reconciliation.py:54`, `validate_doc_claims.py:53`,
  `validate_doc_code_edge.py:48`, `validate_doc_rot.py:52`, `validate_doc_structure.py:67`,
  `validate_git_backlog.py:72`, `validate_no_ff.py:54`, `validate_onboarding_rulings.py:33`).
- **`format_findings`: 6 independent implementations**, four of which separately re-derive the same
  `.replace("|", "/")` markdown-table-safety strip.
- **Date-shape regex: 3 encodings that disagree on the same input.** Given
  `"prefix 2026-07-13 suffix"`: `validate_doc_rot.py:70` (unanchored) **accepts**;
  `validate_onboarding_rulings.py:38` (`^…$`) and `validate_hermetization.py:109` (`^…-`)
  **reject**. Same nominal concept, three anchorings, no shared primitive.
- Only 1 of 5 git call sites in the family is factored into a named wrapper
  (`validate_no_ff.py:70-74`); the rest inline their own `subprocess.run(["git", …])`.
- No `scripts/common.py` exists.

Inside `audit.py` the same shape recurs: the `_run` closure is duplicated at `:1985-1995` and
`:3482-3492` (10 lines, differing by one `.strip()`), and four near-identical YAML loaders sit at
`:2200`, `:2224`, `:2246`, `:2272`.

**Ownership: PARTIAL** — `[#397]` ("scripts/ target structure — rule on the mapped grouping") is the
row this belongs under.

### F12 · LOW · `scripts/gitenv.py:87-90` — the consolidated scrub has no `timeout=`

`git_location_env()` runs `git rev-parse --local-env-vars` with `capture_output`, `text`,
`encoding`, `errors` — and no `timeout=`. Every other git call in the fleet carries one (15s, 30s,
or 60s), including the copy in `gen_handoff.py:202` (`timeout=30`) that F5 proposes to delete.

**What breaks in practice.** A hung `git` blocks the first scrub call in every consumer — which is
the audit gate — with no upper bound. This faithfully preserves the pre-extraction `audit.py`
behavior, so it is **not a regression**; it is the weaker of the two shapes currently in the tree,
and consolidating F5 onto it would lose the timeout that copy has. Fix both together.
**Ownership: UNOWNED.**

---

## 3. Severity tally

```
Critical  0
High      3   (F1, F2, F3)
Medium    5   (F4, F5, F6, F7, F8)
Low       4   (F9, F10, F11, F12)
TOTAL    12
```

Zero Critical is a claim about *this* review's reach, not a clean bill: the gate mesh did not run
here (§1), and assertion quality is unmeasured (§5).

---

## 4. Scope item 1 — is `audit.py` doing too many jobs, and what would decomposition cost?

**Measured shape.** 5072 lines; 137 top-level `def`s; 4 classes; 41 registered checks; **21
functions over 60 lines**, the worst being `check_review_artifact_coverage` (205),
`_commit_routine_outputs` (145), `check_preflight_backlog_ids` (117),
`check_fleet_audit_replication` (109), `_select_active_bundle` (102). 19 `subprocess.run` calls, 6
carrying `env=`. (The contract's figures — `_git` at `:3004`, "7 of 21" — are close but stale; see
§6.)

**Yes, it is doing at least four jobs**, and one of them is the interesting one:

1. the 41-check gate mesh (its stated job);
2. a 6-verb CLI (`run`, `repo`, `registry`, `health`, `ship-gate`, `checks`);
3. **a fleet-automation WRITE path** — `_commit_routine_outputs` (`:4560`, 145 lines),
   `_push_routine_branch` (`:4509`), `_restore_durable_scope` (`:4471`) — which stages, commits,
   and pushes;
4. a registry generator (`regenerate_index`, `:4433`).

Job 3 sits oddly against CLAUDE.md §5 rule 4 / ADR-28 / ADR-36: *"Layer 2 never executes — no
orchestration scripts; `scripts/` contains read-only validators only."* This module commits and
pushes to a durable branch. That may well be sanctioned (ADR-84 is cited in its comments), but the
sanction is not visible at the invariant, and it is the single largest non-check block in the file.

**What a decomposition would cost — the real coupling, not the theoretical kind:**

- **30 test files `import audit` at module level.** Any package split has to keep that name resolving.
- **Dual script/package mode.** 17 `try: from scripts import X / except ImportError: import X` pairs
  (`:91-204`) exist so both `python scripts/audit.py` and `python -m scripts.audit` work. A split
  multiplies that boilerplate rather than removing it.
- **Reflective coupling to `ALL_CHECKS`.** It is a plain list literal (`:4177-4224`) with no
  decorator registry; `check_doc_code_coverage_drift` reads it reflectively (`:2531`), and
  `_markers_for_check` (`:2466`) inspects check *source*.
- **Source-text assertions.** `tests/test_gitenv.py:275-280` asserts `"_git_location_env()"` appears
  in the source of three named functions; `tests/test_reverse_dep_oracle.py:83` pins a
  line-position assumption about where the gitenv import block sits. These break on movement, not
  on behavior change.

**Recommendation: do not split the check mesh now.** The cheap, high-value move is to extract
**job 3 only** — `_commit_routine_outputs` + `_push_routine_branch` + `_restore_durable_scope`,
about 230 contiguous lines at the end of the file. It is the only part that mutates state, it is
the part in tension with the Layer-2 invariant, and it has **no `ALL_CHECKS` coupling at all**, so
it moves without touching the reflective machinery or the 30 importers. That belongs on `[#397]`.

---

## 5. Test-coverage honesty

**The suite did not run here** (§1). Everything below is measured statically.

**Per-check coverage is genuinely complete.** AST-verified against `ALL_CHECKS`:

```
registered: 41   defined check_*: 41
defined but NOT registered: []      registered but NOT defined: []
registered checks NEVER named in any test: 0
named only 1-2x: 1  (check_enforcement_coverage)
named 3+ times: 40
```

**Assertion volume across the 16 hot-spot test files:** 670 test functions, 1417 `assert`
statements, 10,113 lines. Density ranges 1.2–3.1 asserts/test; `test_validate_backlog.py` is the
thinnest at 1.2, `test_deploy_mesh.py` the richest at 3.1.

**Real assertions vs smoke.** The validator family is genuinely assertion-rich — across all 12
validators' suites, **no smoke-only test was found**; every test inspects a specific message
substring, status enum, count, ordering, or exit code. Representative:
`assert vnf.find_violations(repo, baseline="2026-06-10")` yields exactly the FF'd subject — the
load-bearing FF-vs-no-ff distinction, asserted on a real temp repo, not mocked. Two weak spots:
`tests/test_gen_handoff.py:703-708` (`test_seal_identity_accepts_a_correctly_labelled_bundle`) has
**zero assert statements** — its body is a bare call with `# must not raise`; and
`tests/test_check_seal_identity.py:59-61` asserts only an exit code.

**Where the unmeasured-assertion-quality gap matters most.** Mutation testing is not possible in
this repo, so nothing proves these assertions would survive a subtle predicate inversion. That
matters least for the WARN-tier advisory checks (a wrong warning is cheap) and **most for the three
fail-CLOSED organs**: `block_ff_push`, `block_unanchored_push`, and the `journal_anchor` predicate
they share. Those are the only organs with teeth — they refuse pushes — and their correctness rests
entirely on assertions whose sensitivity is unverified. If mutation testing is ever affordable for
exactly one module, it should be `scripts/journal_anchor.py`, because two organs import its
predicate and a silent weakening there disarms both at once.

**A coverage gap that is not about assertion quality at all:** the three unguarded carriers in F4
have **zero** containment tests. That is absence, not weakness, and it is cheaper to fix.

---

## 6. Dead code and drift

**No dead code found.** Every `scripts/*.py` is referenced outside itself; every top-level function
in the four handoff-engine modules has a call site; `ALL_CHECKS` has zero orphans in either
direction.

**Drift found:**

1. **`gitenv.py:10-12` misdescribes its own history.** It says the scrub "lived in three
   hand-copied places (`audit.py`, `fleet_parity.py`, `fleet_analytics.py`)". Per git history,
   `fleet_analytics.py`'s pre-extraction version *delegated* to `audit._git_location_env()` — it was
   never an independent hand-copy. And the docstring omits the copy in `gen_handoff.py` (F5) that
   was present then and is present now. Doc-vs-code drift inside the module written to end drift.
2. **`check_mermaid_theme_directive` — cited by docs, absent from code, and that is correct.**
   Retired 2026-07-05 per the ADR-51 amendment; retirement comments remain at `scripts/audit.py:725`
   and `:4184`, and it is still named in `ADR-51`, `JOURNAL.md`, and four audit artifacts. Those are
   immutable dated records, so the references are history, not rot. Listed here because it *looks*
   like drift and is not — see §7.
3. **`scripts/validate_audit_casing.py` does not exist in the hub.** The contract names it in scope
   item 4. Hub-side audit-casing validation is `validate_hermetization.py` Rule B (`:154-170`, the
   R4 casing branch at `:167-170`). `validate_audit_casing.py` is the **consumer-side** name,
   recorded as a declared d1 divergence at `.methodology.yaml:20-25` ("consumers enforce the R4
   casing branch only …; the enum and date grammar remain hub-side"). Locator correction, not a defect.
4. **The contract's own locators are stale.** It cites `_git` at `:3004` with callers at
   `:1031, :2977, :2978, :3070, :3078, :3084`; measured, `def _git` is at `:2998` (its
   `subprocess.run` at `:3001`) with callers at `:1048, :2971, :2972, :3064, :3072, :3078` — off by
   6–17 lines except `:3078`. And "7 of 21 `subprocess.run` calls carry `env=`" measures as **6 of
   19** by AST. Same shape, different arithmetic. Flagged because this is the `/preflight` class the
   repo already has a command for.

---

## 7. Ranking, and what I found healthy

**The five I would fix first, by (damage if unfixed) ÷ (fix size):**

1. **F1** — one line (`env=` at `:3001`) removes a wrong-repo read from the ratchet gate's baseline
   comparison. Highest ratio in the review by a wide margin.
2. **F6** — one line, *same call site as F1*, converts a gate crash into a verdict. Fix with F1.
3. **F7** — two regex characters' worth of edit closes two silent-staleness holes, and the correct
   pattern is already written in the two sibling hooks.
4. **F3** — reuse an already-written, already-tested guard; stops the only unguarded write into the
   user's home directory.
5. **F2** — needs a ruling before code moves, but it is the largest live inconsistency measured
   (8 of 11 real branches) and it sits underneath an ADR-85 exemption path.

**What I looked at and found healthy** — this list is part of the finding, not filler:

- **`ALL_CHECKS` integrity.** 41 registered, 41 defined, zero orphans either direction, zero checks
  untested. For a 5000-line file grown fast, that is a genuinely good result.
- **The `check_mermaid_theme_directive` retirement is exemplary.** The function was removed *and*
  `tests/test_audit.py:694-695` asserts both that the attribute is gone and that no `ALL_CHECKS`
  member carries the name — a retirement that cannot silently un-retire.
- **`carrier_docs`' containment guard** (F4's first half). Resolves symlinks on both legs,
  re-checks after `mkdir`, refuses Win32 trailing-dot/space aliasing, and its tests actually create
  a symlink and assert the write did not land outside. This is the standard the other carriers
  should be raised to, not a defect.
- **`gitenv`'s by-path loading.** The shadow-hole argument is correct, and
  `tests/test_gitenv.py:153-203` *proves* it by spawning subprocesses with decoy `gitenv` modules on
  `PYTHONPATH` in both shapes and asserting the real file still won — an adversarial test, not an
  assertion of intent.
- **`journal_anchor.py`'s posture.** Fail-loud by construction, predicate defined once and imported
  by both the pre-push organ and the audit backstop, floor SHA read from the ratified ADR rather
  than hardcoded. This is the anti-drift pattern F2 and F5 are missing.
- **`deploy/floor_conformance._rmtree_guarded`** (`:303-325`) — deletion containment done right,
  with both paths `.resolve()`d, and **reused by import** in `lived_sandbox/spawn.py` rather than
  copied.
- **Validator test quality.** No smoke-only test in the entire 12-validator family.
- **CI's uv discipline.** `.github/workflows/report-only-wall.yml:105-106` greps `pyproject.toml`
  to assert the uv pin has not moved, failing the run if it has — a gate that guards its own
  precondition.
- **No dead code.** Nothing in `scripts/` is unreferenced; nothing in the handoff engine is uncalled.

---

## 8. Needs a ruling

1. **Which `LANE_BRANCH_RE` is canonical (F2)?** Either `validate_branch_naming`'s strict
   `lane-<letter>-<id>-<slug>` grammar is right and 8 of 11 recent lanes were misnamed with
   `/lane-boot` bypassed, or the grammar is wrong and should be relaxed to `batch_manifest`'s. Until
   this is ruled, the ADR-85 anchoring exemption and the lane-boot gate disagree by construction,
   and no code change is safe.
2. **Is `audit.py`'s fleet-automation write path compatible with Layer-2 invariant #4?**
   `_commit_routine_outputs`/`_push_routine_branch` stage, commit, and push, inside a repo whose
   canonical instruction file says `scripts/` holds read-only validators only. If sanctioned, the
   exemption should be declared where the invariant is stated; if not, it should move (§4).
3. **Is `_git`'s missing scrub a defect or an exemption (F1)?** `scripts/audit.py:1945-1949`
   enumerates both the sites where the scrub fires and the one site deliberately exempted. `_git`
   is in neither list. I have read it as an omission and rated it HIGH; if it was a deliberate
   exemption, the comment needs to say so and the reasoning is not obvious to a reader.
4. **Cloud-runtime gate coverage (§1).** In this container no `uv run --locked` entry can execute,
   so an unattended session here runs with the entire gate mesh silently absent. If nightly Routines
   run in this class of container, that is a standing hole. `[#453]` is the row; this review is
   evidence for it, not a fix.
</content>
</invoke>
