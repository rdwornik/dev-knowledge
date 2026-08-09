# Night lane N5 — Library-first sweep: what we hand-rolled that we should not have

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** night-n5-library-first-sweep
- **Batch:** night batch 2026-08-09, manifest `docs/audits/2026-08-09-technical-batch-night-manifest.md` (lane N5)
- **Runtime:** CLOUD, no operator reachable. Model opus, effort xhigh, execute-mode.
- **Charter:** the standing posture — stdlib > established dependency > stabilized project > industry
  pattern; hand-rolling justified only by a MEASURED divergence. `"We already built it" is never
  evidence it should exist.`
- **What this is:** evidence + verdicts. **Zero rows born, zero adoptions made, zero installs, zero
  code edited, no `pyproject.toml` touched.** One new path: this file.
- **Network:** PyPI reachable (release versions/dates below are **verified tonight**). GitHub API
  returns 403 through the proxy — every star-count / commit-activity / maintenance-health claim is
  therefore **UNVERIFIED** and is tagged where it appears.

---

## 0 · Bottom line

Three findings, in order of how much they change the picture.

1. **The premise that audit.py is full of generic linting is FALSE, and the inverse is true.**
   0 of its 41 checks is generic lint — every one encodes ADR-cited methodology policy. Meanwhile
   the generic hygiene layer a maintained tool *does* provide is **absent entirely**: zero standard
   `pre-commit-hooks`, zero secret scanning of any kind. The gap is not "we rebuilt a tool", it is
   "we never installed the tool, and built policy instead."

2. **The highest-value swaps tonight are already-ruled adoptions that were never propagated.** The
   2026-08-03 lane ruled `markdown_it` ADOPT for fence handling and landed it at one site. Two
   further sites carrying the same defect class were never examined; measured tonight, they diverge
   from CommonMark on **32** and **8** of 1,633 corpus files. A second 2026-08-03 ADOPT
   (`yaml.safe_load` in `gen_claude_rosters.py`) is still unimplemented. Both need no new
   distribution — the dependency is already declared and paid for.

3. **The most-wanted automation target — batch/lane orchestration — is already thin, and the
   loudest real problem in that area is not a library problem.** The closure-proposal store writes
   to gitignored `logs/` on one machine, so the evidence base for every closure is invisible to
   exactly the cloud sessions being asked to do the work. §7 proposes the durable shape.

A fourth, environmental: **this container cannot run the gate mesh at all.** `uv` here is 0.8.17
against a pinned `==0.11.19`, and all 16 pre-commit entries are `uv run --locked python …`. This is
the **second witnessed instance** of the pin class flagged open at `docs/audits/2026-08-08-technical-library-research.md` item 8c.

---

## 1 · What this sweep stands on (do-not-relitigate register)

This ground has been worked five times. Verdicts already ruled, honoured here and **not reopened**:

- **`python-frontmatter` — REJECTED, "OUT, full stop"** (0/20 byte-identical; `sort_keys=True`
  reorders every key, none of it configurable). `docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md:38,96`
- **`ruamel.yaml` — REJECTED as a swap** (passes fidelity at `width=4096`, but `gen_task_tree.py`
  templates frontmatter fresh rather than round-tripping, so there is nothing to swap). Same file, `:39-40,99-114`
- **`graphlib` / `networkx` — LEAVE** (0 mismatches over 24,000 randomized graphs — measured
  NON-divergence). `docs/audits/2026-08-03-technical-night-le-library-first.md:51,146-159,177`
- **`GitPython` / `pygit2` / `dulwich` — REJECTED** (GitPython shells out to git, so it inherits the
  same env problem and "does not even solve it"). `docs/audits/2026-08-08-technical-library-research.md:285-293`
- **`github-slugger` — KEEP hand-rolled** (abandoned: last release v0.0.3, 2022-12-12). `2026-08-03:35`
- **`tenacity`, `pathspec`, SARIF, `vale`, `commitlint`/`gitlint`, `cosmic-ray`, Danger.js,
  Vale/markdownlint plugins, Sphinx-include class, doctest class — REJECTED** at the cited locators.
- **Already correct, re-confirmed, not re-proposed:** `pydantic` (ADR-109 schema), `pandas`,
  `argparse`, `difflib`, `click`, `tomllib`, `rich`, `packaging`.

**Standing scope exclusions I did not cross** (`2026-08-06:19-21`, `2026-08-08:19-21`): no
agent-orchestration frameworks, no standalone worktree managers, no external SaaS, no re-run of the
vale / commitlint / gitlint evals.

**What the prior lanes explicitly left unreached** (`2026-08-03:205-216`) and this lane therefore
treats as live ground: `deploy/lived_sandbox/`, the ~20 `_git()`/`_run()` wrappers, the
`plugins/tier1-lifecycle/` twins, and the `.ps1` surfacing scripts.

---

## 2 · Measured inventory

Sizes and maintenance are **full-history** numbers. The clone arrived **shallow** (history began
2026-08-04, 310 commits); I ran `git fetch --unshallow` first, giving **4,723 commits**. Any
per-file count taken before that would have been a floor, not a measurement.

Whole surface: **98 Python modules** across `scripts/ deploy/ ecosystem/ plugins/` —
**36,806 LOC production** (27,459 in `scripts/`, 9,347 outside), **38,317 LOC tests**,
**2,441 test functions**. Tests outweigh production code 1.04:1.
Corpus: **1,633 markdown files** — 442 audits, 250 tasks, 83 ADRs, 26 intakes, 105 handoff bundles
(686 files), 12 protocols.

Top mechanisms by maintenance cost (commits all-time / last 30d):

| mechanism | LOC | tests | commits all / 30d | first seen |
|---|---|---|---|---|
| `scripts/audit.py` (41 checks) | 5,072 | 196 | **129 / 56** | 2026-05-15 |
| `scripts/fleet_parity.py` | 2,049 | 77 | 24 / 24 | 2026-07-13 |
| `scripts/gen_task_tree.py` | 1,215 | 57 | 19 / 19 | 2026-07-27 |
| `scripts/fleet_analytics.py` | 1,263 | 64 | 3 / 3 | 2026-07-22 |
| `scripts/enforcement_coverage.py` | 1,180 | 44 | 10 / 3 | 2026-07-03 |
| `scripts/gen_handoff.py` | 878 | 52 | 12 / 6 | 2026-07-04 |
| `scripts/verify_handoff_probes.py` | 697 | 86 | 16 / 5 | 2026-06-13 |
| `deploy/carrier_floor.py` | 946 | 39 | 21 / 17 | 2026-06-29 |
| `scripts/worktree_import_proof.py` | 560 | 37 | 7 / 7 | 2026-08-07 |
| `scripts/propose_closures.py` (+plugin twin) | 441 + 462 | 73 | 7 / 4 | 2026-06-02 |

`audit.py` is the centre of gravity by every measure — largest, most-tested, most-churned (43% of
its lifetime commits landed in the last 30 days).

Two corpus facts that change what a schema validator could bind to (**net-new measurement**):

| corpus | files | with YAML frontmatter |
|---|---|---|
| `tasks/*.md` | 249 | **248 (99.6%)** |
| `docs/audits/*.md` | 442 | **57 (12.9%)** |
| `docs/decisions/ADR-*.md` | 83 | **1 (1.2%)** |

The contract's framing ("~400 audits, 85 ADRs") assumes a uniform frontmatter surface. There isn't
one. ADRs carry a **bullet-list header** (`- **Status:** …`), not frontmatter. This is decisive for §6.

---

## 3 · Ranked verdict table

Ranked by value-per-unit-cost. `Conf` = confidence in the verdict.

| # | mechanism | verdict | candidate | migration cost | what it saves | conf |
|---|---|---|---|---|---|---|
| 1 | `audit.py:2714` `_strip_code_regions` fence regex | **REPLACE** | `markdown_it` (already declared) | ~10 lines, 1 file; blast radius = `check_import_edges` only | correctness on **32/1,633** files measured tonight; the class is already ADOPT-ruled | high |
| 2 | `validate_doc_structure.py:113` `_nonfence_lines` toggle | **REPLACE** | `markdown_it` (already declared) | ~10 lines, 1 file; blast radius = `check_doc_structure` | correctness on **8/1,633** files | high |
| 3 | `gen_claude_rosters.py:61-73` `_frontmatter_field` regex | **REPLACE** | `yaml.safe_load` (already declared) | ~12 lines, 1 file | ruled ADOPT 2026-08-03, never landed; key class `[a-z0-9-]+` matches **no underscore key** | high |
| 4 | generic file hygiene (absent) | **ADOPT (new)** | `pre-commit-hooks` 6.0.0 | 6 config lines, no code; prospective-only | the only hygiene class with **zero** coverage today; 143 files trailing-WS, 51 no-final-newline | high |
| 5 | secret scanning (absent) | **ADOPT (new)** | `detect-private-key` (in #4) | included in #4 | **no secret scanning of any kind exists** — no bespoke shadow, a hole | high |
| 6 | `deploy/manifest-v*.yaml` + workflow validation | **ADOPT-cand.** | `check-jsonschema` 0.37.4 | schema authoring for 6 manifests; workflows need none | already ADOPT-cand. 2026-08-08 item 8b; unchanged by tonight | med |
| 7 | 8 hand-rolled `sys.argv` CLIs | **WRAP** | `argparse` (stdlib, already the plurality) | ~15 lines each, mechanical | idiom convergence: 25 argparse / 11 click / 8 hand-rolled / 0 mixed | med |
| 8 | `_git()` in **16** production files, inconsistent signatures | **WRAP (internal)** | *no library* — GitPython already REJECTED | one shared helper; blast radius wide (16 files) | de-duplication only; **not** a library question | med |
| 9 | repo-root discovery re-derived in 60+ files, 5 idioms | **WRAP (internal)** | shared helper beside `gitenv.py` | mechanical, wide | consistency; no defect class demonstrated | low |
| 10 | closure-proposal store in gitignored `logs/` | **REPLACE (shape)** | git-tracked artifact — see §7 | design ruling needed first | makes closure evidence visible to cloud sessions | high |
| 11 | `audit.py`'s 41 policy checks | **KEEP, justified** | none exists | — | 0/41 are generic lint (§5.1) | high |
| 12 | markdown link / anchor checking | **KEEP, justified** | `lychee` — measurably not worth it | — | living docs: 29 local + 233 anchor links, **0 real breaks** (§5.2) | high |
| 13 | frontmatter parsing + doc schemas | **KEEP, justified** | `python-frontmatter` (ruled OUT), `jsonschema` | — | no uniform corpus schema exists to bind to (§5.3) | high |
| 14 | handoff templating (`str.replace` + FILL-IN splice) | **KEEP, justified** | Jinja2 | — | the splice preserves hand edits byte-for-byte; no engine offers that (§6.1) | med |
| 15 | worktree provisioning (`worktree_seed.py`) | **KEEP, justified** | `git worktree` — *already delegated* | — | it does not reimplement git; it copies 3 untracked paths (§6.2) | high |
| 16 | `propose_closures.py:64` fence/quote stripper | **KEEP, unjustified→justified** | `markdown_it` | — | handles `~~~` **and** equal-length inline pairing; operates on commit messages, not markdown | high |
| 17 | `.worktreeinclude` (3-line manifest) | **KEEP, unjustified** | git sparse-checkout | not worth moving | bespoke by accident, but 3 lines; flagged, not actioned | med |
| 18 | EOL policy | **KEEP — already delegated** | `.gitattributes` | — | correctly git-native already; nothing bespoke shadows it | high |
| 19 | formatting / typing / linting | **KEEP — already delegated** | `ruff` v0.15.5 pinned | — | pin == `[tool.ruff] required-version` floor; no bespoke shadow found | high |
| 20 | `mkdocs` / doc-site generation for the 8 generators | **REJECT** | `mkdocs` 1.6.1 | — | generators emit *marker blocks into existing files*, not a site; no overlap (§6.3) | high |

---

## 4 · The three swaps I would do first

### Swap 1 — propagate the already-ruled `markdown_it` fence adoption to the two unexamined sites

This is the strongest recommendation in the sweep because **the adoption argument is already banked
and ruled**; only the propagation is missing.

On 2026-08-03 the L-E lane ruled `markdown_it` **ADOPT** for fence handling, on the measured ground
that the `^```` toggle "tried to enumerate where NOT to rewrite and missed every fence shape but
one" (`scripts/normalize_headers.py:59-65`). It landed in `normalize_headers.py` and
`toc/generator.py`. `coherence_enumerator.py` was measured and correctly LEFT (1 divergence in 1,493).

**Two more sites were never examined.** Measured tonight against a spec-faithful CommonMark oracle
(stdlib, written from CommonMark §4.5 — deliberately *not* an install; this is the same
oracle-vs-matcher pattern `protocols/STANDING_RULINGS.md` uses for `glob`), over all 1,633 corpus files:

```
site                                              disagrees with CommonMark on
audit.py:2714  _strip_code_regions                32 / 1,633 files
validate_doc_structure.py:113  _nonfence_lines     8 / 1,633 files
```

Why they fail, distinctly:
- `audit.py` anchors at **column 0** (`(?ms)^```…^```), so a fence indented 1–3 spaces — legal
  CommonMark, present in **24 files** including `.claude/commands/override.md` and `lane-boot.md` —
  is never stripped, and its contents leak into the `@import` scan that `check_import_edges` gates on.
- `validate_doc_structure` toggles on any `lstrip().startswith("```")`, so it is blind to `~~~`
  (1 file) and inverts on a 4-backtick fence's inner run (4 files).

Corpus fence shapes measured: 1 file with `~~~`, 24 with 1–3-space indented fences, 4 with 4+-backtick fences.

**Cost:** ~10 lines per site, one file each, no new dependency (`markdown-it-py>=4.0` is already in
`[dependency-groups] dev`). **Rollback:** revert one commit per site. **Blast radius:** `check_import_edges`
and `check_doc_structure` respectively — both already covered by tests.

**One caveat, from this repo's own record:** the 2026-08-03 Codex review raised a HIGH finding
against gating on `heading_open` tokens, because that *excludes* headings inside HTML blocks and can
silently drop TOC entries (`docs/audits/2026-08-03-codex-arc3-mechanical-adoptions.md:30-34`). The
shipped fix uses `markdown_it` only to locate fenced **ranges**. Both swaps here must follow that
same shape — ranges, never token-gating.

### Swap 2 — land the `yaml.safe_load` adoption already ruled for `gen_claude_rosters.py`

Ruled **ADOPT** on 2026-08-03 (`docs/audits/2026-08-03-technical-night-le-library-first.md:46,80-98`)
with a reproduced defect: the sibling regex key class `[a-z0-9-]+` **cannot match any underscore-bearing
key**, and 5 of 6 probes diverged from `yaml`. Its twin `gen_intake_index.py` **was** migrated — its
docstring now records exactly this reason. `gen_claude_rosters.py:61-73` was not, and still carries
the docstring "no yaml dependency for two fields."

This is a ruled adoption sitting unimplemented for six days, in a generator that feeds two
`@`-imported CLAUDE.md fragments read at every session boot. ~12 lines, one file, `pyyaml>=6.0`
already declared.

### Swap 3 — adopt the standard `pre-commit-hooks` set (the genuinely absent layer)

**Verified tonight:** `.pre-commit-config.yaml` has exactly one remote repo — `astral-sh/ruff-pre-commit`
@ v0.15.5. Every other hook is `repo: local`. Grep for the standard set returns **0**: no
`trailing-whitespace`, no `end-of-file-fixer`, no `check-yaml`, no `check-json`, no
`check-merge-conflict`, no `check-added-large-files`, no `detect-private-key`. There is **no secret
scanning of any kind** — bespoke or delegated. Contract area #7 asked whether anything bespoke
shadows a tool already run; the answer is that nothing shadows it because nothing is there.

Measured over 1,975 tracked files: **143** carry trailing whitespace, **51** lack a final newline,
**2** exceed 500 KB (`JOURNAL.md` 2.18 MB — deliberate and append-only; `tests/fixtures/lived-workflow/arc-silent.jsonl` 0.69 MB).

The 143/51 numbers are *not* an argument for a bulk rewrite — most sit in immutable audits that
policy forbids editing. They are the argument for adopting these hooks **prospectively**, which is
what pre-commit does natively (staged files only) and which this repo already has precedent for:
`validate-hermetization` is explicitly "prospective-only on staged ADDs (existing files
grandfathered)". `check-added-large-files` needs an exclude for `JOURNAL.md`.

`pre-commit-hooks` **6.0.0**, released **2025-08-09** (PyPI-verified tonight). Maintenance health
beyond that release date is **UNVERIFIED** — GitHub API is 403 through this proxy.

**Recommended minimum:** `detect-private-key`, `check-added-large-files`, `check-merge-conflict`,
`check-yaml`, `check-json`. I would hold `trailing-whitespace` and `end-of-file-fixer` back — they
*rewrite* files, and a rewriting hook interacts with the append-only and immutability invariants in
ways that deserve their own ruling (see `## Needs a ruling`).

---

## 5 · The three I looked at and concluded should stay hand-rolled

### 5.1 — `audit.py`'s 41 checks. KEEP, justified.

The contract asked how much of this is generic linting a maintained tool already does. Measured
answer: **none of it.**

I enumerated all 41 and spot-verified the three whose names most suggest generic hygiene:

- `check_dot_prefix_discipline` — "Root config files dot-prefixed unless on exception list (**ADR-59 D1**)"
- `check_canonical_md_visibility` — "Mandatory canonical files present + correct ALL-CAPS casing (**ADR-59 D2**)"
- `check_boot_byte_budget` — an **18,000-byte** ceiling on `protocols/HANDOFF_BOOT.md`, "ruled 2026-07-31", single-sourced from `assemble_paste.HANDOFF_BOOT_BYTE_BUDGET`

Every one is an ADR citation with a repo-specific constant. The remaining 38 are the same shape:
`journal_spine_anchor`, `silent_rule_ratchet`, `membership_agreement`, `floor_integrity`,
`fleet_parity`, `task_tree_coherence`. No off-the-shelf tool encodes "ADR-59 D2" — the policy content
*is* the value, which is precisely the case the contract says not to propose replacing.

A subagent classified 14 of the 41 as "generic". That label meant *portable across fleet repos*, not
*off-the-shelf-replaceable* — I checked and am correcting it here rather than passing it through.

**Honest caveat:** 5,072 LOC and 56 commits in 30 days is a real carrying cost, and this verdict does
not address it. It says the cost is not recoverable by adopting a library. Decomposition is a
separate question and I am not opening it.

### 5.2 — Markdown link / anchor checking. KEEP (i.e. do not adopt `lychee`) — and this narrows an open candidate.

`lychee` v0.24.2 was left an **ADOPT-candidate** on 2026-08-06 for (a) local links and (b) heading
anchors. I measured the population it would act on, which the prior lane did not.

Raw scan looks damning: **157 broken local links, 24.4%**. Split by whether the file may ever be
edited, it inverts:

```
LIVING docs (CLAUDE/ARCH/VISION/CONTRIBUTING/BACKLOG/protocols/templates/tasks/.claude)
    local links   29   broken 0 real
    anchor links 233   broken 0 real
IMMUTABLE artifacts (docs/audits, docs/handoffs, archives, ecosystem)
    local links  615   broken 153
```

Both "0 real" figures survived adversarial checking:
- The 4 living-doc local hits are **false positives of my own extractor** — `[#429](b)` and
  `[#430](a)` in `protocols/STANDING_RULINGS.md` are citation prose, not links.
- The 4 living-doc anchor hits (`#update-cadence-1`, `#process-1`, `#rules-1`,
  `#when-a-lesson-becomes-a-rule-1`) are GitHub's **duplicate-heading disambiguation suffix**. I
  confirmed each of those four headings appears **exactly twice** in `PLAYBOOK.md`. The links are correct.

The anchor measurement used **this repo's own `_slugify`** (`scripts/toc/generator.py:31-42`,
already measured 1029/1030 on real headers), replicated faithfully — not a third-party slugger, and
notably `github-slugger` is already REJECTED as abandoned.

So the entire broken-link population lives in artifacts that ADR-101 and CLAUDE.md §4 forbid editing.
A link checker would emit 153 findings that policy prohibits fixing, and 0 that it permits.
**Measured non-divergence on the actionable surface: adopting `lychee` for (a) or (b) buys nothing today.**
That is a stronger statement than the prior lane could make, and it is offered as a narrowing of
their open candidate, not a contradiction of it.

### 5.3 — Frontmatter parsing and document schemas. KEEP, justified — with new evidence.

The parser question is settled and I am not reopening it (`python-frontmatter` OUT; `ruamel` no
simplification). What was **not** settled is the contract's actual question: what a real *schema
validator* would buy across the corpora.

Measured: there is no corpus-wide schema surface for one to bind to.

```
tasks/*.md              249 files   248 with frontmatter (99.6%)  — uniform: id,title,status,priority,size,theme,story,generates
docs/audits/*.md        442 files    57 with frontmatter (12.9%)  — and those 57 are batch manifests (batch/status/closed_by), not audits-in-general
docs/decisions/ADR-*.md  83 files     1 with frontmatter ( 1.2%)  — ADRs use a bullet-list header, not YAML
docs/intake/*.md         26 files     — intake-id/status/origin/consumed-by
```

A `jsonschema` (4.26.0, PyPI-verified) or pydantic model would govern **`tasks/` only** — and
`tasks/` is *already* schema-gated by `validate_backlog.py` (ADR-66) plus `gen_task_tree.py --check`
and the `task_tree_coherence` FAIL check. Adding a schema library there duplicates a working gate;
adding it anywhere else requires first *inventing* frontmatter for 385 audits and 82 ADRs, which is
a doctrine change, not a library adoption.

`pydantic` is already the right tool and is already used correctly for exactly the surface that has
a real schema (ADR-109, `ecosystem/schema/desired_state.py`, 650 LOC, `extra="forbid"`, 19 enums).

---

## 6 · The remaining areas, briefly

### 6.1 Handoff / bundle engine — KEEP, justified

`gen_handoff.py` (878 LOC, 52 tests) renders via `str.replace` on template files, then **splices
FILL-IN regions byte-for-byte from the prior bundle** so hand-written architect content is never
clobbered (`:656-678`). That splice is the mechanism's whole point and no template engine provides
it — Jinja2 renders forward, it does not preserve a human's edits in the output it overwrites.

Probes are **not executed** — `verify_handoff_probes.py` checks *structural resolvability* by
operator ruling (`:2-8`), through a 7-rung classifier including an anti-bluff rung. So "generic
templating plus a test runner" does not describe it: there is no test run, deliberately.
Seal verification is a string comparison of the bundle's declared `Slug` row against its directory
name (`:329-353`) — 25 lines, correctly not a library.

**One real finding here:** this subsystem alone carries **three** CLI idioms — click
(`gen_handoff`, `assemble_paste`, `seed_runbook`), argparse (`verify_handoff_probes`,
`preflight_contract`), and hand-rolled `sys.argv` (`check_seal_identity`,
`validate_residual_completeness`). Row 7 of §3.

### 6.2 Batch / lane orchestration — KEEP, justified; already thin

This is the area the operator most wants automated, so concretely: **it does not reimplement git.**
`worktree_seed.py` never calls `git worktree add` — Claude Code's own `claude --worktree` does, and
the script only reads repo state and emits copy commands for the 3 untracked paths in
`.worktreeinclude` (`.env`, `.claude/settings.local.json`, `ecosystem/*/state.yaml`). Teardown
(`safe_remove.py`) analyses reverse-dependencies and leaves removal to the caller.
`/lane-integrate` is a documented serial `git merge --no-ff` walk plus a 5-item checklist. The
git-native primitives are already delegated; what remains is policy.

`.worktreeinclude` is **KEEP, unjustified** — a 3-line bespoke manifest where git sparse-checkout
exists. Flagged per the contract's instruction to name accidental bespoke even when replacing is not
worth it. It is three lines; I would not move it.

The one non-thin piece is `worktree_import_proof.py` (560 LOC, 37 tests, 7 commits in 7 days) — it
generates a test on the fly, strips `VIRTUAL_ENV`/`PYTHONPATH`, and spawns a child pytest to prove
imports resolve against the right tree. No library does that; it is the `[#502]` sys.path substrate
question wearing a different hat, and that question is already **OPEN** with shapes A/B/C costed
(`2026-08-08` item 5). I add nothing and defer to it.

### 6.3 Index / doc generation — KEEP, justified

Eight generators, all emitting **marker-delimited blocks into existing living files** (or JSON
manifests) — not a documentation site. `mkdocs` (1.6.1, last release **2024-08-30**, PyPI-verified —
two years stale) subsumes none of it: there is no site to build. Six of the eight are already
regen-and-diff gated by a pre-commit hook, which is the correct pattern and uses stdlib `difflib`.

**Two are unguarded** and this is worth naming: `gen_doc_counts.py` (writes `ecosystem/doc-counts.md`)
and `generate_floor.py` (writes `.claude/CLAUDE-FLOOR.md` + sidecars). `generate_floor` is
operator-only by design and its output *is* hash-guarded by `floor-hash-verify`. `gen_doc_counts.py`
has a `--check` mode at `:136-150` and no hook calling it — the contract's "at least one unguarded by
any hook". That is a 6-line config addition, not a library question.

### 6.4 CLI / plumbing — WRAP, low priority

Precise census of all 98 modules (0 import both argparse and click):

```
argparse                     25
click (no argparse)          11   audit.py, deploy/tool.py, fleet_parity.py, gen_handoff.py, +7
hand-rolled sys.argv          8   check_backlog_commit_msg, check_backlog_filing, check_seal_identity,
                                  coherence_nudge, normalize_headers, silent_rule_detector,
                                  validate_residual_completeness, lived_sandbox/cli
entry point, no parsing      22
```

The contract cites today's precedent of ~55 lines deleted by delegating to `argparse`. The same
shape exists in those 8 files — but 6 of them are **hook entry points** taking either zero args or
one commit-message path, where `sys.argv[1]` is arguably the honest expression. Realistic saving is
~40–60 lines total. Worth doing opportunistically; not worth a lane.

Also measured: `_git()` defined in **16** production files with three incompatible signatures;
repo-root re-derived in 60+ files across **5** distinct idioms; **229** `print()` calls across 54
files with stdlib `logging` used only in `deploy/` and `audit.py`. All three are internal
duplication, not missing libraries — and the library answer for `_git` (GitPython) is already
**REJECTED**. `typer` (0.27.1, PyPI-verified) is the natural CLI consolidation target *if* the
surface ever grows, which is what intake #23 P4 already says; nothing tonight changes that.

---

## 7 · The closure-proposal store — the durable shape (contract area #8)

**Measured state.** `propose_closures.py:380-384` writes `logs/PROPOSALS-<YYYY-MM-DD>.md`.
`.gitignore:26` ignores `logs/PROPOSALS-*.md` (confirmed via `git check-ignore -v`). The **only**
tracked file in `logs/` is `TOKEN-LOG.md`. `review_closures.py:198-200` reads the store by
`sorted(glob("PROPOSALS-*.md"))[-1]`. Eleven further load-bearing artifacts are gitignored the same
way (`FLEET-HEALTH.md`, `ENFORCEMENT-COVERAGE.md`, `PARITY-EVENTS.jsonl`, `OVERRIDES.md`, …).

**Why this is a defect and not just a choice.** A proposal record carries `head_commit`,
`since_commit`, `window_commits`, and per-item evidence SHAs — it is *derived from committed git
history*, so it is reproducible, and it is the evidence base a `/review-closures` decision rests on.
Today it exists on exactly one machine. A cloud session — like this one — cannot see it, cannot
audit a past closure decision, and cannot regenerate one for a window whose `since_commit` it has no
record of. `latest()` also silently picks the newest file, so a stale run and a fresh run are
indistinguishable to the reader.

**Proposed durable shape** (design only — I built nothing):

1. **Keep the store derived, make the *decision* durable.** Do not commit `PROPOSALS-*.md`; it is
   regenerable from `(since_commit, head_commit)`. Commit instead a small append-only
   **decision ledger** — `logs/CLOSURE-DECISIONS.jsonl`, tracked — one line per reviewed proposal:
   `{proposed_at, head_commit, since_commit, task_id, tier, evidence_shas, verdict, decided_by}`.
   `.jsonl` matches the ruled `logs/` naming convention (UPPERCASE-KEBAB stem, extension honest to
   format) and the existing `PARITY-EVENTS.jsonl` precedent.
2. **Make regeneration explicit.** Have `propose_closures.py` accept `--since <sha>` so any session,
   anywhere, can reproduce a prior window byte-for-byte from the ledger's `since_commit`.
3. **Make staleness visible.** `review_closures` should refuse a proposals file whose `head_commit`
   is not the current HEAD, rather than accepting the newest file by filename sort.

This keeps the append-only doctrine (a ledger, never edited), adds ~1 tracked file, and makes closure
evidence reviewable from a cloud session. **It needs an operator ruling** — see below.

---

## 8 · Environment findings (unprompted but load-bearing)

1. **The gate mesh cannot run in this container.** `uv --version` → **0.8.17**; `pyproject.toml:25`
   → `required-version = "==0.11.19"`. All 16 pre-commit entries are `uv run --locked python …`, so
   every one fails before reaching its script. `pre-commit` is not installed and `.git/hooks/` holds
   only samples, so nothing was bypassed tonight — but nothing could have been enforced either. This
   is the **second witnessed instance** of the class left OPEN at `2026-08-08` item 8c (`mise`,
   verdict open). Two instances in six days is the shape that usually earns a ruling.
2. **The clone arrives shallow.** History began 2026-08-04 (310 commits) until I unshallowed to
   4,723. Any night lane measuring "commits touching X" without unshallowing first will silently
   report a floor as a measurement. Worth adding to the cloud-lane preamble.

---

## 9 · Verified external facts

PyPI JSON API reachable; **latest version and release date verified tonight**. GitHub API 403
through the proxy → all maintenance-health, star, and commit-activity claims **UNVERIFIED**.

```
pre-commit-hooks    6.0.0    2025-08-09      python-frontmatter  1.3.0    2026-05-20
GitPython           3.1.58   2026-08-04      jsonschema          4.26.0   2026-01-07
typer               0.27.1   2026-08-03      invoke              3.0.3    2026-04-07
mkdocs              1.6.1    2024-08-30      pymarkdownlnt       0.9.39   2026-07-12
detect-secrets      1.5.0    2024-05-06      pathspec            1.1.1    2026-04-27
tach                0.35.0   2026-05-12      griffe              2.1.0    2026-06-19
yamllint            1.38.0   2026-01-13      check-jsonschema    0.37.4   2026-06-29
mdformat            1.0.0    2025-10-16      linkcheckmd         1.4.0    2021-02-28
```

`mkdocs` (2024-08-30), `detect-secrets` (2024-05-06) and `linkcheckmd` (2021-02-28) are stale by
release date alone — none is recommended above.

**Method note.** Where a measurement needed a library this container lacks, I did **not** install it.
The CommonMark oracle in §4 is stdlib written from the spec, and the slugger in §5.2 is this repo's
own `_slugify` replicated faithfully. Both are oracles used to *prove* a hand-rolled matcher, which
is the pattern `protocols/STANDING_RULINGS.md` already sanctions for `glob`. Consequently the §4
divergence counts should be re-measured against `markdown-it-py` itself before the swap lands; I
expect them to hold or grow, but that expectation is **UNVERIFIED**.

---

## Needs a ruling

1. **Do rewriting pre-commit hooks get in?** §4 swap 3 recommends `detect-private-key`,
   `check-added-large-files`, `check-merge-conflict`, `check-yaml`, `check-json` — all read-only. I
   deliberately held back `trailing-whitespace` and `end-of-file-fixer` because they **rewrite staged
   files**, and this repo has append-only files (`LESSONS.md`, `logs/TOKEN-LOG.md`), immutable
   classes (ADRs, transcripts, handoffs, audits), and a `PreToolUse` immutability guard. A rewriting
   hook that touches an immutable artifact during an amendment commit is a doctrine collision. Ruling
   wanted: read-only set only, or the full set with an `exclude` for the immutable paths?

2. **Does the closure-decision ledger (§7) get born, and as what?** The proposal adds one tracked
   append-only `logs/CLOSURE-DECISIONS.jsonl`. That is a new load-bearing path, which CLAUDE.md §5
   item 5 says needs a navigation/growth check, and ADR-101's tree-seal governs new file classes
   under `logs/`. I did not create it. Ruling wanted: ledger as proposed, some other durable shape,
   or leave the store ephemeral and accept that cloud sessions cannot audit closures?

3. **Is the uv-pin class ready for a decision?** Two witnessed instances now (2026-08-08 item 8c, and
   tonight). The open question stated there — "can `mise` fetch a uv release that `uv self update`
   cannot?" — is answerable in one container run, and tonight's container is a second data point that
   the failure is not a one-off. Ruling wanted: schedule the one-run experiment, or accept that cloud
   lanes run without the gate mesh and say so explicitly in the lane preamble.

4. **Who owns propagating a ruled adoption?** Swaps 1 and 2 are both *already-ruled* ADOPTs that
   landed at some sites and not others — `markdown_it` at 2 of 4 fence sites, `yaml.safe_load` at 1
   of 2 frontmatter readers. There is no organ that notices a ruled adoption is only partly applied;
   both gaps were found by reading, not by a gate. Ruling wanted: is "an adoption ruling names all its
   sites, and completion is checked" worth an enforcement leg, or is per-lane reading the accepted
   mechanism?

5. **`docs/audits/` frontmatter (informational, no action requested).** 57 of 442 audit files carry
   frontmatter and all 57 are batch manifests. If audits are ever meant to be machine-queryable, that
   is a doctrine decision with a 385-file backfill behind it — I flag it only because §5.3's verdict
   would change if it were ruled.
