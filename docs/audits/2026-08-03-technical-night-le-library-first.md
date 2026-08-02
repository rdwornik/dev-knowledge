# Night batch 2026-08-03 · lane L-E — library-first sweep, increment 2

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-le-library-first
- **Status:** PROPOSAL — read-only night batch, unattended. No repo file was edited, no dependency
  installed, no swap performed. Every experiment ran in a scratchpad venv importing the repo's own
  unmodified functions read-only; this report file is the only thing written.
- **Base:** `main` = `c7628a3` (`Merge branch 'docs/journal-wrap-w2-475-474'`). Working tree verified
  clean before and after (`git status --porcelain` empty).
- **Method:** read-only. Interpreter = the scratchpad `testenv` (CPython 3.12.3) — `uv run --locked`
  refuses on this box (pyproject pins uv `==0.11.19`, installed 0.8.17). Every row below is either a
  live differential experiment against a stdlib/library oracle or a source-quoted stdlib contract.
- **Increment contract:** this is the NEXT increment after
  `docs/audits/2026-08-02-technical-night-batch-le-library-first.md`. Prior rows are re-verified in
  §"Re-checked from 2026-08-02", not re-reported.

> **FILENAME WARNING (read before committing).** The mandated filename
> `docs/audits/2026-08-03-night-le-library-first.md` **is refused by the live `validate-hermetization`
> pre-commit gate** (ADR-101 R3). Verified by running the repo's own validator:
> `rule_b_violation('docs/audits/2026-08-03-night-le-library-first.md')` returns
> *"class: ... has no CLOSED-enum <class> token after the date (ADR-101 R3:
> technical/functional/qa/census/verification/ecosystem-audit/conformance-nightly-digest/
> changelog-review/codex/fresh-eyes/incident-evidence)"*. The same probe on
> `2026-08-03-technical-night-le-library-first.md` returns OK. The brief named this exact path, so it
> was honored; **rename to insert the `technical-` class token before staging**, or the commit blocks.

---

## Verdict

The version-compare defect this lane reported on 2026-08-02 was **fixed overnight at one of six
sites** (`fleet_parity.py`, commit `a7e42a30`) and `packaging` is now a **declared** dependency
(`pyproject.toml:37`) — which makes the same swap free everywhere else. Five candidates survive,
and **every single adopt row costs zero new distributions**: three ride already-declared or
already-locked packages (`packaging`, `pyyaml`, `markdown-it-py`), two are one-word stdlib fixes.
The four `leave` rows are leaves *on measured evidence*, not on taste: the codemap's recursive DFS
matched stdlib `graphlib` on **24,000 randomized graphs** (so last night's networkx SWAP is
downgraded), and the 198-line pre-commit splice engine handled the real config plus 7 of 8 adversarial
YAML shapes. The recurring shape is not missing libraries — it is **stale "no dep" rationales**: three
separate hand-rolls justify themselves by avoiding a dependency that the repo already declares.

## Ranked table — 10 rows, highest leverage first

| # | hand-rolled spot | what it does | candidate | maturity evidence | cost | risk | recommendation |
|---|---|---|---|---|---|---|---|
| 1 | `scripts/changelog_sentinel.py:45-52` | dotted-int tuple version parse + `is_newer` compare for tool changelogs | `packaging.version.Version` | DECLARED dep, `pyproject.toml:37`; PEP 440 reference impl | S | low | adopt - PROVEN wrong verdict: GA `2.0.15` reads as NOT newer than reviewed `2.0.15rc1`, so the sentinel silently never fires |
| 2 | `scripts/gen_claude_rosters.py:61-73` + `scripts/gen_intake_index.py:47-65` | two hand-rolled frontmatter readers, both justified by "no yaml dep" | `yaml.safe_load` | DECLARED dep `pyyaml>=6.0`, `pyproject.toml:33`; already used at `audit.py:460`, `canonical_freshness_gate.py:52` | S | low | adopt - 5 of 6 probes diverge from yaml (quotes kept, folded scalar returns `>`, duplicate key takes FIRST); the sibling regex cannot match ANY underscore key |
| 3 | `scripts/toc/generator.py:47-50` | `in_fence = not in_fence` toggle on ``` to hide headings inside code | `markdown_it.MarkdownIt` | in `uv.lock:135` v4.2.0 (2026-05-07) via rich; 67 releases, MIT, Google Assured OSS | S-M | low | adopt - toggle is blind to `~~~` fences and inverts on nested 4-tick fences; 8 of 1493 corpus files diverge, and this hook SHIPS to consumers |
| 4 | `scripts/normalize_headers.py:32,69` | same naive ``` toggle, guarding a hook that REWRITES files | same import as row 3 | see row 3 | S | low | adopt - rides row 3; PROVEN to rewrite `## <date>` inside a `~~~` fence, contradicting its own docstring |
| 5 | `scripts/boundary_headers.py:240` | `fnmatch()` decides which files the ADR-boundary metric governs | `fnmatch.fnmatchcase` | same stdlib module; `fnmatch` source shows it calls `os.path.normcase` on both operands | S | low | adopt - the gate is case-SENSITIVE on Linux and case-INSENSITIVE on Windows; also proves `.claude/**/*.md` is a dead glob |
| 6 | `deploy/floor_conformance.py:319` | `shutil.rmtree(onerror=...)` read-only-bit retry | `shutil.rmtree(onexc=...)` | stdlib; installed 3.12.3 docstring: "onerror is deprecated and only remains for backwards compatibility" | S | low | adopt - documented-deprecated stdlib kwarg on a `requires-python>=3.12` repo; a rename plus a one-arg signature change |
| 7 | `scripts/codemap/generator.py:71-86` + `scripts/codemap/mermaid_emit.py:26-56` | two recursive-DFS cycle detectors | `graphlib.TopologicalSorter` (stdlib), NOT networkx | stdlib since 3.9 | M | med | leave - MEASURED CORRECT: 0 mismatches over 24,000 randomized graphs; live codemap is 2 packages, so the recursion limit is unreachable |
| 8 | `deploy/carrier_precommit.py:416-613` | ~198-line surgical text splice preserving consumer YAML comments | `ruamel.yaml` round-trip | measured 20/20 faithful by the 2026-08-01 L4 lane; would be a NEW distribution | L | high | leave - handles the real 178-line config and 7 of 8 adversarial shapes; only flow-style falls back, and pre-commit configs are not written flow-style |
| 9 | `scripts/audit.py:456`, `canonical_freshness_gate.py:48`, `validate_reconciliation.py:109` | `text.split("---", 2)` frontmatter block extraction | internal shared helper (no library) | n/a | S | low | leave - 0 divergences vs the `find("\n---")` variant across 1491 corpus files; 3 lines per site, no library buys it |
| 10 | `scripts/reverse_dep_oracle.py:369-382` | fixed-interval LSP readiness poll with a deadline | `tenacity` | NOT in `uv.lock`; would be a new distribution | S | low | leave - 12 lines wrapping a domain-specific two-consecutive-equal-counts predicate no retry library expresses |

**Adopt: 6 (rows 1-6). Leave: 4 (rows 7-10).** No adopt row adds a distribution to `uv.lock`.

### Note on rank 1 — the defect, reproduced

`parse_version` keeps only the dotted-numeric run (`_VER_RE = r"(\d+(?:\.\d+)+)"` at
`changelog_sentinel.py:38`), so every PEP 440 suffix is discarded. Live output:

```
input                    hand parse_version     packaging.Version
2.0.14-beta              (2, 0, 14)             2.0.14b0
2.0.15rc1                (2, 0, 15)             2.0.15rc1
2.0.14.post1             (2, 0, 14)             2.0.14.post1

is_newer('2.0.15' over reviewed '2.0.15rc1')  hand -> False | PEP440 -> True
```

The last line is the live defect. `/changelog-review` records the reviewed version; if a prerelease
was ever the reviewed value, the GA release that follows compares **equal**, `is_newer` returns
False, and the sentinel goes quiet **permanently for that tool**. This is the same defect family the
2026-08-02 lane found in `fleet_parity._version_tuple` — and the fix that landed there
(`a7e42a30`) already paid the whole cost, because it made `packaging` a declared dependency.

### Note on rank 2 — two stale "no dep" rationales, one fix

`gen_claude_rosters.py:65` says *"no yaml dependency for two fields"*; `gen_intake_index.py:49` says
*"Minimal stdlib parse (no yaml dep -- mirrors gen_audit_index's zero-dep posture)"*. Both premises
are false today: `pyyaml>=6.0` is declared at `pyproject.toml:33` and already imported by 15 modules.
Measured divergence of `_frontmatter_field` against `yaml.safe_load`:

```
double-quoted value        hand='"Run the gate"'   yaml='Run the gate'
single-quoted value        hand="'Run the gate'"   yaml='Run the gate'
folded scalar (>)          hand='>'                yaml='Run the gate over two lines'
quoted value with a colon  hand='"a: b"'           yaml='a: b'
duplicate key              hand='first'            yaml='second'   (YAML: last wins)
```

Separately, `gen_intake_index._FM_KV_RE = r"^([a-z0-9-]+):"` has no `_` in its character class, so
`_FM_KV_RE.match("last_reviewed: 2026-08-02")` returns **None** — every underscore-named frontmatter
key is invisible to it. Both are **dormant** (0/5 command files quote a value, 0/19 intake docs carry
a lost key), but neither output is inert: `commands-repo.md` is `@`-imported into CLAUDE.md, and both
generators are drift-gated by pre-commit (`claude-rosters-freshness`, `intake-index-freshness`), so
the wrong value would be frozen into the agent-instruction surface by a passing gate.

### Note on ranks 3 and 4 — one import, three fence sites

`toc/generator.parse_headers` toggles on `line.lstrip().startswith("```")`. Measured against
markdown-it-py on the ATX-heading basis over 1493 corpus markdown files: **8 files diverge** (worst:
`docs/handoffs/archive/2026-05-09-ai-council-audit-sync/stage1-question.md`, 5 headers found vs 13).
Targeted probes isolate the two causes — a `~~~` fence gets no protection at all, and a 4-tick fence
containing a 3-tick fence inverts the toggle so real code lines are read as headings.

Honest scoping: the **gated** file `protocols/PLAYBOOK.md` agrees exactly (227 = 227 headers), and the
whole corpus contains only 4 tilde fences and 4 four-tick fences — so this is dormant *here*. It is
not dormant *downstream*: `toc-freshness` is a **deployed** methodology hook
(`.claude/methodology-roster.md`), run against consumer documents the hub does not control.

`normalize_headers.py` carries the same class in a worse position — its hook **writes**. Its
docstring promises *"Lines inside fenced code blocks are passed through verbatim"*; measured, a
`## 2026-08-02` line inside a `~~~` fence **is** rewritten to `### 2026-08-02`. (0 live corpus hits;
the indented-fence case is protected only by accident, because `_DATE_ONLY` anchors `##` at column 0.)

Counter-argument acknowledged: extending `_FENCE` to `^(```|~~~)` is a one-character-class fix and
needs no library. The reason to prefer the import anyway is that it is **free** (markdown-it-py is
already resolved in `uv.lock` via rich, the exact shape that made the `packaging` swap cheap) and it
fixes the nesting case too, which no regex toggle can.

### Note on rank 5 — a platform-dependent gate

`fnmatch.fnmatch` case-normalizes both operands (source, read from the running 3.12.3 stdlib):

```
name = os.path.normcase(name)
pat = os.path.normcase(pat)
return fnmatchcase(name, pat)
```

`posixpath.normcase` is identity (verified live: `normcase('AB') -> 'AB'`); `ntpath.normcase`
lowercases (verified live by importing `ntpath` directly: `ntpath.normcase('CLAUDE.md') ->
'claude.md'`). So `boundary_headers._governed_files` selects a **different file set on Windows than on
Linux** — and this repo is operated on both (`.venv/Lib/site-packages` at `fleet_parity.py:798`;
`audit.py:815` cites "Windows' case-insensitive filesystem"; this lane ran on Linux).
`fnmatch.fnmatchcase` is the deterministic sibling in the same module. Same one-word change applies at
`fleet_parity.py:631,1489` and `fleet_analytics.py:211,213`.

Bonus finding from the same probe: `fnmatch`'s `*` crosses `/`, so `.claude/*.md` already matches
`.claude/skills/verify/SKILL.md` — the third entry of
`_GOVERNED_GLOBS = ("CLAUDE.md", ".claude/*.md", ".claude/**/*.md")` (`boundary_headers.py:66`) is
**dead code** that reads as if it were adding recursion.

### Note on rank 7 — this DOWNGRADES the 2026-08-02 networkx recommendation

The prior lane recommended swapping four DFS sites onto networkx, riding [#383]'s dependency-add.
Measured this lane: `has_cycle()` agrees with stdlib `graphlib.TopologicalSorter` on **24,000
randomized graphs** across 1-6 nodes, and `has_cycle()` never disagrees with `mermaid_emit._find_cycles`
on exhaustive small graphs — the warning and the marking are consistent. The only measured weakness is
recursion depth (`RecursionError` at a 3000-node chain, limit 1000; graphlib is iterative), and the
live codemap has **2 packages** (`ARCHITECTURE.md:93`). Two consequences:

1. There is no defect to fix, so this is a `leave`, not a swap.
2. If it is ever done, **stdlib `graphlib` beats networkx for the boolean half** — a new distribution
   should not be spent on something the standard library already ships. networkx is still the right
   answer for `_find_cycles` specifically (it returns *all* cycle edges; `CycleError` returns one
   cycle), so a networkx ride-along would collapse 1 of the 2 codemap sites, not both.

### Note on rank 8 — what the fallback actually costs

`carrier_precommit`'s docstring (line 265) states the splice falls back to a full re-dump on
"flow style, empty block, odd nesting". Probed live: `_scan_repo_spans` parses the hub's real 178-line
`.pre-commit-config.yaml`, and of 8 adversarial shapes only **flow-style** falls back — commented,
tab-indented, anchor/alias, empty-`hooks:`, quoted-key and leading-top-level-key configs all splice.
Measured fallback cost on the hub's own config: **73 comment lines to 0, 10503 bytes to 4077**. So the
degradation is severe but the trigger is rare, `ruamel.yaml` is a new distribution, and the hand-rolled
engine demonstrably covers realistic pre-commit configs. Leave — and the useful deliverable is
recording that the fallback is comment-destroying, so nobody treats it as a benign path.

## Re-checked from 2026-08-02

| prior row | prior verdict | current live status |
|---|---|---|
| 6x dotted-version parse -> `packaging` | SWAP | **PARTLY LANDED.** `scripts/fleet_parity.py:88` now imports `packaging.version`; `_parse_version` (line 822) documents the four defect shapes; `packaging>=24.0` declared at `pyproject.toml:37`; commit `a7e42a30` "fix(fleet-parity): PEP 440 version compare via packaging". **The other 5 sites are untouched** -- 3 of them (`enforcement_coverage.py:814`, `gen_methodology_roster.py:77`, plus the manifest-filename parse) read CONTROLLED filenames where `int()` is safe, so they are correctly left alone; `changelog_sentinel.py:45` reads an EXTERNAL tool version and carries the live defect -> promoted to row 1 here. |
| 4x DFS cycle detection -> `networkx` | SWAP (ride [#383]) | **DOWNGRADED to leave.** networkx still absent from `uv.lock`. Measured correct vs stdlib `graphlib` (24,000 trials, 0 mismatches). See rank-7 note; stdlib beats the new dep for the boolean half. |
| TOC anchor slugger -> `github-slugger` | KEEP + write the why-not into the code | **STILL KEEP; the why-not line was NOT written.** `scripts/toc/generator.py:23` still says only "GitHub-compatible anchor slug (mirrors github-slugger)" -- no maintenance rationale. The prior lane's actual deliverable is still outstanding. |
| 2x fenced-block detectors -> `markdown-it-py` | MEASURE-FIRST | **DISCHARGED -- split verdict.** `coherence_enumerator._find_fenced_blocks`: 1 divergence in 1493 files and 4/4 adversarial probes agree (tilde, 4-tick nesting, close-fence-with-info, indented) -> **leave, it is correct**. `toc/generator.parse_headers`: 8 divergences and 2 reproduced defects -> **adopt** (row 3). Third site found that the prior lane missed: `normalize_headers.py` (row 4). |
| ~13x `_git()` wrappers -> GitPython/pygit2 | MEASURE-FIRST, leaning KEEP | **NOT re-measured this lane** (deliberate: time went to the two rows with reproducible defects). Count re-verified: 20 `_git`/`_run` definitions across `scripts/` and `deploy/`. UNVERIFIABLE - no differential experiment run. |
| "surveyed and already correct" list | not re-proposed | **RE-CONFIRMED.** `rich.table.Table` imported at `deploy/tool.py:50`; `pydantic` at `ecosystem/schema/desired_state.py:28`; `difflib` in all 6 regen-and-diff gates; `argparse` 19x / `click` 11x; `tomllib` at 3 sites (`codemap/generator.py:25`, `fleet_parity.py:708,767`). Table-rendering libraries still correctly unreached for markdown output. |

## Coverage

**Swept (read + at least one live probe or grep-census):**

- `scripts/` — all 57 top-level `.py`. Category greps run repo-wide for: TOML/INI parsing, YAML
  load/dump, frontmatter extraction, `fnmatch`/`glob`/`PurePath` path matching, `difflib`, `argparse`/
  `click`/`sys.argv`, column-padding table rendering, `time.sleep`/retry, `shutil`, `datetime`
  deprecations (`utcnow`), hand-rolled path containment (`startswith(str(root))`), and a
  self-declared-hand-roll grep (`hand-roll|no dep|zero-dep|stdlib only`).
- `scripts/codemap/` — all 7 modules; cycle detection differentially tested against `graphlib`.
- `scripts/toc/` — all 3 modules; `parse_headers` differentially tested against markdown-it-py over
  1493 files.
- `scripts/hooks/` — `block_immutable_edits.py` read in full. `_path_in_zone` uses a lexical
  substring test on canonicalized paths; over-inclusive, which is the correct direction for a
  fail-closed deny guard, and smaller than any library alternative. No row.
- `deploy/` — `carrier_precommit.py` (splice engine exercised live), `floor_conformance.py`,
  `tool.py`, `contract.py`, `release_lint.py`, the 6 manifest YAMLs. `deploy/lived_sandbox/` reached
  only by import-census (see below).
- `ecosystem/dependency-baseline.yaml` read in full — one row (`pytest-xdist`); none of this lane's
  candidates would add a row there (all are hub-only or already declared).
- Corpus experiments ran over **1493 markdown files** and the full `uv.lock` package set.

**Not reached (stated, not implied):**

- `deploy/lived_sandbox/` (8 modules) — import-census only (`subprocess`, `json`, `yaml`, `tempfile`,
  `re`); no file read end-to-end, no probe run. The likeliest remaining candidate area.
- The ~20 `_git()` / `_run()` subprocess wrappers — carried forward UNMEASURED from 2026-08-02.
- `plugins/tier1-lifecycle/` — the mirrored `validate_backlog.py` twin named by the prior lane was
  not opened this lane.
- `scripts/*.ps1` (4 PowerShell surfacing scripts) — out of scope for a Python library-first sweep.
- Anything requiring an install: `pathspec`, `networkx`, `ruamel.yaml`, `tenacity` were all confirmed
  ABSENT from `uv.lock` and were **not** installed, so no third-party candidate outside the existing
  lock was measured. Their rows rest on absence-of-defect in the hand-rolled code, not on a library
  comparison.

---

*Read-only night batch. No swap performed, no dependency added, no repo file modified. Every
experiment ran in an isolated scratchpad venv against unmodified repo functions.*

---

> **Editor's note (wrap, lane L-A) — this file was RENAMED before commit.** It was written to
> the brief's mandated path `docs/audits/2026-08-03-night-<lane>.md` and is committed as
> `docs/audits/2026-08-03-technical-night-<lane>.md`. Reason: the mandated pattern is refused
> by this repo's own `validate-hermetization` Rule B — `night` is not a member of the ADR-101
> R3 closed class enum (`scripts/validate_hermetization.py:89-98`). Inserting the `technical`
> class token is what every 2026-08-01/02 night-batch sibling already does. **The gate was not
> weakened, bypassed or amended.** Any occurrence of the old `2026-08-03-night-...` form below
> is preserved deliberately as the evidence that produced this finding — it is a quotation of
> the blocked name, not a live path. Verified post-rename: `rule_a_violation` and
> `rule_b_violation` both return `None` for all seven artifacts of this batch.
