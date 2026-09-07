# Census — fleet cross-check: every repo root against the #73 root allowlist

> **READ-ONLY. Nothing was moved, deleted, edited or renamed in any repository.** Every verdict
> below is a **PROPOSAL** the operator rules. The only commands issued against a consumer repo
> were `git -C <repo> ls-files`, `rev-parse` and `status --porcelain` — no write, no stage, no
> checkout, no fetch, no clean, no switch. Two consumers were found off `main` or dirty and were
> **measured as found and left as found**.
>
> Lane `lane-s-013-census-fleet-crosscheck` (SWEEP 2026-09-07, row **S-13**), on branch
> `worktree-lane-s-013-census-fleet-crosscheck`. **Substrate deviation, contract §9:** the other
> twelve census lanes run on cloud; this one runs LOCAL, because a cloud checkout is bound to the
> hub repository alone and the eight sibling consumer roots do not exist there at any path.
>
> **This is a SECOND, INDEPENDENT DERIVATION beside `docs/audits/2026-09-07-technical-seal-report-fleet.md`
> (W2-U2).** Per contract §10, disagreements are **LISTED, not reconciled** — §5 is that list. The
> U2 report was read only AFTER this lane's own measurement was complete.

**Consumer:** `[#621]` — the open ADR-114 option (C) row, *"the nine-repo VISION.md to README.md
filename migration"*, whose Done-when asks for *"a sequencing plan across the ADR-104 members
before the first commit"*. This census is that sequencing input measured at the root grain: it
names which seven of the eight children still carry a root `VISION.md`, and it independently
re-derives the row's own *"only 2 of 8 children carry a root README"* claim. The substantive
path citations are `ecosystem/fleet-shape-spec.yaml` (the allowlist as data),
`docs/audits/2026-09-07-technical-seal-report-fleet.md` (the derivation this one stands beside)
and `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md` (intake #73, the filing).

---

## 0 · What "the #73 allowlist" resolves to — stated before it is used

Intake #73 **defines no allowlist of its own.** Its leg **M1** says the permitted root set is
CLOSED and cites ROOT-CONTRACT v1 §C1 as the standing statement, requiring only that the set
become *"repo-KIND-aware and consumer-runnable"*. The set itself became **data** when W2-U1
landed `ecosystem/fleet-shape-spec.yaml`, whose clause `root_allowlist` is what
`scripts/validate_hermetization.py` now derives `SANCTIONED_TIER1_DIRS`,
`SANCTIONED_TIER1_FILES` and `SANCTIONED_TIER1_FILE_GLOBS` from.

**So "the #73 allowlist" measured here is `ecosystem/fleet-shape-spec.yaml` clause
`root_allowlist`, resolved exactly as the module resolves it** — the 14 file literals UNIONed
with `scripts/canonical_docs.py::CANONICAL_MANDATORY` (the `files_from:` join), plus the
directory list, plus the one file glob.

```
directories (20)  .claude .claude-plugin .devcontainer .github .vscode codex config deploy
                  docs ecosystem eval logs models plugins protocols scripts src tasks
                  templates tests
files (20)        .gitattributes .gitignore .methodology.yaml .pre-commit-config.yaml
                  .pre-commit-hooks.yaml .python-version .ruff.toml .worktreeinclude
                  AGENTS.md README.md package-lock.json package.json pyproject.toml uv.lock
                  + ARCHITECTURE.md BACKLOG.md CLAUDE.md CONTRIBUTING.md JOURNAL.md LESSONS.md
                    (joined from CANONICAL_MANDATORY, not restated in the YAML)
file_globs (1)    .*.code-workspace
```

**Grain.** ROOT depth only — a top-level tracked file, or the first path segment of a tracked
path. This is the Rule A file and directory legs. It is deliberately narrower than a full seal
run, and §5 records what that narrowness costs.

**Method.** `git -C <repo> ls-files` per repo; first path segment split; membership tested
against the three clause lists (`fnmatch` for the glob). The allowlist was parsed from the YAML
rather than retyped, so no roster is restated in this file.

---

## 1 · Fleet membership — verified independently, not inherited

The ratified declaration is nine ids. Three surfaces carry it and all three were opened:

- `scripts/audit.py::ADR104_FLEET_DECLARATION` — nine ids.
- `docs/decisions/ADR-104-fleet-repository-shape.md`, inside the machine-locatable
  `adr104-fleet-members` declaration anchor gated by `[#472]` — the same nine, in the same order.
- `ecosystem/registry.md` — nine rows, the same nine.

**Independently re-derived, not taken from U2:** the three non-member directories under `Dev/` —
`illustrated-book-gen`, `overnight`, `_scratch` — are **not git repositories**. Each was probed
with `git -C <dir> rev-parse --show-toplevel`, and each returned
`fatal: not a git repository (or any of the parent directories): .git`. Three further
directories (`.archived`, `.backups`, `.settings`) return the same. There is no tenth repository
a `ls-files` cross-check could have read. **This CONFIRMS U2's §12 arithmetic by a different
command** (`rev-parse` rather than `Test-Path <dir>/.git`).

**OneDrive exclusion zone (contract §9).** Every one of the nine repositories resolves via
`rev-parse --show-toplevel` to a path under `C:/Users/1028120/Documents/Dev/`. **No repository
resolves inside the corporate-OneDrive exclusion zone**, so no path in this census required the
OUT-OF-SCOPE disposition, and none was attempted.

---

## Inventory

### 1.1 · Per-repo totals, stamped

Measured 2026-09-07. `dirty` is `git status --porcelain` line count.

| repo | HEAD | branch | dirty | tracked | root entries | admitted | **out of pattern** |
|---|---|---|---|---|---|---|---|
| `.dev-knowledge` (hub) | `21576e3a` | `worktree-lane-s-013-…` | 0 | 2998 | 36 | 36 | **0** |
| `ai-council` | `7a3c057` | `main` | 0 | 254 | 24 | 20 | **4** |
| `corp-monorepo` | `37b8aa1` | `main` | 0 | 821 | 26 | 23 | **3** |
| `corp-ops` | `3bde930` | `main` | 0 | 60 | 21 | 17 | **4** |
| `corp-sca-time-automation` | `3661b3a` | **`feature/tenrox-loader`** | 0 | 75 | 21 | 16 | **5** |
| `demo-prep` | `1f7c35c` | **`feat/leadership-template-deck`** | **2** | 883 | 22 | 14 | **8** |
| `life-architect` | `7688b76` | `main` | 0 | 45 | 21 | 16 | **5** |
| `terminal-setup` | `d8a7b61` | `main` | 0 | 3 | 3 | 1 | **2** |
| `win-tooling` | `49cb75e` | `main` | 0 | 177 | 24 | 19 | **5** |
| | | | | **5316** | **198** | **162** | **36** |

**Measured as found, left as found (contract §9).** `corp-sca-time-automation` was on
`feature/tenrox-loader` and `demo-prep` on `feat/leadership-template-deck` carrying two dirty
lines (` M .gitignore`, `?? docs/handoffs/2026-09-03-colleague-repo-bootstrap/`). Those two rows
describe a working branch, not `main`. Nothing was cleared, stashed or switched.

**The hub row is measured from this lane's worktree, not the primary checkout** — same
repository and same objects, branch `worktree-lane-s-013-census-fleet-crosscheck` after
`git merge origin/main` fast-forwarded it to `21576e3a`. The worktree-isolation guard refuses a
`git -C` redirect at the shared checkout, so the primary's own working tree was not read; it can
differ from `21576e3a` if another seat has it on a different branch. Stated in §6.

### 1.2 · The 36 out-of-pattern root items, each with a witness

`kind` is how the entry appears in `ls-files`. `witness` is the last content commit for that
path in that repo (`git log -1 -- <path>`), except where a generator or carrier is the stronger
witness and is named instead. Verdicts use **this contract's** enum (§3) — see §5 D5 for how it
maps onto U2's.

| repo | entry | kind | witness | verdict |
|---|---|---|---|---|
| `ai-council` | `VISION.md` | file | `f9d6985` 2026-07-23 · retired by ADR-114 into `canonical_docs.CANONICAL_RETIRED`; hub destination recorded in `CANONICAL_RETIRED_LOCATIONS` | **RELOCATE** → `docs/archive/VISION.md` |
| `ai-council` | `INSTALL.md` | file | **the hub's own carrier** — `deploy/manifest-v1.5.0.yaml` component `install-guide`: `source: plugins/tier1-lifecycle/INSTALL.md` → `path: INSTALL.md` | KEEP |
| `ai-council` | `conftest.py` | file | `dd69003` 2026-07-26 | KEEP |
| `ai-council` | `council_inbox/` | dir | `6342ecd` 2026-02-23 · tracked content is `council_inbox/.gitkeep` and nothing else | KEEP |
| `corp-monorepo` | `VISION.md` | file | `539333b` 2026-06-02 · same ADR-114 witness | **RELOCATE** → `docs/archive/VISION.md` |
| `corp-monorepo` | `INSTALL.md` | file | carrier `install-guide`, as above | KEEP |
| `corp-monorepo` | `tach.toml` | file | `b23d522` 2026-07-17 | KEEP |
| `corp-ops` | `VISION.md` | file | `5515b30` 2026-06-02 · same ADR-114 witness | **RELOCATE** → `docs/archive/VISION.md` |
| `corp-ops` | `INSTALL.md` | file | carrier `install-guide`, as above | KEEP |
| `corp-ops` | `assets/` | dir | `907ea1b` 2026-06-02 · one file, `assets/ruff-pre-commit.yaml` | KEEP |
| `corp-ops` | `tools/` | dir | `b094593` 2026-03-20 · five executables incl. `tools/gdrive-backup.py`, `tools/od-audit-folders.py` | KEEP |
| `corp-sca-time-automation` | `VISION.md` | file | `bf9cb88` 2026-06-02 · same ADR-114 witness | **RELOCATE** → `docs/archive/VISION.md` |
| `corp-sca-time-automation` | `pytest.ini` | file | `ca185bc` 2026-05-28 | KEEP |
| `corp-sca-time-automation` | `requirements.txt` | file | `c013b11` 2026-03-21 · this repo carries no `pyproject.toml` (see §1.3) | KEEP |
| `corp-sca-time-automation` | `assets/` | dir | `586338f` 2026-06-08 · one file, `assets/ruff-pre-commit.yaml` | KEEP |
| `corp-sca-time-automation` | `data/` | dir | `e28afee` 2025-12-29 · two `.gitkeep` placeholders (`data/input/`, `data/output/`) | KEEP |
| `demo-prep` | `VISION.md` | file | `4a23ae1` 2026-07-11 · same ADR-114 witness | **RELOCATE** → `docs/archive/VISION.md` |
| `demo-prep` | `SOURCES.md` | file | `ba2288b` 2026-07-11 | KEEP |
| `demo-prep` | `brand/` | dir | `53fb2ef` 2026-07-21 · 5 files | KEEP |
| `demo-prep` | `examples/` | dir | `4a23ae1` 2026-07-11 · 2 files | KEEP |
| `demo-prep` | `generators/` | dir | `3498662` 2026-09-01 · 34 files | KEEP |
| `demo-prep` | `knowledge/` | dir | `4a23ae1` 2026-07-11 · 686 files — the largest single out-of-pattern population in the fleet | KEEP |
| `demo-prep` | `output/` | dir | `1f7c35c` 2026-09-04 · 32 tracked files | **UNDETERMINED** (§4) |
| `demo-prep` | `pipeline/` | dir | `ba2288b` 2026-07-11 · 45 files | KEEP |
| `life-architect` | `VISION.md` | file | `23247de` 2026-07-07 · same ADR-114 witness | **RELOCATE** → `docs/archive/VISION.md` |
| `life-architect` | `intake/` | dir | `4dfd353` 2026-07-10 · 7 files, dated briefs + `intake/README.md`; `intake` **is** a sanctioned genre in `genre_folders.genres`, and the repo already runs `docs/decisions/` | **RELOCATE** → `docs/intake/` |
| `life-architect` | `OPEN-QUESTIONS.md` | file | `c01371d` 2026-07-07 | KEEP |
| `life-architect` | `dimensions/` | dir | `4dfd353` 2026-07-10 · 9 files | KEEP |
| `life-architect` | `seed/` | dir | `03e0920` 2026-07-07 · 4 files | KEEP |
| `terminal-setup` | `huvix-custom.omp.json` | file | `d8a7b61` 2026-02-18 · one of the repo's three tracked files | KEEP |
| `terminal-setup` | `setup.ps1` | file | `d8a7b61` 2026-02-18 · one of the repo's three tracked files | KEEP |
| `win-tooling` | `VISION.md` | file | `0286cd8` 2026-09-01 · same ADR-114 witness; the newest of the seven | **RELOCATE** → `docs/archive/VISION.md` |
| `win-tooling` | `INSTALL.md` | file | carrier `install-guide`, as above · content commit `cd5d793` 2026-08-29 | KEEP |
| `win-tooling` | `config.yaml` | file | `6771028` 2026-07-11 | KEEP |
| `win-tooling` | `conftest.py` | file | `7e3648d` 2026-08-12 | KEEP |
| `win-tooling` | `tools/` | dir | `6d174ed` 2026-07-11 · 3 files | KEEP |

### 1.3 · The absence half — what the allowlist admits that a root does not have

The allowlist is a permitted set; `CANONICAL_MANDATORY` is the required subset. A seal refuses
what is present and is blind to what is missing, so this table is measured from the same
`ls-files` output and is the half no seal run produces. `+` present, `.` absent.

| repo | 6× CANONICAL | README | AGENTS | `.methodology` | `.pre-commit` | `.gitattributes` | `pyproject` | `uv.lock` | `.python-version` | workspace |
|---|---|---|---|---|---|---|---|---|---|---|
| `.dev-knowledge` | 6/6 | + | + | + | + | + | + | + | + | + |
| `ai-council` | 6/6 | . | . | + | + | + | + | . | . | + |
| `corp-monorepo` | 6/6 | . | . | + | + | + | + | . | . | + |
| `corp-ops` | 6/6 | . | . | . | . | + | + | . | . | + |
| `corp-sca-time-automation` | 6/6 | . | . | . | + | . | . | . | . | + |
| `demo-prep` | 6/6 | . | . | . | + | + | + | . | . | + |
| `life-architect` | 6/6 | . | . | . | + | + | + | . | . | + |
| `terminal-setup` | **0/6** | + | . | . | . | . | . | . | . | **.** |
| `win-tooling` | 6/6 | + | . | . | + | . | + | . | . | + |

Four measurements from that table, each of which changes how the 36 above should be read:

1. **`terminal-setup` carries none of the six canonical mandatory documents** — no
   `ARCHITECTURE.md`, `BACKLOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `JOURNAL.md` or
   `LESSONS.md`, and no workspace file. Its three tracked files are `README.md`,
   `huvix-custom.omp.json`, `setup.ps1`. `ecosystem/registry.md` already records it as
   *"unonboarded … no methodology adoption"*, so this is the register's claim, verified.
2. **`.methodology.yaml` — the ONLY register a declared, time-boxed waiver can live in
   (`scripts/enforcement_coverage.py`: `ALLOWLIST_REL = ".methodology.yaml"`, read at the repo
   ROOT, fail-soft to `[]` when absent) — exists at 2 of 8 consumers.** Six consumers have no
   file in which a waiver can be recorded at all. **The two that have it are exactly the two
   `ecosystem/registry.md` marks `onboarded`** — `ai-council` (v1.3.1) and `corp-monorepo`
   (v1.2.0); the six that lack it are exactly the six marked `unonboarded` or
   `methodology-unonboarded`. The correlation is total, and the deploy manifest expects the file
   at every consumer root (`expect: ".methodology.yaml present at the consumer root with a
   sanctioned_divergences: block"`). Consequence for a waiver-heavy fleet verdict: a waiver can
   be *declared* today in 2 of 8 consumers.
3. **The ADR-106 declared-environment pair is hub-only.** `uv.lock` and `.python-version` are
   present at **0 of 8** consumers. `pyproject.toml` reaches 6 of 8;
   `corp-sca-time-automation` (pre-uv, `requirements.txt` + `pytest.ini`) and `terminal-setup`
   (no Python) have none.
4. **`README.md` is at 2 of 8 consumers** — `terminal-setup` and `win-tooling`. This
   independently re-derives the parenthetical inside `[#621]`'s own row body
   (*"only **2 of 8** children carry a root README, so a flip REDs six"*) from the tree rather
   than from the row. **`AGENTS.md` is at 0 of 8** — ADR-115's portable instruction layer has
   not left the hub.

---

## Proposals

Grouped by verdict, per contract §4. **Every one is a proposal; the operator rules each.**
Nothing here is executed by this lane.

### RELOCATE — 8 items, 7 repos

**R1 · `VISION.md` → `docs/archive/VISION.md` — 7 consumers.**
`ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`,
`life-architect`, `win-tooling`.
*Witness (one, shared).* ADR-114 Amendment 1 retired `VISION` out of
`canonical_docs.CANONICAL_MANDATORY` into `CANONICAL_RETIRED`; `CANONICAL_RETIRED_LOCATIONS`
records the destination as `docs/archive/VISION.md`; the hub executed exactly that move under
`[#614]` lane-e-5 at `24eac392` (2026-09-05), and this lane confirms the hub's root
`VISION.md` is gone at `21576e3a` while `docs/archive/VISION.md` is tracked. The open row that
owns the fleet half is `[#621]`.
*Note on the enum.* The destination is a **retention home**, so `ARCHIVE` is the same act under
a different label in this contract's grammar. Recorded as `RELOCATE` so the two derivations stay
comparable; the operator may prefer the other word and nothing else changes.

**R2 · `life-architect/intake/` → `docs/intake/` — 1 repo, 7 files, no rename.**
*Witness.* `intake` is a member of `genre_folders.genres`, and `home_grammar` admits
`docs/intake` and `docs/intake/archive` — so the content is in-pattern and only the level is
wrong. The repo has already adopted the genre layout for one genre: `docs/decisions/` carries
`ADR-01`…`ADR-07` plus a `README.md`. Its `intake/` holds the same shape the hub's
`docs/intake/` holds — dated briefs (`2026-07-06-life-architect.md`,
`2026-07-08-endpoint-driven-life-brief.md`, …) plus a `README.md`.

### KEEP — 27 items

**KEEP means the file stays exactly where it is and the proposal is directed at the SPEC.**
This contract's enum has no `WAIVE`; see §5 D5. Grouped by the spec change each would need,
smallest change first.

- **K1 · `INSTALL.md` — 4 repos (`ai-council`, `corp-monorepo`, `corp-ops`, `win-tooling`).**
  *Witness: the hub's own deploy carrier writes it.* `deploy/manifest-v1.5.0.yaml` component
  `install-guide` declares `source: plugins/tier1-lifecycle/INSTALL.md` → `path: INSTALL.md`,
  and the hub deliberately grows no root `INSTALL.md` of its own — so the allowlist, which
  unions the spec literals with `CANONICAL_MANDATORY`, cannot admit it.
  **Independently sharpened here.** Intake #73's acceptance criterion 2 is *"the set of `path:`
  values at consumer depth 0 across `deploy/manifest-v*.yaml` is a subset of the admitted root
  set"*. That set was enumerated across **all six** manifests (`v1.0.0` … `v1.5.0`) and is
  **three paths — `.methodology.yaml`, `.pre-commit-config.yaml`, `INSTALL.md`.** Two of the
  three **are** admitted by `root_allowlist.files`. **Exactly one is not, and it is
  `INSTALL.md`** — so criterion 2 fails on one path, not on a class. **Proposed spec change: add
  `INSTALL.md` to `root_allowlist.files`.** One line, four repos.
- **K2 · Standard Python root files — 4 items, 3 repos.** `conftest.py` (`ai-council`,
  `win-tooling`), `pytest.ini` and `requirements.txt` (`corp-sca-time-automation`).
  *Witness: last content commit, per §1.2.* `root_allowlist.files` carries `pyproject.toml`,
  `uv.lock` and `.python-version` and no pre-uv Python root file, and the hub has no
  `conftest.py` anywhere in its tree to have generated one. **Proposed spec change: a
  `python_layout`-adjacent clause admitting the standard root files.** Migrating
  corp-sca's toolchain off `requirements.txt` is a real decision and is **not** proposed here.
- **K3 · Domain top-level directories — 13 items, 6 repos.** `assets/` ×2, `tools/` ×2,
  `data/`, `council_inbox/`, `brand/`, `examples/`, `generators/`, `knowledge/`, `pipeline/`,
  `dimensions/`, `seed/`. (`demo-prep/output/` is the 14th of this shape and is
  **UNDETERMINED**, below, on merits that are orthogonal to the shape question.)
  *Witness: last content commit, per §1.2.* The allowlist has **no domain-directory concept at
  all**: D5 added `src`, `eval` and `models`, which covers a code repo's source but not a
  content repo's subject matter. `demo-prep` is the extreme case — six of its directories are
  its subject matter and `knowledge/` alone is 686 files. **Proposed spec change: the repo-KIND
  axis intake #73 records as its open question 1.** This is the largest group and the only one
  whose fix is a design fork rather than a line.
- **K4 · Non-dot-prefixed root tool config — 2 items, 2 repos.** `corp-monorepo/tach.toml`,
  `win-tooling/config.yaml`. *Witness: last content commit.* ADR-59 Decision 3 puts root tool
  config behind a dot prefix; neither file is dot-prefixed and neither has an allowlist entry.
  Two independent repos hitting one class.
- **K5 · Repo-local root living docs — 2 items, 2 repos.** `demo-prep/SOURCES.md`,
  `life-architect/OPEN-QUESTIONS.md`. *Witness: last content commit.* Each is a living document
  the repo wrote for itself; the allowlist's file half is a closed literal list with no
  repo-local extension point.
- **K6 · `terminal-setup`'s entire content — 2 items.** `huvix-custom.omp.json`, `setup.ps1`.
  *Witness: `d8a7b61` 2026-02-18, the repo's only content commit; `ecosystem/registry.md` records
  the repo as unonboarded with no methodology adoption.* Measuring a 3-file repo that has never
  received the methodology against the methodology's shape measures the absence of adoption.
  **The reportable question is not what to do with these two files — it is whether ADR-104
  membership should imply seal coverage for an unonboarded repo at all.**

### ARCHIVE — 0 items

None proposed. `docs/archive/` appears as the destination of R1, and R1 is recorded as a
RELOCATE for the reason stated there.

### RETIRE — 0 items

**Zero RETIREs across 36 items in eight consumer repositories, and that is a finding, not an
omission.** Not one root item resolved to junk: every one is either a live artifact with a
recent content commit, the repo's own subject matter, a file the hub's own carrier placed, or
the ordinary Python/tooling layout the allowlist happens not to carry. Where a deletion could be
argued, it is UNDETERMINED below rather than proposed.

### UNDETERMINED — 1 item

- **U1 · `demo-prep/output/` (32 tracked files, `1f7c35c` 2026-09-04).**
  *What I could not establish:* whether `output/` is regenerable from `generators/` (34 files)
  and `pipeline/` (45 files), and therefore whether tracking it is a deliberate decision about
  deliverables or accreted build output. Answering that means reading three directories'
  contents in a consumer repo, which is beyond a root cross-check and beyond this lane's
  read-only remit as scoped. **The shape verdict is not in doubt** — it is a domain directory
  and K3's spec change disposes of it as a Rule A item either way. **The merits verdict
  (KEEP vs RETIRE) is, and it is the one row in this census where a deletion is arguable.**
  Recorded as UNDETERMINED rather than waved through as KEEP.

---

## Counts before → proposed after

```
BEFORE (measured 2026-09-07, 9 repositories, root depth)
  repositories in the ratified fleet                            9   (1 hub + 8 consumers)
  root entries examined                                       198
  admitted by the #73 allowlist                               162
  OUT OF PATTERN                                               36   (hub 0 · consumers 36)

VERDICTS PROPOSED (this lane's enum, contract section 3)
  RELOCATE                                                      8   (7x VISION.md + 1 intake/)
  ARCHIVE                                                       0
  RETIRE                                                        0
  KEEP  (file stays; the proposal is directed at the SPEC)      27
  UNDETERMINED                                                  1   (demo-prep/output/ merits)
                                                              ---
                                                               36

AFTER, if the operator rules the 8 RELOCATEs and nothing else
  files that move in a consumer repository                      8
  files deleted anywhere                                        0
  OUT OF PATTERN                                               28   (all 28 in the SPEC, not
                                                                    in any consumer)

AFTER, if the operator ALSO rules the five spec changes named in K1-K6
  K1 admit INSTALL.md to root_allowlist.files                  -4
  K2 admit the standard Python root files                      -4
  K3 the repo-KIND / domain-directory axis (incl. output/)    -14
  K4 a root tool-config clause                                 -2
  K5 a repo-local root living-doc extension point              -2
  K6 seal coverage for an unonboarded repo                     -2
                                                              ---
  OUT OF PATTERN                                                0

RESIDUE SPLIT -- the headline, stated as measured
  attributable to a consumer  (something is in the wrong place)  8 of 36  =  22%
  attributable to the spec    (the allowlist has no entry)      28 of 36  =  78%
```

**Read the split against U2's.** U2 measured 97% waivers across all three rules. This lane
measures 78% spec-residue at the root grain alone. The two numbers agree in direction and differ
because Rule A is the rule that works: **it is the only rule in the seal that produced actionable
findings in either derivation, and it produced all 8 of this census's RELOCATEs.**

---

## 5 · Disagreements with W2-U2 — listed, not reconciled

Contract §10: *"Two independent derivations that agree are evidence; two that have been talked
into agreeing are one derivation."* Nothing below was adjusted after reading U2.

**The eight consumer HEADs this lane stamped are byte-identical to U2's** (`7a3c057`,
`37b8aa1`, `3bde930`, `3661b3a`, `1f7c35c`, `7688b76`, `d8a7b61`, `49cb75e`). The two
derivations therefore measured the same bytes, and a difference below is a difference of
instrument or of judgment, never of input.

**A0 — the agreement, stated first because it is the load-bearing result.** U2's §1.1 reports
Rule A per repo as `A-f` (files) + `A-d` (directories) + `A-g` (genres). Summing its file and
directory columns — the only quantity comparable to a root cross-check — gives
**4 · 3 · 4 · 5 · 8 · 5 · 2 · 5 for the eight consumers and 0 for the hub: 36.** This lane
derives **36**, from a different code path (a YAML parse plus set membership, never
`validate_hermetization`'s rule functions), and the items agree **one for one in all nine
repositories** — same names, same kinds, no item in one list absent from the other.

**D1 — win-tooling: U2 counts 6 Rule A items, this lane counts 5.** The sixth is
`docs/diagrams/`, U2's single `A-g` genre violation across the whole fleet. It is at depth 1 and
a root cross-check is structurally blind to it. **Re-opened before reporting:**
`git -C win-tooling ls-files docs` returns `docs/diagrams/module-map.md` — the item is real and
U2 is right. Listed as a scope difference, not a defect on either side.

**D2 — the hub's tracked-file count: U2 says 2,993, this lane says 2,998.** Different HEAD, and
the difference resolves exactly. U2 measured at `ef53b069`; this lane merged `origin/main`
before its first commit and measured at `21576e3a`. `git diff --diff-filter=A ef53b069 21576e3a`
lists **five** added files — `deploy/floor_mechanisms.py`, `tests/test_floor_mechanisms.py`,
`docs/audits/2026-09-06-technical-erratum-aj-second-pass.md`,
`docs/decisions/ADR-117-carrier-split-by-divergence.md`, and
**`docs/audits/2026-09-07-technical-seal-report-fleet.md`, U2's own report**. 2,993 + 5 = 2,998.
Not reconciled, and it needs no reconciling: U2 measured the hub before its own artifact landed,
which is the correct thing for it to have done. The hub is a moving target while a batch is in
flight; both figures are right at their stamp.

**D3 — the hub reads as "137 items" in U2 and "0" here, and both are true.** U2's hub row is
137 items, **all of them Rule B** (`R0 / T0 / W137`) — the hub's own dated artifacts measured
against its own class enum. Its Rule A columns for the hub are `0 / 0 / 0`. This census measures
Rule A only, so the hub is 0 out-of-pattern at the root. Listed because the two figures read as
a contradiction at a glance and are not one.

**D4 — verdict grammar: the two lanes do not share an enum, and a naive merge will
double-count.** U2's enum is `RELOCATE / RETIRE-PROPOSED / WAIVE / ESCALATED`. This lane's,
fixed by its own contract §3, is `KEEP / RELOCATE / ARCHIVE / RETIRE / UNDETERMINED` —
**there is no `WAIVE`.** The 27 items U2 would waive are recorded here as **KEEP**, which is
the same physical outcome (nothing moves in a consumer) under a different word and with the
proposal pointed at the spec rather than parked. Flagged for filings-N2: one folder appearing
twice in `RATIFICATION-2026-09-07.md` §SWEEP with `WAIVE 27` and `KEEP 27` is one finding, not
two.

**D5 — `demo-prep/output/`: U2 says WAIVE, this lane says UNDETERMINED.** U2's §7 flags it as
*"the one row here where RETIRE-PROPOSED could be argued"* and then waives it. This lane reaches
the same doubt and declines to resolve it, because the fact that would resolve it —
regenerability from `generators/` + `pipeline/` — was not established. A genuine judgment
difference on one row, listed and left open.

**D6 — the carrier/allowlist conflict is exactly ONE path, which U2 did not quantify.** U2
correctly identifies `INSTALL.md` as carrier-written (its Class I, 4 repos). Derived from the
other end here: the set of `path:` values at consumer depth 0 across all six manifests in
`deploy/` is **three** — `.methodology.yaml`, `.pre-commit-config.yaml`, `INSTALL.md` — of which
the first two are admitted by `root_allowlist.files` and **`INSTALL.md` is the only one that is
not.** Intake #73's acceptance criterion 2 therefore fails on one component, not on a class.
This SHARPENS U2 rather than contradicting it, and it makes K1 the cheapest ruling on either
list.

**D7 — a second carrier/spec disagreement, which a presence-only instrument cannot see.**
`deploy/manifest-v1.5.0.yaml` still carries a `doc_shapes:` stanza for `VISION.md` (spine
`## Vision / ## Scope / ## Values / ## Lifecycle / ## References`, `freshness_gated: false`,
comment: *"VISION keeps its spine (still shape-checked, not removed from the tree)"*), and the
same file's header note 3 states *"`VISION.md` is present at repo root today"*. At `21576e3a`
the hub's root `VISION.md` is **not** present — `git ls-files` shows only
`docs/archive/VISION.md` (relocated at `24eac392`, 2026-09-05). **Reported, and deliberately
not called a defect:** `v1.5.0` is the sole **untagged** manifest in `deploy/` (`git tag`
lists `v1.0.0` … `v1.4.0`), i.e. the in-flight one, and it is a batch-U-wave-2 footprint this
lane reads and never writes — it gained 228 lines during this very session. It matters to the
seven R1 proposals because they are proposed against a spec whose carrier still describes the
pre-relocation world, and whoever rules R1 should know that.

**D8 — the absence half is missing from U2, and it is a precondition on U2's own result.**
A seal refuses presence and is blind to absence, which U2 states about itself. Two measurements
from §1.3 bear directly on U2's 336 waivers: **`.methodology.yaml`, the only register a declared
time-boxed waiver can live in, exists at 2 of 8 consumers — exactly the two the registry marks
`onboarded`** — so six consumers have nowhere to record one; and **`terminal-setup` carries none
of the six canonical mandatory documents**,
which is a larger fact about that repo than the two items either lane found in it. Not a
contradiction of U2 — a half its instrument could not reach.

---

## 6 · Gemini fan-out

**fan-out: PARTIAL — and the CLI's state is reported, not simplified to "clean" or "absent".**

- **`gemini` IS on PATH** (`/c/Users/1028120/AppData/Roaming/npm/gemini`, version `0.56.0`) and
  **fails on every invocation**: `IneligibleTierError: This client is no longer supported for
  Gemini Code Assist for individuals. To continue using Gemini, please migrate to the
  Antigravity suite of products`. This is neither "absent" nor "clean" — the binary answers
  `--version` and then refuses all work.
- **The working Gemini path on this machine is `agy`** (`1.1.27`, the Antigravity CLI the error
  message points at). It was used as the reader.
- **Reader mode: tool-denied.** `agy --print` auto-denies any tool needing a permission prompt
  (`a tool required the "command" permission that headless mode cannot prompt for`). Running it
  with `--dangerously-skip-permissions` would auto-approve **all** tools including writes, in a
  read-only census running beside twelve peers — **not done.** The reader was therefore fed the
  inventories as text and given a pure retrieval-and-ranking task.
- **Gemini-read FILES: 0.** Stated plainly rather than inflated: the reader opened no file on
  disk. It was handed **9 root inventories**, one per repository, derived from
  `git -C <repo> ls-files` output totalling **5,316 tracked paths**, and asked to return the
  entries not admitted by the allowlist.
- **Fabrications: 0.** Across all nine repositories the reader returned **36 entries and no
  others**, and named `NONE` for the hub. Every returned entry was re-opened against the
  `ls-files` dump it came from; every one resolves to a tracked path. No entry was invented, and
  no entry present in the data was returned with a name it does not have.
- **Corroboration value, stated honestly.** Because the reader was given the inventory rather
  than the tree, this is an independent check on the *membership test*, not on the *enumeration*.
  It cannot catch an error in the `ls-files` step. It did catch nothing, which is the expected
  result for a set-membership task and is reported as such rather than as a strong second
  opinion.
- **One measured CLI limit, recorded for the next lane.** A single `agy --print` call carrying
  all nine inventories (~5.5 KB of prompt) **exited 0 with completely empty output**. Split into
  nine per-repo calls, every one returned correctly. A silent empty success is the dangerous
  failure mode here: a lane that ran the one big call and reported "the reader found nothing"
  would have reported a clean fleet.
- **Copilot Enterprise offload: NOT AVAILABLE and NOT USED.** It is blocked until `#75` is
  ratified and admitted. Recorded here so no later reading of this batch claims it was used.

---

## Honest limits

This section is the point of the census, not filler. Each item is something this lane could
**not** establish, stated so nobody reads past it.

1. **Root depth only.** This census sees a top-level file and the first segment of a tracked
   path. It is structurally blind to everything Rule B (dated-artifact naming) and Rule C (home
   grammar) measure, and to Rule A's `docs/<genre>/` leg. U2 measured 348 items across all
   three; this lane measured 36. **The 36 are a subset of the 348, not a competing total.**
   D1 is the concrete instance: `win-tooling/docs/diagrams/` is a real Rule A item that this
   instrument cannot see.
2. **Tracked files only.** `git ls-files` reports the index. An untracked or gitignored file
   sitting in a consumer root is invisible to every number in this file. No repository's working
   tree was listed, because listing one is not a read this lane needs and `status --porcelain`
   answered the dirty question without it.
3. **`demo-prep` and `corp-sca-time-automation` were measured on a working branch, not `main`,**
   and `demo-prep` carried two dirty lines. Their rows describe `feat/leadership-template-deck`
   and `feature/tenrox-loader`. What `main` looks like in either repo is **not** measured here,
   and nothing was switched to find out.
4. **The hub row is this lane's worktree, not the primary checkout.** The worktree-isolation
   guard refuses a `git -C` redirect at the shared checkout, so `.dev-knowledge`'s own row is
   `git ls-files` inside `.claude/worktrees/lane-s-013-census-fleet-crosscheck` at `21576e3a`
   — the same repository and objects, but if a concurrent seat has the primary on a different
   branch, its working tree differs from this row. Twelve peer lanes and a wave-2 batch are
   live in this repository right now.
5. **The fleet moved under U2 and can move under this file.** The hub gained five tracked files
   between `ef53b069` and `21576e3a` during this session (D2). The eight consumer HEADs did not move
   between the two derivations — that was checked, not assumed — but nothing prevents them from
   moving after this file is written.
6. **`council_inbox/`'s write-target claim is not verified here.** This lane established that
   its only tracked content is `.gitkeep` (`git ls-files council_inbox`). It did **not** grep
   ai-council's source for something that writes into it, so "a runtime inbox the CLI writes
   into" is U2's finding, cited, not re-derived. KEEP is proposed on the `.gitkeep` witness
   alone, which is the low-risk verdict and not the same as proving the directory is load-bearing.
7. **`demo-prep/output/` is UNDETERMINED on merits** — see U1. Regenerability was not
   established and is the fact that would settle it.
8. **A witness is a last content commit, not a merits review.** For 27 of the 36 items the
   witness establishes *that the file is a live, dated artifact of its repo* — not that its
   content is correct, current, or wanted. This census does not claim any of those.
9. **Three of the four documents this census leans on are not ratified.** `intake #73` is
   `status: DRAFT`; `ecosystem/fleet-shape-spec.yaml` carries `spec_version: 1` and its own note
   that it is *"HUB-READ ONLY -- the consumer carrier is a later act"*; `deploy/manifest-v1.5.0.yaml`
   is untagged and in flight. Only ADR-104's declaration and ADR-114 are ratified. **The
   allowlist this census measures against is therefore a landed but unratified surface**, and a
   change to it changes every count above.
10. **`config/` is unruled and it bounds K3.** Intake #73's open question 8 records that
    `config/`'s fate is undecided and that ROOT-R1 — the census that would have decided it —
    **does not exist in the tree**. `config` is admitted as a bare root directory here and 6 of 8
    consumers use it, so no root item in this census turns on it; the moment K3's repo-KIND axis
    is drafted, it does.
11. **`AUDIT_CLASS_ENUM` scope was not tested by this lane.** The spec marks it
    `audit_class_enum_scope: repo-local`. That is Rule B's territory, it is 194 of U2's 348
    items, and nothing in this file measures or disputes it.
12. **Gemini corroborated the membership test, not the enumeration** — see §6. An error in the
    `git ls-files` step would have survived the fan-out unnoticed.
13. **No consumer repository was modified, and this is checkable rather than asserted.** The
    only verbs issued against a consumer were `ls-files`, `rev-parse` and `status --porcelain`.
    `demo-prep`'s two dirty lines are the same two lines U2 recorded hours earlier, unchanged.
14. **No full suite was run** (contract §6), so no claim is made about the known main RED in
    `tests/test_manifest_link_route.py`. It is not this lane's and was not touched.

---

**Lane:** `lane-s-013-census-fleet-crosscheck` · SWEEP 2026-09-07 row **S-13** · branch
`worktree-lane-s-013-census-fleet-crosscheck` (contract §9 substrate deviation: LOCAL, not cloud)
**Measured:** 2026-09-07, hub at `21576e3a`, eight consumers at the HEADs stamped in §1.1
**Mode:** READ-ONLY REPORT — every verdict is a proposal; the operator rules each list
