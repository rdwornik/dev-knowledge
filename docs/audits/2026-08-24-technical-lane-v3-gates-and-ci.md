# LANE V3 — verification of register rows, domain V3 (gates and CI)

**Lane:** V3 (read-only cloud verification lane) · **Date:** 2026-08-24
**Inputs:** `docs/audits/2026-08-24-technical-research-candidate-register.md` ·
`docs/audits/2026-08-24-technical-research-register-addendum.md` (**the addendum governs**)
**Rows owned:** every register row with `domain: V3` — **C16 · C17 · C18 · C19 · C20 · C21 · C22 · C23** (8 rows)

**This lane rules nothing.** Every verdict below is evidence for the architect's batch ruling.

## Environment declaration

The container shipped `uv 0.8.17`; `pyproject.toml:25` pins `required-version = "==0.11.19"`.
Per the brief, the pinned uv was installed side-loaded and **every** repo command in this lane ran
under it:

```
python3 -m pip install --target ./uvpin "uv==0.11.19"   # -> uv 0.11.19 (x86_64-unknown-linux-gnu)
./uvpin/bin/uv run --locked python scripts/audit.py checks
```

`./uvpin/` was removed before commit (no leftovers, CLAUDE.md §5 rule 9); `.venv/` created by
`uv sync` is gitignored (`.gitignore:11`). The 0.8.17-vs-0.11.19 gap encountered here is
**the same condition C18 cites as its measured evidence** — recorded as a live re-witness, not a
new measurement.

## Verdicts

| row | verdict | locator | note (one line) |
|---|---|---|---|
| **C16** | **CONFLICTS** — ADR-101 (`.github/` sanction decision) + `[#501]` | `docs/decisions/ADR-101-hermetization.md:219` · `.github/workflows/report-only-wall.yml:2-5` · `tasks/501-server-side-report-only-recorder-github-actions.md:13` | Required checks are ruled permanently unavailable, not merely unbuilt — see the quote below. |
| **C17** | **PARTIAL** — dispatch half HAVE, integration half ABSENT; carrier unresolvable | `scripts/single_flight.py:1-45` + `tests/test_single_flight_races.py` (have) · `protocols/STANDING_RULINGS.md:1863-1865` (discipline only) | Serialization exists for *dispatch* (`[#530]`, **closed**); nothing serializes *integration* — the primary checkout rests on ruling Q2, i.e. operator discipline, which is exactly what the claim asks to replace. |
| **C18** | **PARTIAL** — the canary mechanism exists but is scoped to consumers, not to this repo's own gates | `scripts/enforcement_coverage.py:13,41,801` (`fire_test` = clone + inject violation + observe refusal) · `scripts/audit.py:1969-1981` | The doctrine is already implemented verbatim ("static detection is a candidate PRE-FILTER, never a verdict"); missing is coverage of the 21 local pre-commit gates and of the substrate-inertness class the row cites. |
| **C19** | **PARTIAL** — premise half-refuted (addendum governs); generator live, delivery gate absent | `scripts/gen_lane_contract.py:104` (`SHAPE_ENUM`) · `.pre-commit-config.yaml:214` (`lane-contract-check`) · `docs/intake/2026-08-24-tech-contract-integrity-gate.md` (status `READY`) | Addendum §C19 confirmed on all three points: the hook is live, SHAPE_ENUM is shape-selective, and the carrier resolves to the contract-integrity intake — not `NONE`. |
| **C20** | **PARTIAL** — leg 1 partial and advisory; leg 2 (schema ban) ABSENT | `scripts/audit.py` check #42 `preflight_backlog_ids` + #31 `import_edges` (partial leg 1) · `ecosystem/disposition-register.yaml:674,686,696,709,722,733` (leg 2 refuted) | Id-liveness resolves only for `kill-candidates:` values and `@import` targets; the six volatile char-count matchers are still permitted and present — nothing forbids them by schema. |
| **C21** | **ABSENT** — gate not armed; carrier resolves | checked `.pre-commit-config.yaml` (21 ids, no lychee), `.github/workflows/` (1 file, no lychee), repo root (no `lychee.toml`/`.lycheeignore`) | Carrier id resolved (brief: do not guess) → **`[#573]`**, `tasks/573-lychee-zero-baseline-md-link-gate.md`, `status: open`, P3/S — but it scopes lychee as a **pre-commit** gate, not "in CI" as the row claims. |
| **C22** | **ABSENT** — no executable architecture contract | checked `pyproject.toml` (no `import-linter`/`tach` table), `.pre-commit-config.yaml`, `scripts/` (zero non-fixture hits) | Only `tests/fixtures/codemap-with-tach/tach.toml` exists — a fixture the codemap tool reads, not a contract this repo enforces; nearest carrier is intake **34** (`docs/intake/2026-08-16-code-architecture-enforcement.md:41`, status `DRAFT`), which names import-linter as the `[#533]` follow-on. |
| **C23** | **ABSENT** — the enforceable half ships as nothing | `pyproject.toml:182` `extend-select = []` · no `mypy` table anywhere in `pyproject.toml` · no complexity/size ceiling configured | None of B/C90/PLR/SIM/RET/ANN/FBT is selected; addendum §C23's substance is confirmed (blocker disproven) but **its date is refuted** — see below. |

## `measured-here` evidence tags — measurement-artifact locators

Per addendum §"The verification protocol stands as written": a `measured-here` claim without a
findable measurement is downgraded to `practitioner` before it reaches ruling. Four V3 rows carry
the tag.

| row | measurement claimed | artifact locator | outcome |
|---|---|---|---|
| **C17** | "four primary-checkout contention incidents; the fourth corrupted a MEASUREMENT" | **not found** — searched `docs/audits/2026-08-2*.md`, `tasks/`, `protocols/PLAYBOOK.md`; the only in-repo statements of the count are the register (`:200`) and the addendum (`:109-110`) restating each other. Two *witnessed HEAD-swap incidents* are cited at `protocols/STANDING_RULINGS.md:1864` and three coexisting executions at `scripts/single_flight.py:4-6` — neither is four, and neither names a corrupted measurement. | **DOWNGRADE-TO-PRACTITIONER** |
| **C18** | "the uv-pin mismatch made the `uv run --locked` mesh inert in cloud lanes" | `docs/audits/2026-07-31-conformance-nightly-digest.md:65` (explicit evidence line: `uv --version` → `0.8.17` vs `required-version = "==0.11.19"`), corroborated at `2026-07-29:24`, `2026-07-30:25`, `2026-08-01:34`, `2026-08-01-technical-night-batch-plan-prep.md:90`, `2026-08-02-technical-night-ladder-and-plan-audit.md:104` | **HELD** (re-witnessed live this lane) |
| **C19** | "`gen_lane_contract` is on a dead path — every contract this window was hand-authored" | `tasks/539-...md:12` records the original live verification ("**zero occurrences** in `tasks/`, `protocols/` or `scripts/`"); the *current* state refutes the premise — addendum §C19 governs and LANE-L7's rebuild is at `scripts/gen_lane_contract.py:16-18,104` | **HELD but STALE** — the measurement was true when taken, false as of 2026-08-24 |
| **C20** | "phantom standing-ruling (b); disposition on a CLOSED row; six char-count matchers" | **six char-count matchers: HELD** — `docs/audits/2026-08-23-technical-phase0-preconditions.md:1017` ("3 of 6 have already orphaned"), independently re-counted this lane at `ecosystem/disposition-register.yaml:674,686,696,709,722,733` (exactly 6). **phantom standing-ruling (b): not found** — no artifact names a ruling "(b)" as phantom; the nearest is a *different* class, `[#359]`/`[#399]` phantom **enforcement**, and `docs/audits/2026-08-23-technical-ruling-provenance-audit.md:478` explicitly says *"The ruling is not a phantom"*. **disposition on a CLOSED row: not found** as a discrete measurement (nearest: `2026-08-23-technical-phase0-preconditions.md:1008`, "21 of the 25 have a CLOSED owner row"). | **PARTIAL — 1 of 3 legs holds; DOWNGRADE-TO-PRACTITIONER on legs (b) and the closed-row disposition** |

## The two addendum corrections assigned to V3

### §C19 — confirmed in full

All three of the addendum's claims verify:

- `lane-contract-check` is a live pre-commit hook — `.pre-commit-config.yaml:214`.
- Emission is shape-selective, not unconditional — `scripts/gen_lane_contract.py:104`,
  `SHAPE_ENUM: tuple[str, ...] = ("local", "cloud", "interactive")`, with the file's own header
  (`:16-18`) recording that *"Before that lane it emitted `Dispatch-Lane` UNCONDITIONALLY"*.
- The carrier exists — `docs/intake/2026-08-24-tech-contract-integrity-gate.md`, `status: READY`.

The register's `carrier: NONE` is therefore superseded, as the addendum states.

### §C23 — substance confirmed, **date refuted by git**

The addendum writes: *"the artifact has been in-repo at
`docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md` since **2026-08-10**, six days
before the intake claiming to be blocked on it."*

- **Substance HOLDS.** The artifact is in-repo at exactly that path, and it predates intake 34.
  `docs/intake/2026-08-16-code-architecture-enforcement.md:141-146` carries the appended provenance
  reconciliation the addendum describes, and `docs/audits/2026-08-23-technical-phase0-preconditions.md`
  Q5 independently records item 1 as discharged. **C23's prior blocker is genuinely dead.**
- **Date is wrong.** `git log --diff-filter=A --date=short` puts the add at **2026-08-13**
  (`781bd4f`, landing the artifact and `docs/intake/2026-08-09-func-code-style-doctrine.md`
  together), not 2026-08-10. Against intake 34's own date of 2026-08-16 that is **three days
  before, not six**.
- **One further correction, load-bearing for the carrier.** The register's `carrier: intake-34` does
  **not** point at the code-style-doctrine intake: `docs/intake/2026-08-09-func-code-style-doctrine.md`
  is `intake-id: 31`, `status: ACCEPTED`. Intake **34** is
  `docs/intake/2026-08-16-code-architecture-enforcement.md`, `status: DRAFT` — which is the correct
  carrier for C23's config half *and* the nearest carrier for C22, since it names import-linter
  directly (`:41`).

## Two observations reported, not raised as verdicts

- **C16's `conflicts:` cites a number that does not resolve.** "measured commit tax already 148s
  locally" — no in-repo measurement states 148s. The measured figures are 291s
  (`docs/audits/2026-08-18-technical-batch1-integrator-packet.md:278`), 207s→19s
  (`2026-08-20-technical-codespaces-audit.md:65`), and ~90–100s
  (`2026-08-19-technical-n5-codification-pack.md:295`). C16's `evidence:` tag is `independent`, so
  no measurement locator is owed — recorded because the figure sits in a `conflicts:` field a
  ruling would read.
- **C16's conflict is the wrong one.** The register names the Actions-minutes budget as the
  obstacle. The actual obstacle is a ruling, quoted verbatim from
  `docs/decisions/ADR-101-hermetization.md:219`:

  > It is report-only **permanently**, not pending promotion: the repo is private on the Free tier,
  > where required checks are unavailable — no branch protection is touched and none can be.

  `.github/workflows/report-only-wall.yml:2-5` restates it (*"REPORT-ONLY FOREVER, not a gate
  awaiting promotion"*), and `tasks/501-...:13` adds that *"the ADR-at-arming has no live trigger
  until the tier changes; do not plan it early."* Adopting C16 as written requires either a tier
  change or an ADR that supersedes ADR-101 on this point — a budget decision does not reach it.

## Lane ledger

**Did:** verify 8 rows against the tree · resolve C21's carrier id · resolve the intake-34
mis-citation · execute the two V3-assigned addendum corrections · locate 2 of 4 `measured-here`
artifacts in full and 1 in part · run `audit.py checks` under the pinned uv (46 registered checks).

**Did not:** rule anything · file a row · edit `tasks/`, `BACKLOG.md`, `protocols/`,
`docs/decisions/` or either input file · journal (P-1) · merge · leave `./uvpin/` behind.
