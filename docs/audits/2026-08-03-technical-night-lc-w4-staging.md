# Night batch 2026-08-03 · lane L-C — W4 staging: [#383] wave state + [#465] leg-4 contract

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-lc-w4-staging
- **Status:** DRAFT / INPUT — read-only night batch, unattended. Nothing was filed, closed,
  reworded, deleted or committed. Both Part-1 and Part-2 deliverables are **drafts for the
  morning architect to freeze**; neither lands here.
- **Base:** local `main` = `origin/main` = `65a549bf` (2026-07-31), but HEAD =
  `c7628a3e` on `claude/night-batch-2026-08-03-k8djp8`, **174 commits ahead of `main`**
  (`git rev-list --count main..HEAD` = 174). All 2026-08-01/02 work is on HEAD, not on
  `main`. Every spine claim below is read from `git log --first-parent --oneline HEAD`,
  stated as such, never from `main`.
  > **Editor's correction (lane L-A, same night, after `git fetch origin main`):** the
  > `origin/main = 65a549bf` reading above is a **stale container ref**, not repo state.
  > Post-fetch, `origin/main` = `c7628a3e552a3aedff341106e4fb889763bf5b12` — identical to
  > HEAD (`git rev-list --left-right --count origin/main...HEAD` = `0 0`). The **local**
  > `main` branch ref in this container is still stale at `65a549bf`. Reading HEAD's
  > first-parent spine was therefore the correct call and every spine claim below stands
  > unchanged; only the `origin/main` position is corrected.
- **Evidence branch:** `origin/automation/fleet-audit` read via `git show` (refs only; never
  checked out).
- **Method:** read-only. Python = the scratchpad venv
  (`/tmp/claude-0/.../scratchpad/testenv/bin/python`), because `uv run --locked` refuses in
  this environment (`pyproject` pins uv `==0.11.19`, box has 0.8.17). The *numbers* are live;
  the *environment* is not the locked gate environment. Working tree verified byte-clean
  against HEAD before and after (`git diff --stat HEAD` empty).

---

## Verdict

1. **Wave 1/2 hypothesis: PARTIAL.** Both SHAs exist and are both on HEAD's first-parent
   spine. But **only wave 1 discharged ADR-109 §4**; wave 2 (`67863180`) landed a *different*
   amendment (the "9 governs" Related-line gloss) and discharged nothing in §4.
2. **The load-bearing finding: neither wave struck off any [#383] enumerated surface.**
   Wave 1's surface was `docs/intake/`; wave 2's was fleet membership. Neither is on the
   six-surface list. The surface-wave counter has **never advanced past zero**.
3. **Wave 3 = `caches`** (the 8 `ignore-*` rows), derived from the enumeration's own order
   as the first entry not struck off, with independent mechanical support: it is the only
   enumerated surface with a complete row set *and* a real observational probe.
4. **[#383]'s Done-when as written is already vacuously satisfied for all six surfaces.**
   Live report today: the only `diverge` cells in the whole matrix are on `corpus-version`.
   The draft Done-when therefore adds the probe layer. This is the single most important
   thing for the architect to see before freezing anything.
5. **[#465] leg 4** is drafted as a writer-class defect, not a stale-row deletion, with 285-vs-5
   verdict evidence and a dated `pass`-to-`n/a` transition.

---

## Part 1 — [#383] wave state

### 1.1 The row, read in full

`BACKLOG.md:439` and `tasks/383-execution-waves-per-surface.md:14` carry the row **byte-identical**
(the [#439] flip made `tasks/` the source and `BACKLOG.md` the generated artifact). Quoted:

```
- [#383] [P2][L] **Execution waves per surface** - once the schema exists, converge each L0/L2
surface (caches, the `.claude` surface incl. skills, archives-inside-each-folder, docs layout,
Python parity, colours-via-carrier) one wave at a time, worktrees launched **singly, one in focus
at a time** (intake #16 §6 step 4). Wave-done is mechanical, not narrative: **the divergence report
shows zero undeclared divergence for that surface**, and the operator reads the report.
Replication-first - changes land as manifest/carrier material, never as one-off per-repo fixes.
· Done when: per wave, the divergence report shows zero undeclared divergence for that surface and
the operator has read it · refs docs/intake/2026-07-21-func-fleet-north-star.md §6 step 4
· depends-on: 382 · serialize-group: architecture
```

Row status frontmatter: `status: open` (`tasks/383-execution-waves-per-surface.md:5`).

The `refs` target, `docs/intake/2026-07-21-func-fleet-north-star.md:139` (§6 step 4), verbatim:

```
| 4 | **Execution waves per surface** - worktrees launched singly, one in focus at a time;
wave-done = **the pandas report shows zero undeclared divergence** for that surface |
Report-green per wave, operator reads the report | CC (architect reviews) |
```

The six-surface enumeration originates one row earlier, at §6 step 3 (`:137`), as
"L0 surfaces from the operator's checklist (caches, `.claude`+skills, archives, docs layout,
Python parity, colours-via-carrier)". Same six, same order, in both sources.

### 1.2 Hypothesis check: waves 1 and 2 discharged per ADR-109 §4 via `1afd9579` and `67863180`

**VERDICT: PARTIAL.** Three sub-claims; two confirmed, one refuted.

| Sub-claim | Verdict | Evidence |
|---|---|---|
| Both SHAs exist | CONFIRMED | `git show --stat --no-patch` resolves both: `1afd9579a4188e27112ee83c70c12f9da734e217` (Fri Jul 31 23:17:03 2026), `67863180a5ee6100e5f222eff8bdc619f5095d05` (Sat Aug 1 19:25:43 2026) |
| Both on HEAD's first-parent spine | CONFIRMED | each full SHA found in `git rev-list --first-parent HEAD`; both also `git merge-base --is-ancestor <sha> HEAD` = true. Both are `Merge:` commits (two parents each), consistent with the `--no-ff` convention |
| Both discharged ADR-109 §4 | **REFUTED for wave 2** | §4 was discharged **once**, by wave 1 only. Wave 2's ADR-109 amendment is a different amendment on a different subject |

**Wave 1 (`1afd9579`).** CONFIRMED as the §4 discharge. Its merge subject reads
`Merge branch 'feat/intake-split-generality-discharge' - [#383] wave 1: ADR-109 §4 DISCHARGED`.
The committed round-trip proof it merged is `9a75777e` (`feat(intake): split docs/intake/ into
per-item nodes + a residue carrier ([#383] wave 1)`), which is an ancestor of `1afd9579` and of
HEAD but **not itself on the first-parent spine** -- correct, it is a branch commit reached
through the merge's second parent. ADR-109's amendment names that same SHA:

> The second governed surface is **`docs/intake/`**, split by the same engine pattern as
> surface 1 (`BACKLOG.md` <-> `tasks/`), at **`9a75777e`** -- the committed round-trip proof §4
> requires "not by argument".
> -- `docs/decisions/ADR-109-fleet-desired-state-contract-v1.md:297-299`

**Wave 2 (`67863180`).** The merge subject is
`Merge branch 'feat/462-membership-agreement-census' - closes [#462]: the membership blind spot
mechanized, 9 governs`, with body line `Arc 2 / [#383] wave 2. Operator GO recorded 2026-08-01.`
Its ADR-109 amendment is titled `## Amendment - 2026-08-01 (the Related-line matrix-width gloss
corrected: **9 governs**)` (`ADR-109:341`) and its own marker says it is
`Landed by **[#383] wave 2 / [#462]**` (`ADR-109:349`). It corrects a gloss; it does not touch §4.

**What ADR-109 §4 actually says**, and the sentence that governs the rest of Part 1:

> §4's obligation is **DISCHARGED**, so ADR-107 §6.2's generalization clause -- the precondition
> on **[#382]** declaring the fleet contract *general* -- is met. It does **not** close [#383]
> (wave execution continues), and it makes no claim about surfaces beyond the two now shown.
> -- `ADR-109:335-339`

§4's own heading also scopes it narrowly: `## §4 Generality-pending clause (ADR-107 §6.2,
transcribed; owner: [#383] wave 1)` (`ADR-109:123`). §4 is a **generality obligation**, not a
surface-convergence wave. Wave 1 satisfied it. Wave 2 was never §4's to discharge.

### 1.3 Derivation: which surface is next

**Enumeration, from the lane's own definition** (`BACKLOG.md:439` = `tasks/383-*.md:14`, order as
written; identical order at intake `§6 step 3`):

| # | Surface, verbatim | Struck off by wave 1? | Struck off by wave 2? |
|---|---|---|---|
| 1 | caches | no | no |
| 2 | the `.claude` surface incl. skills | no | no |
| 3 | archives-inside-each-folder | no | no |
| 4 | docs layout | no | no |
| 5 | Python parity | no | no |
| 6 | colours-via-carrier | no | no |

**Nothing is struck off.** The two waves' surfaces are not members of this list:

- **Wave 1's surface was `docs/intake/`**, and its scope was the ADR-109 §4 engine-pattern proof.
  ADR-109:339 forecloses reading it wider: it "makes no claim about surfaces beyond the two now
  shown". `docs/intake/` is a hub monolith split, not a fleet L0/L2 surface convergence. (One
  could argue it touches "docs layout"; the ADR's own no-claim sentence and the row's
  replication-first clause -- "changes land as manifest/carrier material" -- both cut against it,
  and the split shipped a hub-only carrier deliberately **not** distributed. See §1.5.)
- **Wave 2's surface was fleet membership**, which the repo already recorded as off-list, in
  advance, at `docs/audits/2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md:103-107`:

  > **Naming collision worth catching early.** [#383]'s own enumerated surfaces
  > (`tasks/383-*.md:14`) -- caches, `.claude`+skills, archives, docs layout, Python parity,
  > colours-via-carrier -- do **not** include fleet membership; and "[#383] wave 1" is already a
  > spent identifier for the §4 discharge. What [#462] calls "the wave-1 member set" may need a
  > **new named surface**, not literally wave 1.

**Independent corroboration that the surface counter is still at zero.** The 2026-08-02 ladder
audit, written after both waves landed, still ranks the next move as
`**Run [#383] wave 1 against one surface**`
(`docs/audits/2026-08-02-technical-night-ladder-and-plan-audit.md:61`) and records for L0:
`**Next action:** [#383] - converge **one** surface until the report shows zero undeclared
divergence for it` (`:118-119`).

**Therefore wave 3 (the brief's label) is the FIRST surface-convergence wave.** Numbering caveat
for the architect: "wave 1" and "wave 2" are spent identifiers for ADR-109-obligation waves, so a
third integer is ambiguous. The repo's own recommendation (L7 pre-analysis, quoted above) is to
**name the wave by its surface**, not by number. The draft below therefore reads
`[#383] wave: caches` and mentions "wave 3" only as the brief's alias.

**Which surface: `caches`.** Two independent derivations agree.

1. *From the enumeration.* The list is the only ordering [#383] supplies, and it is stable across
   both sources. With nothing struck off, the next entry is the first: `caches`.
2. *From mechanical readiness* (a tiebreak, not the primary derivation). `caches` is the only
   enumerated surface that is both fully represented in the parity manifest **and** carries a real
   observational probe. `ecosystem/parity-surfaces.yaml:834-899` defines exactly 8 rows
   -- `ignore-venv`, `ignore-pycache`, `ignore-pytest-cache`, `ignore-ruff-cache`,
   `ignore-mypy-cache`, `ignore-hypothesis`, `ignore-egg-info`, `ignore-node-modules` -- each
   `kind: gitignore-effect` with `probe: {type: check_ignore, candidate: ...}`. The block header
   states the discipline: `check = gitignore parity via the resolver, NEVER presence (intake #12
   Tier-4) and NEVER text-grep` (`:831-832`). By contrast **`colours-via-carrier` has zero rows**:
   a case-insensitive grep for `colou?r|vscode|theme|navy|grey` across the whole manifest returns
   only a comment at `:919-920` about `.vscode` tracking being "register e1 ... until e1 is ruled".
   That surface is not convergeable today at all -- worth the architect knowing before ordering.

### 1.4 The Done-when problem (read this before freezing)

**The row's Done-when as written is already satisfied for `caches`, and for five of the six
surfaces, with zero work done.** Live run today:

```
$ python scripts/desired_state_report.py
summary - conform: 185 · diverge: 3 · declared: 3 · n/a: 219
```

All 8 `ignore-*` rows read `conform` for all three applicable repos. The **only** `diverge` cells
in the entire matrix are on one row: `| corpus-version | · | diverge | declared | diverge |
diverge |`.

Two facts make this a trap rather than a success:

- Those totals are **unchanged for three runs across three dates**. The 2026-08-02 ladder audit
  recorded `conform: 185 · diverge: 3 · declared: 3 · n/a: 219 -- **identical to the 2026-07-31
  run at `f7abe228`**` (`2026-08-02-technical-night-ladder-and-plan-audit.md:112-113`). My
  2026-08-03 run reproduces the same four numbers. Nothing has converged; the number simply does
  not move.
- The report says so itself. From its docstring, `scripts/desired_state_report.py:25-29`:

  > `conform` -- NO divergence is DECLARED for the cell. This is the declaration layer:
  > no observational join is claimed (a reliable surface<->finding join needs the G9
  > crosswalk populated -- #383-era; terra H1), and probe execution stays
  > `scripts/fleet_parity.py`'s.

  Same wording in the rendered report's own HONEST LIMITS block (`:176-179`), and the ladder audit
  states the consequence plainly: `"Conform" still means *no divergence declared*, not a probe
  result` (`:114`).

**Which command produces the divergence report** -- checked, not assumed:

| Script | Is it the divergence report? | Evidence |
|---|---|---|
| `scripts/desired_state_report.py` | **YES** | `:1` docstring `"""ADR-109 divergence report ([#382] W4) - surface × repo × {conform / diverge / declared}.`; emits the header line `DESIRED-STATE DIVERGENCE REPORT (ADR-109 W4 - the declaration layer)` |
| `scripts/fleet_parity.py` | No -- it is the **probe** walk | `:2` `"""fleet_parity.py -- the #328 fleet-parity checker`; the divergence report defers to it by name for "probe execution" |
| `scripts/scan_undeclared_edges.py` | No -- unrelated domain | `:2-3` `"""scan_undeclared_edges.py - #179 undeclared-edge referential-currency scan (FC2).` -- doc-to-spec `reconciled_with` edges, not fleet surfaces |

`desired_state_report.py` takes **no arguments** -- `main()` is `print(render_report(
load_fleet_model(_ROOT))); return 0` (`:190-192`), with no argparse anywhere. There is no
`--surface` filter, so a wave's Done-when must name the row ids and the reader greps them.

`fleet_parity.py` **requires** `--run-date` (witnessed: a bare invocation exits with
`Error: Missing option '--run-date'.`).

**Conclusion for the draft:** a wave-3 Done-when copied literally from the row would be
green-on-arrival. The draft below keeps the row's *spirit* -- "wave-done is mechanical, not
narrative" -- by requiring **both** layers to read clean and to agree, which is exactly the join
the report says it does not yet make.

### 1.5 PASTE-READY -- wave-3 scope statement + Done-when

```
[#383] WAVE 3 (alias) -- properly: [#383] wave: caches
Surface: caches -- the 8 gitignore-effect rows, ecosystem/parity-surfaces.yaml:834-899
  ignore-venv · ignore-pycache · ignore-pytest-cache · ignore-ruff-cache
  ignore-mypy-cache · ignore-hypothesis · ignore-egg-info · ignore-node-modules

WHY THIS SURFACE, AND WHY NOW
It is the first entry in [#383]'s own enumeration (BACKLOG.md:439 = tasks/383-*.md:14, order
as written; same order at intake §6 step 3), and nothing ahead of it is struck off: wave 1
converged docs/intake/ for the ADR-109 §4 generality proof and wave 2 converged fleet
membership, neither of which is a member of the six-surface list (recorded in advance at
docs/audits/2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md:103-107). So this is
the FIRST surface-convergence wave, not the third; "wave 3" is an alias, and the wave should
be named by surface because "wave 1"/"wave 2" are already spent identifiers.
It is also the only enumerated surface that is fully specified AND observationally probed:
all 8 rows carry probe: {type: check_ignore, candidate: ...}, so a claim about them can be
falsified by running something rather than by reading a declaration. By contrast
colours-via-carrier has ZERO rows in the manifest (only an unruled register-e1 comment at
parity-surfaces.yaml:919-920) and cannot be converged at all until e1 is ruled.

SCOPE -- IN
1. Bring every applicable repo to gitignore-EFFECT parity on all 8 candidates, or record a
   declared divergence for each exception with its reason. Effect, never presence, never
   text-grep (parity-surfaces.yaml:831-832; the corp inline-comment gotcha false-passes a
   text probe -- FR-6).
2. Land the changes as manifest/carrier material only. Replication-first: no one-off
   per-repo .gitignore edit that the deploy channel cannot reproduce.
3. Reconcile the stale register-e2 note at parity-surfaces.yaml:876-877 ("FIX-NOW (hub +
   ai-council lack the line today)"): the hub now carries .hypothesis/ at .gitignore:7, so
   the comment is at least half spent. Correct or retire it in the same wave.

SCOPE -- OUT
- The corpus-version row. It is the ONLY row carrying undeclared divergence today (3 cells)
  and it is DERIVED, not a parity surface (desired_state_report.py:184-186). It is not a
  caches concern and must not be swept into this wave.
- Widening resolve_fleet_members. A named ADR-109 §2 ruling; [#472] owns it. The report will
  still render 5 columns and that is a stated consequence, not a wave defect.
- Any second surface. The row mandates worktrees launched singly, one in focus at a time.

THE DONE-WHEN PROBLEM THIS WAVE MUST NOT INHERIT
The row's existing Done-when -- "the divergence report shows zero undeclared divergence for
that surface" -- is ALREADY TRUE for caches, today, with no work done. Live 2026-08-03:
conform 185 / diverge 3 / declared 3 / n/a 219, all 8 ignore-* rows conform, and those four
numbers are byte-identical to the 2026-07-31 run at f7abe228 and to the 2026-08-02 reading.
The report defines conform as "NO divergence is DECLARED for the cell ... probe execution
stays scripts/fleet_parity.py's" (desired_state_report.py:25-29). So the declaration layer
alone cannot signal convergence. The clause below adds the probe layer and requires the two
to agree -- which is the surface<->finding join the report states it does not yet make.

PROPOSED DONE-WHEN (paste as the row's replacement clause)

· Done when: for the 8 gitignore-effect rows at ecosystem/parity-surfaces.yaml:834-899,
(a) `python scripts/desired_state_report.py` shows no `diverge` cell on any of the 8 rows;
AND (b) `python scripts/fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared,
0 must-absent and 0 tombstone-violated across those same 8 rows for every repo it walks,
with any repo it could not walk named in the wave record rather than counted as clean;
AND (c) both runs are pasted verbatim into the wave record and the operator has read them

RESIDUALS THE CLAUSE DELIBERATELY DOES NOT HIDE
- fleet_parity walks only repos present on the running box. In an unattended lane it may
  walk 1 of 9 (witnessed 2026-08-03: "1 repo(s) walked", with ai-council and corp-monorepo
  "unresolved: ... is not a git repo"). Clause (b) therefore requires unwalked repos to be
  NAMED, so a 1-of-9 run can never be read as fleet-green.
- Neither command filters by surface; the reader greps the 8 ids. desired_state_report.py
  takes no arguments at all (main(), :190-192, no argparse).
- If the architect wants the join mechanized rather than eyeballed, that is a separate row
  (the G9 crosswalk, cited as "#383-era" at desired_state_report.py:27) -- file it, do not
  fold it into this wave.
```

---

## Part 2 — [#465] leg 4 contract

### 2.1 The row and the open leg

`BACKLOG.md:266` (task node `tasks/465-fleet-audit-writer-integrity-skip-as-pass-overwr.md`).
Title: **fleet-audit writer integrity -- legs 1-3 DONE, leg 4 open**. Leg statuses as written:
`**(1) DONE** (80e743aa): a skip is no longer emitted pass. **(2)+(3) DONE**: one bug, not two
... **(4)** OPEN -- handoff_tag_canonicity self-disabled.` Row Done-when:
`· Done when: last-run-wins is accepted on record and tag-canonicity is fixed or retired`.

Leg 1's fix commit `80e743aa` is verified: `fix(audit): a skip is never recorded as PASS -- [#465]
leg 1, RED-first, 16 sites`, Sat Aug 1 20:00:50 2026, ancestor of HEAD.

### 2.2 The self-disable, quoted exactly

`scripts/audit.py:715` defines `check_handoff_tag_canonicity`. Two `n/a` exits; the second is the
self-disable. Verbatim, `scripts/audit.py:733-737`:

```
    lines = spec.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines) if re.match(r"^###\s+3\.1\b", ln)), None)
    if start is None:
        return [Finding("handoff_tag_canonicity", "n/a",
                        "§3.1 section not found (consolidated?) — nothing to lint")]
```

The first `n/a` exit, `scripts/audit.py:729-731`, is the consumer-side dead end:

```
    if not spec.exists():
        return [Finding("handoff_tag_canonicity", "n/a",
                        "no protocols/HANDOFF_PROCESS.md — nothing to validate")]
```

And the docstring states the self-disable as intent, `scripts/audit.py:718-720`:

```
    Post-#149 flip the canonical file is v5, which carries no §3.1 four-tag section, so
    this check degrades to a clean pass ("§3.1 not found — nothing to lint"). It remains
    only to guard the historical v4 tag-canonicity invariant if a §3.1 ever reappears.
```

**Note the contradiction:** the docstring promises `a clean pass`; the code at `:736` returns
`n/a`. The docstring was not updated when leg 1 landed at `80e743aa` and now documents exactly the
behaviour leg 1 removed. That is a second, smaller instance of the same writer-integrity class.

Live confirmation on this tree (scratchpad venv, `check_handoff_tag_canonicity(Path("."))`):

```
{'check_name': 'handoff_tag_canonicity', 'status': 'n/a',
 'evidence': '§3.1 section not found (consolidated?) — nothing to lint'}
```

`ALL_CHECKS` length = 38; membership of this check = True.

### 2.3 The subject no longer exists

- `protocols/HANDOFF_PROCESS.md:1,4` = `# HANDOFF_PROCESS v6` / `Version: 6.0.1`. Its `Supersedes:`
  line names `HANDOFF_PROCESS v4.4`. The check's own docstring is scoped to `HANDOFF_PROCESS v4.3
  item F`.
- There is **no `### 3.1`** in the live spec (heading grep returns `## 1.` through `## 16.` plus
  `## Section history`).
- The four-tag vocabulary is gone: a case-insensitive grep for `witnessed|recall|inferred|unknown`
  over the whole spec returns **one** hit, `:1004`, and it is ordinary prose (`the seam witnessed
  and left unpatched`), not a tag enumeration.
- The writer that produces bundles, `scripts/gen_handoff.py`, emits **no provenance tag**: grep for
  `witnessed|recall|inferred|unknown|_TAG|provenance` returns only unrelated uses of the word
  "unknown" as a git-status fallback string (`:249, :265, :363, :365, :372`).

So both exit branches are permanent: on the hub, `§3.1 section not found`; on every consumer, `no
protocols/HANDOFF_PROCESS.md`.

### 2.4 The flap evidence

From `origin/automation/fleet-audit` (read via `git show`, never checked out). Census over **every**
`ecosystem/*/history/*.md` file on that branch:

```
    285  handoff_tag_canonicity | n/a
      5  handoff_tag_canonicity | pass
```

All 5 `pass` readings are on a single date, **2026-06-15**, one per repo
(`.dev-knowledge`, `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`).

The transition is the leg-1 defect itself, visible byte-for-byte -- **same evidence string, different
verdict**:

```
2026-06-15  | handoff_tag_canonicity | pass | §3.1 section not found (consolidated?) — nothing to lint |
2026-06-16  | handoff_tag_canonicity | n/a  | §3.1 section not found (consolidated?) — nothing to lint |
```

Since then it is `n/a` unbroken. Sampled hub dailies 2026-07-17, 07-24, 07-31, 08-01, 08-02 all read
`n/a` with that identical string; every hub daily from 2026-07-07 through 2026-08-02 reads `n/a`.
Cross-repo on 2026-08-02, all five consumers read `n/a | no protocols/HANDOFF_PROCESS.md — nothing
to validate`. The L-B lane recorded the same:

> **Leg (4) - CONFIRM unchanged.** `handoff_tag_canonicity` reads `n/a` every sampled day 07-17 ->
> 08-01: `§3.1 section not found (consolidated?) — nothing to lint`, byte-identical.
> -- `docs/audits/2026-08-02-technical-night-batch-lb-fleet-audit-commits.md:111-112`

On the hub's 2026-08-02 daily exactly four check names emit `n/a`:
`deployed_methodology_version`, `enforcement_coverage`, `floor_integrity`,
`handoff_tag_canonicity`. The first three are legitimately inapplicable to the hub. The fourth is
inapplicable *everywhere*.

### 2.5 The house shape this contract matches

The producer lane is **not** the gated EPIC-H producer role. `protocols/PLAYBOOK.md:3616` (§16):

> **The producer lane is NOT activatable as written today (R4 - reconciliation).** ... the
> hub-owned global config currently **fixes Codex as a read-only reviewer** ... So the producer
> lane is **charter-only** -- a documented intent, not a switch a session may flip -- until the
> activation mechanism (`#341`) lands and is ruled.

The runnable lane is the R5 interim (`PLAYBOOK.md:3617`): *Codex fully specifies the design under a
bounded prompt -> CC implements -> terra read-only review pre-merge*, with Codex emitting text only
and never authoring the merged artifact. The most recent execution of that shape is
`docs/audits/2026-07-31-technical-intake-split-generality-discharge.md:34`:

> **Producer lane.** `codex exec -m gpt-5.6-terra --sandbox read-only`, spec = AC-3/AC-5 verbatim.
> Codex was directed to emit to **stdout only** ... Codex wrote no file.

That record's own skeleton -- architect rulings table, a fidelity check performed *before*
planning, builder-lane evidence with per-defect disposition, RED-witnessed-before-GREEN, and a
"what this does and does not show" section -- is the shape the draft below is written to feed.

### 2.6 PASTE-READY -- [#465] leg 4 contract

```
CONTRACT -- [#465] LEG 4: handoff_tag_canonicity, writer-integrity class
Status: DRAFT for morning freeze. Frozen ex-ante; once frozen it is not edited -- a
discrepancy found later is REPORTED as a line, never corrected into the contract
(LESSONS.md 2026-07-30, the ex-ante-witness rule).

LANE
R5 interim producer lane, NOT the gated EPIC-H producer role (PLAYBOOK.md:3616 -- charter
only until #341 is ruled). Concretely:
  codex exec -m gpt-5.6-terra --sandbox read-only, spec = FR-1..FR-7 + AC-1..AC-7 verbatim,
  emit to STDOUT ONLY. Codex writes no file. CC implements, TDD-first. terra read-only
  review pre-merge. Precedent: 2026-07-31-technical-intake-split-generality-discharge.md:34.

(a) DEFECT STATEMENT

THE DEFECT IS THE WRITER, NOT THE ROW.
[#465] is "fleet-audit writer integrity". Legs 1-3 each fixed a mechanism that emitted a
wrong verdict token, and each closed on a self-enumerating regression over ALL_CHECKS
(tests/test_hub_identity.py:105 -- "Self-enumerating over ALL_CHECKS rather than pinning the
three checks the 07-21 repro" -- is the pattern). Leg 4 is the same class:

  The fleet-audit writer emits a verdict token every day for a check whose subject has not
  existed for two spec generations, and NOTHING in the writer, the dailies, ALL_CHECKS, or
  the ship gate notices. The check occupies a row in all 290 history readings on
  origin/automation/fleet-audit and has never once produced an informative verdict on the
  live corpus.

Cited:
  - 285 n/a vs 5 pass across every ecosystem/*/history/*.md on origin/automation/fleet-audit.
  - The 5 pass are all 2026-06-15, one per repo, and carry the SAME evidence string as the
    n/a's: "§3.1 section not found (consolidated?) — nothing to lint". On 2026-06-16 the
    identical condition began reporting n/a. So the pass era WAS the leg-1 defect (a skip
    recorded as pass), fixed at 80e743aa. The check has therefore been lying or inert for its
    entire recorded life; it has never been correct-and-informative.
  - Hub branch is dead: audit.py:734-737 returns n/a when no "### 3.1" heading is found.
    protocols/HANDOFF_PROCESS.md is v6.0.1 (:1,:4) and has no §3.1; the four-tag vocabulary
    witnessed/recall/inferred/unknown survives only as one incidental prose word at :1004;
    scripts/gen_handoff.py emits no provenance tag at all.
  - Consumer branch is dead: audit.py:729-731 returns n/a when the spec file is absent.
    Verified on all five consumer dailies for 2026-08-02.
  - Second instance of the same class, found while verifying the first: audit.py:718-720
    documents the behaviour as "degrades to a clean pass", which leg 1 removed at 80e743aa.
    The docstring now describes the defect leg 1 fixed.

WHAT WOULD NOT DISCHARGE THIS LEG: deleting check_handoff_tag_canonicity. That repairs the
instance and leaves the class. The next check to lose its subject goes inert identically and
is equally invisible. The row's own Done-when reads "tag-canonicity is fixed or retired" --
the fix-or-retire fork is a FR-5 output here, decided by the detector, not hand-picked.

(b) FUNCTIONAL REQUIREMENTS

FR-1  A check that returns n/a MUST distinguish, in machine-readable form, two reasons:
      SUBJECT-ABSENT (the thing to be checked does not exist anywhere -- the check cannot
      ever fire) and NOT-APPLICABLE (this repo legitimately lacks the surface; another repo
      has it). Today both collapse to the single token "n/a", which is why a dead check and
      a correctly-skipped check are indistinguishable in every daily.
FR-2  ALL_CHECKS MUST be covered by a detector that fails when a member can return only
      SUBJECT-ABSENT for every repo in the fleet -- i.e. the check is unconditionally inert.
      Self-enumerating over ALL_CHECKS, never a hand-maintained list (the leg-2/3 precedent).
FR-3  Verdict posture: the detector reports WARN, not FAIL, and an internal error in the
      detector must surface loudly rather than pass silently. It informs; it does not become
      a new way for the gate to go red on doc drift.
FR-4  Read-only, Layer 2 (CLAUDE.md §5 rule 4 / ADR-28, ADR-36). No orchestration, no writes,
      no new persisted registry -- derive from ALL_CHECKS and the live tree. Adding a
      hand-maintained "known-inert" list would reproduce the registry-sprawl anti-pattern
      ADR-109 exists to dissolve.
FR-5  Apply the detector to handoff_tag_canonicity as its FIRST detected instance and record
      the resulting disposition -- fixed or retired -- as the detector's output, not as a
      prior decision. If retired: remove from ALL_CHECKS, remove the tests, and record the
      retirement where a reader of the dailies will find it (the count drops 38 -> 37).
FR-6  audit.py:718-720's docstring MUST agree with the code. It currently asserts "degrades
      to a clean pass" against a code path that returns n/a. Whatever FR-5 decides, no
      surviving docstring may describe pre-80e743aa behaviour.
FR-7  Consumer safety, the D1 lesson from the wave-1 producer lane: the detector must not
      report a defect on a consumer repo merely because a hub-only surface is absent there.
      The wave-1 Codex output failed exactly this way and would have manufactured a fleet gap
      on corp-monorepo and ai-council (2026-07-31-technical-intake-split-generality-discharge
      .md, defect D1). Repredicate on repo identity via the existing _is_hub() seam.

(c) TDD FIXTURE PLAN

Fixtures (tmp_path trees, no network, no consumer checkout required):
  F1  hub-shaped tree with protocols/HANDOFF_PROCESS.md containing NO "### 3.1" -- the live
      hub condition. Expect: SUBJECT-ABSENT.
  F2  hub-shaped tree with a synthetic "### 3.1" enumerating all four tags. Expect: the
      check fires and passes -- proves the check is not merely deleted, and pins the
      "if a §3.1 ever reappears" clause the docstring claims to preserve.
  F3  hub-shaped tree with a three-tag "### 3.1" and no Amendment-A cross-reference. Expect:
      fail. This is the invariant the check was built for; it must be reachable or the check
      is provably dead.
  F4  consumer-shaped tree with no protocols/ directory at all. Expect: NOT-APPLICABLE, never
      SUBJECT-ABSENT and never a defect report (FR-7).
  F5  a synthetic ALL_CHECKS member that returns SUBJECT-ABSENT for every fixture repo --
      the detector's positive case, independent of handoff_tag_canonicity so the test does
      not evaporate if FR-5 retires it.
  F6  a synthetic member that returns NOT-APPLICABLE on one repo and pass on another -- the
      detector's negative case. Must NOT be flagged.

RED FIRST -- the test that proves the defect before any fix:
  R1  Assert the detector flags handoff_tag_canonicity as unconditionally inert given F1+F4.
      MUST FAIL on unmodified HEAD, because no detector exists. This is the RED that proves
      the defect, and it must be witnessed and recorded before a line of fix is written.
  R2  Assert F3 (three-tag, no cross-ref) is reachable through the live spec. MUST FAIL on
      unmodified HEAD -- it is unreachable, which is the concrete meaning of "self-disabled".
  R3  Assert the docstring at audit.py:718-720 does not contain the string "clean pass".
      MUST FAIL on unmodified HEAD (FR-6).
Run without -x and compare the failure SET against the [#457] standing-RED pair; the step
gate is "no NEW failures beyond the two known ids" (R3 rule, 2026-07-31 discharge record §5).
No skip, no xfail, no deselect on those two.

GREEN:
  R1 green when the detector exists, is self-enumerating over ALL_CHECKS, and reports WARN.
  R2 green when EITHER a reachable §3.1 path is restored (fix) OR the check and its tests
     are removed and R2 is deleted with an explicit retirement note (retire). Both branches
     are legitimate FR-5 outputs; the contract does not pre-decide.
  R3 green when the docstring matches the code.

(d) ACCEPTANCE CRITERIA

AC-1  RED witnessed and recorded BEFORE any fix: the exact R1/R2/R3 failure output is pasted
      into the arc record. A witness authored after the change is a description, not a
      witness (LESSONS.md 2026-07-30).
AC-2  `python scripts/audit.py health` exits clean on the hub after the change, and the
      ALL_CHECKS count is stated explicitly before and after (38 -> 38 if fixed, 38 -> 37 if
      retired). A silent count change is a contract breach.
AC-3  The detector is proven self-enumerating: a test adds a synthetic inert member to
      ALL_CHECKS and the detector flags it with no edit to any list. (F5.)
AC-4  FR-7 witnessed, not argued: the detector is run against a consumer-shaped fixture
      (F4) and reports no defect. This is the D1 regression from the wave-1 lane.
AC-5  Full suite run without -x; the failure set equals the [#457] standing pair exactly.
      ruff check clean. Both outputs pasted.
AC-6  The [#465] row is updated in ONE place -- the task node
      tasks/465-fleet-audit-writer-integrity-skip-as-pass-overwr.md -- and BACKLOG.md:266 is
      REGENERATED, never hand-edited (the [#439] flip: tasks/ is source, BACKLOG.md is
      generated). Closing commit carries [#465] per the backlog-id-on-close commit-msg gate.
AC-7  The row's other open clause is discharged or explicitly carried: "last-run-wins is
      accepted on record". If leg 4 lands without it, the row does NOT close, and the arc
      record says so in one line rather than leaving the reader to diff the Done-when.

TRIPWIRES -- STOP and return to the architect, do not proceed
  T1  If FR-1 turns out to require a change to the Finding type or to the daily's column
      grammar, STOP. That is a writer schema change consumed by state.yaml, index.yaml, the
      dailies and the report; it is a ruling, not an implementation detail.
  T2  If the detector would need to read origin/automation/fleet-audit, STOP. audit.py runs
      against the live tree; reaching across a branch makes a validator branch-aware and is
      a distinct design question.
  T3  If retirement (FR-5) would drop a check that some consumer's deployed methodology still
      declares, STOP and report the declaring surface.
```

---

## Coverage

**Verified live, with the command or path that shows it:**

- `1afd9579` and `67863180` both exist, are both merge commits, and are both on HEAD's
  first-parent spine (`git rev-list --first-parent HEAD` membership, plus
  `git merge-base --is-ancestor`). HEAD = `c7628a3e`, 174 ahead of `main`/`origin/main` =
  `65a549bf`.
- `9a75777e` exists, is an ancestor of both `1afd9579` and HEAD, and is not on the first-parent
  spine -- consistent with being the merged branch's build commit.
- ADR-109 §4's text, its 2026-07-31 amendment, and its 2026-08-01 amendment, read from
  `docs/decisions/ADR-109-fleet-desired-state-contract-v1.md` at the cited line numbers.
- The [#383] enumeration is byte-identical at `BACKLOG.md:439` and
  `tasks/383-execution-waves-per-surface.md:14`; `status: open` at `:5`.
- `scripts/desired_state_report.py` run live 2026-08-03: `conform: 185 · diverge: 3 ·
  declared: 3 · n/a: 219`, all 8 `ignore-*` rows `conform`, only `corpus-version` carrying
  `diverge`. It is the divergence report (docstring `:1`); it takes no CLI arguments
  (`:190-192`).
- `scripts/fleet_parity.py` requires `--run-date` (witnessed error), and is named by the
  report as the probe owner.
- `ecosystem/parity-surfaces.yaml:834-899` -- the 8 `gitignore-effect` rows with
  `check_ignore` probes. `colours-via-carrier` has zero rows (grep for
  `colou?r|vscode|theme|navy|grey` returns only the `:919-920` comment).
- `scripts/audit.py:715,718-720,729-731,733-737` quoted from disk; the check runs live and
  returns `n/a`; `ALL_CHECKS` length 38 with the check a member.
- The 285-vs-5 verdict census, the 2026-06-15 `pass` date, and the 06-15 -> 06-16 same-string
  verdict flip, all from `git show origin/automation/fleet-audit:<path>` over every
  `ecosystem/*/history/*.md`.
- `protocols/HANDOFF_PROCESS.md` is v6.0.1 with no `### 3.1` and no four-tag vocabulary;
  `scripts/gen_handoff.py` emits no provenance tag.
- `PLAYBOOK.md:3616-3617` (R4 charter-only / R5 interim) and
  `docs/audits/2026-07-31-technical-intake-split-generality-discharge.md:34` (the executed
  producer-lane shape).

**Not verified / limits:**

- **`uv run --locked` was never used.** All Python ran under the scratchpad venv. Numbers are
  live; the environment is not the locked gate environment, so a locked-env run could in
  principle differ. UNVERIFIABLE here -- pyproject pins uv `==0.11.19`, box has 0.8.17.
- **`fleet_parity.py` walked 1 repo, not 9.** `ai-council` and `corp-monorepo` resolve to
  non-git paths on this box; `corp-ops` and `corp-sca-time-automation` report
  `skipped-pre-deploy`. So the caches surface is verified converged on the **hub only**. The
  fleet-wide probe leg of the proposed Done-when is UNVERIFIABLE in this environment by
  design -- which is why clause (b) requires unwalked repos to be named.
- **I did not run the full pytest suite** (the [#457] standing-RED pair is cited from the
  2026-07-31 discharge record, not re-witnessed here).
- **The wave-3 surface choice is a derivation, not a ruling.** It follows the enumeration's
  order because that is the only ordering [#383] supplies; the row nowhere states the list is
  an execution order. If the architect intends pain-priority ordering instead, the derivation
  changes and the mechanical-readiness tiebreak (§1.3 point 2) is the argument to re-weigh.
- **Two deviations from this lane's brief, disclosed rather than silently resolved:**
  1. The brief asked for *YAML frontmatter matching sibling files*. The
     `2026-08-02-technical-night-batch-*.md` siblings carry **no YAML frontmatter** -- they use
     an H1 plus an ADR-101 bullet header block (`Class` / `Date` / `Slug` / `Status` / `Base` /
     `Method`). This file matches the siblings, per the instruction's intent.
  2. The mandated filename `2026-08-03-night-lc-w4-staging.md` parses as class `night`, which
     is **not** in `AUDIT_CLASS_ENUM` (`scripts/validate_hermetization.py:89-99`: technical,
     functional, qa, census, verification, ecosystem-audit, conformance-nightly-digest,
     changelog-review, codex, fresh-eyes, incident-evidence). The Rule-B pre-commit gate fires
     prospectively on staged ADDs, so **committing this file as named will be BLOCKED**.
     On-grammar name: `2026-08-03-technical-night-lc-w4-staging.md`. I did not rename it --
     the brief named the path exactly. Architect's call.
- **Writes this lane caused, disclosed:** running `fleet_parity.py` wrote
  `logs/FLEET-PARITY.md` and `logs/PARITY-EVENTS.jsonl`. Both are gitignored
  (`.gitignore:55-56`) and `git diff --stat HEAD` is empty, so the tracked tree is byte-identical
  to HEAD. No tracked file was created, edited, staged or committed; the only file this lane
  authored is this one.
- **Not added to `docs/audits/README.md`.** That index is generated and gated by the
  `audit-index-freshness` pre-commit hook; regenerating it is a write this lane must not make.
  The morning architect should run `python scripts/gen_audit_index.py --write` when this file
  lands.

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
