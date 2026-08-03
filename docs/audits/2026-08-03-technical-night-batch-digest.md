# Night batch 2026-08-03 — digest (INDEX)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-batch-digest
- **Status:** **PROPOSAL — every finding below is for the morning architect to promote or
  reject.** Nothing was decided, filed, closed, reworded, ratified or fixed overnight. No repo
  prose was edited, no BACKLOG row moved, no script changed. `main` was not touched.
- **Base:** `origin/main` = `c7628a3e552a3aedff341106e4fb889763bf5b12`. Branch
  `claude/night-batch-2026-08-03-k8djp8`, identical tip before this commit
  (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
- **Lanes:** L-A here in summary + in full at its own file; L-B..L-F each have their own file,
  linked per section.
- **Read order:** the claim table, then the three REFUTED/UNVERIFIABLE headlines, then the
  per-lane verdict lines.

---

## READ THIS FIRST — two facts that invalidate naive re-runs

**1. The container arrived with a SHALLOW clone AND a stale `origin/main`.** At session start
`.git/shallow` was present (first-parent spine = **89** commits) and both `main` and
`origin/main` pointed at `65a549bf` — 174 commits behind, with **none of the four W2 SHAs
reachable**. A naive verification run stops here and reports the whole W2 window REFUTED. After
`git fetch origin main` + `git fetch --unshallow`: spine = **1286**, `origin/main` =
`c7628a3e`, all four SHAs resolve. **The local `main` branch ref in this container is still
stale at `65a549bf`** — it was never advanced, and nothing depends on it. Every git claim in
every lane file was re-run post-unshallow.

**2. `uv run --locked` cannot run in this container at all.** `pyproject.toml:29` pins
`required-version = "==0.11.19"`; the box carries uv **0.8.17**, so every `uv` verb aborts —
and `uv self update 0.11.19` fails with `The version 0.11.19 was not found`. Since **every**
`language: system` pre-commit entry begins `uv run --locked`, **no gate could be exercised
through its production path tonight.** All lanes ran validators via a lock-version-matched venv
built outside the repo tree (pytest 9.1.1, ruff 0.15.5, pyyaml 6.0.3, click 8.4.2, rich 15.0.0,
pydantic 2.13.4, packaging 26.2, pandas 3.0.5, CPython 3.12.3). Numbers are live; the
environment is not the locked gate environment. This is the single largest limit on the night.

---

## L-A claim table — the W2 execution report, re-derived

Full evidence: `2026-08-03-technical-night-la-w2-verification.md`.

| # | Claim | Verdict |
|---|---|---|
| 1a | Arc 1 ([#475]) merge SHA — truncated in the operator's copy | **RECOVERED:** `087d967f184dcebc34087bbfa97ac42f62ea7100` |
| 1b | Arc 2 `bc0c2ada` | CONFIRMED (`bc0c2ada2374bcb8f76a536c6c8307199b2835c3`) |
| 1c | wrap `76c338fb` merged at `c7628a3e` | CONFIRMED (`c7628a3e` parents = `bc0c2ada 76c338fb`) |
| 1d | anchor `087d967f` | CONFIRMED — **same commit as 1a**, not a fifth SHA |
| 1e | on `main`'s first-parent spine | CONFIRMED post-fetch; would REFUTE on the as-delivered container |
| 2a | `check-seal-identity` in config, `files: ^docs/handoffs/` | CONFIRMED (`.pre-commit-config.yaml:103,113`) |
| 2b | reuses `verify_seal_identity`, no parallel impl | CONFIRMED (one `def` repo-wide, `gen_handoff.py:324`) |
| 3 | `--write` refuses, exit 2, zero bytes written | CONFIRMED (live run; tree digest identical) |
| 4a | 2195 collected, matching the re-pinned doc-counts | CONFIRMED (live 2195; `doc-counts.md:15` = 2195) |
| 4b | failure set = exactly the two `[#457]` ids | **CONFIRMED on repo content; NOT reproducible here** — see below |
| 5a | [#475]/[#474] absent from open BACKLOG | CONFIRMED |
| 5b | `tasks/*` retired `status: closed` (retire-not-delete) | CONFIRMED (files on disk, out of manifest queue) |
| 5c | tree consistent, `--check` exit 0 | CONFIRMED (`gen_task_tree: check ok`) |
| 5d | CLAUDE §9 / ARCHITECTURE Ch2 lockstep, v2.50, 16 gates | CONFIRMED — **exact set equality across 4 surfaces** |
| 5e | `validate_backlog` 186 open+deferred | CONFIRMED — **157 open + 29 deferred** |
| 5f | net −2 (188 -> 186) | CONFIRMED against the pre-arc parent `25e9dc7d` (queue was 188) |
| 6a | ship-gate GREEN in a clean environment | **UNVERIFIABLE HERE** — RED in this container |
| 6b | `[stale]` count 0 | **REFUTED here (= 1)** — container-caused |
| X | "terra review: zero findings both arcs" | **UNVERIFIABLE — no artifact exists anywhere** |

**Nothing in the W2 report was refuted on repo content.** Three items need the architect's eye:

### HEADLINE 1 — the terra review left no artifact (UNVERIFIABLE)

`JOURNAL.md:47` records *"terra review body: zero findings on both arcs"*. There is no
`2026-08-02-codex-*.md`, no terra output under `docs/`, `logs/` or `codex/`, and no review file
in either arc's diff (`git diff --stat` on both merges; `git log 25e9dc7d..c7628a3e` = 6
commits, none a review record). **All 88 prior codex reviews in this repo left a
`docs/audits/<date>-codex-<slug>.md` artifact**, the three most recent dated 2026-08-01 — one
day earlier. Not refuted; **unfalsifiable**, which for a gate-adjacent review is the same
operational problem. Whether the artifact is required is a ruling; that it is absent is a fact.

### HEADLINE 2 — ship-gate RED here, `[stale]` = 1, and one contributor is a real portability defect

`ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 4 new/undispositioned WARN(s))`.
Decomposed, with a control probe: arming `.git/hooks` (`pre-commit install`, untracked, since
reverted) clears the hard fail and one WARN, leaving three. **Every contributor is a container
difference, none is repo content:**

- `hooks_armed` (the hard fail) — `.git/hooks/` held only `*.sample`
- `fleet_parity` x2 — `/home/user/ai-council` and `/home/user/corp-monorepo` are not git repos
- `[stale] warn-fleet-parity-ai-council-root-conftest` — its `match:` string cannot fire with ai-council absent, so **`[stale]` counts are not portable across checkouts**
- `deployed_methodology_version: dev-knowledge not listed` — **the real finding.**

**The portability defect (report line, not fixed).** `scripts/audit.py:2300` —
`repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name` — keys
`ecosystem/deployed-versions.yaml` by repo-root **basename**. The registry key is
`.dev-knowledge` (`ecosystem/deployed-versions.yaml:23`); a GitHub clone lands as
`dev-knowledge`, so the hub cannot find its own row. **This is the identical failure shape
[#465] legs 2+3 fixed at `56f82aa` for hub identity** ("the hub recognises itself from any
checkout") — `resolve_repo_path()` bound `_is_hub()` to the live tree, but this check still
compares names. Same defect class, unfixed surface.

### HEADLINE 3 — the brief's own artifact-naming pattern is refused by this repo's gate

The brief mandates `docs/audits/2026-08-03-night-<lane>.md`. Tested against the live validator:
`rule_b_violation` BLOCKS all seven — `night` is not in the ADR-101 R3 closed class enum
(`scripts/validate_hermetization.py:89-98`). **Four lanes caught this independently.**
Resolution taken: insert the `technical` class token, exactly as every 2026-08-01/02
night-batch sibling already does. **The gate was not weakened, bypassed or amended.** All seven
artifacts verified post-rename: `rule_a_violation` and `rule_b_violation` both return `None`.
Each renamed file carries an editor's note recording it. Flagged so the architect can rule on
the brief's pattern rather than rediscover the collision.

### On claim 4b (the suite) — three runs, and a confound this lane introduced and then removed

`pytest --collect-only` = **2195**, matching `ecosystem/doc-counts.md:15` exactly.

**Run 1 — full serial, as-cloned container:** `2155 passed / 33 failed / 7 skipped` (661s).
The two `[#457]`-owned ids are in the set, and so are 31 others — every one traced to a missing
container prerequisite, not to repo content:

- **19 x `test_fleet_analytics.py`** — `ModuleNotFoundError`. The `analytics` dependency group (pandas) is deliberately optional and was absent.
- **6 x `test_reverse_dep_oracle.py` + `test_safe_remove.py`** — `node_modules/` absent. `package.json` pins the vendored `pyright` 1.1.410 langserver the oracle drives; it is gitignored and `npm install` was never run in this fresh clone.
- **3 x `test_audit.py`** health / synthetic-repo — the gitignored `ecosystem/<repo>/state.yaml` pointers are absent, so `audit.py health` reports `[!!] repos registered (none)`.
- **4 x `test_boundary_report` / `test_carrier_hooks_source` / `test_legibility_graph_conformance` / `test_merge_serialization`** — sibling repos, armed hooks, and real-git/pre-commit spawns.

**Run 2 — targeted re-run of those 33 with pandas installed:** `91 passed / 13 failed` (502s).
18 of the 19 `fleet_analytics` failures clear (residual:
`test_hub_is_included_as_a_mining_target`); the langserver and state.yaml classes persist, as
predicted. **This run carries a confound this lane introduced:** `.git/hooks` were still armed
from the section-6 ship-gate control probe, and under armed hooks
`test_check_fleet_parity_green_on_live_repo` — `[#457]` leg (i) — **PASSED**.

**Run 3 — the confound removed.** `.git/hooks` restored to the as-cloned pristine state
(samples only), then the two ids run alone:

```
FAILED tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
FAILED tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row
    AssertionError: assert '1 declared routine row' in '2 declared routine row(s) name a
    consumer and a consumption_path (live hooks/schedules out of scope — [#426])'
2 failed in 5.22s
```

**Both `[#457]` ids fail in the pristine state, and leg (ii) fails for exactly the reason
`BACKLOG.md:80` states** — the pin says 1, the live check reports 2.

**Verdict: 4b is CONFIRMED on repo content and NOT REPRODUCIBLE as a bare count here.** But
Run 2 surfaces something the row should absorb: **in this container leg (i) fails for a
DIFFERENT reason than the row records.** The row attributes it to the test ignoring the
disposition register for the ai-council `conftest.py` WARN; here it flips to PASS the moment
hooks are armed, i.e. it is failing on the `hooks-armed WARN-undeclared` finding instead. The
test is disposition-blind to *whatever* WARN is live, and the row names only one of them. L-B
independently reached the same place from the other direction ("leg (i) not reproducible —
unarmed hooks give a different WARN"). **Report line for the `[#457]` row, not a fix.**

---

## Per-lane verdicts

### L-B — backlog + architecture currency groom
`2026-08-03-technical-night-lb-groom.md`

1. **Counts confirmed, delta 0.** 186 = **157 open + 29 deferred**; the 29-deferred boot
   baseline holds exactly. Three independent surfaces agree (`validate_backlog`, the
   `tasks/manifest.json` queue, the frontmatter status census).
2. **Two DEAD rows the mechanical checker structurally cannot see.** `[#455]` — `ADR-109:24`
   states *"[#455] becomes moot when §2 lands"* and §2 landed (ADR-109 Accepted, `7ef40567`);
   the row's own kill-candidates reasoning still cites `[#382]` as "gated", but `[#382]` closed
   at `f7abe228`. `[#433]` — all three Done-when legs now met. **Neither carries a `closes`
   token, so `validate_git_backlog` is silent by design.** This is a coverage boundary, not a
   validator bug.
3. **`[#424]`'s fix would immediately RED the gate.** In-memory simulation (repo untouched):
   normalizing the bare `depends-on` ids yields `depends-on references non-existent id #382 —
   [#383] line 439`. **The inertness `[#424]` exists to remove is currently hiding a dangling
   edge.** Its own census is stale too (row says 8 clauses / 4 inert; live is 7 / 3).
4. **Closure drift: independent pass AGREES with the validator.** 1286 commits scanned with a
   wider regex and no quote-stripping; 113 distinct `closes [#N]` ids; intersection with the
   186 open ids **empty**. Both passes blind to ADR-declared disposal (finding 2).
5. **Proposed set = exactly {82, 88, 89}, confirmed** across all 82 ADRs and four status-line
   grammars. 88/89 are already Accepted by in-file marker — recommend a status-line flip.
   **ADR-82 is the real gap:** still `Proposed`, its amendments stop at v5.2, and the live spec
   is `HANDOFF_PROCESS.md:4` **`Version: 6.0.1`** — seven versions behind.
6. **Two Accepted-ADR contradictions.** C1: `ADR-107:458` "§6.2 ... still undischarged" vs
   `ADR-109:337` "**DISCHARGED**". C2: `ADR-108:56-67` calls §E "unratified ... live and
   unanswered" while `ADR-109:8` ratifies §E by promotion — and 109 landed after 108. C2 has
   already escaped into a mutable doc (`docs/intake/2026-07-30-...:7`).
7. **Doc currency: 3 DRIFTED.** `ARCHITECTURE.md:855` repeats the undischarged claim (with
   `last_reviewed: 2026-08-02`, two days after the discharge); `:381` says 13 doc->code rules
   while the organ reports **14**; `:427` cites `logs/parity-events.jsonl` but live is
   `PARITY-EVENTS.jsonl` — and the same file gets the casing right at `:245`/`:247`.

### L-C — W4 staging ([#383] wave state, [#465] leg 4)
`2026-08-03-technical-night-lc-w4-staging.md`

1. **Wave-1/2 hypothesis: PARTIAL.** Both SHAs exist and are on the first-parent spine.
   `1afd9579` CONFIRMED as the ADR-109 §4 discharge (proof commit `9a75777e`, named verbatim at
   `ADR-109:297-299`). **`67863180` REFUTED as a §4 discharge** — it landed a *different*
   amendment, the "9 governs" Related-line gloss (`ADR-109:341`). §4 was discharged **once**.
   `ADR-109:335-339` says the discharge "does **not** close [#383] ... and it makes no claim
   about surfaces beyond the two now shown."
2. **Wave 3 = the FIRST true surface wave.** Derived from the row's own enumeration
   (`BACKLOG.md:439`, byte-identical in `tasks/383-...`): caches | `.claude`+skills |
   archives-inside-each-folder | docs layout | Python parity | colours-via-carrier. **Nothing is
   struck off** — wave 1's surface was `docs/intake/` and wave 2's was fleet membership;
   neither is a list member, a point recorded *in advance* at
   `2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md:103-107`. Proposed subject:
   **caches** — first enumerated, and the only surface both fully specified and probed.
3. **CRITICAL for the freeze: the row's existing Done-when is already vacuously true.** Live
   divergence run tonight: `conform 185 / diverge 3 / declared 3 / n/a 219` — **byte-identical
   to the 07-31 run and the 08-02 reading**. All 8 ignore-* rows conform. The drafted Done-when
   therefore requires both layers and names the unwalked repos.
4. **[#465] leg 4 defect statement (the WRITER defect, not the instance):** the fleet-audit
   writer emits a daily verdict token for a check whose subject has not existed for two spec
   generations, and nothing detects it — **285 `n/a` vs 5 `pass`** across every history file on
   `origin/automation/fleet-audit`, the 5 `pass` all dated 2026-06-15 and carrying the *same*
   evidence string the `n/a`s carry. Self-disable quoted at `audit.py:733-737`; the docstring at
   `:718-720` still promises "a clean pass", the exact behaviour leg 1 removed. Full contract
   drafted paste-ready (FR-1..FR-7, fixtures F1-F6, REDs R1-R3, AC-1..AC-7, tripwires T1-T3).

### L-D — [#472] option B dossier (amendment-shaped)
`2026-08-03-technical-night-ld-472-option-b.md`

1. **HEADLINE: the brief's "ADR-104 §15" does not exist.** ADR-104 is 113 lines with headings
   `## Context`, `## Decision`, `### 1`..`### 5`, `## Consequences`, `## Alternatives
   considered` — **there is no §15**, and no `ADR-104 §15` reference exists anywhere in the
   repo. The fleet enumeration is at **ADR-104 line 15** — a LINE, not a section. The [#462]
   module comment already reads it correctly (`audit.py:3200`: *"can drift from ADR-104:15
   silently"*). **The locus must be corrected before the amendment is drafted for real**, or it
   will cite a non-existent section.
2. **Constraint set verified 3 of 4 clean.** No-new-file SUPPORTED verbatim twice
   (`ADR-109:87`, `ADR-109:265-266`); no-registry-authority SUPPORTED (`ADR-109:382-384` +
   `audit.py:3299-3300`); bind-to-anchor consistent (design constraint, nothing contradicts).
   Amendment-not-edit supported in mechanism (`ADR-94:24`) but **FLAGGED on citation** per (1).
3. **Anchor form chosen on evidence:** an HTML-comment `declaration:start/end` pair — because
   `scripts/` already parses **five** HTML-comment grammars and **zero** fence info-string
   grammars (every fence handler treats a fence as a region to SKIP).
4. **Validator leg:** a new leg *inside* the existing `check_membership_agreement`, after the
   `_is_hub` guard — it already owns the constant, is already gated by `audit-health`, is
   already hub-only, and keeps `len(ALL_CHECKS) == 38` so `doc-counts` does not drift.
   All three artifacts (amendment text, binding spec, 5-line migration note) are paste-ready.

### L-E — library-first sweep (increment 2)
`2026-08-03-technical-night-le-library-first.md`

10 rows, **6 adopt / 4 leave**; no adopt row adds a new distribution to `uv.lock`. Top three,
all **measured defects** rather than style preferences:

1. **`scripts/changelog_sentinel.py:45-52`** — `parse_version`'s regex `(\d+(?:\.\d+)+)`
   discards every suffix, so `2.0.15rc1` -> `(2,0,15)`. Re-verified live by this lane via the
   correct `parse_version` -> `is_newer` composition: `installed=2.0.15, reviewed=2.0.15rc1`
   gives hand-rolled **False** where PEP 440 gives **True**; `2.0.14.post1` vs `2.0.14`
   likewise. **If a prerelease is ever the reviewed value the sentinel goes permanently quiet
   for that tool.** Fix is `packaging.version.Version` — already declared at
   `pyproject.toml:37`. ADOPT.
2. **`gen_claude_rosters.py:61-73` + `gen_intake_index.py:47-65`** — two hand-rolled frontmatter
   readers, both justified by a "no yaml dep" comment that is **now false** (`pyyaml>=6.0`
   declared, already imported by 15 modules). 5 of 6 probes diverge from `yaml.safe_load`; one
   sibling regex has no underscore in its class, so `last_reviewed:` matches nothing. Both
   outputs are pre-commit-gated and one is `@`-imported into CLAUDE.md. ADOPT.
3. **`scripts/toc/generator.py:47-50`** — naive `in_fence` toggle; 8 of 1493 md files diverge
   from `markdown-it-py` (`~~~` fences unprotected; nested 4-tick fences invert the toggle).
   Dormant on the gated file today, but `toc-freshness` is a **deployed** hook that runs on
   consumer docs. `markdown-it-py` is already in `uv.lock` via `rich`. ADOPT.

Re-checked from 2026-08-02: the `packaging` swap PARTLY LANDED (`a7e42a30`, fleet_parity only);
**networkx DOWNGRADED to leave** — the hand-rolled DFS matched stdlib `graphlib` on 24,000
random graphs with 0 mismatches, so stdlib beats the new dep here.

### L-F — rulings prep
`2026-08-03-technical-night-lf-rulings-prep.md`

B-2/B-3/B-4 all located verbatim
(`2026-08-02-technical-night-batch-lb-fleet-audit-commits.md:160-162`); nothing un-locatable.

- **B-2 (SessionStart trigger retirement) — recommend INVESTIGATE-FIRST, premise falsified.**
  The collapse the retirement was argued from was **fixed** at `56f82aaf` ("[#465] legs 2+3");
  all five 2026-08-02 run blocks now read `warn=15 / fail=0 / not-the-hub=0`. Separately the
  lane shows **no 09:00 scheduled run since 2026-07-23** (10 consecutive days), so retiring
  `fleet_health.py` would remove the only live producer. Two corrections to L-B: its headline
  day 07-21 has no 09:00 run at all, though the correlation reproduces exactly on 07-23.
- **B-3 (ratchet n=1) — recommend WATCH.** The FAIL is a read-path transient
  (`ref_state == "invalid"`, `audit.py:2802-2808`) with **five** subsequent clean `pass`
  observations on 2026-08-02 that did not exist when the finding was written.
- **B-4 (lineage authority) — recommend BRANCH-AUTHORITATIVE. Brief premise corrected:** the
  phrase *"Act-1 lossless union"* **is not in the repo** (UNVERIFIABLE as quoted). The referent
  is `55733ea4`, which unified three RUNS of ONE DAY inside the lane — not the two LINEAGES,
  which remain near-disjoint (16 dates main-only, 45 lane-only, 1 shared and unequal). So
  lineage does gate nothing — **but it gated nothing before the union either.**
- **§F numeric target — TWO REFUTED FIGURES, no number recommended (the constraint is honoured).**
  (i) *"+52.8 adds/week"* — an artifact of the ADR-107 migration: **174 of ~211 `tasks/`
  file-adds came from one commit `9bd0d719`**. Wrong instrument — it measured files-as-artifacts,
  not rows-as-work; true rate 5/window. (ii) *"target 150 rows (25% reduction)"* — **no source;
  invented in-lane.** The only in-repo 2026-08-26 references are gates AT the date, not count
  targets. Four candidate *definitions* are laid out with their gates (C1 gross count; C2
  open-only, with the named loophole that deferring becomes a legal way to pass; C3 per-window
  flow invariant `closed >= filed`; C4 directional-only, no gate). **The number is the
  operator's ruling alone and no number or definition is recommended.**

---

## Wrap facts

- **Artifacts:** 7 files, all in the existing `docs/audits/`, all passing both hermetization
  rules. No new directory. No repo prose edit, no BACKLOG edit, no script edit.
- **`docs/audits/README.md` regenerated** (`gen_audit_index.py --write`) and included in this
  commit. This is one file beyond the brief's literal "flat dated files" wording, and it is
  deliberate: the index is a **generated** file gated by the `audit-index-freshness` pre-commit
  hook and by `test_live_index_is_fresh`, so omitting it would leave the branch with a failing
  test and a blocked commit path. **Precedent, not inference:** the 2026-08-02 night batch
  merged at `c30af862` did exactly this — 7 files in one commit, six lane files plus
  `docs/audits/README.md | 8 +-`.
- **No leftovers.** `.git/hooks/` was armed for one control probe and restored to its
  as-cloned state (samples only). Two gitignored artifacts were written by `fleet_parity`
  (`logs/FLEET-PARITY.md`, `logs/PARITY-EVENTS.jsonl`, both matched by `.gitignore:55-56`).
  `git fetch --unshallow` and `git fetch origin main` altered `.git/` refs only. **The tracked
  tree carries exactly the 7 artifact files and nothing else.**
- **One commit, then STOP.** No merge, no PR, no push to `main`.

## Coverage — what this night did NOT establish

- **No gate ran through its production path** (`uv run --locked` unavailable). Every green
  verdict tonight is "green under a lock-matched venv", not "green under the gate environment".
- **Ship-gate GREEN is not witnessable from a cloud clone** (absent siblings, absent gitignored
  `ecosystem/<repo>/state.yaml`, `.`-less directory name). L-A states what would have to be
  true rather than asserting the verdict.
- **The suite's 2-failure claim is not reproducible here** — 33 fail for enumerated missing
  prerequisites. The two `[#457]` ids are present in the set; the other 31 are classified above.
- **Whether the terra review ran** is outside this repo's evidence. Only its artifact absence
  is a fact.
- **`[#457]` leg (i) could not be reproduced** — unarmed hooks produce a different WARN.
- **`[#244]` / `[#401](a)`** need consumer trees not present in this container.
- Machine-local Windows scheduler state (the `\fleet-baseline` task) could not be checked; only
  its OUTPUT was, and absence of output is not proof of breakage.

---

## Follow-up — 2026-08-03 morning absorb (APPENDED at merge; nothing above is edited)

**The production-path caveat is RESOLVED.** The night's single largest stated limit — *"no gate
could be exercised through its production path"* (`uv run --locked` aborts; the box carried uv
0.8.17 against a `==0.11.19` pin) — is an artifact of the cloud container and does not hold on
the operator's machine. Re-run here on the pinned toolchain: **uv 0.11.19** (`uv --version` =
`uv 0.11.19 (7b2cff1c3 2026-06-03 x86_64-pc-windows-msvc)`, exactly the `pyproject.toml:25`
`required-version = "==0.11.19"` pin), environment rebuilt via `uv sync --locked` plus
`uv sync --locked --group analytics`, and **every verdict below produced through
`uv run --locked`** — the same entry point every `language: system` pre-commit hook uses. This
is the gate environment, not a lock-matched stand-in.

**Every gate verdict reproduced line-for-line**, measured on `main` at `c7628a3e` *before* this
merge — i.e. against exactly the content the lanes measured:

- `python scripts/audit.py ship-gate` -> **`ship-gate: GREEN - verification organs green
  against this arc (15 WARN dispositioned)`**. Claim **6a moves UNVERIFIABLE -> CONFIRMED**.
  Claim **6b is CONFIRMED as written (`[stale]` = 0)**, and the container's `= 1` is confirmed
  container-caused exactly as L-A diagnosed: the
  `warn-fleet-parity-ai-council-root-conftest` disposition fires normally where ai-council is
  checked out. Both were correctly reasoned from absence; both are now measured.
- `python -m pytest -n auto` -> **`2 failed, 2190 passed, 3 skipped in 245.35s`**;
  `--collect-only` -> **2195**, matching `ecosystem/doc-counts.md:15`. The failure set is
  **exactly** the two `[#457]`-owned ids
  (`test_routine_consumers_live_backlog_governs_exactly_one_row`,
  `test_check_fleet_parity_green_on_live_repo`). Claim **4b is reproducible here as a bare
  count**; none of the 31 container-prerequisite failures occur.
- `validate_backlog.py` -> `OK (9 themes, 26 stories, 186 tasks, 1 warning(s))`;
  `validate_git_backlog.py` -> `OK - no closed-but-present drift (direction (a) STRONG, full
  history)`; `gen_task_tree.py --check` -> `check ok`. Claims 5c / 5e / 5f stand unchanged.

**What this does NOT resolve.** Every finding that was never environmental survives untouched
and remains the architect's to rule on — this note narrows the environment, not the findings.
HEADLINE 1 (the W2 terra review left no artifact), HEADLINE 2's portability defect
(`audit.py:2300` keys `deployed-versions.yaml` by repo-root basename), HEADLINE 3 (the brief's
`night-<lane>` pattern vs the ADR-101 R3 closed enum), and the Run-2 observation that `[#457]`
leg (i) fails here for a reason the row does not record, are all repo-content findings. They are
routed into this morning's session as separate arcs; none is discharged by this paragraph.
