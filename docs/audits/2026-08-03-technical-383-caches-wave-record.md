# [#383] caches wave — wave record (naming + Done-when ratification)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** 383-caches-wave-record
- **Arc:** ARC 0 of the 2026-08-03 afternoon execution window, branch
  `docs/383-ratify-caches-wave`. Architect-approved contract, amended in-session (below).
- **Status:** **RATIFICATION, not a wave execution.** This record opens the caches wave and
  fixes its Done-when. It closes no row and converges no surface. The wave's own runs — the
  two commands clause (b)/(c) name — belong in this file when the wave is actually executed.
- **Base:** `main` = `0c64a76a`, working tree clean at open.
- **Why this file exists:** the replacement Done-when requires runs "pasted verbatim into the
  wave record" and names any unwalkable repo there. That artifact is this one. Wave 1's record
  (`docs/audits/2026-07-31-technical-intake-split-generality-discharge.md`) is a **different
  wave's sealed record** and was deliberately not reused.

---

## 1. Surface naming — the wave is named by its surface, not by a number

This wave's surface is **caches / gitignore-effect**: the eight rows at
`ecosystem/parity-surfaces.yaml:834-899`, every one carrying `probe: {type: check_ignore}`.

| # | Row id | Probe candidate | Tier |
|---|---|---|---|
| 1 | `ignore-venv` | `.venv/x` | hub+consumer IGNORE |
| 2 | `ignore-pycache` | `__pycache__/x.pyc` | hub+consumer IGNORE |
| 3 | `ignore-pytest-cache` | `.pytest_cache/x` | hub+consumer IGNORE |
| 4 | `ignore-ruff-cache` | `.ruff_cache/x` | hub+consumer IGNORE |
| 5 | `ignore-mypy-cache` | `.mypy_cache/x` | hub+consumer IGNORE |
| 6 | `ignore-hypothesis` | `.hypothesis/x` | hub+consumer IGNORE |
| 7 | `ignore-egg-info` | `probe.egg-info/x` | hub+consumer IGNORE |
| 8 | `ignore-node-modules` | `node_modules/x` | hub only |

It was chosen because it is **the only surface both fully specified and observationally
probed** — the rows carry effect probes (`git check-ignore` via the resolver), not presence
or text-grep assertions. `parity-surfaces.yaml:831-833` states the constraint the class was
built under: *"check = gitignore parity via the resolver, NEVER presence … and NEVER
text-grep (FR-6: the corp inline-comment gotcha false-passes a text probe)."*

**Boundary, recorded so a later reader does not over-read the range.** A ninth
`gitignore-effect` row exists — `ai-env-ignored` at `parity-surfaces.yaml:902`, scoped
`{ai-council: IGNORE}`. It is **outside** this wave's cited `:834-899` range and outside its
Done-when. Named here rather than silently excluded.

## 2. "Wave 3" is an alias, and it is RETIRED

The label "Wave 3" circulated for this work. It is retired as of this record.

Waves 1–2 were **`docs/intake/`** (the ADR-109 §4 generality discharge) and **fleet
membership** (the [#462] membership-agreement census). Neither is a member of [#383]'s own
six-surface list — that list reads *caches, the `.claude` surface incl. skills,
archives-inside-each-folder, docs layout, Python parity, colours-via-carrier*. Counting them
as waves 1–2 makes "wave 3" name the third item of a sequence whose first two members are not
in the sequence.

So this is the **first true surface wave**, and it is named **caches**, not a number. Surface
names are stable; ordinals drift as unrelated work gets retro-numbered into the same series.

## 3. Correction: `67863180` is NOT an ADR-109 §4 discharge

An off-repo claim in circulation held that `67863180` discharged ADR-109 §4. **It did not.**
Both commit messages were read in full to settle it:

- **`67863180`** — *"Merge branch `feat/462-membership-agreement-census` — closes [#462]: the
  membership blind spot mechanized, 9 governs"*. Its ADR-109 edit is stated in its own body:
  *"ADR-109 Related-line gloss corrected by APPENDED amendment (ADR-94): 9 governs; the 5 is a
  data artifact of `resolve_fleet_members` keying on `deployed-versions.yaml`."* A
  Related-line gloss, not a §4 discharge.
- **`1afd9579`** — *"Merge branch `feat/intake-split-generality-discharge` — [#383] wave 1:
  ADR-109 §4 DISCHARGED"*. Its body records the appended §4 amendment marker and the
  byte-exact round-trip proof.

**ADR-109 §4 has been discharged exactly once, at `1afd9579`.** Both commits happen to touch
ADR-109 by +54 lines, which is what makes a stat-only read of the two indistinguishable — the
distinguishing evidence is the message body, not the diffstat.

## 4. Why the Done-when was replaced

The clause this record's arc replaced read: *"per wave, the divergence report shows zero
undeclared divergence for that surface and the operator has read it."*

It was **vacuously true on the day it was written, with zero work done**. Measured live
2026-08-03 on `main` @ `0c64a76a`:

```
$ python scripts/desired_state_report.py
summary — conform: 185 · diverge: 3 · declared: 3 · n/a: 219

| ignore-venv          | conform | conform | conform | · | · |
| ignore-pycache       | conform | conform | conform | · | · |
| ignore-pytest-cache  | conform | conform | conform | · | · |
| ignore-ruff-cache    | conform | conform | conform | · | · |
| ignore-mypy-cache    | conform | conform | conform | · | · |
| ignore-hypothesis    | conform | conform | conform | · | · |
| ignore-egg-info      | conform | conform | conform | · | · |
| ignore-node-modules  | conform | ·       | ·       | · | · |
```

All eight rows already read `conform`, so "zero undeclared divergence for that surface" was
satisfied before the wave began. This run is byte-identical to the 2026-07-31 and 2026-08-02
runs. The defect is the same class this window has paid for repeatedly: **a green that
measures nothing.**

The replacement clause is stricter in three specific ways — it names the exact rows, it adds
a second independent organ (`fleet_parity`, which executes probes rather than reading the
declaration layer), and it forbids counting an unwalkable repo as clean.

**Honest limit of the declaration layer**, quoted from the report's own HONEST LIMITS block:
*"'conform' = no divergence DECLARED for the cell — the declaration layer. No observational
join is claimed (surface⇄finding joins await the G9 crosswalk population), and probe
execution stays fleet_parity's."* That is precisely why clause (b) adds `fleet_parity`: one
organ reads what is declared, the other executes probes. The old clause relied on the
declaration layer alone.

## 5. Wave execution runs

**Not yet executed.** When the wave runs, both commands below are pasted here verbatim, and
any repo `fleet_parity` could not walk is named here rather than counted as clean:

- `python scripts/desired_state_report.py` — no `diverge` cell on any of the 8 rows
- `python scripts/fleet_parity.py --run-date <run-date>` — 0 warn-undeclared, 0 must-absent,
  0 tombstone-violated across those 8 rows, for every repo walked

<!-- WAVE-EXECUTION:START -->

> **Superseded by the block below (in-file amendment marker, CLAUDE.md §5 item 3).** The
> paragraph above is the ex-ante placeholder, preserved verbatim rather than rewritten: this
> record is an audit and audits are immutable, so the execution evidence is APPENDED and the
> "Not yet executed" text stands as what was committed to before the wave ran.

**EXECUTED 2026-08-04.** Both runs verbatim below. **OPERATOR: read the coverage statement in
§5.3 — the clause is met, and it is met over 3 of the fleet's 9 declared repos.**

### 5.1 Run (a) — `PYTHONUTF8=1 python scripts/desired_state_report.py` (exit 0)

VERDICT: **no `diverge` cell on any of the 8 rows.** The report's only three `diverge` cells are
on `corpus-version`, which is not one of the 8 and is out of this wave's scope.

```
summary — conform: 185 · diverge: 3 · declared: 3 · n/a: 219

| surface | .dev-knowledge | ai-council | corp-monorepo | corp-ops | corp-sca-time-automation |
|---|---|---|---|---|---|
| ignore-venv | conform | conform | conform | · | · |
| ignore-pycache | conform | conform | conform | · | · |
| ignore-pytest-cache | conform | conform | conform | · | · |
| ignore-ruff-cache | conform | conform | conform | · | · |
| ignore-mypy-cache | conform | conform | conform | · | · |
| ignore-hypothesis | conform | conform | conform | · | · |
| ignore-egg-info | conform | conform | conform | · | · |
| ignore-node-modules | conform | · | · | · | · |
```

### 5.2 Run (b) — `PYTHONUTF8=1 python scripts/fleet_parity.py --run-date 2026-08-04` (exit 0)

VERDICT: **0 warn-undeclared, 0 must-absent, 0 tombstone-violated on the 8 rows.** No `ignore-*`
row appears anywhere in the 28 findings — grepped, not inferred. The run's single
`warn-undeclared` is `ai-council root-sweep` / `conftest.py`, a DIFFERENT row and the standing
[#430] dispositioned WARN.

```
wrote logs\FLEET-PARITY.md
[fleet-parity] 3 repo(s) walked: 183 at-parity, 20 pass-declared, 1 gate-ahead-declared, 1 warn-undeclared, 0 must-absent, 0 tombstone-violated, 0 advisory-rewarn, 1 stale, 0 refused -- see logs/FLEET-PARITY.md
[fleet-parity] ownership (ADR-103): 57 methodology-generic, 9 project, 15 conditional -- management surface #329
```

### 5.3 Coverage — the repos NOT walked, named rather than counted clean

`fleet_parity` reports **"3 repo(s) walked"**, not 9. Naming every repo the run did not probe,
per this record's own standing requirement:

| repo | in `parity-surfaces.yaml` fleet? | walked? | why not |
|---|---|---|---|
| `.dev-knowledge` | yes | **yes** | — |
| `ai-council` | yes | **yes** | — |
| `corp-monorepo` | yes | **yes** | — |
| `corp-ops` | yes | **no** | `skipped-pre-deploy` — registered, no methodology deployed yet |
| `corp-sca-time-automation` | yes | **no** | `skipped-pre-deploy` — registered, no methodology deployed yet |
| `demo-prep` | **no** | no | absent from the parity manifest's `fleet` list entirely |
| `life-architect` | **no** | no | absent from the parity manifest's `fleet` list entirely |
| `terminal-setup` | **no** | no | absent from the parity manifest's `fleet` list entirely |
| `win-tooling` | **no** | no | absent from the parity manifest's `fleet` list entirely |

So the ratified clause is **met on the evidence available**, and the evidence covers **3 of the
9 repos ADR-104 declares**. The 2026-08-03 witness was 1-of-9; this run is 3-of-9. The remaining
six are two distinct gaps, not one: two are registered-but-undeployed (a lifecycle state the
walk renders explicitly rather than hiding), and four are not in the parity manifest's `fleet`
list at all — the same declared-vs-machine-surface asymmetry `check_membership_agreement`
reports as data.

In run (a) the same three repos read `conform` on all 8 rows while `corp-ops` and
`corp-sca-time-automation` read `·` (no declaration for these rows), which is consistent with
(b): the declaration layer and the probe layer agree about who is covered.

### 5.4 Divergence found: none on the 8 — and one live defect found while running them

No divergence on any of the 8 rows, in either layer, so no consumer-side fix is owed and the
out-of-scope boundary (consumer repairs belong to the consumer repos) was never reached.

Found while executing, recorded rather than dropped: **`scripts/desired_state_report.py` dies on
a cp1252 console** — `UnicodeEncodeError: 'charmap' codec can't encode character '⇄'`
(the `⇄` in its own HONEST LIMITS text). Same class as [#470] (`audit.py checks`, U+2192) but a
different script and a different glyph, so [#470]'s ASCII-swap fix does not cover it. Both runs
above therefore ran under `PYTHONUTF8=1`. Not fixed here — this wave does not own that script.

<!-- WAVE-EXECUTION:END -->

---

**Filed by:** CC, ARC 0, 2026-08-03 · **Governs:** [#383] · **Cites:** `1afd9579`, `67863180`
