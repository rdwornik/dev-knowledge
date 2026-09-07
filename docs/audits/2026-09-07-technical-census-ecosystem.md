# Census — `ecosystem/` (SWEEP 2026-09-07, lane S-08, READ-ONLY)

> **Lane S-08 of the 2026-09-07 SWEEP.** Folder under census: `ecosystem/`. **Nothing in this
> lane was moved, deleted, edited or renamed.** Every verdict below is a **PROPOSAL** the
> operator rules; every one carries a witness, and where a witness could not be established
> the row says `UNDETERMINED` and `## Honest limits` says what was missing.
>
> **Consumed by:** intake **#73** — the shape-spec / tree-seal arc, whose D6 clause is the
> subject of §3 below (`docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`) ·
> `[#171]` the conformance-dashboard row, OPEN (`tasks/171-build-the-conformance-dashboard-at-ecosystem-con.md`) ·
> `[#477]` the deployed-version keying row, OPEN (`tasks/477-deployed-version-check-keys-registry-by-basename.md`) ·
> **ADR-101** the hermetization tree-seal (`docs/decisions/ADR-101-hermetization.md`) ·
> **ADR-86** the dashboard-location decision (`docs/decisions/ADR-86-conformance-dashboard-location.md`).
>
> **Fan-out: NONE.** `gemini` is **not on PATH** in this container (`command -v gemini` →
> absent). Gemini-read files: **0**. Fabricated locators counted: **0** — a count of zero here
> means *no fan-out ran*, not *a clean fan-out ran*. Copilot Enterprise offload was **not
> used and was not available**: intake **#75**
> (`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`) is `status: DRAFT`,
> unratified, verified by reading its frontmatter. Every locator in this file was opened by
> this lane directly.

## Scope and method

`git ls-files ecosystem` returns **106 tracked files**, and `find ecosystem -type f` returns
the same 106 — **no untracked and no ignored file exists in the tree today**
(`git status --porcelain --ignored ecosystem` is empty). The tree therefore has no hidden
half. `ecosystem/*/state.yaml` is gitignored (`.gitignore:78`, confirmed with
`git check-ignore -v ecosystem/ai-council/state.yaml`) and **none is present**;
`ecosystem/trends.html` is gitignored (`.gitignore:93`) and **absent**.

Of the 106, **100 are dated fleet-audit snapshots** under `ecosystem/<repo>/history/`, written
by one generator, read by one consumer set, and governed by one rule. They are inventoried as
**six directory rows** rather than 100 near-identical file rows — collapsing them is a
reporting decision, stated here so it is not mistaken for an omission; the per-directory counts
and date ranges are exact. The remaining **27 files** each get their own row.

Every command in this lane was read-only. `uv run --locked` **could not be used** — see
`## Honest limits`.

## Inventory

`Gen` column: **G** = machine-generated (a named generator owns the bytes) · **H** =
hand-authored · **D** = declared data, hand-authored but machine-read as a contract ·
**M** = measured baseline, written only by an explicit `--write-baseline`.

| # | File | Gen | Generator / author (witness) | Consumers (witness: `grep`) | Freshness (witness) | Verdict |
|---|---|---|---|---|---|---|
| 1 | `audit-consumer-baseline.json` | M | `consumer_at_landing.py --write-baseline` (`scripts/consumer_at_landing.py:98` `BASELINE_RELPATH`) | `scripts/consumer_at_landing.py`, `scripts/audit_checks/check_consumer_at_landing.py`, `scripts/gen_audit_index.py` | in-file `measured_at: 2026-09-01` @ `9644e815`; ratchet, not a currency artifact | KEEP |
| 2 | `audit-funnel-baseline.json` | M | `funnel_coverage.py --write-baseline` (`scripts/funnel_coverage.py:141`) | `scripts/funnel_coverage.py`, `scripts/audit.py`, `scripts/gen_trend_dashboard.py:551`, `tests/test_consumer_at_landing.py` | in-file `measured_at: 2026-09-01` @ `13fb1538` | KEEP |
| 3 | `audit-title-baseline.json` | M | `gen_audit_index.title_less` (in-file `detector` key) | `.pre-commit-config.yaml` (`audit-title-gate`), `scripts/gen_audit_index.py`, `tests/test_gen_audit_index.py` | 20 grandfathered names — matches `CLAUDE.md` §9's "ratchet, 20 grandfathered" exactly | KEEP |
| 4 | `conformance.md` | G | `scripts/gen_dashboard.py:77` `MD_RELPATH` | `scripts/generated_artifact_freshness.py:148`, `scripts/gen_trend_dashboard.py`, `ARCHITECTURE.md`, `protocols/HANDOFF_PROCESS.md`, `tests/test_gen_dashboard.py` | **CONTENT-STALE** — `gen_dashboard.py --check` exits 1; regen-and-diff = **32 changed lines** (§3) | RELOCATE → `docs/dashboard/` (§3) |
| 5 | `conformance.html` | G | `scripts/gen_dashboard.py:79` `HTML_RELPATH` | same as row 4; `ARCHITECTURE.md`, `protocols/STANDING_RULINGS.md`, `tests/test_generated_artifact_freshness.py` | **CONTENT-STALE** — same `--check`; html regen-and-diff = **24 changed lines** | RELOCATE → `docs/dashboard/` (§3) |
| 6 | `dependency-baseline.yaml` | D | hand-authored (`# Hub-recommended dependency baseline -- the #332 / FR-7 …`) | `scripts/fleet_parity.py`, `scripts/gen_handoff.py`, `pyproject.toml`, `ARCHITECTURE.md` | in-file `version: 1.0.0`; last-content date UNDETERMINED (graft, see limits) | KEEP |
| 7 | `deployed-versions.yaml` | D | written by the deploy runbook (`deploy/tool.py`; header: *"NOT the derived index.yaml"*) | `deploy/tool.py`, `scripts/fleet_parity.py`, `scripts/desired_state_loader.py`, `scripts/audit.py`, `tests/test_deploy_tool_execute.py` | 9 repo keys; 2 carry a version (`ai-council` 1.3.1, `corp-monorepo` 1.2.0), 7 `null` | KEEP — **read-only this lane** (§7 footprint) |
| 8 | `disposition-register.yaml` | D | hand-authored, one entry per dispositioned WARN | `scripts/audit.py`, `scripts/fleet_health.py`, `scripts/validate_landing_predicate.py`, `scripts/gen_handoff.py`, `tests/test_ship_gate.py` | last content commit `c4fdc4e` **2026-09-06** (post-graft, reliable) | KEEP |
| 9 | `doc-code-edge.yaml` | D | hand-authored (`# Doc->code edge declaration-doc registry -- #194 Phase-2`) | `scripts/validate_doc_code_edge.py`, `scripts/file_purpose_graph.py:198`, `scripts/audit.py`, `tests/test_doc_code_edge.py` | date UNDETERMINED (graft) | KEEP |
| 10 | `doc-counts.md` | G | `scripts/gen_doc_counts.py --write` (in-file `COUNTS:START` marker) | `.pre-commit-config.yaml` (`doc-counts-pytest-freshness`), `CLAUDE.md` §4, `scripts/audit.py`, `templates/handoff/v5/PROBES.md.tmpl` | last content commit `a49537c` **2026-09-07** (today). Its `pre-commit gates (23)` claim **re-verified live**: `.pre-commit-config.yaml` holds exactly 23 `- id:` entries | KEEP |
| 11 | `fleet-shape-spec.yaml` | D | hand-authored contract data | `scripts/validate_hermetization.py` (`SANCTIONED_GENRES`, `AUDIT_CLASS_ENUM`, `_HOME_PATTERNS` all read it), `tests/test_fleet_shape_spec.py` | last content commit `01104de` **2026-09-07** (today) — *"the fleet shape grammar becomes DATA the tree seal reads"* | KEEP |
| 12 | `index.yaml` | G | `scripts/audit.py::regenerate_index` — *"overwrites it WHOLESALE each run"* (`scripts/audit.py:5854`, quoted in `deployed-versions.yaml`'s own header) | `scripts/audit.py`, `scripts/desired_state_loader.py`, `scripts/fleet_analytics.py`, `scripts/window_metrics.py`, `scripts/probe_child_backlogs.py`, `ARCHITECTURE.md` | **STALE — 33 days.** In-file `generated: '2026-08-05T10:36:01'`, and its content is now factually wrong (§4) | KEEP — regenerate, do not relocate |
| 13 | `north-star.md` | G | `scripts/gen_north_star.py:36` `OUT_RELPATH` | `README.md`, `scripts/gen_north_star.py`, `protocols/STANDING_RULINGS.md`, `docs/handoffs/2026-08-31-dev-knowledge-architect/HANDOFF_BOOT.md`, `tasks/385`, `tasks/386` | **CONTENT-STALE** — `gen_north_star.py --check` exits 1; real count drift, not a HEAD pin (§3) | KEEP — home is `ecosystem/`, confirmed (§3) |
| 14 | `organ-index.md` | G | `scripts/generate_organ_index.py --write` (in-file `generated by` marker, line 26) | `.pre-commit-config.yaml` (`organ-index-freshness`), `CLAUDE.md` §4, `ARCHITECTURE.md`, `protocols/STANDING_RULINGS.md`, `scripts/block_ff_push.py` | **CURRENT** — `generate_organ_index.py --check` exits **0** | KEEP |
| 15 | `organ-registry.yaml` | D | hand-authored — the DECLARED half of `[#132]` (in-file header) | `scripts/generate_organ_index.py`, `tests/test_generate_organ_index.py`, `protocols/STANDING_RULINGS.md` | `version: "1.0.0"`; date UNDETERMINED (graft) | KEEP |
| 16 | `parity-surfaces.yaml` | D | hand-authored — the `#328` versioned parity contract | `scripts/fleet_parity.py`, `scripts/silent_rule_detector.py`, `scripts/funnel_coverage.py`, `deploy/manifest-v1.4.0.yaml`, `deploy/manifest-v1.5.0.yaml`, `.methodology.yaml` | in-file `version: 1.5.0` — agrees with the live manifest `deploy/manifest-v1.5.0.yaml` | KEEP |
| 17 | `proof-layer-baseline.json` | M | `proof_layer.py --write-baseline` (`scripts/proof_layer.py:107`) | `scripts/proof_layer.py`, `scripts/audit_checks/check_proof_layer.py` | in-file `measured_at: 2026-08-27` @ `2d531321`, `guard_count: 243` | KEEP |
| 18 | `provider-registry.yaml` | D | hand-authored; schema-validated by `ecosystem/schema/provider_registry.py` | `.pre-commit-config.yaml` (`provider-registry-agreement`), `scripts/check_provider_registry.py`, `scripts/provider_registry.py`, `scripts/gen_trend_dashboard.py:941`, `CLAUDE.md` §9, `.dev-knowledge.code-workspace` | no in-file stamp; **9 provider/model seams** asserted by a live pre-commit gate | KEEP |
| 19 | `registry.md` | H | **hand-maintained human registry** (own header: *"Hand-maintained human registry"*, census ruling C-10) | `scripts/fleet_analytics.py`, `scripts/desired_state_loader.py`, `scripts/audit.py`, `tests/test_membership_agreement.py`, `templates/README-md-template.md`, `protocols/REPO_ONBOARDING.md` | 9 rows vs 6 `ecosystem/<repo>/` dirs vs 6 `index.yaml` entries vs 9 `deployed-versions.yaml` keys — the gap is **by design** (3 rows are `registered · unonboarded`), verified row-by-row (§4) | KEEP |
| 20 | `routing-table.yaml` | D | hand-authored — the AUTHORITATIVE role→CLI table; residency ruled in-repo by register ruling Z-G3/A2 (in-file header) | `scripts/routing_agreement.py:53`, `scripts/audit_checks/check_routing_agreement.py`, `scripts/preflight_contract.py`, `tests/test_routing_agreement.py`, `protocols/STANDING_RULINGS.md` | `version: 1`; open row `[#627]` (verified `status: open`) reports the `agy` route INERT | KEEP |
| 21 | `satellite-onboarding-rulings.yaml` | D | hand-authored — operator-ruled machine truth (in-file header) | `scripts/validate_onboarding_rulings.py`, `scripts/desired_state_loader.py`, `scripts/check_provider_registry.py`, `scripts/audit.py`, `tests/test_onboarding_rulings.py` | `version: 1`, carries `census_ref` back to its source census | KEEP |
| 22 | `silent-rule-baseline.yaml` | M | `silent_rule_detector.py` (`scripts/silent_rule_detector.py:119`); may be lowered, **never raised** | `scripts/silent_rule_detector.py`, `scripts/audit.py` (`check_silent_rule_ratchet`), `scripts/funnel_coverage.py`, `protocols/STANDING_RULINGS.md` | in-file `measured_at: 2026-09-06` @ `eeac6bef`; last content commit `30c6e58` **2026-09-06** (post-graft) | KEEP |
| 23 | `substrate-registry.yaml` | D | hand-authored — `[#591]`; home argued in-file (*"alongside provider-registry.yaml and tool-versions.yaml"*) | `scripts/validate_substrate.py:103`, `scripts/gen_lane_contract.py`, `tests/test_gen_lane_contract.py`, `protocols/PLAYBOOK.md` | no stamp; date UNDETERMINED (graft) | KEEP |
| 24 | `tool-versions.yaml` | D | written by `/changelog-review` after a real review (in-file header, ADR-80 durable record) | `scripts/changelog_sentinel.py`, `scripts/check_provider_registry.py`, `scripts/provider_registry.py`, `tests/test_provider_registry_schema.py`, `protocols/PLAYBOOK.md`, `ARCHITECTURE.md` | declares last-reviewed `claude-code 2.1.204`, `codex 0.143.0`; currency vs upstream **not measurable here** (no changelog fetch in a read-only lane) | KEEP |
| 25 | `schema/__init__.py` | H | hand-authored package init; directory authorized by ADR-109 §8 (F2) | `scripts/audit.py`, `scripts/fleet_analytics.py`, `scripts/worktree_seed.py`, `scripts/worktree_import_proof.py`, `pyproject.toml`, `tests/test_worktree_seed.py` | re-exports both models; import **not exercisable here** (`pydantic` absent) | KEEP |
| 26 | `schema/desired_state.py` | H | hand-authored pydantic contract — ADR-109 v1, `[#382]` W2 | `scripts/audit.py`, `tests/test_review_artifact_coverage.py`, `ARCHITECTURE.md` | `pydantic` absent in this container → import UNVERIFIED (see limits) | KEEP |
| 27 | `schema/provider_registry.py` | H | hand-authored pydantic contract — LANE L1, 2026-08-23 | `scripts/provider_registry.py`, `scripts/check_provider_registry.py`, `scripts/validate_hermetization.py`, `.pre-commit-config.yaml`, `tests/test_provider_registry_schema.py` | same limit as row 26 | KEEP |
| 28 | `.dev-knowledge/history/` — **17 files** | G | `scripts/audit.py::append_history` (`scripts/audit.py:596`, path built at `:537`) | `scripts/gen_trend_dashboard.py:600` (the ONLY doc-rot trend source), `scripts/window_metrics.py:195`, `scripts/session_end_backpressure.py:405`, `scripts/scan_undeclared_edges.py:99` | `2026-05-15` → **`2026-07-31`**; **38 days with no new snapshot** (§5) | KEEP (append-only, ADR-80) |
| 29 | `ai-council/history/` — **17 files** | G | same generator | same consumer set | `2026-05-15` → **`2026-07-31`** | KEEP |
| 30 | `corp-monorepo/history/` — **15 files** | G | same generator | same consumer set | `2026-05-23` → **`2026-07-31`** | KEEP |
| 31 | `corp-ops/history/` — **14 files** | G | same generator | same consumer set | `2026-06-02` → **`2026-07-31`** | KEEP |
| 32 | `corp-sca-time-automation/history/` — **14 files** | G | same generator | same consumer set | `2026-06-02` → **`2026-07-31`** | KEEP |
| 33 | `win-tooling/history/` — **2 files** | G | same generator | same consumer set | `2026-07-31`, **`2026-08-29`** — the only repo with a post-July snapshot | KEEP |

## §3 — The lane question: `north-star.md` and `conformance.html`

### 3a. `conformance.{md,html}` — home is RULED ELSEWHERE, and the blocker named on 2026-09-01 no longer fires

**The ruled home is `docs/dashboard/`, not `ecosystem/`.** Witness, read in full:
`docs/intake/2026-08-17-tech-fleet-config-standardization.md`, *"AMENDMENT — 2026-09-01 (b)"*.
A root `dashboard/` is **WITHDRAWN**; the dashboard is ruled a **per-repo organ** homed at
`docs/dashboard/`; and — the part that binds this census — **`ecosystem/dashboard` is withdrawn
in the same act, as hub-only and therefore non-scalable**: *"`ecosystem/` is the hub's
fleet-facts tree keyed by consumer repo name, no carrier ships it, and a consumer repo has
none, so an organ placed there could not be per-repo at all."*

That amendment recorded **two** things still owed. This lane measured both against live code:

- **Owed #1 — an ADR-101 Tier-2 genre admission.** The amendment states: *"`SANCTIONED_GENRES`
  is a closed set and `dashboard` is not a member; an added path under an unsanctioned
  `docs/<genre>/` is refused … An ADR-101 amendment is therefore still owed."*
  **THAT IS NO LONGER TRUE AT HEAD, and it changed six days later without an ADR.**
  `scripts/validate_hermetization.py:248` now reads
  `SANCTIONED_GENRES = frozenset(_clause_list(SHAPE_SPEC, "genre_folders", "genres"))` — the set
  is **data**, sourced from `ecosystem/fleet-shape-spec.yaml`, whose `genre_folders.genres` block
  (`:161-174`) lists `dashboard` with the in-file note *"`dashboard` ENTERS it by operator ruling
  D6 of 2026-09-06, admitted 'via #73, as a folder-grammar entry, not ad hoc'"*. Executed live in
  this lane:
  `validate_hermetization.classify("docs/dashboard/conformance.html")` → **`None`** (no
  violation). `home_grammar` admits `docs/dashboard` and `docs/dashboard/*` (`:255-257`).
  The seal **accepts the migration today.** The gate that was the blocker was discharged as a
  **side effect of the D6 data landing** (commit `01104de`, 2026-09-07), not by the ADR-101
  amendment the ruling asked for — the amendment is still unwritten.
- **Owed #2 — the ZONE CLASS, and it is still open.** The same amendment: *"Whether
  `docs/dashboard/` is tracked or ignored is still unruled, still must be ruled the same way for
  both artifacts."* Confirmed live and **unchanged**: `conformance.html` is **tracked**
  (`git ls-files`), `trends.html` is **gitignored** (`.gitignore:93`) and absent from disk. The
  two artifacts the folder would gather are still in **different zone classes**, which is exactly
  what the ruling said must not survive the move.

**PROPOSAL — `RELOCATE ecosystem/conformance.md` and `ecosystem/conformance.html` →
`docs/dashboard/`, ORDER-GATED on one operator ruling: the zone class.** The seal no longer
refuses; the zone class is the only thing left, and it is the operator's to rule, not this
lane's. Nothing was moved.

**Cost the proposal carries, priced rather than hidden.** Relocating changes **two literals in
one generator** (`gen_dashboard.py:77,79`) and then invalidates every path-keyed consumer this
census found: `generated_artifact_freshness.DASHBOARD.outputs` (`:148`, a literal that its own
docstring says is deliberately *not* imported from the generator, so it will **not** follow
automatically), `tests/test_generated_artifact_freshness.py`, `tests/test_gen_dashboard.py`,
`tests/test_trend_dashboard.py`, `ARCHITECTURE.md`, `protocols/HANDOFF_PROCESS.md`,
`protocols/STANDING_RULINGS.md`, and `gen_dashboard.render_commit_path`'s pathspec. Cited by
path so the migration lane can enumerate rather than re-discover.

### 3b. Is `conformance.{md,html}` current against its generator? **NO — genuinely stale, not just HEAD-pinned**

`gen_dashboard.py --check` exits **1: STALE** on both faces. That alone proves nothing —
`generated_artifact_freshness.py`'s own docstring warns *"`--check` is HEAD-pinned: the dashboard
renders HEAD's sha and commit date, so `--check` drifts on EVERY commit."* So this lane rendered
the current output to a scratch file and **diffed it**. The drift is **substantive**:

- `Section 2 — Intake lifecycle gate`: five intakes missing from the committed copy — **#72,
  #73, #74, #75, #77** — and a **duplicate `#70`** in the committed copy that the regeneration
  resolves to `#77`. The committed dashboard therefore shows an intake-id collision that no
  longer exists.
- `Section 1`: `Total live rows: 226` committed vs **224** live; `[E2]` 52→51, `[E7]` 52→51.
- `Section 0`: three release-note rows (`[#630]`, `[#276]`, `[#614]`) that have aged out of the
  7-day window and are still shown.
- `Section 4`: ADR `Proposed 1` → **`Proposed 2`** (ADR-117 landed), header coverage 56 → 57.
- Markdown: **32 changed lines**. HTML: **24 changed lines**. Only 2 of those 32 are the HEAD pin.

The complementary date leg agrees but is quieter, and its quietness is itself worth recording:
`generated_artifact_freshness.py` reports **`FRESH conformance-dashboard: 2d stale (baseline
4d)`** — a WARN-never-FAIL ratchet keyed on a **measured** 4-day baseline. The date leg says
*fresh* while the content leg says *five intakes missing*. That is the gap the module's own
docstring predicts (*"an honest header on a stale trust surface is still a stale trust
surface"*), observed live. Reported, not repaired.

### 3c. `north-star.md` — home is `ecosystem/` and is RULED THERE; it is CONTENT-STALE

**No ruling re-points `north-star.md`.** The `docs/dashboard/` ruling is about *the dashboard*
(`conformance.html` + `trends.html`, named as its two artifacts); `north-star.md` is an arc view,
not a dashboard panel, and appears nowhere in that amendment. Its home is argued in its own
generator, `scripts/gen_north_star.py:31-36`, and the argument is a **refusal witnessed at the
gate**: *"HOME: `ecosystem/`, not `docs/`. ADR-101's home allowlist admits docs GENRE TREES only
… while `ecosystem/` is the admitted home for 'generated / declared ecosystem state', which is
exactly what this view is (`organ-index.md` and `doc-counts.md` are its neighbours). **The gate
refused `docs/NORTH-STAR.md` on first commit and it was right to.**"* Verified live:
`validate_hermetization.classify("ecosystem/north-star.md")` → `None`, and
`fleet-shape-spec.yaml:231-233` lists `ecosystem` under *"generated / declared ecosystem state"*.
**Verdict: KEEP.**

**Current against its generator? NO.** `gen_north_star.py --check` exits 1. Diffed against a
scratch render — the drift is **real count drift**, with no HEAD pin anywhere in this artifact:
`Open rows: 163 of 218 (55 deferred)` → **`171 of 224 (53 deferred)`**; THE METRIC arc `47
(P1 9 / P2 27 / P3 11)` → `51 (P1 11 / P2 29 / P3 11)`; LEARNING LOOP `48 (P1 3 / P2 35 …)` →
`51 (P1 5 / P2 36 …)`; DEPLOYMENT WAVE deferred `11` → `10`; LEGIBILITY `32` → `33`.
**Eight of the file's numbers are wrong**, and the file's own header claims *"this file cannot
drift from the backlog the way a hand-written roadmap does"* — true of the mechanism, false of
the committed bytes, because nothing regenerates it automatically. `README.md` cites it.

*One near-miss corrected rather than reported:* the scratch render is 2 bytes longer **and**
carries one extra trailing newline. The newline is an artifact of this lane's capture — the CLI
ends in `print(body)` (`gen_north_star.py:240`) while `--write` uses `write_text` (`:237`). It is
**not** a defect in the committed file, and is recorded here so no later reader inherits it as one.

## §4 — Two registry findings, both reported and neither repaired

**`index.yaml` is 33 days stale and now asserts something false.** Its own stamp reads
`generated: '2026-08-05T10:36:01'`. Its `.dev-knowledge` block still records
`check_name: vision_md` → `status: pass` / *"VISION.md present"* and lists `VISION.md` first in
`canonical_md_visibility`. Verified live: **`VISION.md` does not exist at the root**
(`ls VISION.md` → No such file); it is at `docs/archive/VISION.md`, relocated under `[#614]`.
`scripts/consumer_at_landing.py:125-129` already carries the corrected pointer with a comment
naming this exact failure mode (*"the literal silently dropped the file from this pool when it
relocated"*). `index.yaml` is a **derived** file — `audit.py::regenerate_index` *"overwrites it
WHOLESALE"* — so the fix is a fleet-audit run, not an edit. **This lane did not run one**
(`audit.py` is unimportable here; see limits). **Verdict KEEP, flagged STALE.**

**`registry.md` roster gaps are BY DESIGN — checked, not assumed.** Four surfaces disagree on
member count and every gap resolves: `registry.md` **9** rows · `ecosystem/<repo>/` **6** dirs ·
`index.yaml` **6** entries · `deployed-versions.yaml` **9** keys. The three repos with a registry
row and no `ecosystem/` dir are `demo-prep`, `life-architect`, `terminal-setup`, and all three
carry an explicit unonboarded status in the registry's own Status column (`terminal-setup`:
*"registered 2026-08-01 ([#462]) · unonboarded … no methodology adoption"*). `registry.md`'s own
header states the split (*"human registry"* vs *"machine registry"*). **No defect. KEEP.** The
row that would have policed this, `[#455]` (*"`registry.md` derived-field drift checker — no
organ reads the file at all"*), is `status: closed` — verified in `tasks/455-*.md`.

## §5 — The fleet-audit history has not advanced in 38 days

`ecosystem/<repo>/history/*.md` is the ADR-80/ADR-84 durable fleet-audit record, appended by
`audit.py::append_history`. Newest snapshot per repo: **`2026-07-31`** for five of six repos;
`win-tooling` alone reaches `2026-08-29`. Today is 2026-09-07.

This is **not** a file-hygiene finding — it is a consumer finding. `gen_trend_dashboard.py:594-600`
declares this tree the **sole** source for the doc-rot trend series
(`predicate="rows matching \`| doc_rot |\` in ecosystem/.dev-knowledge/history/*.md"`,
`:821`), and `window_metrics.read_fleet_history` reads it for window reporting. A series whose
newest point is 38 days old renders as a flat line, not as an absence. **Reported, not repaired,
and no file is touched:** the tree is append-only by rule, and whether the nightly Routine
stopped, was never armed in this window, or is writing somewhere this lane cannot see is
**UNDETERMINED** — `audit.py` cannot be run here.

## Proposals

Grouped by verdict, as the shape requires. **Every one is a proposal for the operator to rule;
this lane executed none of them.**

### KEEP — 31 of 33 rows
Rows 1–3, 6–24, and 25–33 above. Each has at least one live consumer found by `grep` **and** a
generator, an in-file stamp, or a post-graft commit as its freshness witness. Three carry a
reported defect that does **not** change the verdict, because in each case the file belongs where
it is and the defect is currency, not placement:

- **`index.yaml`** — STALE 33 days, asserts a root `VISION.md` that no longer exists (§4).
  Discharge = one fleet-audit run, which regenerates it wholesale.
- **`north-star.md`** — CONTENT-STALE, eight wrong numbers (§3c). Discharge =
  `gen_north_star.py --write` plus a commit; the generator has no writer of its own.
- **the six `history/` directories** — 38 days without a new snapshot (§5). Discharge is an
  operator/Routine question, not a file act.

### RELOCATE — 2 rows, ORDER-GATED
- **`ecosystem/conformance.md` → `docs/dashboard/conformance.md`**
- **`ecosystem/conformance.html` → `docs/dashboard/conformance.html`**

Home ruled 2026-09-01 (`docs/intake/2026-08-17-tech-fleet-config-standardization.md`, AMENDMENT
(b)); `ecosystem/` explicitly withdrawn as hub-only in that same act. The tree seal **already
admits** the destination (§3a, executed live). **Gate: the zone class must be ruled first, and
ruled the same way for `conformance.html` and `trends.html`** — the ruling says so in terms, and
the two are in different classes today. Migration cost is enumerated by path in §3a; the
`generated_artifact_freshness.py:148` literal is the one that will **not** follow the generator
and is the likeliest silent break.

### ARCHIVE — 0 rows
Nothing in `ecosystem/` is a completed record awaiting a retention home. The `history/`
directories look archival but are not: they are the live input to a rendered trend series (§5),
so archiving them would remove a consumer's only source.

### RETIRE — 0 rows
**Every one of the 27 non-history files has at least one live consumer under `scripts/`,
`tests/`, `.pre-commit-config.yaml` or `deploy/`, found by `grep` and re-opened.** The two
plausible retirement candidates were checked and both survive: `registry.md` is
hand-maintained with `[#455]` (its "no organ reads it" row) **closed**, and it is read by
`fleet_analytics.py`, `desired_state_loader.py`, `audit.py` and
`tests/test_membership_agreement.py`; `index.yaml` is stale but is a **derived** file that five
scripts read. Stale is not unused.

### UNDETERMINED — 0 file-level verdicts, 1 field
No file's verdict is undetermined. **One freshness FIELD is:** the exact last-content-change date
for the 21 files whose `git log` resolves to a graft boundary (see limits). For each of those, an
independent witness — an in-file stamp, a generator `--check`, or a live regen-and-diff — carried
the freshness column instead, which is why no verdict fell through.

## Counts before → proposed after

| | Before | Proposed after |
|---|---:|---:|
| Tracked files under `ecosystem/` | 106 | 104 |
| — top-level + `schema/` files | 27 | 25 |
| — `<repo>/history/*.md` snapshots | 100 | 100 |
| — untracked / ignored files present | 0 | 0 |
| Directories (incl. `ecosystem/` itself) | 14 | 14 |
| KEEP | — | 31 rows / 104 files |
| RELOCATE (order-gated on the zone-class ruling) | — | 2 rows / 2 files |
| ARCHIVE | — | 0 |
| RETIRE | — | 0 |
| Files this lane created | — | 1 (this census) |
| Files this lane moved / edited / deleted / renamed | — | **0** |

`104` assumes **both** relocations execute; the ruling may take neither, and the 2-file delta
leaves `ecosystem/` with `north-star.md`, `organ-index.md`, `doc-counts.md` and `registry.md` as
its only `.md` faces.

## Honest limits

What this lane could **not** establish, stated because the section is the point:

1. **`uv run --locked` is unavailable in this container, so no gate was run as the repo defines
   it.** `uv` here is `0.8.17`; `pyproject.toml` pins `required-version = "==0.11.19"`, and
   every invocation aborts with *"Required uv version `==0.11.19` does not match the running
   version"*. Every measurement above was taken under system `python3` 3.11.15 with
   `PYTHONPATH=.`. That worked for `gen_north_star`, `gen_dashboard`, `generate_organ_index`,
   `gen_methodology_roster`, `gen_claude_rosters`, `generated_artifact_freshness` and
   `validate_hermetization` — but it is **not** the declared environment, and a result it
   produced is weaker evidence than the same result under `uv run --locked`.
2. **`click` and `pydantic` are absent, so three things went unmeasured.** `scripts/audit.py`
   is unimportable (`ModuleNotFoundError: click`), so **`audit.py health`, `audit.py checks` and
   `regenerate_index` were never run** — which is why `index.yaml`'s staleness is reported from
   its own stamp and its own content rather than from a regen-and-diff, and why §5's cause is
   UNDETERMINED. `gen_doc_counts.py --check` fails on the same import, so `doc-counts.md`'s
   `54 registered checks` and `pytest --collect-only` claims are **unverified** (its `23
   pre-commit gates` claim *was* verified independently, and still reads 23 at the sync-merge).
   **Limit 8 fired on this very line while the lane ran:** the collected-tests claim was `5187`
   when row 10 was measured and is `5217` after the sync-merge with `origin/main` — a peer
   regenerated it mid-lane, which is the drift this section predicts rather than a defect in
   either number. `ecosystem/schema/*.py` cannot be imported
   (`ModuleNotFoundError: pydantic`), so both contracts are inventoried by reading them, never by
   loading them. `pytest` is absent entirely.
3. **The clone is SHALLOW, and this breaks the "last content commit" witness for 21 of 27
   files.** `git rev-parse --is-shallow-repository` → `true`; 278 commits; `.git/shallow` holds
   **17 graft boundaries**, among them `428656f` and `1cefc30` — and those two are precisely the
   commits `git log --no-merges -1 -- <file>` returns for 21 of the 27 non-history files. Because
   a graft commit has no reachable parent, git reports the whole file as added there. **The dates
   `2026-09-05` those rows would otherwise carry are meaningless**: the true last-content-change
   is *at or before* that date, unbounded below. Only four files have a witness-grade commit
   date: `doc-counts.md` (`a49537c`, 2026-09-07), `fleet-shape-spec.yaml` (`01104de`,
   2026-09-07), `disposition-register.yaml` (`c4fdc4e`, 2026-09-06) and `silent-rule-baseline.yaml`
   (`30c6e58`, 2026-09-06). For the rest the freshness column uses an in-file stamp or a live
   `--check`; where neither exists — `doc-code-edge.yaml`, `organ-registry.yaml`,
   `substrate-registry.yaml`, `provider-registry.yaml`, `registry.md` — **the age is genuinely
   unknown** and the row says so. A deeper fetch would settle all five.
4. **`fan-out: NONE`, and absence is not cleanliness.** `gemini` is not on PATH. **Gemini-read
   files: 0. Fabrications counted: 0** — zero because nothing ran, and a reader comparing this
   lane's fabrication count with a lane that actually fanned out is comparing nothing to
   something. Copilot Enterprise offload was unavailable: intake **#75** is `status: DRAFT`,
   read directly from its frontmatter. Nobody may later claim either was used here.
5. **Consumer discovery is `grep` over basenames, with the same weakness the tool it borrows
   from records.** A file is counted as consumed if its basename appears in a tracked file
   outside `ecosystem/` and `.git`. That over-counts (a mention in a handoff or an old audit is
   a record that the file existed, not evidence anything reads it — the exact objection
   `consumer_at_landing.py:30-36` raises) and under-counts (a consumer that builds the path from
   parts, or reads the whole directory, is invisible). Every consumer listed in the Inventory was
   narrowed to `scripts/`, `tests/`, `deploy/`, `.pre-commit-config.yaml` and the canonical docs,
   and the ones load-bearing to a verdict were **opened** and the reference confirmed — but the
   method cannot prove a **negative**, which is the honest reason `RETIRE` is empty rather than
   small.
6. **`tool-versions.yaml` currency is undecidable from inside the repo.** It declares the last
   *reviewed* upstream versions (`claude-code 2.1.204`, `codex 0.143.0`). Whether upstream has
   moved is a network question a read-only census does not ask; `[#273]`
   (*changelog-review staleness escalation*) is the row that owns it.
7. **Intake #73's own status disagrees with the ruling that is already live in code.** The file
   `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md` reads `status: DRAFT`, while
   `docs/audits/2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-shape-spec-finalize.md`
   describes it as *"#73, ACCEPTED with amendment D5/D6"* and D6 is **in the data and enforced by
   the seal** (§3a). This lane records the discrepancy and rules nothing: which of the two is the
   record is an operator/architect question, and it bears directly on whether §3a's "the seal
   already admits `docs/dashboard/`" rests on a ratified ruling or on unratified data.
8. **Batch U wave 2 was running beside this lane.** `deploy/`, `ecosystem/deployed-versions.yaml`,
   `docs/intake` shape-spec, `templates/ADR-template.md`, `CLAUDE.md` and
   `docs/decisions/ADR-117` were **read, never written**. Every measurement is a snapshot of the
   working tree at `5f27b203c07138374d4cef2ff26564d5c1233d8b`; a peer landing between that commit
   and this file's merge can invalidate a currency verdict here — notably §3b, which will read
   differently the moment anyone regenerates the dashboard.
9. **The known RED on main is not this lane's and is not claimed.**
   `tests/test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`
   was neither run nor investigated. No full suite was run, per contract.

---

**Lane:** S-08 · **Branch:** `claude/census-ecosystem` · **Base:** `5f27b203c071` ·
**Docs-only.** Read-only against `ecosystem/`; one new file; nothing moved, edited, deleted or
renamed.
