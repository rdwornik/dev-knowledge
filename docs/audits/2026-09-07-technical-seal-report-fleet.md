# Tree-seal REPORT — the whole fleet, measured against the ratified shape spec

> **REPORT MODE. Nothing armed, nothing moved, nothing written in any consumer.** The only
> command that touched a consumer repo is `git -C <repo> ls-files` (plus `rev-parse` /
> `status --porcelain` to stamp the measurement). The verbs are **RELOCATE / RETIRE / WAIVE**,
> and per C-8 the deletion verb is **RETIRE-PROPOSED**. No item in this file is executed by
> this lane. The operator rules each list at dawn; execution lanes follow his word.
>
> Produced by lane `lane-u-000-seal-report-fleet` (batch U, NIGHT-2 row `W2-U2`, wave 2), after
> W2-U1 merged at `61728224` and made the fleet shape grammar **data**
> (`ecosystem/fleet-shape-spec.yaml`). Its predecessor is
> `docs/audits/2026-09-06-technical-seal-report-corp-monorepo.md` — one repo, measured against
> the *old* rule where the hub's own tree stood in for the fleet's shape.

**Before → after** — the before half re-measured on this seat, not restated from the contract.

```
before: repos with a seal report: 1  (docs/audits/2026-09-06-technical-seal-report-corp-monorepo.md;
        the only per-repo seal REPORT in docs/audits/ -- the other two `seal` files are a
        pre-commit-gate retro and a window seal, neither a repo tree seal)
after:  repos with a seal report: 9  -- the entire ADR-104 fleet. NOT 10. The contract says ten
        and there is no tenth repo; the arithmetic is resolved in section 12.

before: corp-monorepo unresolved 77 (WAIVE count of the 2026-09-06 report: 78 items = R1 / T0 / W77)
after:  corp-monorepo unresolved 73 (74 items = RELOCATE 1 / RETIRE 0 / WAIVE 72 / ESCALATED 1)
        -- "unresolved" is the same quantity the 77 was: every item NOT proposed for relocation.
```

**The headline, stated plainly because it is the honest one.** RATIFICATION-2026-09-07 §1 set the
test: *"If the number does not move, the universalization claim is not yet earned."* The number
moved by **four**, from 78 items to 74. All four are Rule A. **Rule B moved by zero and Rule C
moved by zero** — 39 and 32 items respectively, unchanged to the item. The contract's expectation
("expect 77 WAIVE → mostly resolved by the new homes") is **not met**, and the reason is
structural rather than accidental: amendment D5 admitted `src/ eval/ models/` as top-level
*directories*, and corp-monorepo has no `src/` tree at all — its out-of-pattern homes are
`tests/<package>/` and `config/**`, which D5 did not touch.

**The universalization claim is earned for Rule A and is not yet earned for Rules B and C.**

---

## 1 · Method — and why no second seal exists

The dispatcher pin is explicit: *"The seal has no consumer mode — reuse the rule functions."*
This run does exactly that. `scripts/validate_hermetization.py` exposes `rule_a_violation`,
`rule_b_violation` and `rule_c_violation` as plain functions over a repo-relative path string;
only its `main()` is coupled to git staging. REPORT mode is feeding a consumer's `git ls-files`
output to those three functions. **No checker was written for this report** — an explicit
anti-pattern of both this lane's contract and its predecessor's.

- **Library-first check (C-11).** Inventoried before any build: `validate_hermetization`
  (Rules A/B/C, now spec-driven), `canonical_docs` (`CANONICAL_MANDATORY`,
  `CANONICAL_RETIRED_LOCATIONS`), `ecosystem/fleet-shape-spec.yaml`. All reused as libraries.
  Nothing hand-rolled, so there is no measured divergence to record.
- **Read-only, provably.** Only `git -C <repo> ls-files`, `rev-parse`, `status --porcelain`.
  Two consumers were dirty or off-`main` **before** the run and were left exactly as found (C-8);
  both are stamped below.
- **Grain, unchanged from the predecessor so the two reports are comparable.** Rule A is reported
  per ITEM (a top-level file, a top-level directory, a `docs/<genre>/`). Rule B is per FILE. Rule C
  is per **distinct home**, never per file — win-tooling's 111 files sit under 42 homes, and 111
  rows is not a list anyone can rule on.
- **Short-circuit parity.** A path that trips Rule A is not also counted under B or C, matching
  `classify()`'s own `A or B or C` ordering. Counts here are therefore the same quantity the gate
  would print.

**Re-run command** (from the hub root; the harness is a throwaway, these calls are the artifact):

```
uv run --locked python -c "import sys,subprocess; sys.path.insert(0,'scripts'); import validate_hermetization as vh; R=r'C:/Users/1028120/Documents/Dev/<repo>'; ps=[p for p in subprocess.run(['git','-C',R,'ls-files'],capture_output=True,text=True).stdout.splitlines() if p.strip()]; print(len(ps),'tracked'); [print(p,'->',vh.classify(p)) for p in ps if vh.classify(p)]"
```

### 1.1 · Fleet totals — measured

```
repo                       head       branch                      tracked  items   A-f  A-d  A-g    B   C-homes (files)
.dev-knowledge             ef53b069   main                           2993    137     0    0    0  137    0     (0)
ai-council                 7a3c057    main                            254     32     3    1    0   26    2    (26)
corp-monorepo              37b8aa1    main                            821     74     3    0    0   39   32   (297)
corp-ops                   3bde930    main                             60      5     2    2    0    1    0     (0)
corp-sca-time-automation   3661b3a    feature/tenrox-loader            75      8     3    2    0    2    1     (1)
demo-prep                  1f7c35c    feat/leadership-template-deck   883     37     2    6    0   28    1     (5)
life-architect             7688b76    main                             45      5     2    3    0    0    0     (0)
terminal-setup             d8a7b61    main                              3      2     2    0    0    0    0     (0)
win-tooling                49cb75e    main                            177     48     4    1    1    0   42   (111)
                                                                     -----   ----   ---  ---  ---  ---  ---
                                                                      5311    348    21   15    1  233   78   (440)

verdicts proposed          RELOCATE 11  ·  RETIRE 0  ·  WAIVE 336  ·  ESCALATED, not verdicted 1
```

**Measurement caveats, stated rather than buried.**
`corp-sca-time-automation` was checked out on `feature/tenrox-loader` and `demo-prep` on
`feat/leadership-template-deck`; both were measured on the branch they were found on, and
`demo-prep` carried 2 dirty lines (` M .gitignore`, `?? docs/handoffs/2026-09-03-colleague-repo-bootstrap/`)
which were left untouched. Those two rows describe a working branch, not `main`.
The hub's own HEAD moved during this batch (`61728224` at lane boot → `ef53b069` at measurement);
`ef53b069` is the figure the 137 was taken at.

### 1.2 · Zero RETIREs, and that is a finding

**Across 348 out-of-pattern items in nine repositories, this report proposes zero RETIREs.**

**Where that evidence stops, stated rather than implied.** Every one of the 348 items was
classified, and each of the fifteen classes in §11 carries a witness for the class — a carrier
manifest stanza, a ratified ADR, a repo's own declared waiver, a spec clause the hub wrote from
its own tree. What was **not** done is an item-by-item merits review of all 348: the Rule B and
Rule C populations (305 items) were ruled at class grain, which is the same grain §1's "Grain"
note declares and the same grain the predecessor used. **So the honest claim is narrower than
"nothing here is junk": no class in this fleet resolves to junk, and no item surfaced during
classification that contradicted its class.** Two rows are flagged in the sections above as the
places where an item-level look at dawn could plausibly change that — demo-prep's tracked
`output/` directory (§7) and ai-council's `.gitkeep`-only `council_inbox/` (§3) — and both are
argued there as WAIVE rather than left silent.

The predecessor said this of corp-monorepo alone ("78 out-of-pattern items with ZERO of them
junk"); it now holds fleet-wide at 4.5× the sample and at class grain.
**A seal whose refusals are 97% waivers is measuring difference-from-the-hub, not shape.**

---

## 2 · `.dev-knowledge` — the hub · 137 items · R0 / T0 / **W137**

`ef53b069` · `main` · 2993 tracked · Rule A **clean**, Rule C **clean**, Rule B 137.

**All 137 are Rule B `class:` — a `docs/audits/*.md` with no CLOSED-enum class token after the
date. All 137 → WAIVE.**

- **Witness — already ruled, by name.** `validate_hermetization`'s own docstring: the gate is
  *"**prospective-only**: it inspects only ADDED paths … so every existing file is grandfathered
  and never checked (ADR-101 section 6 — no retroactive rename over the ~130 subject-before-class
  + 4 class-less legacy files the date-index already disambiguates)"*. The measured 137 is that
  declared ~130+4 population, counted exactly.
- **Witness — the prospective gate holds.** Of the 137, **zero carry a `2026-08` or later date**;
  the newest is `2026-07-09`. Rule B has been armed at the hub since ADR-101 landed and nothing
  has been added past it since. This is the one number in the report that says an organ works.
- **No RELOCATE is proposed.** 137 renames would break every inbound citation in
  `docs/audits/README.md`, the JOURNAL and the ADR corpus, to buy conformance to a vocabulary the
  files predate. ADR-101 §6 already ruled this and the ruling should stand.

---

## 3 · `ai-council` · 32 items · **R1** / T0 / W31

`7a3c057` · `main` · 254 tracked.

**Rule A — top-level files (3)**

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`.** *Class V (see §11).* Witness: ADR-114
  Amendment 1 retired `VISION` from `canonical_docs.CANONICAL_MANDATORY` into `CANONICAL_RETIRED`,
  and `CANONICAL_RETIRED_LOCATIONS` records the destination the hub itself used, executed by
  `[#614]` lane-e-5 on 2026-09-01. ai-council has simply not received that migration.
- **`INSTALL.md` → WAIVE.** *Class I (see §11).* **The carrier wrote this file.**
  `deploy/manifest-v1.5.0.yaml` component `install-guide` declares
  `source: plugins/tier1-lifecycle/INSTALL.md` → `path: INSTALL.md`, and the hub grows no root
  `INSTALL.md` of its own — so `SANCTIONED_TIER1_FILES`, unioned from the hub root and the spec's
  `root_allowlist.files`, cannot admit it. A seal shipped as-is refuses a file the deploy tool put
  there. **Proposed as a spec fix rather than a consumer fix** -- the evidence establishes the
  mismatch, not which side must move; that is the operator's dawn ruling.
- **`conftest.py` → WAIVE.** *Class P (see §11).* A root `conftest.py` is the ordinary pytest
  layout. The hub has **no `conftest.py` anywhere in its own tree** (`find . -name conftest.py`
  returns only a `.venv` vendored copy), so the fleet's file allowlist has no entry for the single
  most standard file in a Python test suite. Spec fix.

**Rule A — top-level directories (1)**

- **`council_inbox/` → WAIVE.** Tracked content is `council_inbox/.gitkeep` alone: a runtime inbox
  the CLI writes into, kept alive by a placeholder. *Class D (see §11).* The `.gitkeep`-only shape
  makes RETIRE-PROPOSED superficially attractive and it is **the wrong verdict** — deleting the
  directory removes the write target, and this report does not propose a deletion it cannot prove
  is safe.

**Rule C — homes (2 distinct, 26 files)**

- **`docs/audits/2026-07-18-cli4-parity/blinded/` (24 files) → WAIVE** and
  **`docs/audits/archive/legacy/` (2 files) → WAIVE.** *Class H2 (see §11).* The spec admits
  `docs/audits` and `docs/audits/*` but stops there, so an audit bundle with **one further level**
  — a blinded corpus, an archive tier — falls out. Compare `docs/handoffs/**`, which the spec
  already writes with an open depth for exactly this shape. **Cheap spec fix: `docs/audits/**`.**

**Rule B — 26 files → WAIVE.** All `class:`, all lowercase and well-formed, all outside the
hub-local enum (`2026-07-20-night-code-audit-opus.md`, `2026-07-19-guards-violation-proof.md`,
`2026-08-08-416-codemap-reverification.md`). *Class B2 (see §11).*

---

## 4 · `corp-monorepo` · 74 items · **R1** / T0 / W72 / E1 — the re-run

`37b8aa1` · `main` · 821 tracked. Previous measurement (2026-09-06): **78 items, R1 / T0 / W77.**

### 4.1 · What the new spec actually resolved — 4 items, all Rule A

| Item | Old verdict | Now | Why |
|---|---|---|---|
| `src/` (214 files) | WAIVE | **resolved** | D5 gave `src` root sanction + `src/**` home |
| `eval/` (54 files) | WAIVE | **resolved** | D5 gave `eval` root sanction + `eval/**` home |
| `models/` (6 files) | WAIVE | **resolved** | D5 gave `models` root sanction + `models/**` home |
| `.corp-monorepo.code-workspace` | WAIVE | **resolved** | hub literal → fleet glob `.*.code-workspace` |

That is the whole delta. **The remaining 74 are the same 74 items the predecessor listed**, with
the same verdicts and the same witnesses, and this report does not re-litigate them — it confirms
them against the ratified spec and carries them forward.

### 4.2 · The dawn list, unchanged

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).* The one RELOCATE, on the
  hub's executed precedent. Sequencing note from the predecessor stands: it pairs with corp's
  missing root `README.md`, which is repo-specific content and **not carrier-deliverable**, so the
  relocation is ready and the replacement front door needs an authoring act.
- **`INSTALL.md` → WAIVE** *(Class I)* · **`tach.toml` → WAIVE** *(Class N — dot-prefix, ADR-59).*
  The `tach.toml` alternative verdict is RELOCATE to `.tach.toml`; **it is still not verified that
  `tach` reads a dot-prefixed config**, and this report will not propose a rename that might break
  a consumer's own gate on an unverified assumption.
- **Rule B, 39 → WAIVE.** Two halves, different standing: **11 UPPERCASE `_TYPE_` files are
  already declared** by corp's own `.methodology.yaml` component `audit-casing-r4`, by
  enumeration, on a review clock (`review_date: 2026-10-12`) — zero operator work. **28 lowercase
  free-slug files** are the *Class B2* over-block corp's own waiver predicted in writing
  (*"corp audit files use free lowercase slugs … outside that enum, so carrying it would
  over-block"*). The measurement confirms the prediction to the file.
- **Rule C, 32 homes / 297 files → WAIVE.** `config/*` (10 homes) and `tests/*` (20 homes) are
  *Class H1*; `scripts/archive/` is *Class H3*; `docs/decisions/transcripts/` (28 files) remains
  *Class T*: **escalated as a question, not a verdict** — the hub deleted its own in-hub transcript archive on
  2026-07-22 by operator ruling and keeps an ADR-77 guard armed against recreating it, and
  RATIFICATION §1 D9 already records that this stays **hub-scoped** and does not propagate.

---

## 5 · `corp-ops` · 5 items · **R1** / T0 / W4

`3bde930` · `main` · 60 tracked.

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).*
- **`INSTALL.md` → WAIVE** *(Class I)* — carrier-written; second confirmation.
- **`assets/` → WAIVE** and **`tools/` → WAIVE** *(Class D).* corp-ops is a PowerShell + Python
  operational toolbox; `tools/` is its executable home and `assets/` its static one. The root
  allowlist has no domain-directory concept at all (§11 Class D).
- **`docs/audits/2026-07-05-x1-backup-proposal.md` → WAIVE** *(Class B2)* — lowercase,
  well-formed, `x1-backup-proposal` is not an enum class.

**Read this row against its size.** 60 tracked files, 5 out-of-pattern, of which one is a real
migration and four are spec gaps. corp-ops is close to clean and the residue is almost entirely
the hub's.

---

## 6 · `corp-sca-time-automation` · 8 items · **R2** / T0 / W6

`3661b3a` · **`feature/tenrox-loader`** (not `main` — measured as found, C-8) · 75 tracked.

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).*
- **`docs/tenrox-console-uploader.md` → RELOCATE.** *The genuine Rule C finding in this repo, and
  it is precisely the class Rule C was built for.* A file loose at the `docs/` root introduces no
  new top-level entry and no new genre folder, so **Rule A is silent by its own literal spec** —
  this is the `docs/ORGAN-INDEX.md` shape named in `validate_hermetization`'s docstring, caught by
  the leg that reads the rest of the path. The repo already carries `docs/archive/`,
  `docs/audits/` and `docs/decisions/`, so a genre home exists; `docs/archive/` is the proposed
  destination and the operator may prefer a different genre. **Destination is his call; that it
  does not belong loose at `docs/` is the finding.**
- **`pytest.ini` → WAIVE** and **`requirements.txt` → WAIVE** *(Class P).* This repo is not on the
  ADR-106 `uv` + `pyproject.toml` stack, and neither file has an entry in
  `root_allowlist.files` — which carries `pyproject.toml`, `uv.lock` and `.python-version` and no
  pre-uv Python root file at all. Migrating corp-sca's toolchain is a real decision and is
  **out of scope for a seal report**; the spec gap is the reportable half.
- **`assets/` → WAIVE**, **`data/` → WAIVE** *(Class D).*
- **2 Rule B files → WAIVE** *(Class B2)* — `2026-07-05-tenrox-aspx-pivot.md`,
  `2026-07-05-tenrox-reconciliation.md`.

---

## 7 · `demo-prep` · 37 items · **R1** / T0 / W36

`1f7c35c` · **`feat/leadership-template-deck`**, 2 dirty lines left as found (C-8) · 883 tracked.

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).*
- **`SOURCES.md` → WAIVE.** A repo-local root register of source material. *Class F (see §11).*
- **Six top-level directories → WAIVE** *(Class D)*: `brand/`, `examples/`, `generators/`,
  `knowledge/`, `output/`, `pipeline/`. This is the widest domain footprint in the fleet and the
  clearest evidence for the repo-KIND axis: demo-prep is a deck-production pipeline and **every
  one of these six is its subject matter.** `output/` is worth a second look at dawn — a tracked
  build-output directory is the one row here where RETIRE-PROPOSED could be argued — but this
  report does not propose deleting tracked deliverables it has not been asked to evaluate.
- **`templates/_PPTX_TEMPLATE_KIT/` (5 files) → WAIVE** *(Class H1).* The spec admits `templates`,
  `templates/archive`, `templates/claude-regions`, `templates/handoff` and `templates/handoff/*`
  — five literals, all of them the hub's own subdirectories. A consumer's template subdirectory
  falls out by construction.
- **28 Rule B files → WAIVE** *(Class B1, `casing:`).* demo-prep uses a lowercase `_type_` form:
  `2026-07-08_report_master-deck.md`, `2026-07-12_plan_night-a-process.md`,
  `2026-09-01_brief_article-harness-substrate.md`. It is a **consistent, self-declared local
  vocabulary** (`report`, `plan`, `brief`, `evidence`, `qa`, `review`, `spec`, `postmortem`) that
  simply uses `_` where R4 requires `-`. Unlike corp-monorepo, demo-prep is
  methodology-unonboarded and has **no `.methodology.yaml` waiver on record**, so this is
  `WAIVE-pending-declaration`: the honest verdict is a waiver, and the durable fix is either a
  declared waiver at onboarding or 28 renames. **Renaming is cheap here relative to corp's 28** —
  demo-prep's audit files are far less cited — so this is the one Rule B population where
  RELOCATE is a live alternative rather than a formality.

---

## 8 · `life-architect` · 5 items · **R2** / T0 / W3

`7688b76` · `main` · 45 tracked.

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).*
- **`intake/` → RELOCATE → `docs/intake/`** *(Class G).* *The strongest non-VISION RELOCATE in the report,
  and it rests on the repo's own half-completed adoption.* life-architect already carries
  `docs/decisions/ADR-01…ADR-07` and `docs/decisions/README.md` — it adopted the `docs/<genre>/`
  layout for decisions. Its `intake/` holds exactly what `docs/intake/` holds at the hub: dated
  briefs (`2026-07-06-life-architect.md`, `2026-07-08-endpoint-driven-life-brief.md`, …) plus a
  `README.md`. `intake` is a **sanctioned genre** (`genre_folders.genres`) and is out-of-pattern
  here only because it sits one level too high. Seven files move; nothing is renamed.
- **`OPEN-QUESTIONS.md` → WAIVE** *(Class F)* — a repo-local root living doc.
- **`dimensions/` → WAIVE**, **`seed/` → WAIVE** *(Class D)* — the repo's subject matter
  (`dimensions/D04-health/…`) and its founding corpus.
- **Rule B: 0. Rule C: 0.** life-architect's `src/life_architect/` and `tests/` are admitted by
  D5's `src/**` and the `tests` home. **It is the one consumer that benefits from D5 today.**

---

## 9 · `terminal-setup` · 2 items · R0 / T0 / **W2**

`d8a7b61` · `main` · **3 tracked files.**

- **`huvix-custom.omp.json` → WAIVE**, **`setup.ps1` → WAIVE.** *(Class U.)*

Both are the repo's entire content. `ecosystem/registry.md` records terminal-setup as
*"registered 2026-08-01 (`[#462]`) · unonboarded · declared fleet by ADR-104 2026-07-24; no
methodology adoption (no VISION.md, no CLAUDE.md, no deploy record)"*, and
`canonical_docs`'s own comment names it as the member *"that has never had a `VISION.md`"*.
**Sealing a 3-file repo with no methodology adoption measures the absence of adoption, not a
defect.** No RELOCATE, no RETIRE. The reportable question is whether ADR-104 membership should
imply seal coverage at all for an unonboarded repo — filed to §11, not decided here.

---

## 10 · `win-tooling` · 48 items · **R3** / T0 / W45

`49cb75e` · `main` · 177 tracked. **The only repo in the fleet with a Rule A genre violation.**

- **`VISION.md` → RELOCATE → `docs/archive/VISION.md`** *(Class V).*
- **`docs/diagrams/` → RELOCATE** *(Class L).* The fleet's **single** unsanctioned `docs/<genre>/`. One file:
  `docs/diagrams/module-map.md`. The predecessor report noted the Tier-2 genre seal was already
  clean at corp-monorepo; across nine repos it is clean at eight. One file moving into an existing
  genre closes it. Named alternative, not recommended: admit `diagrams` to
  `genre_folders.genres` — **a genre admission for a single file in one repo is the drive-by
  growth ADR-101 §1 exists to refuse**, and the report says so rather than leaving the operator to
  infer it.
- **`docs/` home, 2 files → RELOCATE** *(Class L)*: `docs/2026-08-28-nb2-lane-b-packet.md` and
  `docs/2026-09-01-lane-632-codespace-arc-packet.md`. Same class as corp-sca's loose `docs/` file
  — dated lane packets sitting at the `docs/` root where `docs/audits/` is their genre. Note the
  dates: **these are 2026-08/09 artifacts, the newest out-of-pattern files in the fleet.** Every
  other RELOCATE in this report is a legacy migration; this one is live drift, which is what a
  seal is supposed to catch.
- **`INSTALL.md` → WAIVE** *(Class I* — third confirmation*)* · **`conftest.py` → WAIVE**
  *(Class P* — second confirmation*)*.
- **`config.yaml` → WAIVE** *(Class N).* The ADR-59 dot-prefix class, already carried as
  win-tooling row **WT-4** (*"root `config.yaml` not dot-prefixed and not on the ADR-59 exception
  list"*) — an existing, ruled row, and the same class as corp's `tach.toml`. Two independent
  waivers for one class is the argument for a spec clause.
- **`tools/` → WAIVE** *(Class D).*
- **41 of the 42 Rule C homes / 109 files → WAIVE** *(Class H1).* The 42nd is the loose `docs/`
  home ruled RELOCATE two rows up (Class L), and it is deliberately not counted here twice.
  `config/flow-launcher/**` alone is 26 of
  them — a vendored Flow Launcher plugin snapshot, arbitrarily deep by nature. `scripts/<tool>/`
  is 9 more (`scripts/typewhisper/` holds 14 files). **win-tooling has more out-of-pattern homes
  than corp-monorepo (42 vs 32) in a fifth of the tracked files**, which is the sharpest single
  measurement of what Rule C currently measures: `config` and `scripts` are sanctioned as *bare*
  homes with only the hub's own subdirectories enumerated beneath them, so any consumer that
  organizes either directory by tool lights up completely.

---

## 11 · The fleet-wide classes — where the residue actually lives

Fifteen verdict classes account for **all 348 items**, and they reconcile to the measured totals in
§1.1 exactly. Ruling the classes rules the fleet; ruling 348 rows individually is the same work
done 348 times.

```
class  what it is                                     items  repos  proposed verdict
-----  ---------------------------------------------  -----  -----  -----------------------------
B2     Rule B `class:` -- lowercase, well-formed, a      194    5    WAIVE -> spec: split Rule B
       class token outside the hub-local enum                        (date + casing = fleet;
                                                                     class enum = per-repo)
H1     Rule C -- a sanctioned dir organized one level     72    3    WAIVE -> spec: per-repo home
       deeper than the hub organizes it: tests/*,                    declaration (.methodology.yaml)
       config/**, templates/*, scripts/<tool>/
B1     Rule B `casing:` -- a local type vocabulary        39    2    WAIVE (corp: declared by
       using _underscore_ where R4 requires -hyphen-                 .methodology.yaml; demo-prep:
                                                                     pending declaration)
D      Rule A -- a domain top-level directory             14    6    WAIVE -> spec: repo-KIND axis
V      root VISION.md, retired at the hub by ADR-114       7    7    RELOCATE -> docs/archive/
I      root INSTALL.md, written by the deploy carrier      4    4    WAIVE -> spec: add to allowlist
P      a standard Python root file the hub has never       4    3    WAIVE -> spec: conftest.py and
       grown (conftest.py, pytest.ini, requirements.txt)             the pre-uv root files
L      a file loose at docs/ root, or a one-file           3    2    RELOCATE into an existing genre
       docs/<genre>/
H2     Rule C -- a docs/audits bundle one level deep       2    1    WAIVE -> spec: docs/audits/**
N      a non-dot-prefixed root tool config (ADR-59)        2    2    WAIVE -> spec clause
F      a repo-local root living doc                        2    2    WAIVE
U      the entire content of an unonboarded 3-file repo    2    1    WAIVE (see section 9)
G      a root dir duplicating a sanctioned genre           1    1    RELOCATE -> docs/intake/
H3     Rule C -- <sanctioned-parent>/archive, a shape      1    1    WAIVE -> spec: generalize it
       the spec states as six separate literals
T      corp's docs/decisions/transcripts/ -- hub-scoped    1    1    ESCALATED, not verdicted (D9)
                                                         ----
                                                          348      RELOCATE 11 / RETIRE 0 /
                                                                   WAIVE 336 / ESCALATED 1
```

**Read the top three rows together.** `B2 + H1 + B1 = 305 of 348 items — 88% of the fleet's
out-of-pattern surface is two rules whose content is hub-local.` Rule A, the rule ADR-101 was
written for and the one amendment D5 fixed, accounts for **37** items in total (21 files,
15 directories, 1 genre) — and 11 of the report's 11 RELOCATEs live in it or in Rule C's loose-file
leg. **The rule that works produces the actionable findings; the two that do not produce the
waivers.**

**The three spec fixes with the best ratio, named so the operator can rule them cheaply:**

1. **`docs/audits/**` instead of `docs/audits/*`** — 1 pattern, closes Class H2 outright and costs
   nothing; the spec already writes `docs/handoffs/**` for the identical shape.
2. **`<sanctioned-parent>/archive` as a grammar rule** — the spec states this shape as **six
   separate literals** (`protocols/archive`, `templates/archive`, `tasks/archive`,
   `docs/decisions/archive`, `docs/intake/archive`, plus `docs/archive`). Generalizing it removes
   corp's `scripts/archive/` and ai-council's `docs/audits/archive/legacy/` and pre-empts the class
   fleet-wide.
3. **`INSTALL.md` into `root_allowlist.files`** — 4 repos, one line, and it stops the seal
   refusing a file the deploy tool itself writes.

**The two questions that are genuinely the operator's, not the spec's:**

- **Does Rule B's class enum ship to consumers at all?** 205 items say no. corp's own waiver
  reached that conclusion independently, and the spec already marks the enum
  `audit_class_enum_scope: repo-local`. The date-shape and R4-casing legs are fleet clauses and
  are unaffected.
- **Does the shape spec grow a repo-KIND axis, or does Rule C ship with a per-repo home
  declaration?** 74 items and 4 repos ride on it. Waiving `tests/*` and `config/**` per code repo
  forever is what happens if neither is chosen, and it makes the seal a formality.

---

## 12 · The roster arithmetic — nine repos, not ten

**The contract says ten repos and "all NINE consumer repos". The ratified fleet is nine repos
total: one hub and eight consumers. This report seals all nine and invents no tenth.**

Witnesses, resolved before acting on them:

- `scripts/audit.py::ADR104_FLEET_DECLARATION` names **nine** ids, and `[#472]` made it a MIRROR
  of a machine-locatable `declaration:start/end id=adr104-fleet-members` anchor inside
  `docs/decisions/ADR-104-fleet-repository-shape.md`, with an `audit-health` leg that REDs on any
  disagreement. Editing one without the other names which side is stale — so this is a gated,
  ratified roster, not a convention.
- `ecosystem/registry.md` carries **nine** rows, the same nine.
- Three non-member directories exist under `Dev/` — `illustrated-book-gen`, `overnight`,
  `_scratch` — and **none of them is a git repository** (`Test-Path <dir>/.git` is `False` for all
  three). There is no tenth repo a `git ls-files` seal could have read, so the shortfall is not a
  repo this lane skipped.
- The string "ten repos" / "10 repos" appears in this batch **only in this lane's own contract**;
  no DECLARE, no amendment and no other lane contract carries it.

**Contract default applied (C-3), and the deviation recorded rather than guessed:** the closure
clause asks for *"10 sections, counts per verdict, one dawn ruling list per repo"*. This file has
twelve numbered sections, of which **nine are the per-repo seal lists** — one per ratified member,
each with counts per verdict — and the remainder carry the fleet-wide classes and this arithmetic.
The count that binds is *"one dawn ruling list per repo"*, and every repo in the fleet has one.
Escalated as a file, not as a stop: `to-browser/QUESTION-lane-u-000-seal-report-fleet.md`.

---

## 13 · What this lane did NOT do

- **No write, move, deletion or new folder in any consumer repo.** Nine repos read with
  `git ls-files`; two were found dirty or off-`main` and left exactly as found (C-8).
- **No RETIRE executed and none proposed.** The verb is RETIRE-PROPOSED and the count is zero.
  The basis is class-grain, not item-grain — §1.2 states where that evidence stops.
- **No item-by-item merits review of all 348 items.** Rule B and Rule C (305 items) were ruled at
  class grain, the grain §1 declares and the predecessor used.
- **`docs/audits/README.md` not regenerated** — four lanes land an audit artifact this batch and
  the integrator regenerates once on the merged result ([#590]).
- **No JOURNAL entry** — the integrator's surface (STANDING_RULINGS P-1).
- **No edit to `ecosystem/fleet-shape-spec.yaml`.** Every fix in §11 is a *proposal* for the
  operator's dawn ruling. This lane is a report lane and the spec is another lane's footprint.
- **No re-litigation of corp-monorepo's 74 carried items.** They were measured, confirmed against
  the ratified spec, and cited to the predecessor report rather than restated.

---

**Lane:** `lane-u-000-seal-report-fleet` · batch U, NIGHT-2 row `W2-U2`, wave 2
**Measured:** 2026-09-07, after W2-U1 merged at `61728224`
**Mode:** REPORT — proposals only; the operator rules each list at dawn
