---
intake-id: 13
status: plan-of-record-active
revision: v3
origin: architect, 2026-07-11 session wrap
consumed-by:
note: "the incoming sessions' comparison baseline per #301(iv) + the A-F build sequence; Phase A charter = intake #12"
delta-note: "operator re-sequencing — Phase A0 manual template consolidation inserted before #328; plus v2's requirements-first Phase E + Council gate"
---

# Plan-of-record — Fleet Hygiene System build (post 2026-07-11 session)
> REVISION v3 (supersedes v1/v2 — delta vs v2: operator re-sequencing 2026-07-11: NEW Phase A0 (manual template consolidation) inserted BEFORE #328; the checker encodes a SETTLED template instead of chasing a moving target. v2 delta retained: Phase E requirements-first + Council gate; Phase A JSONL least-commitment). Authored by the architect at the 2026-07-11 session wrap; operator-approved framing: the hub is a SIEM-class information system (sensors → event pipeline → rules engine → dashboards → response). This document is the incoming sessions' comparison baseline (#301 iv) and the build sequence. Each phase: goal + exit criteria; strictly ordered unless marked parallel.

## Architecture frame (binding)
Sensors = per-repo gates + nightly legs · Event pipeline = ONE structured event schema (JSONL: repo, check, severity, verdict, sha, ts) emitted by every check · Rules engine = audit.py + the #328 decision tree · Inventory = ownership manifest (intake #12) + REGISTRY + deployed-versions.yaml · Presentation = #322 dashboard + #329 VS Code layer · Response = #324 morning prompt. Open-source posture: libraries not platforms (JSONL + SQLite/DuckDB-class store + one viewer); full SIEM stacks rejected as oversized.

## Phase A0 — TEMPLATE CONSOLIDATION (manual, operator-ruled) — runs FIRST
Operator re-sequencing: before any checker exists, the three repos are brought to ACTUAL conformance with one template, by hand, in a fresh session. Worklist = the fleet-parity register + the ownership manifest (intake #12). The session walks every open row and the operator rules each pending decision on the spot: (1) audit filename convention winner (hub lowercase vs corp _AUDIT_) + rename plan for existing files IF ruled (ADR-100 referential-currency scan gates any move); (2) ONE ruff-config form (three exist today); (3) .vscode — carried template or local; (4) consumer BACKLOG schema (#331) — E-prefix/S-n story-map applied to ai-council + corp if ruled; (5) command-roster target (codex-review leftover archived; evolve/save disposition per #325); (6) CLAUDE.md archived-reference cleanup (#330 applied — boot etc. → templates/archive); (7) any remaining register rows to parity or declaration. Dependency hygiene named by the operator (doc2doc, doc2file, doc2code, code2code) is checked per-edit via the existing edge validators. Exit: all three repos conform; every remaining divergence is a .methodology.yaml declaration; the ownership manifest is promoted from DRAFT to the settled template.

## Phase A — #328: ownership manifest + fleet_parity check (THE root mechanism)
Charter: intake #12 — as PROMOTED by Phase A0 (the checker encodes the settled template; no open rulings remain by construction). Build: manifest file (hub, per-role tiers MUST/SHOULD/LOCAL/IGNORE + inverse rules) · the decision-tree walker as an audit check (WARN-only v1 per §9b; hub included per §9a) · **each verdict emitted as a structured event (the JSONL schema is born here)**.
Exit: check runs on all three repos; today's six known deviations (temp/, ruff-config triple-form, corp protocols/, docs/diagrams, .vscode ruling, audit-naming clash) each appear as a WARN or a declared row — zero silent passes. Event emission is deliberately LEAST-COMMITMENT (JSONL sidecar, schema free to evolve; store/viewer decisions belong to Phase E after requirements) — Phase A does not pre-commit any observability architecture. Candidate FIRST Codex-producer pilot task (bounded, testable) with CC-verifies contract (EPIC-H).

## Phase B — #324 codification: nightly routine + morning prompt (the response loop)
Night batch runs the #328 walker + existing hygiene legs, writes the verdict-sheet FROM the event log; standard morning prompt consumes it (review → consolidate → decide).
Exit: one full night→morning cycle executed on real state; routine doc + prompt template committed.

## Phase C — manifest rev v1.4.0 (carrier debt paydown) — parallel-safe with B
(1) #315 durable INSTALL.md carrier (retires both consumers' interim copies) · (2) re-scope/remove toc-freshness/toc-generate from the fleet-generic set (corp's report-back finding) → RETIRE the consumer hub-toc-hooks waivers · (3) /save command carrier (#325). One release cut, tag-ancestry verified (the v1.3.1 lesson), rollout to both consumers.
Exit: consumers upgraded; waiver count DROPS (the system's first self-cleaning).

## Phase D — manifest consumers (after A): #329 VS Code ownership colors (generated from the manifest, never hand-set) · #331 consumer BACKLOG schema ruling+apply · #330 root-archive rule (+ the CLAUDE.md archived-refs cleanup it mandates) · #327 protocols-as-interface genre ruling + minimal start (README + one interface doc per repo; corp gets protocols/, closing #314).

## Phase E — observability layer: REQUIREMENTS FIRST, then dashboard (#322)
Operator scale concern (2026-07-11): fleet grows to 5-8+ repos; beyond gate verdicts he wants methodology-ADOPTION telemetry (are carried hooks/skills/gotchas actually USED per repo?) and hub-side collection of consumer logs. Leg 0 therefore = a functional-requirements pack (night-leg authored, operator-ruled): event sources + volumes inventory · the questions the operator wants answered · collection model (hub PULL vs consumer PUSH — hermetization implications) · retention · privacy/scope of what consumers expose. ARCHITECTURE DECISION GATE: if the requirements reveal a genuine fork, it goes to AI Council WITH the requirements as material; if not, the architect rules (libraries-not-platforms posture stands: JSONL events + SQLite/DuckDB-class store + one viewer; full SIEM stacks pre-rejected as oversized for this scale). Only then the dashboard build. Visualization of SYSTEM ARCHITECTURE stays deferred (intake #10 is the reopen input) — the dashboard is operational state, not architecture diagrams.

## Phase F — EPIC-H doctrine write-up: Opus/Sonnet/Haiku + Codex sol/terra/luna variant-routing, evidenced by this session (night batch, worktree pair, Codex A3/A4 hit-rate, refuted delete-candidate) + the Phase-A pilot outcome.

## Standing rules carried forward
Consumer rollouts pin TAGS — verify fix-ancestry per tag · architect-produced artifacts are intaken in the same breath · no ticket = didn't happen (both directions) · hub is a fleet role, not an exception · every divergence declared or fixed, never silent · serialization: one merge per repo at a time, operator is the gate.

## Deviation log of the authoring session (for the wrap comparison)
Release-cut phase missing from the original plan (v1.3.1 cut mid-session) · register/consolidation elevated to headline mid-session by operator feedback (plan v3 revision) · #326 hub+ai-council legs were verified no-ops (prior arcs #262/ADR-51 had done the work) · corp carried the only real ToC/Mermaid removal.
