---
intake-id: 13
status: plan-of-record-active
origin: architect, 2026-07-11 session wrap
consumed-by:
note: "the incoming sessions' comparison baseline per #301(iv) + the A-F build sequence; Phase A charter = intake #12"
---

# Plan-of-record — Fleet Hygiene System build (post 2026-07-11 session)
> Authored by the architect at the 2026-07-11 session wrap; operator-approved framing: the hub is a SIEM-class information system (sensors → event pipeline → rules engine → dashboards → response). This document is the incoming sessions' comparison baseline (#301 iv) and the build sequence. Each phase: goal + exit criteria; strictly ordered unless marked parallel.

## Architecture frame (binding)
Sensors = per-repo gates + nightly legs · Event pipeline = ONE structured event schema (JSONL: repo, check, severity, verdict, sha, ts) emitted by every check · Rules engine = audit.py + the #328 decision tree · Inventory = ownership manifest (intake #12) + REGISTRY + deployed-versions.yaml · Presentation = #322 dashboard + #329 VS Code layer · Response = #324 morning prompt. Open-source posture: libraries not platforms (JSONL + SQLite/DuckDB-class store + one viewer); full SIEM stacks rejected as oversized.

## Phase A — #328: ownership manifest + fleet_parity check (THE root mechanism)
Charter: intake #12 (docs/intake/2026-07-11-tech-ownership-manifest.md). Build: manifest file (hub, per-role tiers MUST/SHOULD/LOCAL/IGNORE + inverse rules) · the decision-tree walker as an audit check (WARN-only v1 per §9b; hub included per §9a) · **each verdict emitted as a structured event (the JSONL schema is born here)**.
Exit: check runs on all three repos; today's six known deviations (temp/, ruff-config triple-form, corp protocols/, docs/diagrams, .vscode ruling, audit-naming clash) each appear as a WARN or a declared row — zero silent passes. Candidate FIRST Codex-producer pilot task (bounded, testable) with CC-verifies contract (EPIC-H).

## Phase B — #324 codification: nightly routine + morning prompt (the response loop)
Night batch runs the #328 walker + existing hygiene legs, writes the verdict-sheet FROM the event log; standard morning prompt consumes it (review → consolidate → decide).
Exit: one full night→morning cycle executed on real state; routine doc + prompt template committed.

## Phase C — manifest rev v1.4.0 (carrier debt paydown) — parallel-safe with B
(1) #315 durable INSTALL.md carrier (retires both consumers' interim copies) · (2) re-scope/remove toc-freshness/toc-generate from the fleet-generic set (corp's report-back finding) → RETIRE the consumer hub-toc-hooks waivers · (3) /save command carrier (#325). One release cut, tag-ancestry verified (the v1.3.1 lesson), rollout to both consumers.
Exit: consumers upgraded; waiver count DROPS (the system's first self-cleaning).

## Phase D — manifest consumers (after A): #329 VS Code ownership colors (generated from the manifest, never hand-set) · #331 consumer BACKLOG schema ruling+apply · #330 root-archive rule (+ the CLAUDE.md archived-refs cleanup it mandates) · #327 protocols-as-interface genre ruling + minimal start (README + one interface doc per repo; corp gets protocols/, closing #314).

## Phase E — #322 fleet dashboard: renders the Phase-A event log (fleet level = Context: registry+versions; repo level = parity/gate state). Leg 0 = the buy-vs-build library decision (operator rules). Visualization of SYSTEM ARCHITECTURE stays deferred (intake #10 is the reopen input) — the dashboard is operational state, not architecture diagrams.

## Phase F — EPIC-H doctrine write-up: Opus/Sonnet/Haiku + Codex sol/terra/luna variant-routing, evidenced by this session (night batch, worktree pair, Codex A3/A4 hit-rate, refuted delete-candidate) + the Phase-A pilot outcome.

## Standing rules carried forward
Consumer rollouts pin TAGS — verify fix-ancestry per tag · architect-produced artifacts are intaken in the same breath · no ticket = didn't happen (both directions) · hub is a fleet role, not an exception · every divergence declared or fixed, never silent · serialization: one merge per repo at a time, operator is the gate.

## Deviation log of the authoring session (for the wrap comparison)
Release-cut phase missing from the original plan (v1.3.1 cut mid-session) · register/consolidation elevated to headline mid-session by operator feedback (plan v3 revision) · #326 hub+ai-council legs were verified no-ops (prior arcs #262/ADR-51 had done the work) · corp carried the only real ToC/Mermaid removal.
