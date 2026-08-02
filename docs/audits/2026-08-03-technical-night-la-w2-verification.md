# Night batch 2026-08-03 · lane L-A — adversarial verification of the W2 execution report

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-la-w2-verification
- **Status:** PROPOSAL — read-only verification. No row was closed, reworded or filed; no
  repo prose was edited; nothing was fixed. Findings are REPORTED.
- **Subject:** the JOURNAL `2026-08-02 (f)` entry (`JOURNAL.md:22-53`), written at WRAP by the
  W2 execution session, and the six claim groups the night brief lifted out of it.
- **Base:** `origin/main` = `c7628a3e552a3aedff341106e4fb889763bf5b12`; verification branch
  `claude/night-batch-2026-08-03-k8djp8`, identical tip (`0 0` on
  `git rev-list --left-right --count origin/main...HEAD`).
- **Method:** re-derived from live state only. Every claim below was re-run against the tree,
  never read back from the report. Working tree clean throughout (`git status --porcelain`
  empty before and after every probe).
- **Clone-depth correction (material — read before trusting any history claim).** The container
  arrived with a **SHALLOW** clone (`.git/shallow` present; first-parent spine = 89 commits).
  Lane L-B detected this and ran a read-only `git fetch --unshallow`, which also advanced
  `origin/main` `65a549bf..c7628a3e`. **Every git claim in this report was re-run after the
  unshallow** and is stated against the complete history: spine = **1286** commits,
  `.git/shallow` absent. The four SHAs re-verify identically, `validate_git_backlog` still
  reports `OK — no closed-but-present drift (direction (a) STRONG, full history)` — and that
  phrase now means what it says, which on the shallow clone it did not.

---

## Claim table

Read this first. Verdicts are per the brief's six groups, decomposed to the individual
assertion where a group's parts disagree.

| # | Claim (as briefed) | Verdict | Evidence |
|---|---|---|---|
| 1a | Arc 1 ([#475]) merge SHA — arrived TRUNCATED in the operator's copy | RECOVERED | `087d967f184dcebc34087bbfa97ac42f62ea7100` |
| 1b | Arc 2 merge `bc0c2ada` | CONFIRMED | `bc0c2ada2374bcb8f76a536c6c8307199b2835c3`, on first-parent spine |
| 1c | wrap `76c338fb` merged at `c7628a3e` | CONFIRMED | `c7628a3e` parents = `bc0c2ada 76c338fb` |
| 1d | anchor `087d967f` | CONFIRMED — and it is the SAME commit as 1a | see note A |
| 1e | "exist on `main`'s first-parent spine" | CONFIRMED after fetch — REFUTED as the container first presented it | see note B |
| 2a | `check-seal-identity` present in `.pre-commit-config.yaml`, `files: ^docs/handoffs/` | CONFIRMED | `.pre-commit-config.yaml:103,113` |
| 2b | `check_seal_identity.py` REUSES `gen_handoff.verify_seal_identity`, no parallel impl | CONFIRMED | one `def` repo-wide, `scripts/gen_handoff.py:324` |
| 3 | `gen_task_tree.py --write` REFUSES, exit 2, zero bytes written | CONFIRMED | live run, tree digest identical before/after |
| 4a | collected count 2195, matching the re-pinned `doc-counts` | CONFIRMED | live 2195; `ecosystem/doc-counts.md:15` pins 2195 |
| 4b | failure set is EXACTLY the two `[#457]` ids (2190 pass / 2 fail) | CONFIRMED | see section 4 |
| 5a | [#475]/[#474] absent from open BACKLOG | CONFIRMED | `grep '#475\|#474' BACKLOG.md` -> no match |
| 5b | `tasks/*` retired with `status: closed` (retire-not-delete) | CONFIRMED | both files on disk, `status: closed`, dropped from `manifest.json` queue |
| 5c | regenerated tree consistent (`--check` exit 0) | CONFIRMED | `gen_task_tree: check ok`, exit 0 |
| 5d | CLAUDE §9 roster / ARCHITECTURE Ch2 lockstep — §9 v2.50, 16 gates | CONFIRMED | exact three-way set equality, see section 5 |
| 5e | `validate_backlog` = 186 open+deferred | CONFIRMED | 186 = 157 open + 29 deferred |
| 5f | net −2 (188 -> 186) | CONFIRMED | queue at `25e9dc7d` = 188, at HEAD = 186 |
| 6a | ship-gate GREEN in a clean environment | **UNVERIFIABLE HERE** — RED in this container, every contributor traced to container difference | see section 6 |
| 6b | `[stale]` count 0 | **REFUTED here (=1)** — the one stale is container-caused | see section 6 |
| X | "terra zero findings both arcs" | **UNVERIFIABLE** — no artifact exists | see section 7 |

**Nothing in the W2 report was refuted on repo content.** The two non-green verdicts (6a, 6b)
and the one unverifiable (X) are the headline, and are described precisely below — 6a/6b are
container artefacts, X is a missing artifact.

---

## Headline

**1. The only claim that fails on repo evidence is one the report never made: the terra review
left no artifact.** The JOURNAL states *"terra review body: zero findings on both arcs"*
(`JOURNAL.md:47`). There is no `docs/audits/2026-08-02-codex-*.md`, no terra output anywhere
under `docs/`, `logs/` or `codex/`, and no review file in either arc's diff. Every one of the
**88** prior codex reviews in this repo left a `docs/audits/<date>-codex-<slug>.md` artifact —
the three most recent being `2026-08-01-codex-460-replication-and-close.md`,
`2026-08-01-codex-462-membership-agreement-census.md`,
`2026-08-01-codex-generator-newlines-and-groom.md`. W2 broke that precedent silently. The
claim is not refuted — it is **unfalsifiable**, which for a gate-adjacent review is the
same operational problem.

**2. `ship-gate` is RED in a clean cloud checkout, and three of the five contributors are
portability defects, not just "missing siblings".** Details in section 6. The one that is a
real finding rather than an environment fact: `check_deployed_methodology_version` keys the
registry by the repo-root **directory basename**, so this checkout — cloned as
`dev-knowledge`, not `.dev-knowledge` — is reported as an unregistered repo. That is the same
defect class [#465] legs 2+3 fixed for `_is_hub()` (`56f82aa` "the hub recognises itself from
any checkout"); the fix did not reach this check.

**3. The brief's own artifact-naming pattern is refused by this repo's ADR-101 gate.** See
section 8. Reported, and worked around by naming, not by weakening the gate.

---

## 1. Merge SHAs — note A and note B

All four commits exist and resolve. Full identities:

```
087d967f184dcebc34087bbfa97ac42f62ea7100  2026-08-02T21:33:07+02:00
  Merge branch 'fix/475-seal-identity-precommit-gate' — seal identity becomes a pre-commit gate, closes [#475]
  parents: 25e9dc7dd3fc6804b237c29cc798d366b5310c83 23366cb769d221a2ead0bfc077214e02b17c6c7b

bc0c2ada2374bcb8f76a536c6c8307199b2835c3  2026-08-02T21:45:37+02:00
  Merge branch 'fix/474-gen-task-tree-write-guard' — --write warned-means-abort guard, closes [#474]
  parents: 087d967f184dcebc34087bbfa97ac42f62ea7100 6850bf57087d9d3ff20e361775c77ae8d756cc3b

76c338fbe03c894d375ccb7f157f6ea85034226e  2026-08-02T21:46:37+02:00
  docs(journal): 2026-08-02 (f) — W2 mechanism pair wrap ([#475] 087d967f, [#474] bc0c2ada)
  parents: bc0c2ada2374bcb8f76a536c6c8307199b2835c3     (single parent — a branch commit, not a merge)

c7628a3e552a3aedff341106e4fb889763bf5b12  2026-08-02T21:47:40+02:00
  Merge branch 'docs/journal-wrap-w2-475-474' — JOURNAL 2026-08-02 (f) W2 wrap
  parents: bc0c2ada2374bcb8f76a536c6c8307199b2835c3 76c338fbe03c894d375ccb7f157f6ea85034226e
```

**Note A — the "truncated Arc 1 SHA" and the "anchor" are one commit, not two.** The brief
lists `anchor 087d967f` alongside a separately-missing Arc 1 merge SHA. They are the same
object: `087d967f...` IS the `fix/475-seal-identity-precommit-gate` merge. Recovered in full:
**`087d967f184dcebc34087bbfa97ac42f62ea7100`**. There is no fifth SHA outstanding.

**Note B — first-parent spine membership.**

```
087d967f  first-parent-spine=YES  ancestor-of-origin/main=yes
bc0c2ada  first-parent-spine=YES  ancestor-of-origin/main=yes
76c338fb  first-parent-spine=NO   ancestor-of-origin/main=yes
c7628a3e  first-parent-spine=YES  ancestor-of-origin/main=yes
```

`76c338fb` off the first-parent spine is CORRECT, not a defect: under `--no-ff` the branch
commit is the merge's SECOND parent. The claim's own wording ("wrap `76c338fb` **merged at**
`c7628a3e`") matches the topology exactly.

**The container caveat, stated because it nearly produced a false REFUTED.** At session start
the container's `origin/main` and local `main` both pointed at `65a549bf94bdd08698b2a48f7622780003880398`
(2026-07-31, the ratification batch) — 174 commits behind, with none of the four SHAs
reachable. Only the session branch had been fetched. After `git fetch origin main`,
`origin/main` = `c7628a3e` and all four resolve as tabled above. **The local `main` ref in this
container is still stale at `65a549bf`** — an artefact of the clone, not of the repo. Anyone
re-running this verification must fetch first or they will "refute" a true claim.

---

## 2. The hook is real and armed

- `.pre-commit-config.yaml:103` — `- id: check-seal-identity`
- `.pre-commit-config.yaml:113` — `files: '^docs/handoffs/'`
- `.pre-commit-config.yaml:114` — `pass_filenames: true` (explicit, so FR1 cannot be silently un-armed)
- `.pre-commit-config.yaml:111` — `entry: uv run --locked python scripts/check_seal_identity.py`

**One verifier, confirmed.** Repo-wide there is exactly ONE definition:

```
scripts/gen_handoff.py:324:def verify_seal_identity(bundle_dir: Path) -> None:
scripts/gen_handoff.py:304:class BundleIdentityError(RuntimeError):
```

`scripts/check_seal_identity.py:35` imports it (`from gen_handoff import BundleIdentityError,
verify_seal_identity`) and calls it at `:70`. No parallel implementation, no re-derived
slug-vs-directory comparison: `grep -rn "def verify_seal_identity" --include=*.py .` returns
the single `gen_handoff.py:324` hit. The module even documents WHY the bare import comes
first — "so every launch path (pytest, hook, direct run) resolves ONE module object for
gen_handoff — the #153 two-copies identity/monkeypatch trap"
(`scripts/check_seal_identity.py:30-32`).

The config is additionally pinned by a structural test that compiles the hook's own `files:`
regex out of the YAML rather than hand-mirroring it (`tests/test_check_seal_identity.py:108-121`).

**Honest limit, restated from the source and unchanged:** this catches the Slug row versus the
directory, not a stale P0c/P3/P8 locator inside a correctly-labelled bundle
(`scripts/check_seal_identity.py:27-29`).

---

## 3. The [#474] guard is real — run live against the populated tree

Run exactly as the brief specified — no `--force`, refusal is the behaviour under test:

```
$ python scripts/gen_task_tree.py --write
gen_task_tree: --write REFUSED (nothing written) -- 2 warning condition(s):
  - /home/user/dev-knowledge/tasks/manifest.json exists -- the target is a POPULATED source-of-
    truth tree, and the import would rewrite it from the generated file
  - 212 task file(s) present under /home/user/dev-knowledge/tasks -- an import re-derives
    filenames from titles, which can re-slug live ids and orphan the originals (the [#473]
    incident: 17 files re-slugged by one mistaken run)
  The routine post-flip regen is --emit-source (tree -> BACKLOG.md).
  To run the import anyway, re-run with --write --force.
EXIT=2
```

Zero bytes written, proven independently of the program's own claim:

```
tasks tree digest BEFORE: e6bc57bb314de97a3bda103bb8b17efd
tasks tree digest AFTER : e6bc57bb314de97a3bda103bb8b17efd     (find tasks -type f -exec md5sum {} \; | sort | md5sum)
git status --porcelain   : empty, before and after
```

Both refusal conditions, the `--force` escape hatch and the `--emit-source` routine direction
are all named in the refusal text — the [#474] acceptance contract, met.

---

## 4. Suite

- **Collected: 2195.** `pytest --collect-only -q` -> `2195 tests collected in 5.26s`.
- **`ecosystem/doc-counts.md:15`** pins `- tests: **2195 collected**`. Doc and live agree; the
  re-pin claim is CONFIRMED.
- **Failure set:** see the fenced block below — it is EXACTLY the two `[#457]`-owned ids
  (`test_check_fleet_parity_green_on_live_repo`,
  `test_routine_consumers_live_backlog_governs_exactly_one_row`), matching the `[#457]` row at
  `BACKLOG.md:80` which names both by name and by cause.

**Run 1 — full serial, as-cloned container:** `2155 passed / 33 failed / 7 skipped` in 661s.
The two `[#457]` ids are present, plus 31 others, all traced to missing container
prerequisites: 19 x `test_fleet_analytics` (pandas / `analytics` group absent), 6 x
`test_reverse_dep_oracle` + `test_safe_remove` (`node_modules/` absent — `package.json` pins
the vendored pyright 1.1.410 langserver, gitignored, `npm install` never run), 3 x
`test_audit` health/synthetic (gitignored `ecosystem/<repo>/state.yaml` absent -> `[!!] repos
registered (none)`), 4 x boundary/carrier/legibility/merge-serialization (siblings, armed
hooks, real-git and pre-commit spawns).

**Run 2 — those 33 re-run with pandas installed:** `91 passed / 13 failed` in 502s. 18 of the
19 `fleet_analytics` failures clear (residual `test_hub_is_included_as_a_mining_target`).
**Confound disclosed:** `.git/hooks` were still armed from the section-6 control probe, and
under armed hooks `test_check_fleet_parity_green_on_live_repo` PASSED.

**Run 3 — confound removed.** `.git/hooks` restored to pristine (samples only), the two ids run
alone:

```
FAILED tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
FAILED tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row
  AssertionError: assert '1 declared routine row' in '2 declared routine row(s) name a
  consumer and a consumption_path (live hooks/schedules out of scope — [#426])'
2 failed in 5.22s
```

Both fail in the pristine state; leg (ii) fails for exactly the cause `BACKLOG.md:80` records.

**What Run 2 surfaces, and the row does not say.** Leg (i) flips to PASS the instant hooks are
armed — so in this container it is failing on the `hooks-armed WARN-undeclared` finding, NOT on
the ai-council `conftest.py` disposition the row names. The test is disposition-blind to
*whatever* WARN happens to be live; the row records only one instance of that class. **Report
line for `[#457]`, not a fix.**

**Environment caveat that applies to this whole section.** `uv run --locked` — the invocation
every gate entry and the repo's own docs use — **cannot run in this container**:
`pyproject.toml:29` pins `required-version = "==0.11.19"` and the box carries uv 0.8.17, so
every `uv` verb (including `uv python list`) aborts with
`Required uv version ==0.11.19 does not match the running version 0.8.17`. `uv self update
0.11.19` fails with `The version 0.11.19 was not found`. The suite was therefore run from a
venv built OUTSIDE the repo tree at the `uv.lock` versions (pytest 9.1.1, ruff 0.15.5,
pyyaml 6.0.3, click 8.4.2, rich 15.0.0, pydantic 2.13.4, packaging 26.2, pre-commit 4.6.1) on
CPython 3.12.3. This is lock-faithful but is NOT `uv sync --locked`, and that difference is a
real limit on how strongly section 6 can speak.

---

## 5. Closure hygiene

**[#475]/[#474] absent from open BACKLOG.** `grep -n '#475\|#474' BACKLOG.md` returns nothing.

**Retire-not-delete honoured (ADR-107 §6.3).** Both task files remain on disk with
`status: closed`:

```
tasks/474-gen-task-tree-write-import-recovery-footgun.md   status: closed
tasks/475-seal-identity-as-a-pre-commit-gate-on-bundles.md status: closed
```

and both have dropped OUT of the `tasks/manifest.json` queue (186 non-prose nodes; ids 474,
475 — and 473, 476, 462 — absent; 472, 465, 383 still present). That is exactly the shape
ADR-107 §6.3 describes: the file remains as the allocation record, the id leaves the queue.

**Tree consistent.** `python scripts/gen_task_tree.py --check` -> `gen_task_tree: check ok`,
exit 0. `python scripts/validate_git_backlog.py` -> `OK — no closed-but-present drift
(direction (a) STRONG, full history)`, exit 0.

**Counts.** `python scripts/validate_backlog.py` -> `OK (9 themes, 26 stories, 186 tasks, 1
warning(s))`, exit 0. The single warning is pre-existing and unrelated to W2: `user story with
no tasks — story "[S24] Declare desired state once, as data, inste" line 432`.

**The exact split the brief asked for** (from `grep -h '^status:' tasks/*.md | sort | uniq -c`):

```
open      157
deferred   29
closed     26      (retired files, out of queue)
---------------
queue     186      = 157 open + 29 deferred
```

`186 = 157 + 29` reconciles against `validate_backlog`'s 186 and against the manifest's 186
non-prose nodes. Three independent surfaces agree. **Deferred = 29 matches the 2026-08-02 boot
baseline exactly — zero drift.**

**Net −2, verified against the pre-arc parent** rather than taken on report:
`git show 25e9dc7d:tasks/manifest.json` -> queue size **188**, with ids 474 and 475 both
present. HEAD -> **186**, both absent. 188 -> 186 = −2, and the delta is exactly the two ids
claimed. No third row moved.

**Lockstep — §9 v2.50, 16 gates — is exact, not approximate.** Machine set-comparison across
three surfaces:

```
LIVE .pre-commit-config.yaml ids (16): audit-health, audit-index-freshness,
  backlog-filing-backpressure, backlog-id-on-close, block-ff-push, check-seal-identity,
  claude-rosters-freshness, codemap-freshness, coherence-nudge, intake-index-freshness,
  normalize-dated-headers, roster-freshness, ruff, toc-freshness-playbook, validate-backlog,
  validate-hermetization

ARCHITECTURE.md Ch2 gate list ids (16): identical set   -> live == ARCH: True
CLAUDE.md S9 roster ids (16):          identical set    -> live == CLAUDE S9: True
missing from ARCH: []      missing from CLAUDE S9: []
```

`ecosystem/doc-counts.md:14` independently pins `- pre-commit gates (16)`. Four surfaces,
one number, one membership. `CLAUDE.md:223` carries the `v2.50` section-history entry;
`ARCHITECTURE.md:17` carries the matching `Last updated: 2026-08-02 — [#475]` line naming both
the Ch2 gate list and the Validators list, and `ARCHITECTURE.md:495` carries the gate itself.
Lockstep CONFIRMED on content, not just on the assertion that lockstep happened.

---

## 6. Ship-gate — RED here, and why

`python scripts/audit.py ship-gate` in this container exits 1:

```
ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 4 new/undispositioned WARN(s))
```

Decomposed, with each contributor traced to a cause:

| Contributor | Cause | Container or repo? |
|---|---|---|
| `[!!] hooks_armed` (the 1 hard fail) | `.git/hooks/` holds ONLY `*.sample` — no armed hook | container |
| `[~~] fleet_parity .dev-knowledge hooks-armed WARN-undeclared` | same root cause | container |
| `[~~] fleet_parity ai-council fleet-membership unavailable` | `/home/user/ai-council is not a git repo` | container |
| `[~~] fleet_parity corp-monorepo fleet-membership unavailable` | `/home/user/corp-monorepo is not a git repo` | container |
| `[~~] deployed_methodology_version: dev-knowledge not listed` | registry key is `.dev-knowledge`; this checkout's basename is `dev-knowledge` | **container-triggered, repo-portability defect** |
| `[stale] warn-fleet-parity-ai-council-root-conftest` | the WARN it dispositions cannot fire with ai-council absent | container |

**The decisive probe.** `.git/hooks/` was armed (`pre-commit install -t pre-commit -t
commit-msg -t pre-push` — writes only untracked files under `.git/`, reverted afterwards) and
ship-gate re-run:

```
ship-gate: RED — not shipped-ready (3 new/undispositioned WARN(s))
```

The hard fail and one WARN vanish. **The residual three are the two absent sibling repos plus
the directory-name key.** No repo-content organ contributes to the RED.

**Verdict 6a: UNVERIFIABLE in this environment**, with the strong qualifier that every
contributor is accounted for and none of them is repo content. GREEN cannot be positively
witnessed from a cloud clone that lacks `/home/user/ai-council`, `/home/user/corp-monorepo`,
and the `.`-prefixed directory name.

**Verdict 6b: REFUTED here — `[stale]` is 1, not 0.** The stale disposition is
`warn-fleet-parity-ai-council-root-conftest` (`ecosystem/disposition-register.yaml:311`, ref
`#430`, `review_date: 2026-08-26`). It is stale here for the same reason as the WARNs: its
`match:` string is `"ai-council root-sweep WARN-undeclared: top-level entry 'conftest.py'"`
and ai-council is unresolvable. On the operator's machine, with siblings present, it would
match. **This is not evidence against the W2 report** — it is evidence that `[stale]` counts
are not portable across checkouts, which is worth a row of its own.

**Related, same probe:** `python scripts/audit.py health` also reports `health: DEGRADED`
(exit 1) here, and the FAIL is the operational preflight `[!!] repos registered (none)` — the
per-repo `ecosystem/<repo>/state.yaml` pointers are gitignored and absent in a fresh clone.
Self-audit line: `self-audit (.dev-knowledge) - 29/50 pass`.

**The portability finding, stated as a report line (not fixed).**
`scripts/audit.py:2300` — `repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name`
— keys `ecosystem/deployed-versions.yaml` by the repo-root **basename**. The registry's key is
`.dev-knowledge` (`ecosystem/deployed-versions.yaml:23`); a GitHub clone lands as
`dev-knowledge` (no leading dot), so the hub does not find its own row and WARNs. This is the
identical failure shape [#465] legs 2+3 fixed at `56f82aa` for hub identity ("the hub
recognises itself from any checkout") — `resolve_repo_path()` bound `_is_hub()` to the live
tree, but `check_deployed_methodology_version` still compares names. Evidence, not a patch.

---

## 7. The unclaimed gap — terra review left no artifact

`JOURNAL.md:47` states *"terra review body: zero findings on both arcs"*. Live searches:

- `ls docs/audits/ | grep -E '^[0-9-]+-codex'` -> 88 files, newest `2026-08-01-codex-*` (three of them). **None dated 2026-08-02.**
- `ls docs/audits/ | grep '2026-08-02'` -> 7 files, all `technical`/`conformance-nightly-digest` class, none a review.
- `grep -rln 'terra' logs/ codex/` -> no match. `logs/` holds only `FLEET-PARITY.md`, `PARITY-EVENTS.jsonl`, `TOKEN-LOG.md`; `codex/` holds only `AGENTS.md`.
- `git diff --stat 087d967f^1 087d967f` and `... bc0c2ada` -> 9 and 7 files, no review artifact in either arc.
- `git log --oneline 25e9dc7d..c7628a3e` -> 6 commits total, none a review record.

**Verdict: UNVERIFIABLE.** Not refuted — there is no evidence the review did not happen, and
the JOURNAL is a first-hand record. But the claim cannot be checked by anything except the
claim, and that is a departure from 88 consecutive precedents in this repo (the pattern the
2026-08-01 arcs still followed one day earlier). Whether the review artifact is required is a
ruling; that it is absent is a fact.

---

## 8. Deviation taken by this lane — artifact naming

The night brief specifies `docs/audits/2026-08-03-night-<lane>.md`. **That pattern is BLOCKED
by this repo's own `validate-hermetization` gate.** Tested against the live validator, not
inferred:

```
$ python -c "from validate_hermetization import rule_b_violation; ..."
BLOCK  docs/audits/2026-08-03-night-batch-digest.md
BLOCK  docs/audits/2026-08-03-night-la-w2-verification.md
   -> class: has no CLOSED-enum <class> token after the date (ADR-101 R3:
      technical/functional/qa/census/verification/ecosystem-audit/
      conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence;
      whole-token longest-match)
pass   docs/audits/2026-08-03-technical-night-la-w2-verification.md
pass   docs/audits/2026-08-03-technical-night-batch-digest.md
```

`night` is not in the ADR-101 R3 closed 11-class enum
(`scripts/validate_hermetization.py:89-98`). Every prior night-batch artifact already resolves
this the same way — `2026-08-02-technical-night-batch-lb-...`, `...-le-library-first`, etc.,
i.e. class `technical`, slug `night-...`.

**Resolution taken:** the `technical` class token was inserted, preserving the brief's intent
(flat, dated, in the existing `docs/audits/`, lane-named) while satisfying the gate. The gate
was NOT weakened, bypassed, or amended. **Every file this night batch writes carries
`2026-08-03-technical-night-<lane>.md`.** Flagged here so the morning architect can rule on
the brief's pattern rather than discover the collision at commit time.

---

## Coverage

**Covered — re-derived live:** all six briefed claim groups; the four merge SHAs in full
including the truncated recovery; hook config + single-verifier proof; the `--write` refusal
run live against the real 212-file tree with an independent before/after digest; collect count
vs the doc-counts pin; the full closure-hygiene set (BACKLOG absence, task-file status,
manifest queue membership, `--check`, `validate_backlog`, `validate_git_backlog`, the 188->186
delta against the pre-arc parent); machine set-equality of the gate roster across four
surfaces; full ship-gate decomposition with the armed-hooks control probe; the terra-artifact
search; the artifact-naming gate collision.

**NOT covered, and why:**
- **`uv sync --locked` fidelity.** Impossible here (uv 0.8.17 vs the `==0.11.19` pin; the
  pinned version is not fetchable). The suite ran on a lock-version-matched venv built outside
  the tree. A version-resolution difference between that and a true `uv sync --locked` cannot
  be excluded.
- **Ship-gate GREEN.** Not witnessable from this container at all (absent siblings, absent
  gitignored `ecosystem/<repo>/state.yaml`, `.`-less directory name). Section 6 states what
  WOULD have to be true instead of asserting the verdict.
- **Whether terra ran.** Only its artifact absence is a fact; the review itself is outside
  this repo's evidence.
- **The pre-commit hooks' real behaviour under `uv run --locked`.** Every `language: system`
  hook entry begins `uv run --locked`, which aborts in this container, so the hooks cannot be
  exercised end-to-end here even when armed. The armed-hooks probe in section 6 measured
  `hooks_armed` presence only, and `.git/hooks/` was restored to its as-cloned state
  (samples only) afterwards — no leftovers.
