---
intake-id: 14
status: DRAFT
origin: research session (execution mode, operator-directed brief), 2026-07-12/13 overnight — intake #13 v4 Phase E Leg 0 pulled FORWARD as research-only; no decision, no tool selection
consumed-by: "2026-07-12-siem-requirements-ruled-pack.md (#14 RULED consolidation pack; this draft retained as provenance)"
---

> **Intake note:** The functional-requirements pack intake #13 v4 Phase E names as its Leg 0 — event sources + volumes, the operator's questions, collection model (pull vs push), retention, privacy/scope — plus the four-question pattern survey the operator's brief ordered (parity-as-versioned-state · fire-telemetry schema · pull-vs-push · conformance decision-tree). Requirements before tools; every requirement traces to a witnessed failure or a named register row (Annex E). Per the Phase E ARCHITECTURE DECISION GATE this doc RECOMMENDS where the evidence is lopsided and forks only what is genuinely contested — nothing here is decided until the operator rules (ADR-98 §4 confirm-gate).

# Fleet observability & conformance layer ("SIEM" track) — requirements and patterns

## Problem / motivation

The fleet (hub + 2 active consumers, registry already tracking 6, plan-of-record scale 5–8+) enforces methodology by carried organs — hooks, gates, skills, commands, configs. Three facts, each witnessed on 2026-07-12 alone, show the current layer sees **presence** but not **state, fidelity, or execution**: identical Stop-hook wiring fired in corp-monorepo and stayed silent in ai-council with nothing detecting the silence; pytest-xdist sat absent in ai-council so its suite silently degraded to serial until a human noticed `-n` was unrecognized (BACKLOG #332's witnessed trigger); and a deliberately-pruned ruff gate was re-activated on a mis-addressed cross-repo pointer because no machine-checkable record answered "why is this absent HERE". Twenty sessions of manual root-diffing produced the fleet-parity register (2026-07-11); Phase A0 is settling the template by hand — but A0's own exit doctrine (`presence ≠ enforcement ≠ usable`, intake #13 v4) says hand-witnessing does not scale to 8 repos. This intake captures what the automated layer must do, so Phase A (#328) builds against settled requirements instead of improvising an observability architecture mid-checker.

## The operator's questions this layer must answer

(Phase E Leg 0 deliverable per intake #13 v4 — the questions, verbatim-faithful to the evidence base.)

1. **Conformance** — is every fleet repo shaped as the settled template says, per its role and tiers? (intake #12 decision tree; parity register §9)
2. **Fidelity** — is what the hub shipped still what is there: same tag/rev/hash/ids, nothing silently drifted, re-grown after a prune, or locally mutated undeclared? (intake #12 Tier-1 "present ≠ carried"; ai-council ruff re-activation)
3. **Execution** — did the carried organs actually FIRE this session / this week, and which went silent? (stop-hook silence, 2026-07-12)
4. **Divergence** — which differences are declared-and-sanctioned vs new-and-silent, and which declarations have gone stale? (register anti-regress property; ADR-75 stale-decoration)
5. **Versions** — are consumer dependencies at the hub-recommended pinned set? (#332)
6. **Delta** — what changed across the fleet since yesterday, consumable in one morning read? (#324 morning prompt)
7. **Scale** — does any of the above need re-architecture when repos 7 and 8 join? (intake #13 Phase E scale concern)

## Scenarios (+1 view)

- **S1 — the silent Stop hook (witnessed 2026-07-12).** Both consumers carry byte-similar `.claude/settings.json` Stop wiring (`session_end_backpressure.py` + tier1-lifecycle plugin — verified this session). The operator watches the hooks fire in corp and stay silent in ai-council. Today: nothing records either fact; presence-checkers verify wiring and pass both. With the layer: each fire appends one event record locally; the nightly join of *expected-fires* (from the parity manifest: organ × trigger) against *observed events* WARNs `ai-council: stop-organ expected, 0 events in window` the next morning. The silence-class mechanism is already on record once (ai-council 2026-07-08: bare-`python` venv resolution failed a SessionStart leg silently, gap G8) — the class recurs; only an expectation-join detects it, because a hook that never runs writes no log line.
- **S2 — the silently-serial test suite (#332).** ai-council's 2026-07-12 arcs report "Full serial suite 444 passed" — green, and degraded: pytest-xdist absent, `-n` unrecognized. No gate models "hub recommends dep X at version Y". With the layer: the dependency-parity leg compares each consumer's declared/installed set against a hub-versioned recommended manifest and WARNs `ai-council: pytest-xdist absent (hub-recommended >=N)` — drift surfaced, never blocked (#332: routine manual checking is the anti-pattern this exists to prevent).
- **S3 — the resurrected prune (witnessed 2026-07-12).** A prompt justifies re-activating ai-council's ruff gate via "divergence-register item 9 UNRESOLVED"; recon finds the pointer was hub-side, mis-addressed as local, and the gate was deliberately PRUNED 2026-07-04 ([#244] deploy `31e785d`) — the operator must intervene and rule "re-activate knowingly". With the layer: deliberate absence is first-class queryable state (`removed: <component>, by: <deploy sha>, declared: <waiver>`); a conformance run answers "why is X absent here" before any re-add, and an undeclared re-appearance of a tombstoned component WARNs on the next nightly instead of riding in silently.
- **S4 — the carry that didn't take effect (witnessed 2026-07-12).** corp's `.vscode` carry first wrote `!.vscode/settings.json  # comment` — git treats the inline comment as part of the pattern, so the file stayed ignored while the `.gitignore` line *textually matched* the template. Caught only because that arc hand-verified with `git check-ignore`. With the layer: probes assert **effect, not text** — `check-ignore` semantics for ignore rules, `.git/hooks/*` + armed stages (and no relic `core.hooksPath`) for hook installation, tag-ancestry for pinned revs. A text-grep probe would have false-passed S4 by construction.
- **S5 — the three-name organ (d1 port review, 2026-07-12).** One casing gate now lives in three repos as `rule_b_violation` / `audit_casing_violation` / `casing_violation`; the adversarial three-way review found ten cosmetic divergences and exactly one behavioral one (corp's enumerated 11-name grandfather skip-set — itself declaration-worthy). Meanwhile both consumers deliberately keep ruff at the bare `id: ruff` no-`name:` byte-shape precisely so the hub remove-leg refuses rather than deletes. Identity by filename or byte-shape is therefore ALREADY load-bearing and fragile in both directions. With the layer: every carried organ has one canonical id in the manifest; local names/paths/extracts map to it; fidelity is judged at contract level (verdict-equivalence + declared divergences), not byte level.
- **S6 — the morning read (+1 view).** The operator opens one surface after the nightly run: per-repo conformance/fidelity/execution/version verdicts in the register's own grammar, new-undeclared items flagged, stale declarations decorated, deltas since yesterday on top — and rules FIX / DECLARE / TICKET from there (#324 loop). No dashboards to operate, no service to keep alive; at 8 repos the read is the same, just more rows.

## Functional requirements

Trace tags [W*/R*] resolve in Annex E. MUST = the layer's floor (v1); SHOULD = first hardening; COULD = only when a witnessed need arrives (rent rule).

**Must:**
- **FR-1 One parity manifest as versioned data.** Hub-owned, in-git, machine-readable: surfaces × role-tiers (intake #12 MUST/SHOULD/LOCAL/IGNORE + inverse rules) × one probe each; consumes the A0-settled template, never a moving target. [R1,R2,W6]
- **FR-2 Canonical organ identity.** Every carried mechanism gets one stable id used by manifest, checker, deploy legs, and event records — independent of local filename, `name:`, or extract shape. Byte-shape (bare-id) prune-safety remains honored, but identity never rests on it. [W4,W6-d1]
- **FR-3 Deterministic read-only conformance walk.** The #328 decision tree evaluated per registered repo (hub included, §9a) from a facts-snapshot; same inputs → same verdicts; register-grammar output (AT-PARITY / PASS-declared / WARN-undeclared / MUST-absent class); WARN-only surfacing in v1 (§9b, ADR-85 hardening pattern); zero mutations, ADR-28/36 Layer-2 posture. [R1,R2,W6]
- **FR-4 Declared divergence honored, with shelf-life.** Every verdict consults the repo's `.methodology.yaml`; declared+current → PASS-declared; `review_date` past → advisory re-WARN (v1); declarations that match no live divergence decorate stale (extends ADR-75 / disposition-register semantics — waivers must not rot into paper suppressions). [R2,R4,W3]
- **FR-5 Deliberate absence is first-class state.** absent-by-design (manifest `status: removed`, tombstone, declared waiver) ≠ absent-gap; the checker distinguishes them, the record answers "why absent here", and an undeclared re-appearance of a removed component WARNs. [W3,R4]
- **FR-6 Effect-probes over text-probes.** Wherever a surface has observable semantics, the probe asserts the effect (check-ignore verdicts, installed+armed hook stages, no relic `core.hooksPath`, tag-ancestry of pinned revs), not the text. [W5,W7]
- **FR-7 Dependency-version parity leg.** Consumer declared/installed dependency versions verified against a hub-recommended versioned manifest carried with the methodology package; drift/absence = WARN, never a hard block; one-time manual alignment permitted as bootstrap. (#332 charter, verbatim scope.) [W2]
- **FR-8 Per-fire event emission.** Every methodology-organ invocation appends one bounded, structured event record (JSONL-class, append-only, repo-local, gitignored runtime); emission is fail-open — the emitter may never block, break, or perceptibly slow the organ (a telemetry wrapper that can crash a hook would reintroduce the S1 silence class it exists to catch). [W1,R5]
- **FR-9 Silence detection by expectation-join.** A non-firing organ writes nothing, so silence is detectable only against an expectation model (manifest: organ × trigger × cadence); the nightly run joins expected vs observed over a window and WARNs expected-but-silent per repo+organ. Complementary to `enforcement_coverage`'s fire_test: the Informant proves an organ CAN fire (synthetic clone probe); telemetry proves it DID fire (production evidence). Neither substitutes for the other. [W1,R5,R7]
- **FR-10 No consumer-side egress coupling.** The collection mechanism must not require any consumer to carry a hub address, write outside its own tree, or block on hub availability — consumers stay hermetic (write local; know nothing about the hub). Cross-repo pointers are the witnessed-fragile element (S3); today's pre-commit store-lock contention shows shared-write-target risk on Windows. (This requirement constrains the Annex C fork; the recommendation there follows from it.) [W3,R6,R7]
- **FR-11 Privacy scope: metadata only.** Event records and collected state carry ids, verdicts, counts, durations, shas, repo names — never file contents, command payloads, client/product content, or user-absolute paths. corp-monorepo client content never leaves corp; the OneDrive exclusion zone is untouched in all tiers; app logs are out of collection scope (methodology organs only). [R6, core-invariants]
- **FR-12 Extend, don't duplicate.** The layer lands as extensions of the existing organs — `audit.py` checks, `enforcement_coverage.py` (already the `.methodology.yaml` reader), `fleet_health.py` digest, `disposition-register` semantics, `deployed-versions.yaml` pattern — one taxonomy, no parallel machinery. [R3,R4]
- **FR-13 Bounded retention, durable digests.** Raw event files are rotation-capped (size/age) gitignored runtime artifacts; committed nightly digests are the durable record (FLEET-HEALTH precedent). Append-only JSONL sidecars are merge-conflict-free by construction — unlike the witnessed parallel-JOURNAL prepend collisions. [R5,R7,W8]

**Should:**
- **FR-14 Register-faithful output grammar.** The machine emits the same verdict vocabulary the human registers use (FIX-NOW / DECLARE-LOCAL / TICKET / AT-PARITY lineage), so registers regenerate from runs instead of drifting from them. [R1]
- **FR-15 Fleet-member onboarding by registration.** A new repo enters coverage via one registry row + role/tier applicability in the manifest — no per-repo checker code (the 3→8 scale test). [W8,R3]
- **FR-16 Verdict/severity vocabulary interop.** Event outcomes align with the existing Finding statuses (OK/WARN/FAIL) so ship-gate and disposition tooling can consume them later without translation. [R3,R4]
- **FR-17 SessionStart delta surfacing.** Yesterday's new WARNs (silence, drift, undeclared divergence) surface at hub session start (fleet_health precedent) in addition to the nightly digest. [R7]

**Could:**
- **FR-18 Derived local read-model.** A disposable SQLite/DuckDB-class index built FROM the JSONL when a witnessed query need arrives — rebuildable, never the system of record, no server. [R5]
- **FR-19 One local viewer.** The #322 dashboard consumes the digest/read-model as a local-HTML surface (intake #9 class) — operational state only; architecture visualization stays deferred (intake #10). [R1,R8]
- **FR-20 Organ latency watch.** duration_ms aggregation to spot degrading hooks (the 6-minute lock-contention class) — only if latency pain recurs. [R7]

## Acceptance criteria (ex-ante)

1. **Undeclared-divergence WARN:** seeding a deliberate undeclared divergence in a throwaway consumer clone yields exactly one WARN naming repo + surface in register grammar on the next run; adding the `.methodology.yaml` declaration flips it to PASS-declared with no code change. (The register §9 anti-regress property, demonstrated.)
2. **Version drift WARN:** a consumer missing a manifest-pinned dep (the pytest-xdist case) yields a WARN naming dep + expected-vs-actual; an at-parity or declared consumer yields none. (#332 Done-when, honored verbatim.)
3. **Silence caught within one cycle:** with telemetry live in both consumers, either the event log shows ≥1 Stop-organ fire per consumer session, or the next nightly emits expected-but-silent for the quiet repo — i.e. S1 as witnessed would have surfaced without operator observation within one day.
4. **Identity across names:** the d1 three-way state (one organ, three local names, one behavioral skip-set divergence) is representable: one canonical id maps all three; corp's skip-set reads as a declared divergence; the run reports fidelity with zero byte-diff noise.
5. **Effect-probe teeth:** the S4 `.gitignore` inline-comment state (line textually present, semantically inert) is reported as non-conforming by the probe; a text-grep would false-pass it — the test asserts the probe uses effect semantics.
6. **Tombstone teeth:** re-adding a `status: removed` component to a consumer without a declaration WARNs on the next run (S3 as witnessed becomes machine-caught).
7. **Bounded and resident-free:** a full-fleet run at 8 registered repos completes without cloning in bounded time on this machine; no process outlives the run; raw event volume stays within the rotation caps (Annex A orders of magnitude).
8. **WARN-only v1:** the layer introduces zero new blocking gates; every new signal is WARN/advisory; any hardening is a separate later ruling (ADR-85 pattern, §9b).

## Non-goals

Reaffirming the standing CONSIDERED+REJECTED register (binding — do not relitigate) plus this doc's own exclusions:

- **Full SIEM / log-platform stacks — Grafana, Loki, ELK-class: PERMANENTLY REJECTED** (oversized for a single-operator fleet; kills hermetization). Posture stands: libraries-not-platforms — JSONL events + SQLite/DuckDB-class store + one viewer. Annex A's volumes make the scale case terminal: the fleet's worst-case event volume is orders of magnitude below any threshold that justifies a log platform.
- **No resident anything:** no daemons, agents, services, watchers, message queues, or brokers; every component is a run-to-completion script under existing surfaces (pre-commit, session hooks, nightly, CLI).
- **No cloud/SaaS telemetry destination;** all data stays on this machine's disk.
- **No auto-remediation:** detect-and-propose stands (ADR-96 refusal semantics; deploy legs converge only under operator-ratified runs). Telemetry and conformance NEVER gate in v1 (WARN-only; §9b).
- **No dashboards-as-service:** the viewer class is local HTML opened in the editor (intake #9); architecture visualization stays deferred wholesale (intake #10 is the reopen input; #326 ruling).
- **Platform tripwire (operationalizing libraries-not-platforms):** a candidate component is a PLATFORM — and out — if it runs resident, owns state not regenerable from git + JSONL, carries its own upgrade/ops lifecycle, or introduces a query/rule DSL to learn (a Rego-class engine fails this even though the policy-as-code *pattern* is adopted).
- **Out of collection scope:** application logs, transcripts, client/product content, OneDrive-zone paths (all tiers), and anything beyond methodology-organ metadata (FR-11).
- **Not this doc:** tool selection, schema finalization (born in Phase A per intake #13), store/viewer build (#322, after this pack is ruled), BACKLOG mutations, or any build.

## Impact sketch (4+1 lite)

- **Logical:** two genuinely new concepts — the expectation model (organ × trigger × cadence) and the event record; everything else extends existing organs (manifest, walker, waiver semantics, digests).
- **Process:** nightly run grows conformance/silence/version legs; #324 morning prompt consumes one digest; SessionStart surfacing extends fleet_health; A0 leg-(b) manual witnessing becomes the automated floor.
- **Development:** hub-side script extensions (audit.py / enforcement_coverage.py / fleet_health.py) + manifest data; consumer-side only the emitter wrapper, carried via the deploy manifest at its own P6-class rollout — no consumer code before the carrier exists.
- **Physical:** local disk only; gitignored rotation-capped JSONL per repo + committed digests at the hub; no network, no services, no new top-level dirs without ADR-101 sanction.

## Open questions (operator)

1. **Retention window:** raw JSONL rotation — strawman 90 days or size-cap, digests permanent. Ratify or set numbers.
2. **Hub self-telemetry:** the hub emits events like any fleet member (§9a symmetry says yes) — confirm.
3. **Emitter wiring locus:** wrap each organ vs a harness-level wrapper around hook invocations — technical-architect question, recorded not answered here.
4. **Event fields beyond the floor:** session-id? duration_ms in v1 or deferred to FR-20? (Privacy note: session-id is metadata, but confirm.)
5. **Collection cadence:** nightly-only, or also on-demand/SessionStart pulls?
6. **Pull ratification:** accept Annex C's PULL recommendation (fork judged not-genuine), or send to AI Council regardless? (Intake #13 pre-identified it as the likely fork; the evidence turned out lopsided.)
7. **Consumer event-log path convention:** one fleet-standard gitignored path (e.g. under each repo's `logs/`) — name it at Phase A.
8. **Filename/infix:** this doc landed at the operator-specified name without the README §4 `tech-` infix — rename before merge, or accept as-is?

## Status

DRAFT — awaiting the ADR-98 §4 operator confirm-gate. Everything herein is requirements + pattern input for the technical architect (Phase A/#328 and Phase E proper); the Annex C recommendation and Annex D field-floor are proposals, not decisions.

---

# Annex A — Event sources + volumes inventory (Leg 0)

**Sources (per repo, all existing today — nothing here is hypothetical):**

| Source class | Instances today | Fires on |
|---|---|---|
| pre-commit gate hooks | hub ~15; ai-council ~6; corp ~8 | every commit |
| commit-msg hooks | hub 2 (`backlog-id-on-close`, `filing-backpressure`); consumers 1 | every commit |
| pre-push hooks | `block-ff-push` (hub + both consumers since v1.3.1) | every push |
| SessionStart legs | hub 4–5; consumers 2–3 (floor guard, pre_commit install, surfacing) | every session start |
| Stop legs | seb + plugin propose_closures (hub + both consumers) | every turn stop |
| nightly battery | audit.py check set (~30 checks) + fleet_health (6 repos) + triage legs | nightly |
| commands/skills | /ship, /review-closures, /handoff, /save, /override, validators | on invocation |

**Volumes (order-of-magnitude, heavy day, 8-repo fleet):** ~10–40 commits/day × ~10 hook-fires + ~5–15 sessions × ~6 session-legs + nightly ~30 checks × 8 repos ≈ **low thousands of events/day worst case**; at ~150–250 bytes/JSONL line ≈ **≤1 MB/day, tens of MB/month uncompressed** before rotation. Three-plus orders of magnitude below any volume that motivates a log platform — the scale argument for ELK-class is dead on arithmetic, independent of the standing rejection.

**Existing event-adjacent surfaces the schema must not orphan:** `logs/coherence-nudge.log` (hook append-log), `logs/OVERRIDES.md` (override audit), `logs/FLEET-HEALTH.md` / `ENFORCEMENT-COVERAGE.md` / `BOUNDARY-DRIFT.md` (committed digests), the `Routine: <name>` commit trailer (#123), `ecosystem/deployed-versions.yaml` (durable committed version record: written-by-command, read-by-check — the pattern FR-7's dep manifest reuses), `ecosystem/<repo>/state.yaml` (gitignored mutable pointer).

# Annex B — Pattern survey (library-scale extraction; tools named as exemplars, never candidates)

| # | Industry class | The pattern worth extracting | Library-scale translation here | Embryo already in-repo |
|---|---|---|---|---|
| 1 | GitOps drift detection (Argo CD / Flux class) | Desired state versioned in git; a reconciler diffs live vs declared per resource and surfaces OutOfSync; sync is a separate, gated act | Declared state = parity manifest + deploy manifest + `.methodology.yaml`; a run-on-demand/nightly differ emits per-surface verdicts; NO controller, NO auto-sync (convergence stays in operator-ratified deploy runs) | floor sha256 sidecar + `floor-hash-verify` (hash-guarded replica); `roster-freshness` regen-and-diff gates |
| 2 | Config-management check mode (Ansible `--check/--diff`, Puppet noop class) | Idempotent desired-state modules with a dry-run that reports would-change per item; drift report ≠ enforcement | The checker is PERMANENTLY check-mode; `deploy/tool.py` carriers keep the apply/verify/detect legs | carrier detect/verify verdicts (PRESENT_CORRECT / DRIFTED / ABSENT) |
| 3 | Policy-as-code (OPA/conftest class) | Rules evaluated over structured input yielding deny/warn + message; policy separate from data; EXCEPTIONS are data with expiry | Rules as YAML rows (surface, tier, probe) + a small Python evaluator inside the audit battery; no rule DSL/engine (platform tripwire); waiver-with-shelf-life is the exception model | `disposition-register.yaml` (signature-keyed match, ADR-75 stale decoration, `auto_clearable_by`); `.methodology.yaml` `review_date` |
| 4 | Renovate/Dependabot class | Version manifest-of-record; scheduled drift detection; PROPOSAL artifacts, never silent auto-merge; central presets + per-repo config | Hub-recommended pinned-dep manifest carried with the methodology package; comparator reads consumer pyproject/venv; proposals = WARN rows in the digest; zero auto-bumps | `ecosystem/deployed-versions.yaml` + `tool-versions.yaml` (committed, written-by-command, read-by-check) |
| 5 | Monorepo workspace conformance (Nx conformance / Rush repo-policies class) | Named workspace-level lint rules over project graph + configs, run as a gate, with per-project opt-outs RECORDED | The #328 decision tree IS workspace-lint for a poly-repo fleet; opt-out = `.methodology.yaml` declaration; tiers = intake #12 | `validate_backlog`, `validate_hermetization`, boundary_report — per-surface lints awaiting one manifest |
| 6 | Heartbeat / dead-man's-switch (healthchecks-class), audit-log lineage (syslog/CEF) | Silence is only detectable against an expectation: expected-fire schedule + observed-fire log → silence alarm; audit events are append-only, minimal, uniform | The FR-9 expectation-join; one flat event shape for every organ class; append-only JSONL per repo | `enforcement_coverage` fire_test (CAN-fire proof) — telemetry adds the DID-fire half |
| 7 | Store/viewer discipline (log-file + embedded-DB class) | Flat files as source of truth; embedded DB as disposable derived index; viewers read, never own | JSONL = record of truth; SQLite/DuckDB-class only as FR-18 rebuildable index; one local-HTML viewer (intake #9) | committed digests (FLEET-HEALTH et al.) as today's "viewer" |

**Cross-cutting invariants extracted:** (1) desired state is versioned data in git; (2) checkers are read-only, deterministic, diff-shaped; (3) exceptions are first-class data with expiry and stale-surfacing; (4) detect-and-propose, never auto-converge; (5) identity is canonical ids, not names or byte-shapes; (6) probes assert effect, not text; (7) silence needs an expectation model; (8) flat append-only records + derived disposable indexes.

# Annex C — Collection model at 3→8 repos: PULL vs PUSH

**PULL** = consumers write events/state only into their own tree (gitignored `logs/`); a hub-side read-only collector (nightly / on-demand) reads registered consumer paths and builds the digest. **PUSH** = consumer organs write to a hub-owned destination at fire time.

| Criterion | PULL | PUSH |
|---|---|---|
| Hermeticity | consumer knows nothing about the hub; zero egress config (FR-10) | every consumer carries a hub address — the S3 mis-addressed-pointer fragility class, times 8 repos |
| Failure blast radius | collector failure = stale digest only | write failure can break/slow the firing organ (violates fail-open; Stop legs run on 15s timeouts) |
| Windows reality | single reader, N independent local writers — no shared-lock surface | concurrent cross-process writes to one target; the pre-commit store-lock contention hang is the witnessed cost of shared write-targets on this box |
| Freshness | as fresh as collection cadence (nightly suffices for a single operator + #324 morning loop) | real-time — an advantage with no consumer at n=1 operator |
| Privacy | egress decided centrally at collection (one scope filter, FR-11) | each writer decides at fire time (N scope filters to keep correct) |
| Precedent | fleet_health, enforcement_coverage, boundary_report, nightly triage — the incumbent pattern, n≥4 organs | none in-fleet; the hardcoded marketplace path in consumer settings.json is the nearest analogue and is a known wart |
| Retention | one rotation/retention policy at the collector + local caps | scattered across writers |

**Verdict: NOT genuinely contested — RECOMMEND PULL** (proposal; operator/architect ratifies per the Phase E gate). Every standing doctrine — hermetization, fail-open organs, Windows lock avoidance, incumbent read-only fleet organs, single-operator nightly cadence — lands on PULL; PUSH's sole advantage (freshness) has no consumer at this scale. Sending a lopsided question to AI Council would be the manufactured ceremony the architect's own tension-log warns against. **Reopen tripwires (any one revives the fork):** the fleet spans machines (no shared local disk); a near-real-time consumer appears (e.g. cross-repo gating mid-session); a repo joins that the hub may not read (privacy boundary inversion).

# Annex D — Event-record requirements (constraints, NOT the schema — the schema is born in Phase A per intake #13)

The record MUST capture: timestamp (UTC ISO-8601) · repo · **canonical organ id** (FR-2) · organ class (pre-commit / commit-msg / pre-push / session-start / stop / nightly-check / command) · trigger · outcome (aligned with Finding statuses + block/skip/error, FR-16) · HEAD sha at fire · schema version · optionally a bounded evidence one-liner (metadata-only, FR-11). Emission MUST be: fail-open (never breaks the organ), append-only single-line writes, repo-local gitignored, rotation-capped (FR-8/FR-13). Non-firing is NOT an event — silence is computed by the FR-9 expectation-join, never logged by the silent party. Least-commitment stands: field names, file layout, and any store/viewer remain Phase A/E build decisions; this annex only pins what the record must be able to answer (S1–S6).

# Annex E — Traceability register

| Tag | Evidence (path + locus) |
|---|---|
| W1 | Stop-organs fired in corp / silent in ai-council — operator-witnessed 2026-07-12 (session brief); presence-parity verified this session: `ai-council/.claude/settings.json` + `corp-monorepo/.claude/settings.json` carry identical Stop wiring (seb + tier1 plugin); silence-class mechanism on record: ai-council JOURNAL 2026-07-08 (G8 venv-`python` SessionStart leg failed silent); doctrine already written: `scripts/enforcement_coverage.py` docstring ("registered and structurally 'wired' yet … only RUNNING it tells enforcement from inert") |
| W2 | pytest-xdist hub-present / consumer-absent, suite silently serial — BACKLOG #332 witnessed-trigger clause; hub JOURNAL 2026-07-12 (#332 filing); ai-council JOURNAL 2026-07-12 ×2 ("Full serial suite 444 passed") |
| W3 | Pruned ruff gate re-activated on a mis-addressed cross-repo pointer — ai-council JOURNAL 2026-07-12 "ruff-gate RE-ACTIVATION" (premise correction: pointer was hub-side, mis-addressed as local; reverses documented prune [#244] deploy `31e785d`; operator ruled re-activate knowingly) |
| W4 | Prune-safety byte-shape (bare `id: ruff`, no `name:`) deliberately carried in BOTH consumers so the hub remove-leg refuses rather than deletes — ai-council JOURNAL 2026-07-12; corp JOURNAL 2026-07-12 "delete docs/diagrams + unify ruff + adopt .vscode" |
| W5 | `.gitignore` inline-comment gotcha: negation pattern textually present, semantically inert; caught by `git check-ignore` hand-verification — corp JOURNAL 2026-07-12 (same entry, "Gotcha caught & fixed mid-run") |
| W6 | Divergence classes + verdict grammar + the manual walk to automate — `docs/audits/2026-07-11-technical-fleet-parity-register.md` (§0 rows a1–g2/M, §9 design, §10 verb-ruling summary); `docs/audits/2026-07-11-technical-fleet-structure-comparison.md`; **W6-d1** = the three-way port review `codex-casing-review-out.md` (1 behavioral / 10 cosmetic; verdict CLEAN) |
| W7 | presence ≠ enforcement ≠ usable; A0 exit leg (b) WITNESSED operational minimum; manual witness cost per repo — intake #13 v4 Phase A0; SUPPLEMENT ANSWERS A1/A2; ai-council + corp JOURNAL 2026-07-12 d1 entries (throwaway-commit trip-tests as today's manual telemetry) |
| W8 | Scale 3→5-8+; 6 repos already digested; parallel-prepend merge-conflict class — intake #13 v4 Phase E; `logs/FLEET-HEALTH.md` 2026-07-12 run (6 repos, absent-organs column); hub JOURNAL 2026-07-12 #330 integration (JOURNAL prepend collision resolved newest-first) |
| R1 | `docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` v4 — Architecture frame (binding), Phase A (#328, JSONL born, least-commitment), Phase E (Leg 0 pack, decision gate, libraries-not-platforms posture) |
| R2 | `docs/intake/2026-07-11-tech-ownership-manifest.md` (intake #12) — tier vocabulary MUST/SHOULD/LOCAL/IGNORE + inverse rules; fidelity "present ≠ carried"; the nightly decision tree |
| R3 | BACKLOG #328 (charter: parity-surfaces.yaml + WARN-only fleet_parity extending `enforcement_coverage.py`; §9a hub `.methodology.yaml`; §9b advisory review_date) + #332 (dep-parity leg) |
| R4 | `ecosystem/disposition-register.yaml` (signature-keyed suppression, precision-over-recall, ADR-75 stale decoration, `auto_clearable_by`) + `scripts/enforcement_coverage.py` (verdict honesty: enforcing-local / absent / hub-scoped; static = pre-filter, fire_test = truth-maker) |
| R5 | intake #13 Phase A event seed (JSONL: repo, check, severity, verdict, sha, ts) + standing store/viewer ruling (JSONL + SQLite/DuckDB-class + one viewer) |
| R6 | SUPPLEMENT §3 CONSIDERED+REJECTED (binding): Grafana/Loki/ELK rejected permanently; hermetization posture; §2(e) ceremony-vs-lane (Council only on a genuine fork) |
| R7 | Live organ inventory + fail-postures — CLAUDE.md §9 / ARCHITECTURE Ch2 organ map; `logs/` digest corpus; pre-commit store-lock contention (witnessed hang class, LESSONS-carried) |
| R8 | Viewer/visualization boundaries — intake #9 (dashboards as local HTML), intake #10 (deferred architecture viz), #322/#324/#329 (dashboard, morning prompt, VS Code colors fed by the same manifest) |
