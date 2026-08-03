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

---

**Filed by:** CC, ARC 0, 2026-08-03 · **Governs:** [#383] · **Cites:** `1afd9579`, `67863180`
