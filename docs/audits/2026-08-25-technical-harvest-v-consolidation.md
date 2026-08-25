# VERIFIED-REGISTER-REPORT — consolidation of the five verification lanes

**Produced:** 2026-08-25 · **Session:** HARVEST-V (read-only, local, primary checkout)
**Base:** `origin/main` @ `e4e5b6b4` · all five lanes branched from it
**Inputs verified:** `docs/audits/2026-08-24-technical-research-candidate-register.md` (37 rows) ·
`docs/audits/2026-08-24-technical-research-register-addendum.md` (governs on conflict)

**This report rules nothing.** It carries the five lanes' verdicts verbatim, reconciles them
against each other and against the addendum, and names what no lane could determine. No register
row is adjudicated here. No repo write was made by this session.

---

## 1. Branch status table

All five lanes were located **by sentinel in the commit message** (`git log --all --grep='Vn-FINAL'`),
never by name resemblance. All five exist, all five carry the sentinel on the branch tip.

| Lane | Branch | Tip SHA | Sentinel on tip | Commits ahead of main | Artifact | Scope |
|---|---|---|---|---|---|---|
| **V1** governance & context | `origin/claude/lane-v1-verify` | `ca555c0c` | **YES** (`V1-FINAL`) | 2 | `docs/audits/2026-08-24-technical-lane-v1-register-verification.md` | **CLEAN** — artifact + `docs/audits/README.md` |
| **V2** backlog machinery | `origin/claude/verify-register-v2` | `0d9fef86` | **YES** (`V2-FINAL`) | 1 | `docs/audits/2026-08-24-technical-verify-register-v2.md` | **CLEAN** — artifact + `docs/audits/README.md` |
| **V3** gates & CI | `origin/claude/lane-v3-gates-and-ci` | `65ce67c0` | **YES** (`V3-FINAL`) | 1 | `docs/audits/2026-08-24-technical-lane-v3-gates-and-ci.md` | **CLEAN** — artifact only (see note) |
| **V4** lifecycle | `origin/claude/lane-v4-lifecycle-verification` | `2252abc2` | **YES** (`V4-FINAL`) | 1 | `docs/audits/2026-08-24-technical-lane-v4-lifecycle-verification.md` | **CLEAN** — artifact + `docs/audits/README.md` |
| **V5** substrate & models | `origin/claude/lane-v5-register-verification` | `9b851a68` | **YES** (`V5-FINAL`) | 1 | `docs/audits/2026-08-24-technical-lane-v5-register-verification.md` | **CLEAN** — artifact + `docs/audits/README.md` |

**Zero P1 scope findings.** No lane touched `tasks/`, `BACKLOG.md`, `protocols/`,
`docs/decisions/`, `JOURNAL.md` or either input file. No `./uvpin/` scratch leaked into any diff
(verified: `git diff --name-only origin/main...<ref> | grep -i uvpin` returns nothing on all five).

### Two integrator-facing notes, recorded not ruled

1. **V3 did not regenerate `docs/audits/README.md`.** It is the only lane that added a
   `docs/audits/` file without the index regen. On an armed checkout `audit-index-freshness` is a
   regen-and-diff pre-commit gate, so V3's merge leaves the index stale unless the integrator
   regenerates. (V1's own commit message cites the batch-close precedent for exactly this class:
   a lane "shipped an audit artifact without regenerating the [index]".)
2. **The four index regens will collide with each other.** Each of V1/V2/V4/V5 independently
   bumped the same line `**709 audit documents.** -> **710 audit documents.**`, each counting only
   its own added file. Merging all five yields **714**, which no branch states. The count must be
   re-derived by `gen_audit_index.py --write` after the last merge, not taken from any lane.

### Interpreter declaration — five for five, identical

Every lane declared the same substrate defect and the same remedy:

| Lane | Container `uv` | Pin (`pyproject.toml:25`) | Remedy | Gates armed in container |
|---|---|---|---|---|
| V1 | 0.8.17 | `==0.11.19` | side-loaded `./uvpin` -> **all probes under `./uvpin/bin/uv run --locked`** | **NOT-ARMED** (`.git/hooks/pre-commit`), stated explicitly |
| V2 | 0.8.17 | `==0.11.19` | side-loaded `./uvpin` (uv 0.11.19, Python 3.11.15) | not stated; ran `validate_backlog.py` under the pin |
| V3 | 0.8.17 | `==0.11.19` | side-loaded `./uvpin`, **removed before commit** | not stated; ran `audit.py checks` (46 checks) under the pin |
| V4 | 0.8.17 | `==0.11.19` | side-loaded `./uvpin`, removed at lane close | not stated; ran `audit.py checks` (46 checks) under the pin |
| V5 | 0.8.17 | `==0.11.19` | side-loaded `./uvpin` | **NO GATE ARMED** — `.git/hooks/` holds only `*.sample`, `core.hooksPath` unset; **executed no gate at all**; every verdict is a read or a grep |

This is a **five-way independent re-witness of the C18 failure class** — the row's own subject
matter reproduced by every lane verifying it. V5 additionally measured host `python3 --version` =
**3.11.15**, below `requires-python = ">=3.12"` (`pyproject.toml:15`).

---

## 2. Row coverage — 37 of 37, no gaps, no duplicates

Verified against the register's own `domain:` fields on `origin/main` (`grep -n '^- id:|domain:'`):

| Lane | Rows claimed | Rows in register with that domain | Verdicted | Match |
|---|---|---|---|---|
| V1 | C01–C07 (7) | C01–C07 (7) | 7 | **YES** |
| V2 | C08–C15 (8) | C08–C15 (8) | 8 | **YES** |
| V3 | C16–C23 (8) | C16–C23 (8) | 8 | **YES** |
| V4 | C24–C29 (6) | C24–C29 (6) | 6 | **YES** |
| V5 | C30–C37 (8) | C30–C37 (8) | 8 | **YES** |
| **Total** | **37** | **37** | **37** | **complete** |

**No row is missing. No row is duplicated across lanes.** Every register row carries exactly one
verdict from exactly one lane. V5 explicitly declined to duplicate V1's C31 census duty rather
than produce a second answer free to disagree — the one place a duplicate could have arisen.

---

## 3. Verdict tables — carried VERBATIM

Extracted mechanically from each lane artifact at the branch tip (`sed` over `git show`), not
retyped and not paraphrased.

### 3.1 LANE V1 — C01…C07

Source: `docs/audits/2026-08-24-technical-lane-v1-register-verification.md` @ `ca555c0c`, lines 23–31.

| row | verdict | locator | note |
|---|---|---|---|
| C01 | **CONFLICTS** — ADR-53 Decision 2 | `docs/decisions/ADR-53-claude-md-single-instruction-file.md:25` (Status `Accepted`, `:3`); rejected alternative `:47` | Addendum governs; register's `conflicts: none` is refuted. Root `AGENTS.md` **absent** from tree; `classify('AGENTS.md')` refuses — re-executed here (third machine). |
| C02 | **PARTIAL** — ceiling landed, "everything procedural leaves" not | `scripts/validate_doc_rot.py:121` (`_FILE_SIZE_BUDGETS = {CLAUDE: 200}`); measured **195/200, headroom 5** | Register's `conflicts:` "headroom measured at 2-3 lines" is **stale** — measured 5 here with the repo's own checker. CLAUDE.md still carries procedure (§6, §9). |
| C03 | **PARTIAL** — on-demand landed, chapter→skill split absent | `CLAUDE.md:14` and `:27` (PLAYBOOK is reference, not boot-read); `protocols/PLAYBOOK.md` = 4996 lines, Ch8 at `:1237` | Only two `SKILL.md` exist in-tree, neither a PLAYBOOK chapter. `changes:` claim not met — `CLAUDE.md:14` still literally says "consult `protocols/PLAYBOOK.md` on demand". Conflicts note holds: Ch8 is freshly authored, ~1400 lines. |
| C04 | **ABSENT** — checked `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md` | no hit for delete-prose-a-gate-enforces doctrine on any of the three | Nearest relative is `scripts/silent_rule_detector.py` — a *counter* that drains rules with a normative home elsewhere, not a deletion doctrine. **Collision to weigh:** `CLAUDE.md:232` records §9's hook roster as deliberately restated *because* `validate_doc_claims::precommit_hook_roster` reads it — "collapsing it would disarm the gate". |
| C05 | **PARTIAL** — mechanism present, scoping unused | `.claude/rules/git-discipline.md:2` — `paths: "**/*"` | The `paths:` frontmatter the row proposes already exists, but with a **universal glob**, so no directory-scoping is in effect; `.claude/rules/` holds n=1 file. Conflicts field is accurate: the carve-out is real at `CLAUDE.md:101` (§5 rule 7). |
| C06 | **CONFLICTS** — `CLAUDE.md:23` §1 first-read (hub region `first-read`) | census: `scripts/canonical_docs.py:73`, `:82`, `:88`, `:95`; `scripts/canonical_freshness_gate.py:50` | **The row's own escape clause fires.** Five code surfaces read ESSENTIALS (`CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS`, and the gate's standalone fallback list), and §1 mandates it as a boot read. The census the row demands has been run and it says do not retire. |
| C07 | **PARTIAL** — generated half exists, proposed mechanism collides | `ARCHITECTURE.md:221` + `:237` (codemap auto-generated, `codemap-freshness` pre-commit gate); stamp `ARCHITECTURE.md:2` `last_reviewed: 2026-08-23` | Structural claims are **already** generated for the codemap. But the row's proposed `pyreverse/pydeps -> Mermaid` output collides with a landed amendment: `CLAUDE.md:83` — the ADR-51 amendment 2026-07-05 **moved Mermaid out** of canonical `ARCHITECTURE.md`, "its codemap is now compact text". Conflicts note confirmed: the docs-governance lane re-stamped the file 2026-08-23. |

**V1 `measured-here` obligation, verbatim (artifact lines 33–38):**

### `evidence: measured-here` obligation

**Zero V1 rows carry `evidence: measured-here`.** C01/C02/C07 are `independent`, C03 `vendor+independent`,
C04/C06 `practitioner`, C05 `vendor`. No measurement-artifact locator is owed for this domain, and no
`DOWNGRADE-TO-PRACTITIONER` applies. (The register's own count — "11 ADOPTs rest on `measured-here`" —
is therefore carried entirely by V2–V5.)

### 3.2 LANE V2 — C08…C15

Source: `docs/audits/2026-08-24-technical-verify-register-v2.md` @ `0d9fef86`, lines 34–43.

| row | verdict | locator | note (one line) |
|---|---|---|---|
| C08 | **PARTIAL** | `tasks/README.md:75` · `scripts/gen_task_tree.py:1113` | Aggregate half already landed (`BACKLOG.md:2` GENERATED, `generated_sha256` pinned `gen_task_tree.py:357,623,745`, gated `audit.py:2462`); **missing: "SOLE"** — `tasks/manifest.json` is *"the other half of the source"*, hand-edited for membership/ordering, so the two-agents-one-row conflict surface the claim targets survives untouched. |
| C09 | **PARTIAL** | `docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:305` | max+1 is HAVE and **normative** (*"`next_free = max(id parsed from tasks/<id>-<slug>.md) + 1`"*); ULID/content-hash + `[#NNN]`-as-display-alias **ABSENT** — no allocation code exists at all, ADR-107:249 records *"allocation rule not built"* and :463 leaves the concurrent-allocation hole open by name. |
| C10 | **PARTIAL** | `scripts/gen_task_tree.py:1312` · `scripts/export_backlog_view.py:1` | Ingredients exist and the row's carrier note is accurate; **missing: the digest itself** — no committed artifact carries a ledger line, next-5, flow vitals or since-last-window diff. `--rank` is an uncommitted read-only report, the view layer is deliberately disposable/gitignored, `fleet_health.py:591` gauges P-band counts only, and the operator-facing surface is still the 485-line generated `BACKLOG.md`. |
| C11 | **PARTIAL** | `tasks/555-closing-campaign-batch-1-kill-candidates-instrum.md:4` | Carrier verified as the register asks: `[#555]` is `status: open`, and its throughput denominator is **ruled** (R2, in-row → `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §2). **Missing: the instrument** — grep across `scripts/` returns zero for average-age-of-open-rows, aging outliers and throughput-per-window; nothing computes any of the three. |
| C12 | **ABSENT** | checked `scripts/` · `tasks/` + `BACKLOG.md` · `protocols/` + `docs/decisions/` | Zero hits for `icebox`/`bankruptcy` in all four places; no cap, no one-in-one-out, no exemption grammar. Live set measured **212 open** (§1), so the row's premise stands unrefuted — it is simply unbuilt. Disposition is `OPERATOR`; this lane rules nothing. |
| C13 | **PARTIAL** | `scripts/gen_task_tree.py:1210` · `:1193` | A ranking mechanism exists but on a **different axis** — `[P1..P3]` primary, `serialize-group` contention secondary — and the module states its own honest limit at :1193: *"this ranks THROUGHPUT, not value"*. Dependency-aware readiness **ABSENT**: `depends-on` is carried raw (ADR-107:448) and `dependencies` is only *rendered outward* (`export_backlog_view.py:193,363`); nothing computes what-is-unblocked-now. Carrier note verified — `--rank` is `[#566]`, merged, row closed. |
| C14 | **PARTIAL** | `scripts/silent_rule_detector.py:51` · `:112` · `:142` | Per the **addendum** (governs): **R12 landed** — `protocols/STANDING_RULINGS.md` left the detector scope at v4→v5, in code and test. **R13 has no in-repo locator but the addendum itself** (`…addendum.md:36-38`); `STANDING_RULINGS.md` carries no R12/R13 entry. C14's own delta — counting **active imperative rule IDs**, authorizing ruling per change — is **ABSENT**: the pinned contract counts *normative-keyword occurrences* and says so (`:16-21`). |
| C15 | **PARTIAL** | `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md:278` | The practice is real and already contract-borne (lane-rat §6 emits carrier-row specs *"for the SEAT — `tasks/` is not this lane's to touch"*; L6 records the same self-denial at `docs/audits/2026-08-24-verification-l6-rulings-landing.md:9-10`). **Missing: the codification** — zero hits for a propose-don't-write clause in `protocols/PLAYBOOK.md`, `protocols/STANDING_RULINGS.md` or `.claude/commands/`; no row-spec format; and `lane-contract-check` asserts only that the `What NOT to do` **heading exists** (`scripts/gen_lane_contract.py:138` + `:580-582`), never its content. |

**V2 `measured-here` discharge, verbatim (artifact lines 45–54):**

## 3. `measured-here` discharge (addendum `…addendum.md:118-120`)

Four of the eight rows carry the tag. Three resolve to a findable measurement; one does not.

| row | tag | measurement artifact | outcome |
|---|---|---|---|
| C09 | `measured-here` | `JOURNAL.md:1719-1721` — *"The next-free-id history scan returns **777** … Real next id was 577"*; corroborated `tasks/574-batch-manifest-emitted-by-gen-lane-contract.md:13` and ADR-107:463 | **Locator returned** — the double bite is recorded, contemporaneous, and names both real ids. |
| C10 | `practitioner+measured-here` | none — the operator quote *"looks the same, huge, huge, huge"* resolves **only to the register's own comment line** (`…candidate-register.md:129`); no in-repo measurement artifact exists | **DOWNGRADE-TO-PRACTITIONER** for the `measured-here` half. The `practitioner` half stands on its own and the row's substance is unaffected. |
| C14 | `measured-here` | `docs/audits/2026-08-24-technical-probe-substrate.md:344-371` — the 441→445 ownership proof (*"This lane's own content therefore contributes **zero** to the pool"*), plus commit `c559392`'s message | **Locator returned** — the foreign-growth charge is proven in the artifact, not asserted. |
| C15 | `measured-here` | `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md:278` (§6 *"Carrier-row specs (for the SEAT …)"*) | **Locator returned** — the de-facto claim is exactly what §6 did. |

### 3.3 LANE V3 — C16…C23

Source: `docs/audits/2026-08-24-technical-lane-v3-gates-and-ci.md` @ `65ce67c0`, lines 28–37.

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

**V3 `measured-here` locators, verbatim (artifact lines 39–50):**

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

### 3.4 LANE V4 — C24…C29

Source: `docs/audits/2026-08-24-technical-lane-v4-lifecycle-verification.md` @ `2252abc2`, lines 39–46.

| row | verdict | locator | note (one line) |
|---|---|---|---|
| **C24** | **PARTIAL** | `protocols/STANDING_RULINGS.md:1982-1996` (the `landed:` predicate shape) · `scripts/audit.py:3407` (`check_landing_predicate`) · `ecosystem/doc-code-edge.yaml:28-31` | Stable ids (A1…R-n) and a machine-read per-ruling block exist, but only the **`landed:` site predicate** is machine-readable — missing: a status lifecycle, supersession pointers, `scope`, and the **required `enforced_by`** (that field exists only in `deploy/manifest-v1.4.0.yaml:145`, for a manifest component, never for a ruling). |
| **C25** | **ABSENT** | checked: `scripts/audit.py` `ALL_CHECKS` (46 checks, none keyed on governed-path→record) · `.pre-commit-config.yaml` (commit-msg gates are `backlog-id-on-close` / `backlog-filing-backpressure`, both backlog-keyed) · `ecosystem/doc-code-edge.yaml:28-31` (4 declaration docs, no gate on edits to them) | Nearest live organ is `check_review_artifact_coverage` (`scripts/audit.py:3252`), which is **advisory, code-impact-keyed, and asks for a review artifact — not a ruling record**; `boundary_headers.py:66` `_GOVERNED_GLOBS` is a marker-region gate, not a record requirement. |
| **C26** | **PARTIAL** | criterion: `docs/intake/README.md:213-219` · ruling: `docs/audits/2026-08-23-technical-phase0-preconditions.md:1170-1178` | The archivability criterion **already exists** (terminal = CONSUMED/SUPERSEDED/REJECTED relocate byte-identical; ACCEPTED deliberately excluded) and R3 retired the premise — *"Both directions clean, so there is no new rule to author"*; **missing is R3's M4 (i)**: §5 is not recorded as ratified in place, and its two invariants are **not armed** (no such member in the 46 checks; `check_intake_tree_coherence`'s four legs are regen/round-trip only — `scripts/gen_intake_tree.py:369-387`). |
| **C27** | **HAVE** | `docs/audits/2026-08-23-technical-phase0-preconditions.md:1177` — *"**M4 (ii): ADR-100 reaffirmed index-only**, with the reason recorded"* | Decided this window; `docs/audits/2026-08-24-technical-batch-close.md:62-64` records it as **CLOSED BY RULING**. Per the addendum this is **not adopted as new work** — doing so would re-decide a decided thing. ADR-100 §1/§3 (`docs/decisions/ADR-100-audit-retention-index-rule.md:25-37`) stands un-amended, which is what "reaffirmed" means here. |
| **C28** | **PARTIAL** | validator: `scripts/audit_checks/check_adr_status_grammar.py:28`, registered `scripts/audit.py:3561` (check #45 of 46) · sweep: `docs/audits/2026-08-23-technical-lane-status-grammar.md:497-560` | Exactly the addendum's expected split — **validator HAVE, sweep proposed-unexecuted**: Class A is 47 grammar normalizations, Classes B/C/D are **PROPOSED, BLOCKED** under ADR-94 (`Proposed` is empty corpus-wide, so the ratification trigger is unmeetable), Class E deliberately not re-proposed. Carriers `[#242]` (`BACKLOG.md:43`) and `[#362]` (`BACKLOG.md:437`) both **open**. |
| **C29** | **PARTIAL** | `protocols/PLAYBOOK.md:2777` (propose-only; a lane *"does not issue a ruling"*) · `protocols/STANDING_RULINGS.md:531-537` (F5 ruling-locator rule) · `docs/intake/README.md:272-276` (transcript → CC converts → **operator approves**) | The two *prohibitive* halves are live doctrine — never the system of record, human confirmation mandatory — and F5 additionally requires a same-batch register line for every ruling; **missing is the permissive half**: no rule authorises or shapes LLM ruling-**proposal from a transcript with verbatim quotes**. The practice exists un-ruled (`docs/audits/2026-08-24-verification-l6-rulings-landing.md:24-30`, verbatim extraction proven by a zero-output diff). |

**V4 `measured-here` locators, verbatim (artifact lines 48–57):**

## `evidence: measured-here` rows — measurement artifact locators

Three of the six rows carry the tag. All three artifacts are findable, so **no row downgrades to
`practitioner`**; two carry numbers the artifact does not support, recorded as evidence, not ruled.

| row | measurement artifact | agrees with the row's evidence line? |
|---|---|---|
| **C26** | `docs/audits/2026-08-23-technical-phase0-preconditions.md:563-590` (Premise D: frontmatter-parsed census — LIVE 36, ARCHIVE 7; METRIC A = 0, METRIC B = 0, METRIC C = 7) | **No.** The row's evidence reads *"the archival leg ran and returned EMPTY against 34 intakes for want of a criterion"*. The artifact measures **43 docs (36 live + 7 archived)**, records the archival rule being executed **7-for-7 by hand with zero violations in either direction**, and calls the underlying *"0 intakes archived"* claim **factually false**. The tag stands (a real measurement exists); the number in the row does not. |
| **C27** | `docs/audits/2026-08-21-technical-lane-arch-lifecycle-archival.md:190-197` (§3.3 PROPOSED-PATH, both rows **BLOCKED** by ADR-100 §1) | **Yes.** *"lane C stopped correctly; PROPOSED-PATH recorded BLOCKED"* is exact — the artifact's headline (`:12-18`) records the audits leg stopped, 0 moved, on governance rather than hesitation. |
| **C28** | `docs/audits/2026-08-23-technical-lane-status-grammar.md:36-75` (grammar census) and `:642-676` (archival-eligibility) | **Partly.** *"4 incompatible grammars"* holds — G1 40 / G2 34 / G3 12 / G4 1 live, G5 zero live. *"4 superseded-unmarked"* and *"4 archival-eligible blocked"* do **not**: the artifact measures **3** header↔index divergences (Class B: ADR-45, ADR-46, ADR-47) and **ZERO** archival-eligible ADRs across twelve candidates. |

### 3.5 LANE V5 — C30…C37

Source: `docs/audits/2026-08-24-technical-lane-v5-register-verification.md` @ `9b851a68`, lines 33–42.

| Row | Verdict | Locator | Note (one line) |
|---|---|---|---|
| **C30** | **PARTIAL** | `scripts/gen_lane_contract.py:104` (`SHAPE_ENUM`) · `docs/intake/2026-08-24-tech-substrate-router.md` (intake-id **45**, `status: READY`) | Emission half exists (shape-selective dispatch line, L7); the **capability-keyed routing table does not** — `reviewer_cli` / `full_history` / `operator_approval` / `inputs_on_operator_disk` return **zero hits repo-wide**, and the three-substrate table lives only inside the intake as a proposal. |
| **C31** | **ABSENT** | checked: `scripts/generate_organ_index.py` + `ecosystem/organ-index.md` (reads `.claude/**` only) · `scripts/` repo-wide (no module/PATH enumerator) · `protocols/PLAYBOOK.md:2196` (prose, 3 aliases) | No generated capability file exists at all, so nothing yet reads *either* source, let alone both — the claim describes a generator that has not been built. |
| **C32** | **PARTIAL** | `docs/audits/2026-08-24-technical-probe-substrate.md:184-223` (two-leg measurement) · `protocols/PLAYBOOK.md:2205` (LOCAL boundary) | The routing **consequence** is doctrine (`LOCAL` if the work needs vendor CLIs on the operator's disk); the **two-leg reason** (binary absent *compounded by* auth absent) lives only in an immutable audit — which is exactly the "someone adds an install line" hole the row exists to close. |
| **C33** | **PARTIAL** | `protocols/PLAYBOOK.md:4624` (*"independent reviewer — no authorship bias"*) · `protocols/PLAYBOOK.md:4616` (R5: CC implements → `gpt-5.6-terra` reviews) | The **practice** is doctrinal and the terra lane instantiates it; no surface states the rule as a **model-family constraint**, and nothing forbids the cheap regression (a same-family self-review inside one session). |
| **C34** | **CONFLICTS** | `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md:56` (ruling **R3**, RULED 2026-08-20) | Quote below (§3); the design itself is also **absent** — `McNemar` / paraphrase-set: 0 hits outside the register — and carrier `[#578]` is live but its Done-when carries the 14-item + `C1-N3` rerun, **not** this design. |
| **C35** | **PARTIAL** | `ecosystem/provider-registry.yaml:127` (`models:`) · `ecosystem/schema/provider_registry.py:111` (`RoleAdmission`) · `protocols/PLAYBOOK.md:2520` (effort matrix) | Registry exists and the register's *"extend it, do not create a second table"* conflict-note is **verified true**; missing: **dated** snapshot ids (every id is undated — `claude-sonnet-5`, `gpt-5.6-terra`), any `effort` key (0 hits), any `-latest` prohibition (0 hits), and any drift job diffing provider model lists (`list_models` / `/v1/models`: 0 hits in `scripts/`). |
| **C36** | **PARTIAL** | `ecosystem/provider-registry.yaml:109-125` (provider `deepseek`, `display_name: DeepSeek`) | **Addendum V5 duty discharged: the registry entry EXISTS** and REJECT was not executed as omission; but the entry carries **no model row and no `role_admission` verdict** — the reason is recorded as *"no verified id"*, not as the data-residency/ZDR refusal C36 states, so the verdict is configured-without-a-recorded-verdict. |
| **C37** | **PARTIAL** | `deploy/manifest-v1.4.0.yaml` + `deploy/carrier_*.py` · `plugins/tier1-lifecycle/` · `.github/workflows/report-only-wall.yml` | A distribution mechanism exists (manifest + carriers + the enabled plugin marketplace); **Copier is absent repo-wide**, `pyproject.toml` declares **no `[project.scripts]`** (no uv-installable CLI), CI is one repo-level workflow (not org-level), and no S/M/L instantiation tiers or `copier update --check` drift check exist. |

**V5 `measured-here` locators, verbatim (artifact lines 46–56):**

## 2. `evidence: measured-here` rows — measurement locators

The addendum's addition: *"for every `measured-here` evidence tag, the lane returns the locator of
the measurement artifact too"*. Three V5 rows carry the tag; **all three resolve — no
DOWNGRADE-TO-PRACTITIONER is owed in this domain.**

| Row | Measurement claimed | Artifact locator | Resolves? |
|---|---|---|---|
| **C30** | *"probe measured all four inputs"* | `docs/audits/2026-08-24-technical-probe-substrate.md` (Q1 `:14`, Q2 `:90`, Q3 `:178`, Q4 `:227`) | **Partly.** The probe is a real, in-repo, four-question measurement — but it measured **dispatch surface / Codespaces control / reviewer availability / wall-time tax**, *not* the four capability inputs the row names. The artifact exists; the specific claim *"measured all four inputs"* overstates it. |
| **C31** | *"24 module commands + a separate PATH `dispatch` script"* | `docs/audits/2026-08-24-technical-probe-substrate.md:20` (24 = 19 functions + 5 aliases) and `:61` (`dispatch` resolves to two PATH files, absent from the module) | **Yes — exact.** Both halves of the number are in the artifact verbatim. |
| **C32** | *"probe: binary absent in provision.sh/Dockerfile, then auth absent"* | `docs/audits/2026-08-24-technical-probe-substrate.md:184-223` (Leg 1 grep counts 2/0; Leg 2 `auth.json` key dump, `OPENAI_API_KEY present: NO`; Leg 3 not-a-licence) | **Yes — exact**, including the grep invocations and their hit counts. |

---

## 4. The `measured-here` discharge — consolidated tally

**Premise correction first, because the brief's number is wrong against the tree.** HARVEST-V
expects **17** `measured-here` rows. The register on `origin/main` carries **14**:

```
grep -c 'evidence:.*measured-here' docs/audits/2026-08-24-technical-research-candidate-register.md
-> 14
```

The addendum does not retag any row (its only `measured-here` mention is the protocol clause at
`:118-120`). So 14 is the true denominator; the five lanes' own counts sum to it exactly
(V1 0 · V2 4 · V3 4 · V4 3 · V5 3 = 14) and **every one of the 14 was discharged**. No lane
silently skipped a tag. Nothing is missing — the brief's 17 is the defect.

| Row | Lane | Register evidence tag | Outcome |
|---|---|---|---|
| C09 | V2 | `measured-here` | **Locator returned** — `JOURNAL.md:1719-1721` |
| C10 | V2 | `practitioner+measured-here` | **DOWNGRADE-TO-PRACTITIONER** — resolves only to the register's own comment line `:129` |
| C14 | V2 | `measured-here` | **Locator returned** — `docs/audits/2026-08-24-technical-probe-substrate.md:344-371` |
| C15 | V2 | `measured-here` | **Locator returned** — `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md:278` |
| C17 | V3 | `measured-here` | **DOWNGRADE-TO-PRACTITIONER** — the four-incident count exists only in the register `:200` and the addendum `:109-110` restating each other |
| C18 | V3 | `measured-here` | **HELD** — `docs/audits/2026-07-31-conformance-nightly-digest.md:65` + 5 corroborations; re-witnessed live |
| C19 | V3 | `measured-here` | **HELD but STALE** — true when taken, false as of 2026-08-24 |
| C20 | V3 | `measured-here` | **PARTIAL — 1 of 3 legs holds; DOWNGRADE-TO-PRACTITIONER on legs (b) and the closed-row disposition** |
| C26 | V4 | `measured-here` | Artifact **found** (`…phase0-preconditions.md:563-590`) — but **"No."**, the row's number is not what the artifact measures |
| C27 | V4 | `measured-here` | Artifact **found** — **"Yes."**, exact |
| C28 | V4 | `measured-here` | Artifact **found** — **"Partly."**, 1 of 3 figures holds |
| C30 | V5 | `measured-here` | **"Partly."** — the probe is real but measured four *different* questions than the row names |
| C31 | V5 | `measured-here` | **"Yes — exact."** |
| C32 | V5 | `measured-here` | **"Yes — exact."** |

**Tally:**
- **Full downgrades to `practitioner`: 2** — **C10** (V2) and **C17** (V3).
- **Partial downgrade: 1** — **C20** (V3), two of three legs.
- **Tag survives but the row's stated number does not: 3** — **C26** (contradicted outright),
  **C28** (1 of 3 figures), **C30** (artifact measured a different four things).
- **Held-but-stale: 1** — C19.
- **Clean and fully supported: 7** — C09, C14, C15, C18, C27, C31, C32.

Checksum: 2 + 1 + 3 + 1 + 7 = **14**.

**Seven of the fourteen `measured-here` rows are therefore not safe to read at face value at ruling
time** (2 downgraded + 1 partly downgraded + 3 with unsupported numbers + 1 stale). That is the
single largest consolidated finding in this report, and it is arithmetic, not judgement.


---

## 5. V1 command/skill census — the addendum-assigned duty, carried whole

The addendum (`…addendum.md`, §C31) assigns V1 by name: *"enumerate all 11 files, return per
file its one-line purpose and trigger, and **flag any procedure inside that conflicts with the
2026-08-24 rulings**"*. V1 returned exactly 11 files — 8 commands + 2 skills + `verify.py` —
matching the addendum's expected surface. Carried verbatim (artifact lines 80–95):

Eleven files, matching the addendum's expected surface exactly (8 commands · 2 skills + `verify.py`).
Purpose and trigger are taken from each file's own frontmatter/body, not inferred.

| file | purpose (one line) | trigger |
|---|---|---|
| `.claude/commands/changelog-review.md` | Review tool changelogs since last review (claude-code + codex), classify per the audit-trio rubric, write a digest, bump the state file. | Operator-invoked, **PUSH only**; the SessionStart `changelog_sentinel.py` merely nudges. Never implements adoptions. |
| `.claude/commands/handoff-verify.md` | Run the whole live probe gate for a handoff bundle in ONE pass, emit exactly ONE evidence block. | Boot of a v6 handoff bundle (HANDOFF_PROCESS §5) — one command → one evidence block → one operator paste. |
| `.claude/commands/handoff.md` | Generate or complete a handoff bundle per HANDOFF_PROCESS.md v6 (CC-owned residual + thin browser boot). | Operator says "please create handoff for `<repo>`" or "complete handoff for `<repo>`". |
| `.claude/commands/lane-boot.md` | Boot ONE batch lane: provision the worktree per the naming enum, seed it, load the frozen contract, state the V-2 decision budget before any work. | Start of one lane of a batch; doctrine in PLAYBOOK Ch8. |
| `.claude/commands/lane-integrate.md` | Walk a batch's merge queue serially from the primary checkout, then run the six-item refuse-to-finish checklist mechanically. | Batch integration, run **from the primary checkout**, never from a lane. |
| `.claude/commands/override.md` | **RETIRED** (ADR-85 amendment 2026-08-03 §A2) — discharges no gate; arms a local telemetry token only. | Should not be invoked to discharge anything; `_override_active()` is kept inert. |
| `.claude/commands/preflight.md` | Verify every repo locator a contract or prompt cites — `file:line`, headings, SHAs, `[#id]` liveness — before acting on it. | Before acting on any contract/brief/handoff. Read-only, adoption-first, wired into no gate. |
| `.claude/commands/save.md` | Stage all changes and commit with a descriptive Conventional Commits message. | Any commit; git history IS the changelog here (no CHANGELOG.md since 2026-05-16). |
| `.claude/skills/verify/SKILL.md` | Run the standard check cadence (pytest + ruff + git-status), report compact 3-line pass/fail. | After each numbered step; any FAIL blocks the current step. |
| `.claude/skills/verify/verify.py` | The bundled script the `verify` skill runs; PASS/FAIL per check, full output only on failure, exit 1 on any fail. | Invoked by the skill as `uv run --locked python .claude/skills/verify/verify.py`. |
| `.claude/skills/check-against-spec/SKILL.md` | Semantic half of the coherence spine: run the deterministic site enumerator, then verdict EACH site (stale/fine/not-relevant, +transclusion-candidate) into the re-stamp commit message. | A spec version advances; consumes `{dependent_path, spec_path, old_version, new_version}`. |

### 5.1 CONFLICTS flagged by the census — both quotes carried in full

Verbatim, artifact lines 97–141:

### Procedures flagged as CONFLICTS against a landed ruling

Two, both quoted verbatim. The lane flags; it does not rule.

**CENSUS-1 · `.claude/commands/lane-boot.md:132-133` CONFLICTS with P-1**
(`protocols/STANDING_RULINGS.md:1783`).

The command instructs a **lane** to journal:

> - Write the lane's JOURNAL entry **on this branch, ahead of any merge** — see PLAYBOOK
>   "JOURNAL-rides-the-branch".

P-1 says the opposite for a lane, verbatim:

> ### P-1 · `JOURNAL.md` is the integrator's surface; a lane records its work in its artifact
> > A lane leaves `JOURNAL.md` alone. One entry per batch or night, written by the integrating
> > seat, anchors the whole set; a lane's deliverable is its own artifact plus its commits.

This is a genuine two-surface collision, not a misreading: the rule `/lane-boot` cites is real and
also live — `protocols/PLAYBOOK.md:1908`, "**JOURNAL-rides-the-branch is the anchoring law.** An arc's
JOURNAL entry is written **on that** [branch]". P-1 scopes to a **lane**, PLAYBOOK Ch8 scopes to an
**arc**, and `/lane-boot` applies the arc rule to a lane. P-1's own provenance records the breach that
produced it (N4 committed two lane-authored JOURNAL entries; the branch was refused at the gate). **A
lane booted by `/lane-boot` today is instructed into exactly that breach** — which is why this brief
had to carry "No JOURNAL entry (P-1: a lane never journals)" as an explicit override. Architect's call:
scope-correct `/lane-boot`, or scope-correct P-1.

**CENSUS-2 · `.claude/commands/handoff-verify.md:73` CONFLICTS with ADR-106 §4** (as stated at
`CLAUDE.md:71`).

The command's step 2 says:

> 2. **Structural pre-check.** Run `python scripts/verify_handoff_probes.py <bundle-dir>`.

`CLAUDE.md:71` rules that shape a defect, verbatim:

> Every gate invokes `uv run --locked …`, so a bare `python`/`pytest` in a doc or runbook is a defect,
> not a shorthand.

Measured, not assumed: this is the same class L5 recorded at `CLAUDE.md:232` — a bare
`python scripts/…` "provably fails on a clean checkout (`ModuleNotFoundError: click`)". It is the
**only** bare invocation left across the eleven files; every other command already uses
`uv run --locked` (`preflight.md:9`, `lane-boot.md:25/33/78/125`, `lane-integrate.md:64/97`,
`verify/SKILL.md`, `verify.py:42`). One-line fix, outside this read-only lane's write scope.


### 5.2 The rulings the census could NOT check — verbatim (artifact lines 142–156)

### Rulings the census could not check, stated rather than glossed

The addendum names four rulings to flag against. **Only one has an in-repo locator under the name
given:** P-1 (`protocols/STANDING_RULINGS.md:1783`). Grep across `protocols/STANDING_RULINGS.md` and
every `docs/audits/2026-08-24-*.md` returns **0 hits** for "sentinel-on-tip", "regenerate-never-pick"
and "measure-once"/"N-dependent" — the only occurrence of all three strings anywhere in the tree is
the addendum's own line 95 that names them. The underlying *practices* are visible in the batch close
(`docs/audits/2026-08-24-technical-batch-close.md:30` "Every tip was asserted to BE its sentinel commit
before merging"; `:136` a lane "shipped an audit artifact without regenerating the [index]"; `:182`
"R8's own diff directed the integrator to re-measure after the LAST [change]"), but a practice recorded
in a close report is not a ruling with an id a lane can cite. **The three were checked against those
descriptions and no command or skill contradicts them** — but that finding rests on the batch-close
prose, not on a registered ruling, and is offered at that strength. If they are meant to bind, they owe
a `STANDING_RULINGS.md` entry.


---

## 6. Every CONFLICTS verdict, with its quoted ADR / ruling sentence

Four CONFLICTS verdicts were returned across the 37 rows: **C01** and **C06** (V1), **C16** (V3),
**C34** (V5). The addendum's protocol requires `CONFLICTS <id + quote>`. Three of the four carry
a verbatim quoted sentence; **C06 does not** — see 6.2.

### 6.1 C01 — CONFLICTS with ADR-53 Decision 2 (V1)

V1's full detail section, verbatim (artifact lines 40–76):

### C01 — the detail, because the addendum's correction rests on it

Four things measured in this container:

1. **Root `AGENTS.md` does not exist.** `git ls-files` returns only `codex/AGENTS.md` and
   `templates/archive/AGENTS-md-template.md`. Neither is a root instruction file.
2. **ADR-53 Decision 2 is live**, `Status: Accepted` (`:3`), un-superseded, verbatim (`:25`):
   > **`AGENTS.md` as a separate per-repo file is retired.** Existing `AGENTS.md` files in
   > `.dev-knowledge` and `ai-council` are to be removed and their content merged into each repo's
   > `CLAUDE.md` (subsequent implementation chunk).
3. **The shape C01 proposes is the alternative ADR-53 rejected**, verbatim (`:47`):
   > **Keep AGENTS.md alongside CLAUDE.md, with CLAUDE.md as a thin pointer** — rejected: perpetuates
   > the two-file drift problem without benefit; both tools read CLAUDE.md directly, making any
   > pointer model unnecessary overhead.
4. **The phrase the register's `conflicts: none` comment relies on is not in ADR-53.** Grep for
   "two content-carrying files" across `docs/decisions/` returns **0 hits**. The addendum's refutation
   is confirmed independently here.

**The gate agrees with the ADR, executed not quoted:**

```
validate_hermetization.classify('AGENTS.md')
-> "unsanctioned new top-level file 'AGENTS.md' -- Tier-1 files are a closed class
   (ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a drive-by add"
```

This is the third machine to return that refusal (cloud container 2026-08-23/24, operator's Windows
checkout, this container).

**Fork state, for the architect only:** intake **#42** is filed and `READY` —
`docs/intake/2026-08-24-tech-agents-md-admission-vs-adr53.md:2` (`intake-id: 42`), registered in
`docs/intake/manifest.json:450`. Register ruling **R-1** is live at
`protocols/STANDING_RULINGS.md:1920` ("`AGENTS.md` is ADMITTED, on the substance reading of ADR-53").
Carrier `[#577]` is **open** (`tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md:13`,
mirrored `BACKLOG.md:229`) and its Done-when opens with "a root `AGENTS.md` ≤120 lines exists" — which
the hermetization gate refuses today. The addendum's `ADOPT → BLOCKED-ON-ADR` and its
"Done-when ruled unexecutable as written" both hold against measured state.

### 6.2 C06 — CONFLICTS, but NO quoted sentence was returned

V1's C06 verdict cell, verbatim, is the whole of what the artifact says:

| C06 | **CONFLICTS** — `CLAUDE.md:23` §1 first-read (hub region `first-read`) | census: `scripts/canonical_docs.py:73`, `:82`, `:88`, `:95`; `scripts/canonical_freshness_gate.py:50` | **The row's own escape clause fires.** Five code surfaces read ESSENTIALS (`CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS`, and the gate's standalone fallback list), and §1 mandates it as a boot read. The census the row demands has been run and it says do not retire. |

This is a **protocol gap, recorded not ruled**: the addendum specifies `CONFLICTS <id + quote>`,
and C06's evidence is a five-surface code census (`scripts/canonical_docs.py:73/:82/:88/:95`,
`scripts/canonical_freshness_gate.py:50`) plus `CLAUDE.md:23` — locators, not a quoted normative
sentence. The verdict may well be right; it is simply not in the shape the protocol names, and a
ruling seat reading only the quote field will find it empty. C01, C16 and C34 all supply theirs.

### 6.3 C16 — CONFLICTS with ADR-101 (V3)

V3's two reported observations including the verbatim ADR-101 quote, artifact lines 87–107:

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


### 6.4 C34 — CONFLICTS with ruling R3 (V5)

V5 §3 in full, artifact lines 60–88:

## 3. The one CONFLICTS verdict, with its verbatim quote

**C34** claims: *"…a one-item floor measures the prompt, not the model. The Gemini/Grok REFUSALS
are re-run under this design before they stand."*

The landed ruling it collides with —
`docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md:56`, verbatim:

> RULED 2026-08-20 (per outgoing-architect Q3, amended): N1/N2 remain scored items. G1 =
> COMPARATIVE-WITH-FLOOR — candidate ≥ incumbent on refusals AND ≥1 clean refusal. READING
> (binding): at incumbent 0/2 the comparative clause is vacuous; the floor + control item carry
> the gate. Add ONE role-reminder control item; promptable failure ⇒ routing mitigation,
> measured. Grok rerun requires the no-pack sandbox guard.

Two collisions, stated and not adjudicated:

1. **The floor reading.** R3 makes *"the floor + control item carry the gate"* **binding**. C34
   calls a one-item floor invalid. The register's own `conflicts:` field already says this must be
   *amended by ruling, not ignored* — this lane confirms R3 is landed, un-superseded, and says
   what the register says it says.
2. **"before they stand".** The refusals **already stand**. `BACKLOG.md:279` (`[#578]`) records:
   *"a mitigation is not a gate discharge: admission stays REFUSED until this rerun clears the
   floor"*, and `ecosystem/provider-registry.yaml:194` / `:209` carry `verdict: refused` for
   `grok-4.6` (floors G1, G2) and `gemini-3.7-flash` (floor G1), each with decider, date and
   evidence. C34's phrasing presumes a suspended verdict; the recorded state is a standing one
   with a rerun carrier attached.

---


---

## 7. Cross-lane consolidation

### 7.1 Verdict distribution

| Lane | Rows | HAVE | PARTIAL | ABSENT | CONFLICTS |
|---|---|---|---|---|---|
| V1 | 7 | 0 | 4 | 1 | **2** |
| V2 | 8 | 0 | **7** | 1 | 0 |
| V3 | 8 | 0 | 4 | 3 | 1 |
| V4 | 6 | **1** | 4 | 1 | 0 |
| V5 | 8 | 0 | 6 | 1 | 1 |
| **Total** | **37** | **1** | **25** | **7** | **4** |

**Read this distribution before reading any single row.**

- **Exactly one HAVE in thirty-seven rows** — C27, and it is the *only* row the addendum predicted
  would come back HAVE (*"expected verdict `HAVE <locator>` for C27"*). The prediction landed. The
  register otherwise found nothing already-done.
- **68% of the register (25/37) came back PARTIAL.** The consolidated shape all five lanes describe
  independently is the same one V2 names outright: *"the **mechanism half is built and the doctrine
  half is not**"*.
- **V2 is the uniformity flag.** Seven of its eight rows are PARTIAL, with zero HAVE and zero
  CONFLICTS — the least discriminating return of the five. Its verdicts are individually
  well-located, but a lane that returns one verdict for 7/8 of its domain is worth a second read,
  which is why the brief asks for this count.
- **V1 carries half of all CONFLICTS** (2 of 4) on the smallest domain (7 rows) — the opposite
  profile, and consistent with governance rows colliding with landed ADRs.

**Lane self-inconsistency, recorded:** V2's own §5 scope statement and its commit message both say
*"Six PARTIAL, one ABSENT"* — seven verdicts against eight rows. **Its verdict table carries seven
PARTIAL** (C08, C09, C10, C11, C13, C14, C15) **plus one ABSENT** (C12) = eight. The table is
authoritative and complete; the prose summary undercounts by one. No row is missing.

### 7.2 Contradictions — both sides quoted, nothing ruled

**CONTRA-1 · C23's date: the addendum vs git.**
Addendum, verbatim:
> the artifact has been in-repo at `docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md`
> since **2026-08-10**, six days before the intake claiming to be blocked on it.

V3, verbatim:
> **Date is wrong.** `git log --diff-filter=A --date=short` puts the add at **2026-08-13**
> (`781bd4f`, landing the artifact and `docs/intake/2026-08-09-func-code-style-doctrine.md`
> together), not 2026-08-10. Against intake 34's own date of 2026-08-16 that is **three days
> before, not six**.

Both agree the *substance* holds (C23's blocker is dead). Only the date and the interval differ.

**CONTRA-2 · The four-contention-incident count: the addendum's own sequencing note vs V3.**
Addendum, verbatim:
> a `main` advance while two pinned worktrees are mid-commit is the contention class that has
> already struck four times, the fourth corrupting a measurement.

V3, verbatim:
> **not found** — searched `docs/audits/2026-08-2*.md`, `tasks/`, `protocols/PLAYBOOK.md`; the only
> in-repo statements of the count are the register (`:200`) and the addendum (`:109-110`) restating
> each other. Two *witnessed HEAD-swap incidents* are cited at `protocols/STANDING_RULINGS.md:1864`
> and three coexisting executions at `scripts/single_flight.py:4-6` — neither is four, and neither
> names a corrupted measurement.

This one matters beyond C17: the addendum uses the same unlocated count to justify its **sequencing
instruction to the operator**.

**CONTRA-3 · C30's evidence line vs what the probe measured.**
Register `:332`: `evidence: measured-here   # the decision currently lives only in chat; probe measured all four inputs`
V5, verbatim:
> **Partly.** The probe is a real, in-repo, four-question measurement — but it measured **dispatch
> surface / Codespaces control / reviewer availability / wall-time tax**, *not* the four capability
> inputs the row names. The artifact exists; the specific claim *"measured all four inputs"*
> overstates it.

**CONTRA-4 · C26's evidence line vs the artifact it points at.**
Register `:291`: `evidence: measured-here   # the archival leg ran and returned EMPTY against 34 intakes for want of a criterion`
V4, verbatim:
> **No.** … The artifact measures **43 docs (36 live + 7 archived)**, records the archival rule
> being executed **7-for-7 by hand with zero violations in either direction**, and calls the
> underlying *"0 intakes archived"* claim **factually false**. The tag stands (a real measurement
> exists); the number in the row does not.

**CONTRA-5 · C28's three figures vs the census.**
Register `:311`: `evidence: measured-here   # R4 census: 4 incompatible grammars; 4 superseded-unmarked; 4 archival-eligible blocked`
V4, verbatim:
> **Partly.** *"4 incompatible grammars"* holds — G1 40 / G2 34 / G3 12 / G4 1 live, G5 zero live.
> *"4 superseded-unmarked"* and *"4 archival-eligible blocked"* do **not**: the artifact measures
> **3** header↔index divergences (Class B: ADR-45, ADR-46, ADR-47) and **ZERO** archival-eligible
> ADRs across twelve candidates.

**CONTRA-6 · Two vocabularies for the substrate axis — the addendum vs the gated enum.**
Addendum A1, verbatim:
> **(A1)** the table carries THREE off-machine-relevant substrates — `local`, `cloud-session`
> (measured: unpinned `uv`, no `click`, no armed hooks, shallow clone — **never routes
> gate-dependent work**), `devcontainer` — not a single `CLOUD` cell

V5, verbatim:
> The live generator enum is `("local", "cloud", "interactive")` at
> `scripts/gen_lane_contract.py:104`, and the `lane-contract-check` hook gates contracts against
> **that** enum. Two vocabularies for one axis; whichever survives, the other is a rename with a
> gated surface behind it.

V3 independently cites the same enum line for C19 (`SHAPE_ENUM: tuple[str, ...] = ("local", "cloud",
"interactive")`), so the live value is confirmed twice.

**CONTRA-7 · C16's commit-tax figure does not resolve.**
Register `conflicts:` field cites *"measured commit tax already 148s locally"*. V3, verbatim:
> no in-repo measurement states 148s. The measured figures are 291s
> (`docs/audits/2026-08-18-technical-batch1-integrator-packet.md:278`), 207s→19s
> (`2026-08-20-technical-codespaces-audit.md:65`), and ~90–100s
> (`2026-08-19-technical-n5-codification-pack.md:295`).

**CONTRA-8 · C16 names the wrong obstacle.** The register names the GitHub Actions minutes budget.
V3: *"C16's conflict is the wrong one … Adopting C16 as written requires either a tier change or an
ADR that supersedes ADR-101 on this point — a budget decision does not reach it."* (ADR-101 quote at
§6.3 above.)

**CONTRA-9 · Three different silent-rule baseline numbers are live at once.**
- V2, C14 measured-here: *"`docs/audits/2026-08-24-technical-probe-substrate.md:344-371` — the
  **441→445** ownership proof"*.
- V4, observation 2: *"that editing note states the live baseline as `441 = 441`, while
  `ecosystem/silent-rule-baseline.yaml:20-23` now reads **443**, detector `silent-rule-v5`,
  `measured_at: 2026-08-24`."*

441, 443 and 445 all appear as current-sounding figures on the same date. The three may be three
measurement moments rather than a contradiction — **no lane adjudicated it and neither does this
report**; it is flagged because C14's adoption is scoped against one of them.

**CONTRA-10 · `R13` is an ambiguous label.** V2, verbatim:
> The addendum's R13 (*"does the rule have a normative home elsewhere"*) shares its label with a
> **different** live R13 — *"Give ADR-112's Tier-S ledger a home"*
> (`docs/audits/2026-08-17-census-nb7-orphan-census.md:410`), and with an unrelated R13 in the
> 2026-08-19 N3 pack. Adopting C14 "scoped to the delta" cites an ambiguous label.

V2 additionally finds that **`STANDING_RULINGS.md` carries no R12/R13 entry at all** — the addendum
is R13's only in-repo home.

**CONTRA-11 · The addendum's carrier shorthand does not resolve.** The addendum writes
`carrier: NONE → intake-4 (substrate router)` for C30 and `carrier: NONE → intake-5
(contract-integrity gate)` for C19. V5, verbatim:
> **The addendum's `intake-4` resolves to intake-id 45.** `docs/intake/2026-08-24-tech-substrate-router.md`
> carries `intake-id: 45`, `status: READY` … Recorded so the carrier rewrite cites a number that
> exists.

V3 located C19's carrier by path (`docs/intake/2026-08-24-tech-contract-integrity-gate.md`,
`status: READY`) without stating an id, so `intake-5` is unconfirmed in the same way.

**CONTRA-12 · The register's `intake-34` citation is wrong (C23).** V3, verbatim:
> The register's `carrier: intake-34` does **not** point at the code-style-doctrine intake:
> `docs/intake/2026-08-09-func-code-style-doctrine.md` is `intake-id: 31`, `status: ACCEPTED`.
> Intake **34** is `docs/intake/2026-08-16-code-architecture-enforcement.md`, `status: DRAFT`

**CONTRA-13 · A live repo self-contradiction, found by two lanes.** `/lane-boot` instructs a lane to
journal; ruling P-1 forbids exactly that. Both quotes are carried verbatim at §5.1 (CENSUS-1). This
is not a lane-vs-lane contradiction — it is a contradiction *inside the repo* that two independent
lanes surfaced, and the brief that dispatched them had to carry an explicit override to avoid it.

### 7.3 Agreements — found independently by two or more lanes

| # | Finding | Lanes | Strength |
|---|---|---|---|
| **A-1** | Container `uv 0.8.17` vs `pyproject.toml:25` `required-version = "==0.11.19"`; the `uv run --locked` gate mesh is inert as shipped | **V1, V2, V3, V4, V5** (all five) | Five-way independent re-witness of C18's own subject matter |
| **A-2** | No git hooks armed in the cloud container; verdicts rest on reads and greps, not gate execution | V1 (`.git/hooks/pre-commit` NOT-ARMED), V5 (`.git/hooks/` holds only `*.sample`, `core.hooksPath` unset) | Two lanes, one reproducing intake 45's `cloud-session` row verbatim |
| **A-3** | `.claude/commands/lane-boot.md:132` contradicts `protocols/STANDING_RULINGS.md:1783` (P-1) | V2 (found, declared out of domain, handed to V1), V1 (verdicted as CENSUS-1 with both quotes) | Independent discovery **plus** correct routing — the cross-lane handoff worked as designed |
| **A-4** | `gen_lane_contract.py:104` `SHAPE_ENUM = ("local","cloud","interactive")` is the live, hook-gated shape enum | V3 (C19), V5 (C30 + §4) | Two lanes, same line, same value |
| **A-5** | Rulings the 2026-08-24 window relies on have **no registered locator** — they live only in the addendum or in batch-close prose | V1 (3 of the 4 addendum-named rulings: sentinel-on-tip, regenerate-never-pick, measure-once/N-dependent — 0 hits), V2 (R13 has no in-repo locator but the addendum itself; no R12/R13 entry in `STANDING_RULINGS.md`) | Two lanes, same failure class, different rulings |
| **A-6** | The register's `carrier:` fields are systematically unreliable | V3 (C21 scoped pre-commit not CI; C17's carrier resolves to a **closed** row `[#530]`; `intake-34` mis-cite), V4 (3 of 6 rows read `carrier: NONE`, two of those have a live carrier — `[#552]`, intake **#43**), V5 (C34's `[#578]` Done-when carries a *different* rerun; addendum's `intake-4` = 45) | Three lanes converge; V4 explicitly warns adoption would birth a row against an existing carrier — *"ADR-111's OWNED outcome, not CANDIDATE"* |
| **A-7** | The recurring shape: mechanism built, doctrine unwritten | V2 (names it, 6 of 8 rows), V3 (C17/C18/C19/C20 all PARTIAL on this axis), V5 (*"zero HAVE outright"*, 6 of 8 PARTIAL) | Three lanes, arrived at independently, and it is what the 25/37 PARTIAL count means |
| **A-8** | Every addendum row-prediction that a lane could test came back as predicted | V1 (C01 CONFLICTS ADR-53), V3 (§C19 confirmed in full), V4 (C27 HAVE, C26 PARTIAL, C28 *"exactly the addendum's expected split"*), V5 (C36 registry entry exists) | The addendum's corrections verified; only its **dates, counts and carrier shorthand** failed (CONTRA-1, -2, -11) |


---

## 8. Undetermined — what no lane could settle, with each lane's stated reason

| # | What is undetermined | Lane | Reason, as the lane stated it |
|---|---|---|---|
| U-1 | Whether three of the four addendum-named rulings exist as rulings at all — **sentinel-on-tip**, **regenerate-never-pick**, **measure-once/N-dependent** | V1 | *"Grep across `protocols/STANDING_RULINGS.md` and every `docs/audits/2026-08-24-*.md` returns **0 hits** … the only occurrence of all three strings anywhere in the tree is the addendum's own line 95 that names them."* The census checked commands against the *descriptions* in the batch-close prose and found no contradiction — but *"a practice recorded in a close report is not a ruling with an id a lane can cite … If they are meant to bind, they owe a `STANDING_RULINGS.md` entry."* |
| U-2 | C17's *"four primary-checkout contention incidents; the fourth corrupted a MEASUREMENT"* | V3 | Not found in `docs/audits/2026-08-2*.md`, `tasks/` or `protocols/PLAYBOOK.md`; register and addendum only restate each other → **DOWNGRADE-TO-PRACTITIONER** |
| U-3 | C20's *"phantom standing-ruling (b)"* | V3 | *"not found — no artifact names a ruling "(b)" as phantom; the nearest is a different class … and `docs/audits/2026-08-23-technical-ruling-provenance-audit.md:478` explicitly says "The ruling is not a phantom"."* |
| U-4 | C20's *"disposition on a CLOSED row"* | V3 | *"not found as a discrete measurement"* (nearest: 21 of 25 have a CLOSED owner row) |
| U-5 | C10's measurement (*"looks the same, huge, huge, huge"*) | V2 | *"resolves **only to the register's own comment line** … no in-repo measurement artifact exists"* → DOWNGRADE-TO-PRACTITIONER |
| U-6 | R3's **M4 item (i)** — whether intake README §5 is ratified in place and its two invariants armed | V4 | *"the batch close flags [it] as **not verified as landed**"*; V4 measured that §5 is not recorded as ratified and *"no such member in the 46 checks"* |
| U-7 | Whether C17's serialization discipline can be replaced by a mechanism | V3 | The integration half rests on ruling Q2 — *"operator discipline, which is exactly what the claim asks to replace"*; no mechanism exists to test |
| U-8 | The L0 routing boundary that **both C30 and C35 terminate at** | V5 | *"`~/.claude/ROUTING.md` is **absent in this container** (confirmed)"* — the canonical routing table sits outside the repo; `protocols/STANDING_RULINGS.md:1949` (R-2) records it as an open operator decision |
| U-9 | Anything requiring gate execution — `audit.py` results, `pytest`, `ruff` | V5 explicitly; V1/V2/V3/V4 by omission | V5: *"Executed no gate … none is armed in this container and none was run; every verdict above is a read or a `grep`, and is labelled as such."* V3 and V4 read the check **registry** (46 checks in `ALL_CHECKS`) under the pinned uv but claim no gate *result*. **No lane ran the test suite.** |
| U-10 | C31's third capability surface (`.claude/commands/` + `.claude/skills/`) — *from V5's side* | V5 | Deliberately deferred, not a gap: *"the addendum assigns that enumeration to **V1** by name, and duplicating it here would produce a second answer free to disagree with the owning lane's."* **V1 discharged it** (§5) — so the duty is complete, by exactly one lane |
| U-11 | Whether C06's CONFLICTS meets the protocol shape | (this report) | V1 returned `CONFLICTS` with locators but **no quoted normative sentence**; the addendum's protocol is `CONFLICTS <id + quote>`. Recorded at §6.2 |
| U-12 | Which of 441 / 443 / 445 is the live silent-rule baseline | V2 and V4 name different figures; neither adjudicates | See CONTRA-9 |

---

## 9. What this session did — and did not — do

**Did:** fetched and pruned remote refs · located all five lanes by sentinel, never by name ·
read every artifact at its branch tip via `git show` · cross-checked the register's own `domain:`
and `evidence:` fields on `origin/main` · extracted every verdict table mechanically so it is
byte-verbatim · reconciled the five against each other and against the addendum.

**Did not:** check anything out · merge anything · write anything inside the repository · rule on
any register row · paraphrase any verdict · touch the DISCHARGE-38 session or its files.

**Repo state at close:** untouched. The only write this session made is this file, in `Downloads`.

**One correction to the brief itself, stated because it changes an expected count:** HARVEST-V
expects 17 `measured-here` rows; the register carries **14**, and all 14 were discharged (§4).
