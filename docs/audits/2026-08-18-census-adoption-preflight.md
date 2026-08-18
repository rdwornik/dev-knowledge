# Adoption preflight — LANE I (NB7-D′, local rerun)

**Contract of record:** `docs/audits/2026-08-18-technical-adoption-preflight-lane-contract.md`
(dispatch-stamp commit `05af91e4`, ruling A8 — the stamp exists so *dispatched-and-died* can never
again be indistinguishable from *never-dispatched*, which is what happened to NB7-D).

**Standing constraint, restated:** measurements only. **No adoption verdicts, no rows, no
BACKLOG/tasks writes, no persistent installs, no merge.** Every number below is a reading, not a
recommendation; where a reading contradicts an existing artifact that is recorded as a correction to
the *reading*, never as a disposition.

---

## Per-item verdict lines

| # | item | verdict |
|---|---|---|
| 1 | lychee (link checker) trial | **CLEAR** — acquired ephemerally, run twice over 1865 files; 1344 links, 237 error occurrences, 16–23 s |
| 2 | Intake #31 §D residue | **CLEAR** — residue existed (steps 3/4/5); all three executed here |
| 3 | `gh` CLI formalization readiness | **CLEAR** — nothing blocks it on four checked legs; landing site quoted below |
| 4 | Tier-S home absence | **CLEAR** — R13 premise holds, with one wording correction to the census |

---

## Item 3 — `gh` CLI formalization readiness · **CLEAR**

### The claim as stated, and the part of it that is unlocatable

The contract asks to verify *"the (e)-substitute claim: nothing blocks it and it is one ledger line
in intake #27"*. The label **`(e)`** is **unlocatable in-tree** — `git grep` for
`(e)-substitute` / `e-substitute` returns exactly one hit, this lane's own contract file. The
lettered enumeration it belongs to lives in the NB7 briefing, off-repo. Recorded as unlocatable, not
as unruled: the *substance* of the claim is fully checkable in-tree and is checked below.

### Leg 1 — the tool is live on this box

```
gh --version   -> gh version 2.93.0 (2026-05-27)
gh auth status -> Logged in to github.com account rdwornik (keyring); Active account: true
                  Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

De-facto adoption is not a claim here, it is an observation: the CLI is installed, authenticated,
and already on `PATH` at `/c/Program Files/GitHub CLI`.

### Leg 2 — the target file's own recorded standing permits the edit

Intake #27 is `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md`, frontmatter
`status: DRAFT`. Its own `note:` states the editability rule and cites it as already-relied-upon,
verbatim:

> ERRATUM 2026-08-08 (morning integrate-and-cut arc, operator-directed): **while `status: DRAFT`
> this ledger is editable** — the same standing the 2026-08-06 §D repair above relied on — and four
> ledger-truth edits landed.

Three prior errata (2026-08-06, 2026-08-08, 2026-08-09) added or amended §A rows on exactly this
standing, each recording **zero BACKLOG rows born, zero closed, no row removed**. The precedent for
a births-free ledger append is therefore established *in the file itself*, not merely permitted.

### Leg 3 — the file is not freshness-gated

`DEFAULT_FRESHNESS_FILES` (`scripts/canonical_freshness_gate.py:32`) is
`VISION.md · ARCHITECTURE.md · CLAUDE.md · CONTRIBUTING.md · docs/handoffs/README.md ·
protocols/ESSENTIALS.md`; `_HUB_ONLY_FRESHNESS_FILES` (`scripts/audit.py:321`) adds
`protocols/SESSION_SETUP.md · protocols/AI_COUNCIL_PROCESS.md · protocols/DEFINITION_OF_DONE.md`.
**No intake path appears in either list**, so no `last_reviewed` stamp is owed and the A2 gate
cannot fire.

### Leg 4 — neither intake generator sees a body edit

`gen_intake_tree.py:100` declares `_PROJECTED_FM_KEYS = ("intake-id", "status")`, and
`gen_intake_index.py` groups by frontmatter `status:`. A row appended to the §A table changes
`intake-id`, `status` and title **not at all**, so `intake-index-freshness` (pre-commit) and
`intake_tree_coherence` (audit) both stay green without a regen. This closes the known
two-generator trap, which applies to an intake **add**, not to a body edit.

**Nothing blocks it: 4 legs checked, 0 blockers.**

### Where the line would land — quoted

The ledger surface is §A, whose header and column contract read verbatim:

> `## §A — Ledger (status vocabulary: ADOPTED-live / EVAL-RUN(result) / SCHEDULED(where) / UNPLACED / REFUTED / DEFERRED(trigger) / DORMANT)`
>
> `| # | Item | Status | Evidence / locator | Priority class (§C) |`

That is `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` §A, table header at lines
16–19. **The next free row number is 41.** Live row numbers are `1–37` and `40`; the `38/39` gap is
not free, and the file says so in its own numbering note:

> The `38`/`39` gap in this table is therefore deliberate, not a dropped row.

**One existing row must not be mistaken for this one.** §A row 7 reads
`| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | night finding 5 (rate
limits, ~150→403) | P-C |` — that is `gh` as an *Issues sink*, a P-C arc. The de-facto-adoption line
is about `gh` as an *installed tool*. Distinct items; row 7 does not discharge the obligation.

The obligation itself is R3 of the NB7 orphan census, whose Done-when names three lines, verbatim:

> intake #27 carries a dated §C cross-reference amendment; the `gh` de-facto-adoption ledger line
> exists; and `ponytail` + `skill-creator` each carry a Tier-S KEEP or DELETE line under ADR-112's
> *"one ledger line either way"*.

So the append is two-part by R3's own text: a **row in §A** (number 41) and a **dated `## …
amendment` section**, following the shape already on file at line 99,
`## Ratification amendment — 2026-08-08 (batch-3 GO)`, which opens *"Appended rather than folded:
every section above stays exactly as written."*

**Size check against the claim "one ledger line":** the §A row is one line. R3's full discharge is
three lines across two sections. The claim is accurate for the `gh` item alone.

---

## Item 4 — Tier-S home absence · **CLEAR** (premise holds; one census wording correction)

### ADR-112 names no home — its own words

`docs/decisions/ADR-112-*.md` line 109:

> **The ledger has no declared home in this ADR.** Intake #28 §C routes its verdicts into ledger
> #27 as a cross-referenced amendment; a standing home for Tier S ledger lines is left to the
> ratifying act rather than invented here.

The mechanism it mandates (line 53) is `Install → **30-minute sandbox try** → **KEEP or DELETE** →
**one ledger line either way**`, and line 57 states why the line matters: *"recording it is what
stops the same candidate being re-tried every quarter by a seat that does not know it was already
tried."* A mandated record with no surface to write to is the R13 gap.

### Live greps — no Tier-S ledger surface exists

```
git grep -n -iE "tier[- ]s\b" -- .        -> 20 hits, 0 of them a ledger surface
git ls-files | grep -i ledger             -> 7 files, none a Tier-S ledger
```

The 20 `Tier S` hits are: the ADR itself, its ratification pack, `ARCHITECTURE.md:1014` (which
*describes* the mechanism), a JOURNAL entry, and audits/censuses *discussing* the tier. The 7
`ledger`-named tracked files are an overnight-mission ledger, a night-divergence ledger, a
silent-rule ledger, a WARN ledger, a lane contract, an audit-disposition ledger, and a `tasks/`
row — **none carries a Tier-S KEEP/DELETE line, and none is named as the home.** Zero Tier-S ledger
lines exist because there is nowhere to write one.

### Live state — the two TRY-NOW candidates are not installed

```
ls ~/.claude/skills/                     -> gotchas          (only)
cat ~/.claude/plugins/installed_plugins.json
                                         -> tier1-lifecycle@dev-knowledge-methodology  (only)
ls ~/.claude/plugins/marketplaces        -> claude-plugins-official   (only)
```

Neither `ponytail` nor `skill-creator` is installed, in any scope, from any marketplace. **Never
tried is confirmed against live machine state, not only against the tree.**

### The one correction owed to the census

`docs/audits/2026-08-17-census-nb7-orphan-census.md:184` records the carrier test as
**`ponytail`/`skill-creator` → 0 hits tree-wide**. That was true when written and is **no longer
literally true** — re-run live, the two tokens return **10 distinct matching lines across 4 files**:

| file | hits | what the hit is |
|---|---|---|
| `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md` | 4 | the original TRY-NOW nomination — lines 17 (provenance), 36 + 37 (the two Tier-S table rows), 55 (candidate-row note) |
| `docs/audits/2026-08-17-census-north-star-inventory.md` | 3 | the same-day sibling census recording them **DECIDED-UNFILED** |
| `docs/audits/2026-08-17-census-nb7-orphan-census.md` | 2 | the census's own rows 30 and R3 — i.e. its record of the absence |
| `docs/audits/2026-08-18-…-lane-contract.md` | 1 | this lane's contract |

**Every one of the 10 is a reference to the candidacy or to its absence. Not one is a trial record,
an install, or a KEEP/DELETE line.** So the R13 premise — *the two TRY-NOW candidates have never
been tried, and no surface exists to record it either way* — **holds without qualification**; only
the census's *phrasing* of the carrier test has been overtaken by the census's own existence. The
durable form of that test is **"0 hits that are a trial record"**, which a later seat can re-run
without it going false the moment someone writes the finding down.

---

## Item 1 — lychee trial · **CLEAR**

**Library-first note honoured:** lychee *is* the library. Nothing was hand-rolled; the only code
written was throwaway analysis over lychee's own JSON output.

### Acquisition — ephemeral, checksum-verified, nothing installed

No acquisition channel existed on PATH: `lychee`, `scoop` and `cargo` are all absent. `winget` and
`npm` exist but both install persistently, which the contract forbids. The permitted channel — *a
downloaded release binary run from the worktree* — was used, and the binary was placed in the job
temp dir rather than the worktree so the tree stayed byte-identical throughout (no-leftovers rule).

```
curl -sS -L https://api.github.com/repos/lycheeverse/lychee/releases/latest -o rel.json
# -> tag lychee-v0.24.2
curl -sS -L -o lychee.zip        https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-pc-windows-msvc.zip
curl -sS -L -o lychee.zip.sha256 https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-pc-windows-msvc.zip.sha256
sha256sum lychee.zip
#   published 32975d1493ee1a975d6bb41e4fb56fe419cb442ded628bb772ba2e614acfacad
#   measured  32975d1493ee1a975d6bb41e4fb56fe419cb442ded628bb772ba2e614acfacad   MATCH
unzip -o -q lychee.zip -d lychee-bin
./lychee-bin/lychee-x86_64-pc-windows-msvc/lychee.exe --version   # -> lychee 0.24.2
```

**Persistent-install count: 0.** Nothing was added to PATH, `pyproject.toml`, `uv.lock`, `package.json`
or the worktree.

### The surface, and the two runs

```
git ls-files '*.md' > mdfiles.txt            # 1865 tracked markdown files

# run A — offline (local file links only)
lychee.exe --offline --no-progress --format detailed \
  --output lychee-offline.txt --files-from mdfiles.txt

# run B — full (local + network), definitive JSON record
lychee.exe --no-progress --format json --max-concurrency 8 --timeout 20 \
  --retry-wait-time 2 --max-retries 2 \
  --output lychee-full.json --files-from mdfiles.txt
```

| quantity | run A (offline) | run B (full) |
|---|---|---|
| **runtime** | **2 s** | **16 s** (a first `--format detailed` pass measured 23 s) |
| files scanned | 1865 | 1865 |
| **total links** | 1344 | **1344** |
| unique links | 1176 | **1176** |
| successful | 862 | **1075** |
| **errors (occurrences)** | 134 | **237** |
| excluded | 348 (all network, by `--offline`) | 6 |
| timeouts | 0 | **0** |
| redirects | 0 | 4 |
| files with ≥1 error | — | **46** |

**Headline: 1344 links across 1865 files checked in 16 seconds, 237 error occurrences.**

**A reconciliation note, because the summary block is misleading.** lychee's terminal summary prints
`Errors 237` beside `Unsupported 237` — the two are *not* both 237. The JSON record shows
`unsupported: 26`, and the `--format detailed` listing shows **134 unique** failing links against
**237 occurrences**. Anyone quoting the pretty summary will double-count. The numbers above are
taken from the JSON, which is the only self-consistent surface lychee emits.

### Error breakdown (237 occurrences, from `error_map`)

| count | class |
|---|---|
| 113 | local — "File not found" |
| 94 | HTTP 404 |
| 24 | "Cannot resolve root-relative link" (`/C:/…` absolute-path citations) |
| 7 | HTTP 403 |
| 1 | HTTP 410 |
| 1 | cached error |

Concentration is extreme: **77 of 237 (32 %) are in one file**,
`docs/archive/2026-04-27-handoff-patterns-external-research.md`, and 89 of the 102 HTTP failures are
one host, `vertexaisearch.cloud.google.com`.

### False-positive sample — 5 links hand-checked

| # | link (as lychee reports it) | lychee | hand-check | verdict |
|---|---|---|---|---|
| 1 | `docs/audits/2026-08-07-technical-batch-2-packet.md` → `docs/audits/a` | File not found | source line 157 reads `` the [#430](a) ruling `` — the repo's `[#id]` + `(a)`/`(b)` sub-item prose parses as a markdown link | **FALSE POSITIVE** — not a link |
| 2 | `docs/audits/2026-07-31-ecosystem-audit.md` → `docs/audits/ecosystem/corp-ops/history` | File not found | source writes a Windows-backslash target `` [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/) ``; `ecosystem/corp-ops/history` **exists** at repo root | **FALSE POSITIVE** — target exists; backslash + wrong base |
| 3 | `docs/handoffs/2026-05-25-dev-knowledge-session-sync/03_PLAYBOOK.md` → `…/docs/decisions/ADR-36-audit-tool-architecture.md` | File not found | link is written repo-root-relative from a file two dirs deep; `docs/decisions/ADR-36-audit-tool-architecture.md` **exists** | **FALSE POSITIVE** — target exists; wrong base |
| 4 | `https://medium.com/opendoor-labs/our-python-monorepo-d34028f2b6fa` | 403 Forbidden | `curl` default UA → **403**; `curl` with a browser UA → **200** | **FALSE POSITIVE** — bot block, page is live |
| 5 | `https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuXBGOW…` | 404 Not Found | `curl -L` with a browser UA → **404** | **TRUE POSITIVE** — expired one-shot grounding token |

**4 of 5 hand-checked errors are false positives.**

### Full-population classification (all 237, not just the sample)

Each of the five sample classes was then counted across the whole error set by re-resolving every
as-written target against the repo root and re-testing every HTTP failure's class:

| count | share | class | actionable as "broken link"? |
|---|---|---|---|
| 89 | 37.6 % | expired `vertexaisearch` grounding-redirect tokens | **yes**, but unfixable — the token was the only record of the source |
| 69 | 29.1 % | root-relative-intent local links; **target exists at repo root** | no — config, not rot |
| 21 | 8.9 % | codex-review `[label](/C:/abs/path:line)` citations | no — a citation convention lychee cannot model |
| 20 | 8.4 % | markdown-syntax collisions (`[#430](a)`) | no — not links |
| 18 | 7.6 % | Windows-backslash targets read as markdown escapes (`ecosystem\.dev-knowledge` → `ecosystem.dev-knowledge`) | no — target exists |
| 7 | 3.0 % | HTTP 403 bot blocks | no — verified live at 200 with a browser UA |
| 7 | 3.0 % | other HTTP 404 / 410 / cached | **yes** |
| 6 | 2.5 % | stale ADR slugs in sealed 2026-05-25 handoffs (`ADR-33-vision-md-standard.md` → renamed to `ADR-33-vision-universalization.md`) | **yes** — genuine rot |

**Measured true-positive rate: 102 of 237 = 43 %.** Of those 102, **89 (87 %) are expired
grounding tokens inside two immutable `docs/archive/` research artifacts**, and 6 more are inside
immutable handoff bundles — so the count of true broken links in *mutable* surfaces is **7**.

Two configuration facts fall straight out of the numbers and are recorded as measurements, not as
recommendations: **`--base-url <repo root>` would remove 87 of the 237 occurrences** (classes B and
the backslash class, whose targets all exist), and the repo's own `[#id](a)` prose convention plus
the codex citation format account for a further 41 — i.e. **128 of 237 (54 %) are addressable by
configuration alone, before anyone touches a single link.**

---

### Cross-check: is lychee's link total credible?

`total: 1344` looks low against 1865 files, so it was corroborated independently rather than taken
on trust. A throwaway regex pass over the same file list, skipping fenced code blocks, counts
**1281 inline `[text](target)` links + 6 autolinks = 1287**, plus 70 bare URLs. lychee's 1344 sits
between those two figures, which is the expected place for it. **The tool did read all 1865 files;
the corpus is simply prose-heavy with backtick-quoted paths rather than markdown links.**

---

## Item 2 — Intake #31 §D residue · **CLEAR** (residue existed; all of it executed here)

### §D read verbatim, and what it demands

`docs/intake/2026-08-09-func-code-style-doctrine.md` §D, in full:

> ## §D — Proposed ruling 4: NO fleet-wide refactor without a hotspot measurement
>
> Do not refactor code merely because it predates these patterns. Procedure, in order:
> churn-vs-complexity hotspot analysis (change frequency is the better-supported signal; a small
> fraction of files typically carries most of the work) · complexity and file-length distributions ·
> coverage on the hotspots · duplication rate · dependency cycles. **Refactor only where high churn
> ∩ high complexity, tests first where coverage is thin; everywhere else, ratchets + opportunistic
> improvement as agents touch the code.** Big-bang rewrites are the recorded failure mode;
> strangler-fig is reserved for a genuinely load-bearing, high-churn, high-complexity module.

That is a **five-step procedure**, stated in order: (1) churn × complexity · (2) complexity and
file-length distributions · (3) coverage on the hotspots · (4) duplication rate · (5) dependency
cycles.

### The residue, proven by the baselines artifact's own words

There **is** residue, and `docs/audits/2026-08-18-technical-phase0-baselines.md` says so twice
without being asked. T0.5's method section:

> This arc executes **steps 1 and 2**; coverage, duplication and cycles are not run here and are
> recorded as open below.

and its own closing subsection, verbatim:

> ### Open legs of section D's procedure, not run here
>
> Coverage on the hotspots (step 3) · duplication rate (step 4) · dependency cycles (step 5). Each
> is a separate measurement; none is implied by the table above.

T0.5 also states the consequence it could not discharge: *"Section D's 'tests first where coverage
is thin' clause **cannot be discharged from this artifact**: coverage on the hotspots is procedure
step 3 and was not measured."*

**Residue = steps 3, 4 and 5. All three are executed below.** Method follows T0.5's own precedent
exactly — library-first, ephemeral `uv run --with` installs, no `pyproject.toml` entry, no
`uv.lock` churn, no committed script.

### Step 3 — coverage on the hotspots · **RUN**

The hotspot set is T0.5's own top-20 ranking. **11 of those 20 are test files**, which have no
meaningful "coverage on the hotspot", so the measurable set is the **9 source files** in the top 20.

```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
uv run --with pytest-cov pytest -q --cov=scripts --cov=deploy \
  --cov-report=json:coverage.json --cov-report=term
```

**Runtime 1626.98 s (27 min 06 s)** — 2961 passed, 3 failed, 9 skipped, 1 xfailed. (The three REDs
are addressed below; none is this lane's.)

| T0.5 rank | file | churn 180d | cc | statements | missed | **coverage** |
|---|---|---|---|---|---|---|
| 1 | `scripts/audit.py` | 135 | 709 | 1663 | 212 | **87.3 %** |
| 3 | `scripts/fleet_parity.py` | 24 | 507 | 1062 | 97 | **90.9 %** |
| 10 | `deploy/carrier_floor.py` | 21 | 209 | 402 | 10 | **97.5 %** |
| 11 | `scripts/gen_task_tree.py` | 19 | 231 | 581 | 52 | **91.0 %** |
| 15 | `deploy/tool.py` | 13 | 212 | 576 | 92 | **84.0 %** |
| 16 | `scripts/enforcement_coverage.py` | 10 | 251 | 623 | 124 | **80.1 %** |
| 17 | `scripts/fleet_health.py` | 14 | 179 | 410 | 28 | **93.2 %** |
| 18 | `scripts/verify_handoff_probes.py` | 16 | 154 | 289 | 10 | **96.5 %** |
| 20 | `deploy/carrier_precommit.py` | 6 | 285 | 550 | 40 | **92.7 %** |
| | **hotspot aggregate** | | | **6156** | **665** | **89.2 %** |
| | **`scripts/` + `deploy/` overall** (114 modules) | | | **17074** | **2364** | **86.2 %** |

**This answers §D's open clause directly, and the answer is the opposite of the worry.** §D says
*"tests first where coverage is thin"*. **The hotspots are not thin — they are better covered than
the codebase around them: 89.2 % against an 86.2 % baseline, and no hotspot falls below 80 %.**
The worst hotspot, `scripts/enforcement_coverage.py` at 80.1 %, still sits above every module in
the repo-wide bottom five:

| coverage | module (≥100 statements) |
|---|---|
| 57.1 % | `scripts/reverse_dep_oracle.py` (317 stmts) |
| 64.8 % | `deploy/lived_sandbox/cli.py` (122) |
| 70.8 % | `scripts/safe_remove.py` (144) |
| 71.5 % | `scripts/review_closures.py` (151) |
| 74.1 % | `scripts/gen_intake_tree.py` (228) |

Recorded as a measurement with no verdict attached: **§D's "tests first" precondition finds no
hotspot to fire on.** What that implies for §B's sequencing is the architect's ruling, not this
lane's.

#### The three REDs — reported, not dispositioned

None of the three is attributable to this lane, and the evidence is in the failure text itself.
This lane added **two files under `docs/audits/`** and **no test, no script, no BACKLOG row**.

| failing test | assertion | attribution |
|---|---|---|
| `tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | `RotFinding(category='backlog-accretion', locus='BACKLOG#293', detail='4 history dates spanning 40d, 2864 chars')` | live **BACKLOG** row #293; this lane made no BACKLOG edit |
| `tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` | `assert '1 declared routine row' in '3 declared routine row(s)'` | live **BACKLOG** routine-row count; same, not this lane's |
| `tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | asserts on `WindowsPath('C:/Users/1028120/Documents/Dev/.dev-knowledge/…')` | **environmental** — the known lane-worktree class; the suite is running from a linked worktree |

Two live-BACKLOG REDs plus one worktree-environmental RED. **Stated, not adjudicated:** a lane does
not disposition a RED it did not create.

### Step 4 — duplication rate · **RUN**

Library-first: `symilar`, the duplicate-block detector shipped inside pylint, installed ephemerally
through `uv run --with` exactly as T0.5 installed `radon`. No `pyproject.toml` entry, no `uv.lock`
churn, nothing added to the operator environment.

```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
uv run --with pylint --no-project python -m pylint.checkers.symilar \
  --duplicates=8 --ignore-comments --ignore-docstrings --ignore-imports \
  $(git ls-files '*.py')
```

Minimum block = 8 lines; comments, docstrings and import blocks excluded. **Runtime 99 s** over
**257 tracked `.py` files / 82 135 lines**.

| quantity | value |
|---|---|
| total lines scanned | 82 135 |
| duplicate lines | **693** |
| **duplication rate** | **0.84 %** |
| duplicate blocks | 22 |

**The headline rate is not the finding — its composition is.** Of the 693 duplicate lines,
**525 (75.8 %) sit in 10 blocks that are hub `scripts/` ↔ `plugins/tier1-lifecycle/scripts/`
carrier twins** — i.e. deliberate, architecturally-mandated replication, since the plugin ships its
own copy of what the hub owns. The four largest blocks are all twins:

| lines | block |
|---|---|
| 137 | `plugins/tier1-lifecycle/scripts/propose_closures.py` ↔ `scripts/propose_closures.py` |
| 128 | `plugins/tier1-lifecycle/scripts/review_closures.py` ↔ `scripts/review_closures.py` |
| 61 | `plugins/tier1-lifecycle/scripts/propose_closures.py` ↔ `scripts/propose_closures.py` |
| 47 | `plugins/tier1-lifecycle/scripts/validate_backlog.py` ↔ `scripts/validate_backlog.py` |

**Non-carrier duplication is 12 blocks / 168 lines = 0.20 % of the corpus** — the largest single
instance being 25 lines shared by `tests/test_gen_handoff.py` and `tests/test_v6_frozen_contract.py`.

Recorded as a measurement, with no verdict attached: a duplication gate configured against the raw
0.84 % would be measuring the carrier architecture, not code hygiene. Whether that matters is the
architect's call, not this lane's.

**One gotcha triggered and recorded** (existing entry, `~/.claude/skills/gotchas/gotchas.md`,
`Last triggered` bumped to 2026-08-18): the first run did all 99 s of work and then exited 1 with
`UnicodeEncodeError: 'charmap' codec can't encode character '→'` — `symilar` prints a `→` in
its own report header, and Windows stdout is cp1252. The new wrinkle over the prior instances is
that the crashing `print` was **inside a third-party tool**, so it could not be audited in advance;
the durable fix is to run every third-party CLI under `PYTHONUTF8=1` by default rather than
reacting to the traceback.

### Step 5 — dependency cycles · **RUN**

Library-first: pylint's `cyclic-import` checker (R0401), same ephemeral channel. Chosen over
`import-linter` because it needs no contract file — a contract would have been a committed artifact
this lane is not permitted to create.

```
uv run --with pylint --no-project python -m pylint --disable=all --enable=cyclic-import \
  --recursive=y --ignore=.venv,node_modules,.claude scripts deploy tests
```

**Runtime 42 s. Six cycles reported; five are real, one is a planted fixture.**

| # | cycle | status |
|---|---|---|
| 1 | `audit → enforcement_coverage` | real |
| 2 | `audit → fleet_parity → enforcement_coverage` | real |
| 3 | `audit → fleet_parity → fleet_health → enforcement_coverage` | real |
| 4 | `audit → verify_handoff_probes` | real |
| 5 | `assemble_paste → gen_handoff` | real |
| 6 | `pkg_a.module → pkg_b.thing` | **fixture** — `tests/fixtures/repo-with-structural-checks/`, planted on purpose |

**Verified at source rather than taken from the report**, because pylint attributes every R0401 to
the last module it analysed (here `tests/fixtures/.../my_pkg/__init__.py`), which is misleading:

```
scripts/audit.py:112,114               from scripts import verify_handoff_probes as _vhp
scripts/audit.py:1900,1902             from scripts import enforcement_coverage as _enfcov
scripts/enforcement_coverage.py:566,695,753   from scripts import audit as _audit
scripts/verify_handoff_probes.py:187,190      from audit import _select_active_bundle
```

**The material qualifier, which the raw count hides: every one of these imports is function-local,
not module-level.** They are the deferred-import pattern used deliberately to break load-time
cycles. So the five cycles are real in the *import graph* and produce **no import-time cycle at
all** — the codebase already applies the standard mitigation. A tool run without this check would
report "5 cycles" and imply a defect that is not there.

**Section-D procedure status after this lane:** step 1 ✅ (T0.5) · step 2 ✅ (T0.5) · step 3 ✅ ·
step 4 ✅ · step 5 ✅. **All five legs of §D's stated procedure now have a measurement.** Whether
that discharges §D's *binding* status on §B is a ruling, not a measurement, and is not made here.

---

## Exact commands, verbatim

All run from the lane worktree
`.claude/worktrees/lane-i-31-adoption-preflight` unless noted. `$T` = the session temp dir
(`~/.claude/jobs/04ebb0be/tmp`), which is outside the repo by design.

### Item 1 — lychee

```
curl -sS -L --max-time 60 https://api.github.com/repos/lycheeverse/lychee/releases/latest -o $T/rel.json
curl -sS -L --max-time 300 -o $T/lychee.zip        https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-pc-windows-msvc.zip
curl -sS -L --max-time 60  -o $T/lychee.zip.sha256 https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-pc-windows-msvc.zip.sha256
sha256sum $T/lychee.zip                     # matched the published sha256
unzip -o -q $T/lychee.zip -d $T/lychee-bin
$T/lychee-bin/lychee-x86_64-pc-windows-msvc/lychee.exe --version

git ls-files '*.md' > $T/mdfiles.txt

$T/lychee-bin/lychee-x86_64-pc-windows-msvc/lychee.exe --offline --no-progress \
  --format detailed --output $T/lychee-offline.txt --files-from $T/mdfiles.txt

$T/lychee-bin/lychee-x86_64-pc-windows-msvc/lychee.exe --no-progress --format json \
  --max-concurrency 8 --timeout 20 --retry-wait-time 2 --max-retries 2 \
  --output $T/lychee-full.json --files-from $T/mdfiles.txt

# hand-checks of the 5 sampled links
curl -sS -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36" \
  --max-time 30 "https://medium.com/opendoor-labs/our-python-monorepo-d34028f2b6fa"      # 200
curl -sS -o /dev/null -w "%{http_code}\n" --max-time 30 \
  "https://medium.com/opendoor-labs/our-python-monorepo-d34028f2b6fa"                     # 403
curl -sS -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 …Chrome/140…" -L --max-time 30 \
  "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuXBGOWYQmBteNKFtqRckfM3TLAalVyEnvIES8JuUAN0Cjm_l588uDWNIM2YSY-7dpzxXO7BmcrMC87iuBhtGKrTzZa43bZxYQm0zSB9EPEIzTsjGgI9HoH7tbLH-g"   # 404
```

### Item 2 — intake #31 §D steps 3/4/5

```
uv sync --locked --group analytics

# step 3 — coverage on the hotspots
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
uv run --with pytest-cov pytest -q --cov=scripts --cov=deploy \
  --cov-report=json:$T/coverage.json --cov-report=term

# step 4 — duplication rate
git ls-files '*.py' > $T/pyfiles.txt
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
uv run --with pylint --no-project python -m pylint.checkers.symilar \
  --duplicates=8 --ignore-comments --ignore-docstrings --ignore-imports $(cat $T/pyfiles.txt)

# step 5 — dependency cycles
uv run --with pylint --no-project python -m pylint --disable=all --enable=cyclic-import \
  --recursive=y --ignore=.venv,node_modules,.claude scripts deploy tests
```

### Item 3 — `gh` readiness

```
gh --version
gh auth status
head -8 docs/intake/2026-08-06-tech-adoption-consolidation-intake.md          # status: DRAFT
grep -oE "^\| [0-9]+ \|" docs/intake/2026-08-06-tech-adoption-consolidation-intake.md \
  | grep -oE "[0-9]+" | sort -n                                              # 1..37, 40
sed -n '32,40p' scripts/canonical_freshness_gate.py                          # DEFAULT_FRESHNESS_FILES
grep -n "_HUB_ONLY_FRESHNESS_FILES" -A6 scripts/audit.py
grep -n "_PROJECTED_FM_KEYS" scripts/gen_intake_tree.py
grep -n "intake" .pre-commit-config.yaml
```

### Item 4 — Tier-S absence

```
git grep -n -i "ponytail" -- .
git grep -n -i "skill-creator" -- .
git grep -n -iE "tier[- ]s\b" -- .
git ls-files | grep -i "ledger"
grep -n -i "ledger" docs/decisions/ADR-112*.md
ls ~/.claude/skills/
cat ~/.claude/plugins/installed_plugins.json
ls ~/.claude/plugins/marketplaces
```

---

## No-leftovers proof

Every tool used in this lane was ephemeral. Nothing was installed persistently, and the two
artefacts the runs left behind were removed and their removal verified.

| artefact | where it went | state |
|---|---|---|
| lychee 0.24.2 binary + zip | `$T/lychee-bin/`, outside the repo | never in the tree |
| `pylint`, `pytest-cov` | `uv run --with` ephemeral layer | **not** in `pyproject.toml`; `uv.lock` untouched |
| `.coverage` data file | written into the worktree root by the suite | **removed** — `rm -f .coverage` |
| `C:\c\Users\…\coverage.json` | stray tree from an MSYS path-conversion trap (below) | **removed** — `rm -rf /c/c`; `ls -d /c/c` → *No such file or directory* |

Final `git status --short` shows exactly the intended artifacts and nothing else.

**A second gotcha triggered and recorded as a NEW entry** in `~/.claude/skills/gotchas/gotchas.md`:
git-bash suppresses its POSIX→Windows argument conversion when the path sits behind a `prefix:` in
the same argument, so `--cov-report=json:$T/coverage.json` wrote to `C:\c\Users\…` while printing a
success message naming the intended path. Silent, exit 0, and expensive — the 27-minute run looked
like it had discarded its own output. Both the stray tree and the `.coverage` file are cleaned above.

---

## What this lane did NOT do

No adoption verdict on lychee or on any §D finding. No BACKLOG row born, closed or edited. No
`tasks/` write. No disposition of any finding, including the three suite REDs, which are reported
with attribution and left for the architect. No intake edit — item 3 establishes *where* the `gh`
line would land and that nothing blocks it; **the line itself is not written here.** No persistent
install. No merge, no push to `main`.

Two files outside `docs/audits/` were touched, both in `~/.claude/skills/gotchas/gotchas.md` and
both required by the standing execution-loop rule (step 5: a triggered gotcha updates its
`Last triggered`, a new pattern gets an entry): the cp1252 print-crash entry was re-dated to
2026-08-18 with the third-party-tool wrinkle recorded, and the MSYS `prefix:` path-conversion trap
was added as a new entry. Flagged here rather than left silent, since it is the only write this
lane made outside the repo.
