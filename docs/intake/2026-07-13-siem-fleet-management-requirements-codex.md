---
intake-id: 14
status: DRAFT
origin: "Codex (sol), operator-directed independent derivation, 2026-07-12"
consumed-by:
---

# Fleet-management and observability requirements — independent Codex derivation

Author: Codex (sol) — independent derivation, one of two; parallel: Fable

Status: **DRAFT**. This is a WHAT/WHY requirements input, not a tool-selection or build authorization. Phase A0 still has to settle and operationally witness the template; A1 creates least-commitment JSONL; Phase E makes the collection/store/viewer decision only after this requirements pack is ruled. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A0 (lines 17–18), §Phase A (lines 20–22), §Phase E (lines 34–35); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Answers 1 and 5 (lines 38, 46).

## (a) Functional-requirements pack

### Problem and operator questions

The current fleet can prove some carried mechanisms are present or can be made to fire, but it cannot answer one coherent question per repository: **what was supposed to be carried, what version is actually there, is it armed, did it fire when eligible, and is any difference explicitly sanctioned?** Presence alone has already produced false confidence, while a missing dependency silently downgraded an intended parallel test run to serial. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 4–14, 32–47); `.dev-knowledge/JOURNAL.md` §2026-07-12 — file [#332] (lines 50–60); `.dev-knowledge/BACKLOG.md` §E6/S15 [#332] (line 175).

The operator must be able to answer, without manually walking three trees:

1. Which folders, files, libraries, hooks, configs, skills, commands, and handoff mechanisms are required, conditional, local, ignored, forbidden, or unavailable in each repo role? Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Severity model and Tiers 1–4 (lines 12–45); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-structure-comparison.md` §Findings (lines 28–108).
2. Which carried mechanisms match their versioned contract semantically, including their source version, hook roster, configuration, dependency set, and declared exceptions? Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Architecture frame and §Phase A (lines 14–22); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 (lines 169–186).
3. Which mechanisms merely exist, which are armed, which pass a synthetic fire test, and which actually fired during eligible operator work? Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 4–36) and §Organ registry + evaluation (lines 702–738); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A0 and §Phase E (lines 17–18, 34–35).
4. When an expected event is absent, is the repo inactive, the organ inapplicable, the organ skipped, the organ silent, the collector stale, or the telemetry broken? The witnessed Stop-hook asymmetry—corp fired while ai-council was silent—makes a bare “last seen” field unsafe. Evidence: operator-supplied 2026-07-12 (the named Stop-hook observation was absent from all three available JOURNAL files); `.dev-knowledge/scripts/enforcement_coverage.py` §Result shapes and verdict vocabulary (lines 72–131).
5. Can every warning be traced to exact expected state, observed state, repo/commit, declaration or disposition, and raw evidence without a second suppression system? Evidence: `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 1–27); `.dev-knowledge/scripts/enforcement_coverage.py` §Consumer-side sanctioned-divergence allowlist (lines 158–247).

### Functional requirements

#### FR-01 — One versioned fleet contract, role-aware rather than byte-uniform

The layer **MUST** consume one versioned, machine-checkable contract for every parity surface. Each surface needs a stable canonical id, kind, owner, applicable repo roles, tier, expected state, probe, version/fingerprint source, dependency edges, waivability, and privacy class. The tier vocabulary **MUST** preserve `MUST`, `SHOULD`, `LOCAL-declared`, `UNDECLARED`, `IGNORE`, and inverse/forbidden rules; the hub **MUST** be modeled as a fleet role, not as an implicit exception. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Severity model, Tiers 1–4, and inverse rules (lines 12–45); `.dev-knowledge/BACKLOG.md` §E6/S15 [#328] (line 172); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Answer 5 (line 46).

The A1 build **MUST NOT** encode intake #12 unchanged: its DRAFT says `.methodology.yaml` is consumer-only and forbidden in the hub, while the later operator ruling requires the hub to carry its own `.methodology.yaml`. Phase A0 promotion is therefore a blocking contract-reconciliation step, not editorial cleanup. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Tier 1 inverse rule (lines 29–31); `.dev-knowledge/BACKLOG.md` §E6/S15 [#328] (line 172); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A0 and §Phase A (lines 17–22).

#### FR-02 — Five distinct mechanism states

For every hook, config, skill, command, handoff mechanism, and methodology dependency, the layer **MUST** report five distinct states: `desired`, `detected/carried`, `armed`, `synthetic-fire-proven`, and `operationally-observed`. A state may be `retired`, `not-applicable`, `unavailable`, `unknown`, or `stale`; no later state may be inferred from an earlier one. Synthetic probes **MUST** remain labelled synthetic and must never count as operator adoption. A deliberately retired command that is absent is at parity, not missing—the #330 sweep removed archived `/boot` and `/evolve` from live rosters for exactly that reason. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 4–43), §Organ registry + evaluation (lines 711–738), and §Tier-2 presence (lines 741–778); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A0 (line 18); `.dev-knowledge/JOURNAL.md` §2026-07-12 — [#330] root-archive prohibition (lines 36–46); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §3 c3 (lines 85–91).

#### FR-03 — Semantic parity with byte evidence, not byte equality as policy

The checker **MUST** compare a declared behavioral contract—scope, regex/decision rule, prospective-vs-retroactive behavior, fail posture, exit semantics, git selection, and version—while retaining byte hashes as evidence. Cosmetic source differences **MUST NOT** become parity failures when behavior is equivalent; genuine role-specific behavior **MUST** be declared. The d1 review found clean three-way fidelity: ten differences were cosmetic, and the only behavioral divergence was corp's enumerated eleven-name grandfather skip-set, declared in both repos' `.methodology.yaml`. Evidence: d1 review verdict, operator-supplied 2026-07-12; `Dev/ai-council/JOURNAL.md` §2026-07-12 — Fleet ruling d1 (lines 13–19); `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — Deploy docs/audits R4 casing gate (lines 612–618).

#### FR-04 — Canonical identity and address safety

Every component **MUST** have a stable canonical id separate from display `name`, local hook `id`, path, and repo-specific alias. Any prune, carry, or comparison proposal **MUST** resolve `repo + component id + source version + expected byte/semantic fingerprint`; a bare id or a cross-repo prose pointer is insufficient authority. The system **MUST** surface ambiguous or mis-addressed pointers instead of acting on them. Evidence: `Dev/ai-council/JOURNAL.md` §2026-07-12 — ruff-gate re-activation (line 5), where a hub-side pointer was mis-addressed as local and reversed a documented prune; `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — fleet rulings (line 630), where bare `id: ruff` versus canonical-name byte shape was deliberately prune-sensitive; `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 8–22), which rejects bare-id matching for dispositions.

#### FR-05 — Methodology dependency-version parity

The version contract **MUST** cover only dependencies required to operate methodology mechanisms, not force application-library uniformity. For each applicable dependency it **MUST** report the recommended constraint, repo declaration, active-environment version, interpreter/environment identity, source manifest version, and evidence path. Missing, mismatched, or uninspectable dependencies **MUST** WARN, never hard-block in v1; an at-parity or valid `.methodology.yaml` declaration **MUST** clear the parity warning without erasing the observed version. Evidence: `.dev-knowledge/BACKLOG.md` §E6/S15 [#332] (line 175); `.dev-knowledge/JOURNAL.md` §2026-07-12 — file [#332] (lines 50–60).

This check **MUST** catch declared-versus-installed drift. The triggering case was `pytest-xdist` absent in ai-council, making `-n` unrecognized and silently degrading the suite to serial; recurring manual comparison is explicitly the anti-pattern. Evidence: `.dev-knowledge/JOURNAL.md` §2026-07-12 — file [#332] (line 52); `.dev-knowledge/BACKLOG.md` §E6/S15 [#332] (line 175).

#### FR-06 — Deterministic decision-tree/graph conformance

The #328 leg **MUST** deterministically walk both directions: every expected surface against observed state, and every observed surface against the role contract. It **MUST** evaluate required presence, conditional presence, fidelity/version, inverse absence, local declaration, ignore status, dependency edges, and undeclared extras. Output **MUST** distinguish `PASS`, `PASS-declared`, `WARN`, rule-level `ERROR`, `not-applicable`, `unavailable`, and `unknown`; the v1 fleet-audit integration remains WARN-only and does not turn rule-level errors into commit blockers. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Nightly decision tree (lines 55–70); `.dev-knowledge/BACKLOG.md` §E6/S15 [#328] (line 172); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 (lines 167–186).

The graph **MUST** represent at least `owns`, `applies-to`, `carries`, `requires`, `declares`, `versioned-by`, and `observed-at` edges over repos, folders/files, libraries, configs, and organs. Each run **MUST** stamp repo HEAD, dirty-state caveat, contract version, collector version, and completeness; unavailable roots or approximate scans cannot pass green. This automates the manual L1/L2/L3 walk whose counts were explicitly approximate and point-in-time. Evidence: `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-structure-comparison.md` §Scope/method (lines 116–126); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 surface manifest and anti-regress property (lines 172–182).

#### FR-07 — Versioned JSONL event contract

Every check and adoption sensor **MUST** emit newline-delimited, schema-versioned events. The minimum common fields are `schema_version`, `event_id`, `ts_utc`, `collector_seen_ts`, `repo_id`, `repo_head`, `dirty_state`, `organ_id`, `organ_kind`, `event_type`, `severity`, `verdict`, `mode` (`actual` or `synthetic`), `source_version`, `run/session correlation`, `evidence_ref`, and `emitter_version`. This extends, rather than replaces, the already-ratified core fields `repo`, `check`, `severity`, `verdict`, `sha`, and `ts`. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Architecture frame (lines 14–15) and §Phase A (lines 20–22).

Writers **MUST** tolerate forward-compatible unknown fields but reject or quarantine records missing required identity/provenance fields. Duplicate `event_id` ingestion **MUST** be idempotent. A malformed record, partial trailing line, schema mismatch, or emitter exception **MUST** be counted and surfaced; it cannot disappear as a green run. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A least-commitment clause (line 22); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 anti-regress property (lines 180–182).

#### FR-08 — Opportunity, firing, completion, and silence telemetry

Operational adoption **MUST** be measured with a denominator. For each eligible lifecycle or operator action, telemetry needs an `opportunity` event, an `organ-fired` event, and a terminal `passed | blocked | failed-soft | errored | skipped` event, correlated to the same invocation. A missing fire is `silent` only when an eligible opportunity and fresh collection are both proven; otherwise it is `unknown`, `inactive`, or `collection-gap`. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E (line 35); operator-supplied 2026-07-12 (corp Stop hooks fired; ai-council Stop hooks silent); `.dev-knowledge/scripts/enforcement_coverage.py` §Cell model (lines 92–131).

Hooks, skills, commands, and handoffs **MUST** report through their executing path or a mechanically correlated wrapper. File presence, agent narration, shell history, or a synthetic injection alone **MUST NOT** be treated as real adoption. Handoff telemetry **MUST** distinguish generated, structurally verified, handed to a consumer, and actually consumed. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 10–14); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A0 operational minimum (line 18); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Answer 1 (line 38).

Passive guidance such as gotchas does not “fire.” It **MUST** use a narrower `loaded | consulted | unobservable` vocabulary, and the layer **MUST NOT** claim the guidance changed behavior. If there is no instrumented consumption path, its operational-adoption state remains `unobservable` rather than inferred from installation. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E adoption question (line 35); `.dev-knowledge/scripts/enforcement_coverage.py` §Organ registry, whose measurable fire surface is explicitly bounded (lines 689–708).

#### FR-09 — Consumer-local spooling and collection integrity

Each repo **MUST** emit only to a repo-local, gitignored spool; the hub collector **MUST** read consumers without mutating them and write collected state only in the hub. Collection **MUST** be incremental, restartable, and idempotent, with per-segment identity and checkpoint, newline-complete reads, rotation/truncation detection, duplicate suppression, and an explicit lag/watermark per repo. Open or locked Windows files **MUST** degrade to a visible retry state rather than loss or a false empty result. Evidence: `.dev-knowledge/ARCHITECTURE.md` §Layer Boundaries & Invariants (lines 102–111); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E (line 35); `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 45–47).

Spool-ignore safety **MUST** be verified with Git's own ignore resolver, not by grepping `.gitignore`. Comments **MUST** occupy their own lines: corp witnessed that an inline/trailing `#` became part of the pattern and left the intended file ignored. Evidence: `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — Fleet rulings: delete docs/diagrams + unify ruff + adopt .vscode (line 631).

#### FR-10 — Extend existing declarations and dispositions; do not duplicate them

Repo-specific sanctioned divergence **MUST** remain in that repo's `.methodology.yaml`, using the existing loader and mandatory reason/date shape. Known hub finding dispositions **MUST** remain in `ecosystem/disposition-register.yaml`. The observability layer may annotate events with those decisions but **MUST NOT** create a third waiver/suppression registry or delete raw observations. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` §Consumer-side sanctioned-divergence allowlist (lines 158–247); `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 1–27); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 home/reuse ruling (lines 180–186).

Matching **MUST** be one concern per finding and keyed to a specific benign signature, never a bare id; unmatched dispositions **MUST** surface as stale. For the new fleet-parity projection, an expired `review_date` is advisory-WARN in v1, per the later operator ruling; changing the older enforcement-coverage allowlist policy is a separate decision, not an accidental side effect of this layer. Evidence: `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 8–27); `.dev-knowledge/BACKLOG.md` §E6/S15 [#328] (line 172); `.dev-knowledge/scripts/enforcement_coverage.py` §Allowlist validation (lines 222–247).

#### FR-11 — One read-only operator viewer, question-led

One local viewer **MUST** answer: current contract/parity by repo; dependency version drift; last actual and synthetic fire separately; eligible opportunities versus silence; collection freshness; undeclared versus declared differences; active and stale dispositions; and a per-organ history with raw evidence references. Every summary cell **MUST** drill to contract version, observed repo SHA, exact expected/actual values, and source event/finding. The viewer **MUST NOT** mutate repos, deploy carriers, acknowledge findings by rewriting source, or become a control plane. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E (lines 34–35); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42).

#### FR-12 — Retention, privacy, and observability of the observer

Retention **MUST** remain undecided until event sources and measured volumes are inventoried. The eventual policy **MUST** be bounded by age and size per source class, keep raw JSONL long enough to rebuild the derived store, and report local-spool and hub-store pressure. The collector **MUST NOT** ingest prompts, transcripts, secrets, environment values, or arbitrary file contents by default; event payloads are allowlisted operational metadata plus evidence references. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E requirements list (line 35).

The observer **MUST** expose its own health: last attempted and completed collection per repo, records accepted/rejected/duplicated, partial lines, lag, schema versions seen, store rebuild status, and gaps. “No findings” with a stale collector **MUST** render unavailable, never green. Evidence: `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 anti-regress property (lines 180–182); `.dev-knowledge/scripts/enforcement_coverage.py` §Fleet report assembly (lines 929–944) and unavailable-consumer handling (lines 1060–1066).

### Ex-ante acceptance criteria

1. A hermetic three-repo fixture covers every ownership branch—MUST, SHOULD, LOCAL-declared, UNDECLARED, IGNORE, inverse, not-applicable, and unavailable—and produces deterministic results on two runs. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Severity model and nightly decision tree (lines 12–16, 55–70).
2. One hook fixture independently demonstrates desired-only, carried-not-armed, armed-but-unproven, synthetic-fire-proven, and actually-observed states; no state collapses into another. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 4–43) and §Evaluation (lines 711–738).
3. A dependency fixture with missing `pytest-xdist` WARNs with declared and installed evidence; an at-parity fixture and a valid declared divergence do not WARN. Evidence: `.dev-knowledge/BACKLOG.md` §E6/S15 [#332] (line 175).
4. Opportunity-without-fire renders `silent`; no opportunity renders `inactive/unknown`; stale collection renders `collection-gap`, not silent or green. Evidence: operator-supplied 2026-07-12 (Stop-hook asymmetry); `.dev-knowledge/scripts/enforcement_coverage.py` §Result shapes (lines 92–131).
5. The d1 three-way fixtures compare semantically clean while surfacing only corp's eleven-name declared grandfather behavior. A separate failure-injection test invokes a **real non-zero git subprocess**, closing the shared gap where fail-open was proven only with a monkeypatched `RuntimeError`. Evidence: d1 review verdict, operator-supplied 2026-07-12.
6. A mis-addressed component pointer and a bare-id/canonical-name mismatch produce ambiguity/refusal findings; neither proposes carry, prune, or re-activation. Evidence: `Dev/ai-council/JOURNAL.md` §2026-07-12 — ruff-gate re-activation (line 5); `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — fleet rulings (line 630).
7. Collection fixtures cover duplicate delivery, collector restart, file rotation/truncation, a partial final JSONL line, and a temporarily locked source; after recovery, exactly one normalized row exists per `event_id`, and every degradation is visible. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A least-commitment and §Phase E collection requirements (lines 22, 35).
8. A `.gitignore` fixture with an inline comment fails the ignore-safety check, while the same comment on its own line passes through `git check-ignore`. Evidence: `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — Fleet rulings (line 631).
9. One disposition cannot suppress two concerns; a new warning sharing only a bare id re-surfaces; a disposition matching no live warning appears stale. Evidence: `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 8–27).
10. Deleting the derived query store and rebuilding it from retained JSONL yields the same normalized rows, conformance verdicts, and viewer totals for the fixture corpus. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A JSONL least-commitment (line 22) and §Phase E sanctioned storage shape (line 35).

### Non-goals

- No Grafana/Loki/ELK-class stack, no hosted service, and no always-on fleet platform; that option is permanently rejected. Evidence: `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42).
- No orchestration, deployment, pruning, self-healing, or consumer mutation by the observability layer. Evidence: `.dev-knowledge/ARCHITECTURE.md` §Layer Boundaries & Invariants (lines 102–111); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 (lines 165–186), which specifies a WARN-only check.
- No forced byte identity, global application-dependency lockstep, retroactive rename, or erasure of declared local behavior. Evidence: `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Tensions weighed and §Considered + rejected (lines 40–42); d1 review verdict, operator-supplied 2026-07-12.
- No dashboard implementation or system-architecture visualization before the collection and query requirements are ruled. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E (lines 34–35).

## (b) Architecture sketch under the binding constraints

This is a sanctioned **shape**, not a selected product stack:

```text
versioned contracts
  ownership/parity surfaces + deploy versions + dependency recommendations
  + per-repo .methodology declarations + existing WARN dispositions
                         |
                         v
repo-local producers --> repo-local JSONL segments
  hooks/config probes      actual + synthetic events kept distinct
  skill/command adapters   no cross-repo writer
  handoff lifecycle
                         |
                    hub PULL collector
                  checkpoints + gap telemetry
                         |
                         v
             retained raw JSONL in the hub
                         |
                 validate + deduplicate
                         |
                         v
       one rebuildable embedded query store
             (SQLite-class OR DuckDB-class)
                 /                       \
                v                         v
 deterministic parity graph         one read-only viewer
 existing audit/enforcement          questions + evidence links
 machinery extended
```

The contract plane **extends** the chartered `parity-surfaces` mechanism and the existing deploy manifest, `.methodology.yaml` loader, enforcement reporter, and disposition register; it does not invent parallel authorities. Evidence: `.dev-knowledge/BACKLOG.md` §E6/S15 [#328] (line 172); `.dev-knowledge/scripts/enforcement_coverage.py` §Allowlist reader and Tier-3 classification (lines 158–247, 781–906); `.dev-knowledge/ecosystem/disposition-register.yaml` register contract (lines 1–27).

The producer plane is deliberately tiny and repo-local. Existing organs emit a common envelope at their executing path; adapters may differ by organ kind, but all write JSONL and never reach into another repo. Synthetic conformance probes and actual operator events share the schema but not the `mode`, so the store cannot accidentally turn testability into adoption. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 10–14, 38–47); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Architecture frame and §Phase A (lines 14–22).

The collection plane is one operator-invoked or scheduled hub library/CLI, not a daemon. It reads only complete consumer segments, checkpoints progress, and writes raw copies plus collection-health events in the hub. This preserves the hub's read-only sibling boundary. Evidence: `.dev-knowledge/ARCHITECTURE.md` §Layer Boundaries & Invariants (lines 102–111); `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 45–47) and §Fleet enumeration (lines 914–926).

The data plane retains JSONL as the rebuild source and uses **one** embedded store class, not both. SQLite-class versus DuckDB-class remains open until event volume, query shape, concurrent-read needs, and rebuild time are measured. The viewer technology also remains open; it is selected only after the operator questions and acceptance fixtures are stable. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A least-commitment (line 22) and §Phase E (lines 34–35); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42).

The rules plane extends `enforcement_coverage.py` and the ecosystem audit with deterministic surface and dependency probes. It does not turn the viewer into a rules engine, and it does not allow a UI acknowledgement to rewrite declarations or dispositions. Evidence: `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 home and anti-regress design (lines 169–186); `.dev-knowledge/scripts/enforcement_coverage.py` §Tier-3 drift surfacing (lines 781–906).

## (c) PULL vs PUSH consumer-log collection at 3→8 repos

### PULL case

PULL keeps consumers hermetic: they emit locally and need no hub address, receiver credential, retry protocol, or network client. One hub process owns checkpoints and can reuse the already-registered sibling-path resolution. At the stated 3→8-repo scale, its operational surface is bounded and consistent with the current read-only fleet reporter. Evidence: operator-supplied task constraints, 2026-07-12 (single operator, Windows-first, hermetic, libraries-not-platforms); `.dev-knowledge/scripts/enforcement_coverage.py` §Fleet enumeration (lines 914–926); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E scale statement (line 35).

PULL's weakness is completeness: a missing/moved/offline repo, stale checkout, open file, or skipped schedule can look like no activity. Therefore PULL is acceptable only with explicit repo watermarks, collection-attempt events, unavailable/gap states, incremental checkpoints, and an on-demand catch-up command. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` §Unavailable consumer handling (lines 1060–1066); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E collection requirement (line 35).

### PUSH case

PUSH gives each consumer immediate control over delivery and becomes attractive when repos run on machines the hub cannot read, when latency matters more than polling, or when the fleet is no longer one locally reachable estate. Those conditions are not established in the present evidence. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E, which leaves PULL versus PUSH open pending requirements (line 35); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Open questions (line 44).

PUSH would currently require either a listening service/shared sink or direct consumer writes into the hub, plus authentication, buffering, retry/idempotency, and failure handling in every repo. The first shape moves toward a platform; the second breaches the read-only sibling boundary. Evidence: operator-supplied task constraints, 2026-07-12; `.dev-knowledge/ARCHITECTURE.md` §Layer Boundaries & Invariants (lines 102–111); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42).

### Recommendation

Adopt **PULL for the 3→8-repo horizon**, with consumer-local JSONL spools and a hub-owned incremental collector. Preserve transport neutrality in the event schema so delivery can change without changing producers or historical data. This is a recommendation, not a tool selection. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E scale/collection fork (line 35); `.dev-knowledge/scripts/enforcement_coverage.py` §Fleet enumeration (lines 914–926); operator-supplied task constraints, 2026-07-12.

Reopen the fork—and route it to AI Council—only if one of these measured triggers appears: a consumer is routinely unreachable from the hub, the fleet becomes multi-machine, required detection latency is shorter than a safe pull interval, or collection retries/lag exceed the agreed survival metric. This follows the existing rule that Council fires only when requirements reveal a genuine fork. Evidence: `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Tensions weighed and §Open questions (lines 40, 44); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E decision gate (line 35).

## (d) ADVERSARIAL — three riskiest ways to build this layer wrong

### Risk 1 — Telemetry theatre: a green dashboard that cannot distinguish silence from absence

The most dangerous wrong build counts installed files, successful synthetic probes, or missing events as adoption. That would report ai-council's silent Stop hooks as “unused” or “healthy” depending on the query, while corp's fired hooks look identical unless eligible opportunities and collection freshness are recorded. It recreates the exact presence-versus-enforcement failure the existing Informant was built to correct. Evidence: operator-supplied 2026-07-12 (Stop-hook asymmetry); `.dev-knowledge/scripts/enforcement_coverage.py` module contract (lines 4–14) and §Tier-2 presence warning (lines 741–778).

**Counter-pressure:** make `opportunity → fired → terminal outcome` and collector watermarks non-negotiable; keep actual and synthetic modes separate; render missing denominator as unknown. Evidence: `.dev-knowledge/scripts/enforcement_coverage.py` module contract and distinct result shapes (lines 4–43, 92–131); `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase E adoption telemetry (line 35); operator-supplied 2026-07-12 (Stop-hook asymmetry).

### Risk 2 — A parity engine that becomes an accidental fleet mutator

A naive engine will treat hub bytes as universal truth, match components by unstable names, and turn every difference into a repair. That can re-activate a deliberately pruned hook from a mis-addressed pointer, prune a valid gate because bare-id and canonical-name shapes differ, or flag ten cosmetic d1 port differences while missing the one real grandfather behavior. Evidence: `Dev/ai-council/JOURNAL.md` §2026-07-12 — ruff-gate re-activation (line 5); `Dev/corp-monorepo/JOURNAL.md` §2026-07-12 — fleet rulings (line 630); d1 review verdict, operator-supplied 2026-07-12.

**Counter-pressure:** the layer stays read-only; role/applicability and declarations precede comparison; canonical ids are distinct from display/local ids; semantic probes and byte evidence coexist; ambiguity refuses. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md` §Tiers and decision tree (lines 18–70); `.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md` §9 (lines 169–186).

### Risk 3 — The sanctioned “small SIEM” shape becomes the platform tax it was meant to avoid

JSONL + an embedded store + one viewer is lighter than a full stack, but it can still be the wrong answer for a single operator. If event volume is tiny and the only recurring decisions are a nightly parity matrix plus “last fired,” a database schema, migrations, retention jobs, collector checkpoints, and a viewer may cost more attention than they save; JSONL plus deterministic reports might be sufficient. Conversely, PULL can become a false-completeness machine if the fleet moves off one locally reachable estate. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A least-commitment and §Phase E requirements-first gate (lines 22, 34–35); `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42).

**Counter-pressure:** require measured event volume, named operator queries, a rebuild-time target, and a survival metric before adding the embedded store or viewer. Ship in reversible slices: JSONL schema first, collection second, derived store only when queries justify it, viewer last. The operator should explicitly retain the right to stop at JSONL + reports. Evidence: `.dev-knowledge/docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` §Phase A and §Phase E sequencing (lines 20–22, 34–35); `.dev-knowledge/docs/intake/README.md` §7 Rent rule (lines 166–178).

**Constraint-risk flag, not an override:** permanently rejecting Grafana/Loki/ELK-class platforms is rational for the present single-operator, hermetic fleet, but it could become costly if the fleet becomes multi-host and durable remote ingestion becomes the dominant requirement. That future constraint conflict belongs to the operator; this derivation does not reopen it. Evidence: `.dev-knowledge/docs/handoffs/2026-07-11-dev-knowledge-architect-phase-a0/SUPPLEMENT.md` §Considered + rejected (line 42); operator-supplied task constraints, 2026-07-12.
