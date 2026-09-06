---
intake-id: 73
status: DRAFT
origin: "operator definition of universalization, 2026-09-05, recorded verbatim-in-substance in ARCHITECT-INBOX-2026-09-05-023.md; drafted by lane lane-t-000-shape-seal (batch T wave 1) 2026-09-06"
note: "CANDIDATE filing attributes, carried here rather than as frontmatter keys because README section 3 declares any other key off-schema: theme E6, size L, carried-by manifest. Written against inbox 023 ONLY -- inbox 024's packaging rule and its floor v1.5.0/v1.6/v1.7 staging are CITED as an OPEN architect proposal, never adopted. Companion evidence: docs/audits/2026-09-06-technical-seal-report-corp-monorepo.md, the first measured seal report, by the same lane."
consumers: "the H0 runbook (docs/audits/2026-09-05-technical-fleet-readiness.md section 4) and the per-repo seal reports it would gain as a first step; no ADR proposed here"
---

# Shape spec + tree-seal shipped to consumers (universalization by mechanism)

## Problem / motivation

The operator's definition of universalization, given 2026-09-05: **one pattern of SHAPE for every
repo** — root contents, folder names, where docs / tasks / logs / config / tests / scripts live,
which files may sit in the root and which may not, naming grammar, the handoff engine present.
Content stays each repo's own; SHAPE is identical. Everything outside the pattern is REVIEWED and
then RELOCATED or RETIRED, with the operator's word on every removal. The test is not a metric: the
operator opens any repo and finds his way, because it is the same.

The hub already enforces that shape **on itself** and nowhere else. `validate_hermetization`'s tree
seal, `dot_prefix_discipline` and the `fleet_parity` root sweep between them say *nothing in the
root outside the pattern* — and all three are hub-scoped. Consumer roots therefore grew without a
shape to grow against.

**What has changed since 023 was written: the first consumer has been measured, and the measurement
partly contradicts 023's own diagnosis.** The companion report ran the seal against `corp-monorepo`
(821 tracked files) and found **78 out-of-pattern items — and zero of them junk**:

| root item | cause |
|---|---|
| `INSTALL.md` | **the hub** — `deploy/manifest-v1.5.0.yaml` component `install-guide` writes it to the consumer root, while the hub deliberately grows no root copy of its own |
| `.corp-monorepo.code-workspace` | **the hub** — `SANCTIONED_TIER1_FILES` holds the literal `.dev-knowledge.code-workspace` where the fleet rule is the glob `*.code-workspace` |
| `VISION.md` | **the hub** — an ADR-114 migration the hub executed on itself and has not shipped |
| `tach.toml` | the consumer — a genuine local tool config, in active use |

One level down, the three refused directories (`src/` 214 files, `eval/` 54, `models/` 6) are
refused because `SANCTIONED_TIER1_DIRS` **has no source-code home at all** — the hub is a governance
repo whose code lives in `scripts/`. And 30 of 32 refused homes are refused because `_HOME_PATTERNS`
is, by its own docstring, *"DERIVED FROM THE LIVE TAXONOMY"* of this repo.

So the itch is not that consumers are dirty. **It is that no shape has been written down
independently of the hub's own tree**, and the hub's tree is therefore standing in for a spec it was
never designed to be. Every one of those 78 items is a place where the substitute leaks. If this
stays unaddressed, the seal ships as-is, refuses a file its own carrier placed, refuses the
consumer's source tree, and gets waived into irrelevance at the first repo — which is worse than not
shipping it, because it spends the operator's ruling budget to change nothing.

## Scenarios (+1 view)

1. **The dawn ruling.** As the operator I open one report per repo, each a list of out-of-pattern
   items with a proposed RELOCATE / RETIRE / WAIVE beside each. I rule the list once. I am never
   asked to re-derive what the pattern is while ruling whether something violates it. *(This
   scenario is live today for exactly one repo and produced 78 items in one pass.)*

2. **The new repo.** As the operator I create a repo, deploy the methodology, and its shape is
   correct on day one because the shape is a shipped component, not a thing the repo invents. I do
   not later run a cleanup arc against it.

3. **The wrong-place file.** As a session I add a file to a consumer in a home that has no
   convention. The consumer's own gate refuses at commit time and names the home the class belongs
   to. Today no consumer gate exists for this: ROOT-CONTRACT v1 §C2 states the hole in its own
   words — *"a consumer's misplaced file is caught by nobody today."*

4. **The repo that is not the hub.** As the operator I open a code repo and find `src/`, `tests/`
   and a data home exactly where the shape says they go — and the seal does not flag them, because
   the shape covers code repos and not only governance hubs. *(Fails today: three WAIVEs per code
   repo, forever.)*

5. **The migration that arrives.** As the operator I execute a shape change once at the hub
   (`VISION.md` → `docs/archive/`) and every consumer receives it as a version bump, rather than each
   consumer drifting until a census finds it. *(Fails today: corp-monorepo still carries root
   `VISION.md` nine days after the hub relocated its own.)*

6. **Finding my way.** As the operator I open `corp-monorepo` looking for the handoff bundle and
   there is no `docs/handoffs/`, no `protocols/HANDOFF_PROCESS.md` and no `/handoff` command. The
   seal reports zero problems, because a seal only refuses what is present. *(This is the largest
   measured gap at the first consumer, and the current mechanism is blind to it.)*

## Functional requirements

The six legs below are the operator's definition, decomposed. Each names the surface that would
carry it and states plainly whether that surface exists.

- **Must:**
  - **M1 — Root allowlist.** The permitted root set is CLOSED; nothing is at a root by mere
    presence. **Already stated** as ROOT-CONTRACT v1 §C1 (N=8 intake amendment 2026-08-31), naming
    two surfaces at two scopes: `validate_hermetization` Rule A (hub, prospective) and
    `fleet_parity::_eval_sweep` (fleet, retrospective, top-level grain). This intake does not restate
    C1; it requires that the set become **repo-KIND-aware and consumer-runnable**, which C1
    explicitly does not claim.
  - **M2 — Folder grammar.** Where docs / tasks / logs / config / tests / scripts live, stated once
    for the fleet rather than derived from the hub's tree. The nearest existing surface is Rule C's
    `_HOME_PATTERNS`, and the measurement is that it does not survive contact with a consumer: 32
    homes refused at `corp-monorepo`, 30 of them ordinary `config/` and `tests/` nesting.
  - **M3 — Required docs.** The presence half. **Exists and works:** `canonical_docs`
    `CANONICAL_MANDATORY` (six files), read fleet-wide by `ADR38_BASELINE_REQUIRED` and
    `check_canonical_md_visibility`. `corp-monorepo` passes it. This leg needs extension, not
    invention.
  - **M4 — Naming grammar.** Dated-artifact naming, per class. The existing surface is Rule B, and
    it has **two separable legs**: the date-shape + R4 casing leg, which travelled to a consumer
    intact (corp runs it locally as `validate_audit_casing.py`), and the CLOSED 11-class
    `AUDIT_CLASS_ENUM`, which did not — adopted per its own comment from *"what three repos already
    write"*, hub-adjacent practice rather than a fleet ruling, and measured to over-block 28
    correctly-named corp artifacts.
  - **M5 — Handoff engine present.** Named by the operator as a member of the shape.
    **No surface asserts it anywhere**, at the hub or in the fleet. `corp-monorepo` has none —
    no `protocols/HANDOFF_PROCESS.md`, no `docs/handoffs/`, no `/handoff` command — and every seal
    check passes it silently, because the seal refuses presence and is blind to absence.
  - **M6 — Every consumer report is REPORT-first.** A repo's first contact with the seal is a list
    with proposed verdicts, never a refusal. Arming is a separate, later, per-repo act following the
    operator's ruling.

- **Should:**
  - **S1 — Sorting convention, filed once.** The operator's convention: **smallest first, with
    `LESSONS` / `ARCHITECTURE` at the top.** Filed here, at fleet scope, so it is not improvised per
    folder. Partly asserted already: `check_workspace_settings._WORKSPACE_REQUIRED_SETTINGS` pins
    `explorer.sortOrder: default` and `explorer.sortOrderLexicographicOptions: upper` (ADR-59
    Decision 3), and `upper` is what clusters the ALL-CAPS canonical docs above the lowercase
    configs — the *"LESSONS/ARCHITECTURE at top"* half. **The "smallest first" half is asserted by
    nothing and may not be assertable:** the only related key the hub carries,
    `explorer.sortOrderReverse: true`, is NOT in the required set (ROOT-CONTRACT v1 §C4 names this
    gap by hand), and it produces newest-first inside dated folders, which is not the same property.
    Recorded as a **declared-unasserted** clause rather than over-claimed.
  - **S2 — The shape is versioned like every other component.** A shape change is a manifest version
    bump with a drift check on both sides and a per-consumer waiver, not a per-repo act.
  - **S3 — Waivers are time-boxed and reviewed.** The mechanism exists
    (`.methodology.yaml` + `enforcement_coverage.validate_allowlist_entry`) and already shows wear:
    `corp-monorepo`'s `.vscode` entry carries `review_date: 2026-08-26` and is eleven days expired.

- **Could:**
  - **C1 — `<sanctioned-parent>/archive` as a grammar rather than six literals.** `_HOME_PATTERNS`
    spells this one shape out six times (`protocols/`, `templates/`, `docs/decisions/`,
    `docs/intake/`, `tasks/`, plus `templates/claude-regions`), and `corp-monorepo`'s
    `scripts/archive/` is out-of-pattern only because the tuple enumerates instead of generalizing.
  - **C2 — A retrospective leg.** Every gate in play is prospective-only (staged ADDs); the
    companion report had to drive the rule functions retrospectively over 821 existing files to see
    anything at all. ROOT-CONTRACT v1 §C1 names this the one hole it leaves open.

## Acceptance criteria (ex-ante)

Written as the tests that would actually be run, not as intentions.

1. **The spec resolves without reading the hub's tree.** Someone given only the shape spec can say
   whether an arbitrary path in an arbitrary repo is in-pattern. Concretely: it answers `src/`,
   `tests/rfp/fixtures/`, `INSTALL.md` and `.corp-monorepo.code-workspace` — the four classes that
   produced 71 of the 78 measured items — without consulting `.dev-knowledge`.
2. **The carrier and the seal agree.** For every component the manifest writes to a consumer root,
   the shape spec admits that path. Test: the set of `path:` values at consumer depth 0 across
   `deploy/manifest-v*.yaml` is a subset of the admitted root set. **This FAILS today** on
   `install-guide` and is the cleanest single regression test the spec buys.
3. **A REPORT run on any consumer emits a per-item verdict list**, and re-running it changes nothing
   in that consumer — verified by a clean `git status --porcelain` before and after.
4. **The absence half reports.** A repo with no handoff engine is named as such by the report,
   rather than passing silently. Test: `corp-monorepo` today yields at least one M5 finding.
5. **Every WAIVE is time-boxed.** No item leaves a report as a permanent waiver without a
   `review_date`, and an expired one surfaces.
6. **The 78 items resolve into a stable number.** Re-run against `corp-monorepo` after the spec
   lands: the count moves because the SPEC changed (repo-kind axis, parameterized workspace member,
   carrier-written roots admitted), not because the consumer was edited. The consumer-cleanup
   residue should be small — the measurement says **1 of 78** today.

## Non-goals

- **Arming anything.** Not this intake, not the companion report. Every seal named here is
  report-mode; arming is a separate per-repo act after the operator rules that repo's list.
- **Building a new checker.** The hub mechanisms are inventoried above and the companion report ran
  entirely on them. A second implementation of the tree seal is the failure mode this intake exists
  to avoid.
- **Adopting inbox 024's staging.** 024's packaging rule and its floor v1.5.0 / v1.6 / v1.7 ladder
  are **cited as an OPEN architect proposal awaiting the operator's ruling**, not adopted here. The
  measurement independently supports 024's *direction* — 77 of 78 items are packaging, not cleanup —
  and that is a corroboration, not an adoption.
- **Sameness of content.** Shape is identical; content stays each repo's own. This corrects the
  architect's earlier *"floor conformance, not sameness"* note in
  `ARCHITECT-INBOX-2026-09-05-009.md`, per 023.
- **Deleting anything.** The verb is RETIRE-PROPOSED and the operator's word comes at dawn (C-8).
  The first measured report proposed **zero** retirements.
- **Opening the deploy gate.** The 2026-08-29 standing constraint — *no further consumer deploys
  beyond the landed floor until it is ruled* — is untouched by this filing, exactly as ROOT-CONTRACT
  v1 was careful to say of itself.

## Impact sketch (4+1 lite)

- **Logical:** one SHAPE SPEC becomes the authority; the hub's own tree stops being the implicit
  spec. Today's sanctioned sets are re-read as *the hub's instance of the spec*, which is the frame
  ROOT-CONTRACT v1 already used for its own measurement.
- **Process:** scale is **1 spec + N reports + N rulings + N execution lanes**. The operator's cost
  is N rulings, once, on lists someone else measured. The first ruling list exists.
- **Development:** the parameterization sites are known and few — `SANCTIONED_TIER1_DIRS`,
  `SANCTIONED_TIER1_FILES`, `_HOME_PATTERNS`, `AUDIT_CLASS_ENUM` — plus a consumer entry point,
  since the module has no CLI beyond `main()`'s staged-adds path. No new organ.
- **Physical:** the seal runs where the consumer's tree is readable. The fleet-readiness audit
  established this is **LOCAL** (B1.2: the deploy tool resolves consumers as `hub_root.parent/repo`,
  which no cloud substrate satisfies), so report generation is a local-substrate act.

## Open questions

Recorded rather than answered — the ADR-98 genre bars solutioning, and each of these is a design
fork whose answer changes the shape of the work.

1. **Repo-KIND axis, or one universal set?** Does the spec carry per-kind sanctioned sets
   (governance hub vs code repo vs satellite), or does it widen the universal set to include `src/`
   and a data home? The measurement forces the question — three WAIVEs per code repo forever is the
   outcome if neither is chosen — but it does not answer it. **The largest fork here.**
2. **What admits a carrier-written root file?** `INSTALL.md` is at consumer roots because the
   manifest puts it there. Does the shape spec derive the admitted root set partly *from* the
   manifest, or is the manifest constrained by an independently-stated spec? These give different
   answers when the two disagree, and today they do.
3. **Is the audit CLASS ENUM fleet vocabulary or hub vocabulary?** corp's own `.methodology.yaml`
   already ruled it hub-local for itself and the measurement vindicated that. Does the spec ratify
   that split (date-shape + casing fleet-wide, class enum per-repo), or is a fleet enum the goal?
4. **Was the 2026-07-22 transcript-archive deletion hub-scoped or fleet-scoped?** It decides WAIVE
   vs RETIRE-PROPOSED on `corp-monorepo`'s `docs/decisions/transcripts/` (28 files), and it is the
   first instance of a general class: *a hub ruling that removed something from the hub, met in a
   consumer that still has it.* Escalated separately as
   `to-browser/QUESTION-lane-t-000-shape-seal.md` (C-3 class (c) — no standing ruling).
5. **How is M5 (handoff engine present) asserted?** Presence of `protocols/HANDOFF_PROCESS.md` and
   `docs/handoffs/`? Or a working `/handoff` that produces a valid bundle? These differ by an order
   of magnitude in cost, and a presence check that passes on an inert engine is the
   `CS-3 + CS-4` failure the fleet-readiness audit already named — *a hash-clean floor is not a
   working floor.*
6. **Can "smallest first" be asserted at all?** VS Code's `explorer.sortOrder` enum has no size
   member; `sortOrderReverse` gives newest-first inside dated folders, which is a different
   property. If it cannot be asserted, does the convention stay a declared-unasserted clause, or
   leave the spec?
7. **What is the retrospective leg?** Every gate here is prospective-only, so an already-present
   misplaced file in a consumer is caught by nobody. Is the answer a periodic report (cheap, no new
   gate) or a retrospective check (expensive, and every consumer starts RED)?
8. **`config/` fate is still unruled**, and it blocks part of M2 — see the reconciliation note
   below.

## Reconciliation against what has already landed

Required by the lane contract, and recorded so this filing is read as an extension rather than a
competitor.

**ROOT-CONTRACT v1 (N=8 intake `2026-08-17-tech-fleet-config-standardization.md`, ACCEPTED,
amendment 2026-08-31) already states C1–C4** — permitted set, relocation, workspace declaration,
ordering. **This intake does not restate them.** M1 and S1 above cite C1 and C3/C4 as the standing
statement and add only what the measurement showed is missing: repo-kind awareness, a
consumer-runnable mode, and the absence half. That amendment also predicted, in its reconciliation
finding 3, that *"the hub-only-gate-versus-fleet-rule seam … will recur"* — the
`.corp-monorepo.code-workspace` item is its first recurrence, and it recurred on the first consumer
measured.

**The ACCEPTED N=8 intake — `docs/intake/2026-08-17-tech-fleet-config-standardization.md` — is the
parent filing**, and its R18 conformance scorecard is PARKED on tested conditions. Nothing here un-parks it; the per-repo REPORT is a different
instrument from a fleet scorecard, and the N=8 amendment says so itself: *"the fleet answer is R18's
scorecard and not a command pasted into a document."*

**Fleet-readiness §2's floor-diff tables are cited as the first measured OUT-OF-PATTERN list**, per
023's filing instruction. Their grain is components and hooks (`CM-1…CM-10`, `AC-*`, `WT-*`,
`CO-*`, `CS-*`), which is a different axis from tree shape — the two are complements, not
duplicates. §4's H0 runbook currently begins with an operator ruling (Step 0) and a freshness
re-stamp (Step 1); 023 asks that the seal report come **first**, and the companion report is that
proposed new first step. **It is a proposal against §4, not an edit of it** — §4 is an immutable
landed audit.

**The ROOT-R1 census does not exist in the tree.** The lane contract asked for reconciliation
against it; a full-repo sweep finds four mentions and no artifact, every one of them describing it
as dispatched-and-unlanded (`protocols/HANDOFF_PROCESS.md`: *"blocker: ROOT-R1 unlanded"*; the
2026-09-01 architect bundle: *"ROOT-R1 `config/` verdict — FILL vs DISSOLVE into `pyproject`; census
dispatched, **unruled**"*). Reconciliation is therefore performed against **ROOT-CONTRACT v1**, which
is the census's landed downstream statement, and the gap is recorded rather than papered over. Its
live consequence for this filing is open question 8: M2's folder grammar cannot state `config/`'s
role while `config/`'s own fate is unruled — and `config/` subtrees are 10 of the 32 measured
out-of-pattern homes.

**Inbox 024** is cited as an OPEN proposal in two places (Non-goals; Problem/motivation) and adopted
in none.

## Hub mechanisms this reuses, inventoried BEFORE any new one

The lane contract's closure clause requires this list, and it is also the library-first check
(C-11). Every mechanism below already exists and was exercised by the companion report.

```
validate_hermetization.py       Rule A top-level seal (SANCTIONED_TIER1_DIRS / _FILES / SANCTIONED_GENRES)
                                Rule B audit-name grammar (date shape + R4 casing + AUDIT_CLASS_ENUM)
                                Rule C home allowlist (_HOME_PATTERNS)
canonical_docs.py               CANONICAL_MANDATORY (required-docs leg, already fleet-wide)
                                CANONICAL_RETIRED + CANONICAL_RETIRED_LOCATIONS (the VISION.md relocation target)
audit_checks/                   dot_prefix_discipline (ADR-59 root config rule)
                                check_workspace_settings (_WORKSPACE_REQUIRED_SETTINGS -- S1's asserted half)
                                check_canonical_md_visibility / adr38_baseline (M3's presence leg)
fleet_parity.py                 _eval_sweep root sweep (the fleet-scope, retrospective, top-level leg)
enforcement_coverage.py         .methodology.yaml waiver read + validate_allowlist_entry (S3's time-box leg)
deploy/manifest-v*.yaml         the component/version/carrier vehicle S2 would use
```

**No new mechanism is proposed by this filing.** What it proposes is that four existing constants
stop being hub-tree snapshots and become spec-derived, and that a consumer entry point exist. Where
a leg has no surface at all — M5's handoff-engine presence, S1's "smallest first" — that is stated
as a gap above rather than closed here, because closing it is a build act and this is an intake.

## Status

**DRAFT** — a CANDIDATE for intake triage per ADR-111; no BACKLOG row is born here. Filing
attributes: theme E6, size L, `carried-by: manifest` (carried in `note:` above, as
`docs/intake/README.md` §3 declares any non-schema frontmatter key off-schema). Companion evidence
landed in the same batch: `docs/audits/2026-09-06-technical-seal-report-corp-monorepo.md`.

**On the id.** `intake-id: 73` was computed at write time by scanning every distinct
`docs/intake/` blob reachable from any ref (269 blobs, 72 ids allocated, max 72, no gaps below it)
rather than taken from the folder listing — because the folder listing under-reports. **Three ids
are double-allocated in history** and the newest is nine days old:

```
14  2026-07-12-siem-requirements-ruled-pack.md / 2026-07-13-siem-fleet-management-requirements{,-codex}.md
42  2026-08-23-tech-generated-artifact-currency.md / 2026-08-24-tech-agents-md-admission-vs-adr53.md
70  2026-09-05-tech-aj-second-pass.md / 2026-09-05-tech-session-roles-with-a-carrier.md
```

`README.md` §3 calls `intake-id` *"the join key the accepting ADR and the resulting epic(s) cite
back"*, so a duplicated id makes a bare `#N` citation ambiguous rather than merely untidy — cite
intake docs **by path**. Recorded as an observation, not a filing: no id is renumbered here (§3
forbids it), and closing this is not in this lane's footprint.
