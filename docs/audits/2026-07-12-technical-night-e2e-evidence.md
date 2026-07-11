# E2E consumer-lifecycle gauntlet — captured evidence

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-12
- **Source-session:** night-batch 2026-07-11→12, Phase 2.5 (E2E-1/E2E-2)
- **Status:** complete — 10/11 stages green, 1 conditional SKIP (documented)
- **Model:** claude-opus-4-8 (orchestrator); gauntlet is deterministic Python (no model in the loop)

## Executive so-what

A THROWAWAY synthetic consumer lived the ENTIRE methodology lifecycle end-to-end. **10 of
11 stage-checks PASS across 3 consecutive deterministic runs; 0 FAIL; 1 conditional SKIP**
(the HUB-ONLY `validate_hermetization` sub-check, which self-skips on a branch where #306
is not present and auto-activates once #306 merges). The full run — including that 3c
sub-check — went green 3× on `feat/306` where the hardened validator lives. The persisted
opt-in pytest (`tests/test_e2e_consumer_lifecycle.py`, `feat/e2e-lifecycle` `abcf8c2`)
reproduces 10/11 with 3c self-skipped. **Recommendation: ai-council rollout GO** — tomorrow's
grandfather + carrier-arm + reporter steps are now a rehearsed move, not a first attempt.

## E2E-0 — ai-council's enforcement-sandbox role (as designed vs as lived)

**As designed:** ai-council is the fleet's **n=1 onboarding pilot / enforcement-sandbox** — the
first consumer the deploy subsystem (ADR-91/92), the enforcement-transfer mesh (#235–#238), and
the v5 handoff-process were piloted against. Its pilot arcs are the hub's
`…-ai-council-measurement-2/3/4.md` audits (2026-07-05→07), which surfaced the pilot gaps still
open as BACKLOG #294 (validate_backlog carrier), #296 (audit --repo-path report), #297 (observe-arc
dry mode), #267 (armed-but-skipped scope witness). **As lived:** genuinely exercised, not nominal —
4 measurement arcs through 2026-07-07, its tracked `ecosystem/ai-council/state.yaml` shows
`last_audit: 2026-07-11` (a hub audit ran against it TODAY), and it is the sole consumer already
converged onto the ADR-66 story-map (#281). Role-as-designed ≈ role-as-lived: the sandbox is real.
**The one gap:** the enforcement MESH is measured (Informant rows), but the FIVE hub-only organs
(session_end_backpressure, canonical_freshness, doc_claims, git_backlog_drift, the coherence spine)
remain hub-only — the founding-standard gap epic S8 (#235–#238) exists to close. Tonight's E2E
rehearses the CARRIED gates (block-ff-push / backlog-id-on-close) that DO transfer; those five are
the un-transferred remainder.

## Findings (per-stage evidence, run-1 on feat/306; identical on runs 2-3)

Flat evidence table (fenced — render-layer discipline):

```
stage                        status  evidence
1-onboard                    PASS    consumer + bare origin scaffolded; origin/main established hook-free
2-arm                        PASS    3-stage install rc=0; present={pre-commit,commit-msg,pre-push}=True;
                                     populated (pre-commit signature) all True — the Surface-3
                                     armed-but-EMPTY defect did NOT reproduce
3a-blockff-logic             PASS    native-stdin gate REFUSED a direct-to-main commit (rc=1, "REFUSED")
3a-blockff-adapter           SKIP*   CAPTURE-ONLY Codex-#3 probe: real push via pre-commit pre-push
                                     adapter refused=True (rc=1) — the adapter DID catch the common
                                     single-ref push; empty-remote/multi-ref edges NOT exercised
3b-backlog-id                PASS    commit-msg gate BLOCKED a close-without-[#id] (rc=1, cited #999)
3c-hermetization             PASS    NEW off-grammar audit BLOCKED (casing); grandfathered MODIFY passed
                                     (prospective-only) — [self-SKIPs on feat/e2e-lifecycle, #306 absent]
4-positive                   PASS    compliant commit + compliant audit name both passed; block-ff
                                     ALLOWS a clean --no-ff merge (rc=0)
5-grandfather+6-match        PASS    marked consumer aligns to hub baseline: status=pass, "2 hub regions
                                     match", "1 project"
6-drift                      PASS    injected drift detected + NAMED region id: "drift: alpha"
6-parsewarn                  PASS    broken marker pair -> LOUD parse warning: "missing: beta [parse:
                                     ... id=beta ... never closed]"
7-teardown                   PASS    tmp removed; hub tree unmutated (baseline-compared)
```

`*` 3a-adapter is marked SKIP in the pytest port because it is **capture-only** (not
asserted — its outcome is scenario-dependent per Codex finding #3). The captured value
(refused=True) is recorded above, not asserted.

## Stability

3 consecutive standalone runs on `feat/306`: **10 PASS / 0 FAIL / 1 SKIP** each — fully
deterministic, no flakiness. Persisted as `tests/test_e2e_consumer_lifecycle.py` behind an
opt-in gate (`RUN_E2E=1` + `slow` marker) so it never taxes the fast ship-gate; verified it
SKIPs in a normal run and PASSes (78s) under `RUN_E2E=1`.

## Scope / method

- Sandbox: pytest `tmp_path` — a git repo + bare origin + isolated `PRE_COMMIT_HOME`; never
  a real consumer, never registered in the hub's tracked `ecosystem/` state (hard-limit held).
- Gates exercised via REAL `pre-commit install` (3 stages) + REAL git commits/pushes for the
  arming + firing checks; block-ff-push gate LOGIC additionally proven via a deterministic
  native-stdin probe (isolates the gate from the pre-commit pre-push adapter Codex flagged).
- The reporter (`boundary_report.run_report`) run against an isolated 2-region fixture hub +
  the synthetic consumer via monkeypatched `discover_repos`/`load_state`.
- **NOT covered** (honest boundary — fuller list from the E2E-3 Codex pass in the
  codex-review deliverable): the block-ff pre-push ADAPTER edge cases (empty-remote initial
  push, multi-ref push — Codex #3); a real deploy-manifest carrier install (the gauntlet
  wires hub scripts as `repo: local` hooks, not via `repo: <hub> rev:` clone); DRAFT /
  READY-FOR-TECHNICAL / REJECTED intake states in the reporter path; multi-consumer fleet
  diff; the actual v1.3.0 tag/rev (none cut — hard limit).
```
