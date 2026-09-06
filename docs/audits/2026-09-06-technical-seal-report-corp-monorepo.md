# Tree-seal REPORT — `corp-monorepo`, the H0 runbook's first step

> **REPORT MODE. Nothing armed, nothing moved, nothing written in `corp-monorepo`.** This file is
> the operator's dawn ruling input for the first consumer: a root list with a proposed verdict per
> item. The verbs are **RELOCATE / RETIRE / WAIVE** — and per C-8 the deletion verb is
> RETIRE-**PROPOSED**. No item here is executed by this lane.
>
> Produced by lane `lane-t-000-shape-seal` (batch T, wave 1), against inbox item 023's plan step (3):
> *"per repo the seal prints OUT-OF-PATTERN items with a proposed verdict RELOCATE / RETIRE /
> WAIVE"*. Its sibling deliverable is the intake DRAFT that states the shape spec.

**Before → after**

```
before: corp-monorepo out-of-pattern items: 78 (unclassified — no measured list, no proposals on record)
after:  corp-monorepo out-of-pattern items: 78 (RELOCATE 1 / RETIRE 0 / WAIVE 77) — proposed only
```

The tree is **unchanged**: 78 → 78 is the honest reading of a report lane. What the run produced is
the classification, not a reduction. Nothing counts as progress until the operator rules the list
and a separate execution lane runs.

---

## 1 · Method — and why no new checker exists

The hub already owns the mechanism inbox 023 names, so this run **reuses it as a library** rather
than reimplementing it. `scripts/validate_hermetization.py` exposes `rule_a_violation`,
`rule_b_violation` and `rule_c_violation` as plain functions over a repo-relative path string; only
its `main()` is coupled to git staging. REPORT mode is therefore: feed the consumer's
`git ls-files` output to those three functions.

- **Read-only, provably.** The only command touching `corp-monorepo` is
  `git -C <corp-monorepo> ls-files`. `corp-monorepo` was clean before the run
  (`git status --porcelain` empty) and untouched after. Head at measurement:
  `37b8aa1` on `main`.
- **Library-first check (C-11):** the hub mechanisms were inventoried before any build —
  ADR-101's `validate_hermetization` (Rules A/B/C), `canonical_docs`
  (`CANONICAL_MANDATORY` / `CANONICAL_RETIRED_LOCATIONS`), `fleet_parity`'s root sweep,
  `check_workspace_settings`. All four were reused. **No hand-rolled checker was written**, which
  is also an explicit anti-pattern of this lane's contract.
- **Grain.** Rule A and Rule B are reported per ITEM (a file, a directory, a filename). Rule C is
  reported per **distinct home**, not per file: 297 files sit under 32 homes, and 297 rows would be
  a list nobody can rule on.

**Re-run command** (from the hub root; the script is a throwaway, the three calls are the artifact):

```
uv run --locked python -c "import sys,subprocess; sys.path.insert(0,'scripts'); import validate_hermetization as vh; R=r'C:/Users/1028120/Documents/Dev/corp-monorepo'; ps=[p for p in subprocess.run(['git','-C',R,'ls-files'],capture_output=True,text=True).stdout.splitlines() if p.strip()]; print(len(ps),'tracked'); [print(p,'->',vh.classify(p)) for p in ps if vh.classify(p)]"
```

## 2 · Measured totals

```
tracked files                                821
RULE A  unsanctioned top-level FILES           4
RULE A  unsanctioned top-level DIRECTORIES     3
RULE A  unsanctioned docs/<genre>/             0
RULE B  off-grammar docs/audits/*.md          39
RULE C  homes with no hub convention          32   (297 files beneath them)
                                              --
                                              78
```

`docs/<genre>/ = 0` is worth saying out loud: corp-monorepo's `docs/` carries `archive`, `audits`,
`decisions` and `intake` — **four sanctioned genres and nothing else**. The Tier-2 genre seal is
already clean at the first consumer.

---

## 3 · THE ROOT LIST — the operator's dawn ruling input

### 3.1 Rule A — top-level FILES (4)

**`.corp-monorepo.code-workspace` → WAIVE**
Not a corp defect. `SANCTIONED_TIER1_FILES` carries the **hub literal**
`.dev-knowledge.code-workspace`; the fleet grain is the glob `*.code-workspace`
(`ecosystem/parity-surfaces.yaml` row `root-code-workspace`). This is exactly ROOT-CONTRACT v1's
reconciliation finding 3 — *"a hub-specific literal … correct for a HUB-ONLY gate and wrong as a
fleet rule"* — reproducing itself as predicted the first time the gate meets a consumer. corp's file
is fully C3/C4-conforming: dot-prefixed, `folders[0].path == "."`, and both pinned sort keys carry
the required values. **The spec must parameterize this member; the consumer must not be waived
around it forever.**

**`INSTALL.md` → WAIVE**
**The carrier itself put it there.** `deploy/manifest-v1.5.0.yaml` component `install-guide`
declares `source: plugins/tier1-lifecycle/INSTALL.md` → `path: INSTALL.md`, on the operator's
Surface-8 ruling *"INSTALL.md uniform fleet-wide, hub-owned, deploy-carried"*, and the same stanza
states the hub *"grows no root INSTALL.md of its own"* — confirmed: `INSTALL.md` is absent from the
hub root and present only at `plugins/tier1-lifecycle/INSTALL.md`. Because
`SANCTIONED_TIER1_FILES` is derived from the HUB's root, it cannot admit a file that exists only at
consumer roots. **A seal shipped as-is would refuse a file the carrier wrote.** This is the
sharpest structural finding in the report and it is a hub defect, not a corp one.

**`VISION.md` → RELOCATE → `docs/archive/VISION.md`**
The one RELOCATE, and it is proposed on the hub's **own executed precedent**, not on judgment:
ADR-114 retired `VISION` from `canonical_docs.CANONICAL_MANDATORY` into `CANONICAL_RETIRED`, and
`CANONICAL_RETIRED_LOCATIONS` records the destination the hub actually used — `docs/archive/VISION.md`
(executed by `[#614]` lane-e-5). corp-monorepo has simply not received that migration.
**Sequencing note:** it pairs with corp's missing root `README.md` (§5). The ruled order is
hub → monorepo → ai-council → win-tooling, and the manifest block for `[#614]` deliberately declares
**no carrier pair yet**, because a root README is repo-specific content and this carrier ships
verbatim hash-guarded replicas. So the relocation is ready; the replacement front door is not
carrier-deliverable and needs an authoring act.

**`tach.toml` → WAIVE** *(dot-prefix divergence, ADR-59 class)*
A genuine consumer-local tool config with no hub equivalent. Its class is the one win-tooling row
WT-4 already names — *"root `config.yaml` not dot-prefixed and not on the ADR-59 exception list"* —
so this is a **recurring fleet class, not a corp one-off**, and it deserves a spec clause rather
than two independent waivers. The alternative verdict is RELOCATE to `.tach.toml`; **I did not
verify that `tach` reads a dot-prefixed config**, and proposing a rename that might break the
consumer's own gate on an unverified assumption is not something this report will do. WAIVE with the
contingency named is the honest proposal. (corp's existing `hub-codemap-hooks` waiver already cites
*"dotted `tach.toml` keys"* as load-bearing, so the file is in use.)

### 3.2 Rule A — top-level DIRECTORIES (3)

All three carry the **same** verdict for the **same** reason, and it is a finding about the spec, not
about corp:

**`src/` (214 files) → WAIVE · `eval/` (54 files) → WAIVE · `models/` (6 files) → WAIVE**

`SANCTIONED_TIER1_DIRS` **has no source-code home at all.** The hub is a governance repo whose own
code lives in `scripts/`; corp-monorepo is a code repo with a `src/corp/` package. A seal derived
from the hub's tree necessarily refuses the single most load-bearing directory in a consumer that
holds software. `eval/` (CLI help snapshots + evaluation harness) and `models/` (trained classifier,
train/test splits, CV report) are the same class — artifact homes a code repo needs and a
governance hub never grew.

**The consequence for the spec:** either the shape spec carries a **repo-KIND axis** (governance
hub vs code repo, each with its own sanctioned set), or `src` / `tests` / and a data-artifact home
join the universal set. Waiving three directories per code repo, forever, is the outcome that
happens if neither is chosen — and it makes the seal a formality. This is stated in the intake
DRAFT as the first design fork.

Alternatives named for the operator, not recommended: `eval/` → RELOCATE under `tests/`;
`models/` → RELOCATE under `config/` or a declared data home. Both are real moves in a live code
repo and both are worse than fixing the spec.

### 3.3 Rule B — audit filename grammar (39)

Split, because the two halves have different standing:

**(a) 11 files, UPPERCASE `_TYPE_` form → WAIVE — ALREADY DECLARED, zero operator work.**
corp-monorepo's `.methodology.yaml` component `audit-casing-r4` grandfathers **exactly these 11
filenames by enumeration** (not by pattern), carried both in the waiver and as a skip-set in corp's
own `scripts/validate_audit_casing.py`. The measured 11 and the declared 11 are the same 11. This
half of Rule B is already ruled and is on a review clock (`review_date: 2026-10-12`).

**(b) 28 files, lowercase but no CLOSED-enum class token → WAIVE (recommended).**
Examples: `2026-07-05-estate-recon.md`, `2026-07-05-deep-dealloop.md`, `2026-07-18-process-audit.md`,
`2026-08-08-hybrid-classifier-duplication-disposition.md`. **corp has already recorded the reason,
and it is the right one.** The same `audit-casing-r4` waiver states that Rule B is *"NOT carried and
stays hub-local"* because *"corp audit files use free lowercase slugs … outside that enum, so
carrying it would over-block."* The measurement confirms the prediction exactly: carrying Rule B
unchanged would mark 28 existing, correctly-named, heavily-cited artifacts as violations.

The alternative is RELOCATE — 28 renames — which breaks every inbound citation to those files and
buys conformance to a **hub-local vocabulary**. `AUDIT_CLASS_ENUM`'s 11 classes
(`technical`, `functional`, `qa`, `census`, `verification`, `ecosystem-audit`,
`conformance-nightly-digest`, `changelog-review`, `codex`, `fresh-eyes`, `incident-evidence`) were
adopted, per the module's own comment, from *"what three repos already write"* — hub-adjacent
practice, never a fleet ruling. **Spec proposal:** the DATE-SHAPE and the R4 CASING legs of Rule B
are fleet clauses; the CLASS ENUM is hub-local vocabulary and ships, if at all, as a per-repo
declared enum. corp's waiver reached this conclusion first and by itself; the spec should adopt it
rather than re-litigate it.

### 3.4 Rule C — homes (32 distinct, 297 files)

```
config/extractor/ · config/extractor/prompts/ · config/extractor/templates/
config/opportunity/ · config/project/ · config/project/schemas/ · config/rfp/
config/rfp/product_profiles/_effective/ · config/rfp/product_profiles/_overrides/
config/rfp/prompts/ · docs/decisions/transcripts/ · scripts/archive/
tests/extractor/ · tests/extractor/fixtures/ · tests/integration/ · tests/opportunity/
tests/project/ · tests/rfp/ · tests/rfp/fixtures/ · tests/safety/ · tests/schema/
tests/scripts/ · tests/test_actions/ · tests/test_cleanup/ · tests/test_doctor/
tests/test_extraction/ · tests/test_extraction_non_project/ · tests/test_freshness/
tests/test_ingest/ · tests/test_ops/ · tests/test_overnight/ · tests/test_retrieve/
```

**30 of 32 (`config/*`, `tests/*`) → WAIVE. Rule C is not shippable to a consumer as written.**
`_HOME_PATTERNS`' own docstring says it is *"DERIVED FROM THE LIVE TAXONOMY"* of **this** repo, and
`test_rule_c_admits_every_tracked_path` pins it to the hub's `git ls-files`. Run against a consumer
it therefore measures *difference-from-the-hub's-tree*, which is not the same quantity as
*out-of-shape*. The hub admits bare `tests` plus `tests/fixtures`/`tests/fixtures/**` because the
hub's test tree is flat; any consumer with a real package structure nests one level further and
lights up immediately. This is a **measurement-validity finding**, and it is why the intake DRAFT
proposes that Rule C ship only with a per-repo home declaration (`.methodology.yaml`), never with
the hub's tuple.

**`scripts/archive/` (10 files) → WAIVE, with a cheap spec fix available.**
The hub already admits `protocols/archive`, `templates/archive`, `templates/claude-regions`,
`docs/decisions/archive`, `docs/intake/archive` and `tasks/archive` — `<sanctioned-parent>/archive`
is a **hub shape stated six times as six literals**. `scripts/archive/` is that same shape and is
out-of-pattern only because the tuple enumerates instead of generalizing. Proposal: make
`<sanctioned-parent>/archive` a grammar rule. It costs one pattern and removes a whole class of
false positives fleet-wide.

**`docs/decisions/transcripts/` (28 files) → WAIVE, ESCALATED as a question (not a verdict).**
This is the one item where I decline to propose a verdict with confidence. The hub **deleted its
in-hub Council transcript archive on 2026-07-22 by operator ruling** and keeps the ADR-77 guard
armed with a standing *"do not recreate it"*. Whether that ruling was hub-scoped or fleet-scoped
decides whether corp's 28 transcripts are a conforming consumer-local class (WAIVE) or a
RETIRE-PROPOSED candidate. No standing ruling covers the scope question, so per C-3(c) it is filed
as `QUESTION-lane-t-000-shape-seal.md` rather than guessed. **Recorded as WAIVE in the tally**,
because WAIVE is the verdict that changes nothing while the operator rules — and because
RETIRE-PROPOSED on 28 files based on an inferred scope extension would be exactly the failure C-8
exists to prevent.

---

## 4 · Tally

```
RELOCATE   1   VISION.md -> docs/archive/VISION.md
RETIRE     0
WAIVE     77   4 root files (-1 relocated) = 3 · 3 root dirs · 39 audit filenames · 32 homes
              -- of which 11 audit filenames are ALREADY declared in corp's .methodology.yaml
              -- of which 1 home (docs/decisions/transcripts/) is waived pending an escalated ruling
```

## 5 · What the seal CANNOT see — the absence half

The seal is **one-directional**: it refuses what is present and unsanctioned, and is silent about
what is required and missing. The operator's shape definition (inbox 023) explicitly includes
*"required docs"* and *"the handoff engine present"*, so these belong in the same ruling input:

- **No handoff engine at all.** corp-monorepo's `protocols/` holds exactly two files —
  `CORP_INTERFACE.md` and `README.md`. There is **no `protocols/HANDOFF_PROCESS.md`, no
  `docs/handoffs/` tree, and no `/handoff` command** (`.claude/commands/` carries only
  `override.md`). Against a shape definition that names the handoff engine as a member, this is the
  largest single gap at the first consumer — and the seal reports 0 for it.
- **No root `README.md`.** ADR-114's front-door migration lists corp-monorepo as the next repo after
  the hub; §3.1's `VISION.md` relocation should not land before the replacement front door exists,
  or the repo loses its purpose document to gain conformance.
- **All 6 `CANONICAL_MANDATORY` files are present** — `ARCHITECTURE.md`, `CLAUDE.md`, `BACKLOG.md`,
  `CONTRIBUTING.md`, `JOURNAL.md`, `LESSONS.md`. The required-docs leg passes.
- **One waiver has EXPIRED.** The `.vscode` entry in corp's `.methodology.yaml` carries
  `review_date: 2026-08-26`; today is 2026-09-06. It is 11 days past its own review clock and is
  owed either a renewal or a retirement.

## 6 · The finding 023's framing does not predict

Inbox 023 names today's failure mode as *"consumer roots grew junk (vision.md, install, agent.md,
loose configs, tooling links) because no shape was enforced there — each repo invented its own."*
Measured at the first consumer, **that is only a quarter true, and the quarter that is true is the
hub's doing**:

| root item | who caused it |
|---|---|
| `INSTALL.md` | **the hub** — the carrier writes it there by manifest declaration |
| `.corp-monorepo.code-workspace` | **the hub** — the gate holds a hub literal where the fleet rule is a glob |
| `VISION.md` | **the hub** — a migration the hub executed on itself and has not shipped |
| `tach.toml` | corp — a genuine local tool config, in active use |

**RETIRE = 0 is the report's result, not an omission.** Nothing at corp-monorepo's root is junk.
Two of four root files are artifacts of the hub's own carrier and gate, one is an undelivered hub
migration, and the fourth is load-bearing. The same pattern holds one level down: the three refused
directories are refused because the hub has no source-code home, and 30 of 32 refused homes are
refused because the home allowlist is a snapshot of the hub's own tree.

This does not weaken the universalization case — it **relocates** it. The work is a
**packaging/spec** problem (inbox 024's reading) far more than a **cleanup** problem (023's), and the
first consumer measured says so quantitatively: 1 item of 78 is a consumer cleanup act.

## 7 · Honest limits of this report

1. **REPORT mode is not the shipped seal.** The seal has no consumer mode and no `--report` flag;
   this run drove its rule functions from the hub. What a real carrier-shipped seal would refuse in
   `corp-monorepo` may differ once the sets are parameterized — that is the intake DRAFT's subject.
2. **Prospective vs retrospective.** `validate_hermetization` is prospective-only in production
   (staged ADDs). This run applied it **retrospectively** to 821 existing tracked files. Every
   finding above is therefore about the *existing tree*, which the live gate never inspects — the
   hole ROOT-CONTRACT v1 §C1 names by hand: *"Neither covers an already-present unsanctioned file
   inside a consumer."*
3. **Tracked files only.** `git ls-files` never sees untracked or ignored entries. corp's root
   carries `.venv`, `.pytest_cache`, `.ruff_cache`, `.hypothesis`, `data/`, `logs/`, `output/`,
   `.worktrees/` untracked-or-ignored; per ROOT-CONTRACT v1's own finding, cache dirs are noise, not
   signal, and they are correctly invisible here.
4. **`docs/audits/README.md` was NOT regenerated** by this lane (`[#590]`, dispatcher pin). The
   generated index does not yet list this file; the integrator regenerates once on the merged result.

---

**Lane:** `lane-t-000-shape-seal` · **Batch:** T wave 1 · **Substrate:** local
**Measured:** 2026-09-06 against `corp-monorepo@37b8aa1` (`main`, clean tree)
**Writes in `corp-monorepo`:** none — `git ls-files` only
