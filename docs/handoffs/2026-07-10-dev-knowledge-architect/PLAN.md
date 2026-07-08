<!-- scope: meta -->
> **PLAN.md — operator plan of record (plan-v3), copied into this bundle BY HAND.**
> Manual instance of the `#301` session-plan-artifact pattern (mode->artifact symmetry): the
> architect-mode PLAN.md generator feature is filed (2026-07-09 night run) but NOT yet built, so
> plan-v3 was copied in verbatim below. Source: the operator's
> `2026-07-09-program-plan-fleet-execution-v3.md` (supersedes plan v2). On close, the `#301` pattern
> calls for a RETROSPECTIVE fill here (done / not-done / incidents / carry-forward) — deferred to the
> generator build; for now the plan is read-only.

---

# PROGRAM PLAN v3 — Fleet Execution & Methodology Rollout
**Status:** SESSION RETROSPECTIVE + FORWARD PLAN · **Supersedes:** v2
**Session reviewed:** 2026-07-09-dev-knowledge-architect (executed 07-08/09 wall-clock)
**New drivers:** session incidents I1–I6 · operator directives OD1–OD4 (QA-in-process, proportional test depth, subagent utilization, night schedule)

## CHANGELOG v2 → v3
| Δ | Change |
|---|---|
| RETRO | §A added: full done/not-done/incident accounting for the executed session |
| OD1 | QA role arc formalized: EPIC G (intake → ADR → build → fleet carrier). Evidence register I1–I6 attached |
| OD2 | Proportional test-depth requirement keyed to existing T1–T5 scope-tags — routed into EPIC G intake as structural requirement |
| OD3 | Subagent/model-routing doctrine gap acknowledged (opusplan exists; deliberate Opus→Sonnet→Haiku orchestration is uncodified) → EPIC H (research + PLAYBOOK doctrine + carrier) |
| OD4 | Night schedule: routed to existing intake-id 8 (night-routines suite) — GATED by #270, which therefore RE-ENTERS admission (it now unblocks an operator-demanded capability) |
| NEW | EPIC I: docs-taxonomy hermetization (filed this session) — BEFORE Wave-2 |
| D-reg | D1 demoted to INTERIM (operator questioned twice) — final ruling in hermetization ADR d(i). D8 added (night-layer go/no-go rests on #270 + intake-8 triage) |

---

## §A — SESSION RETROSPECTIVE (vs v2 §4 plan)

### Done (planned)
| Item | Evidence |
|---|---|
| GATE-0 P2–P10 | all PASS; P10 bonus: mode-split already shipped → C rescoped finish-only |
| A-S1 #286 | 5dd2907 · [S1]–[S20] visible · validator grammar + tests · hub-only scope call RATIFIED |
| A-S2 #292 | filed, kill-candidate #117 · backpressure hook FIRST LIVE FIRING: correct |
| A-S3 runbook F5 | 6cf51a6 · markings [hub-runnable]/[consumer-only] + --run-date note |
| B-S1 ai-council pilot | 1bdc2ea · contract 10/10 · fire_test FIRED · gap-notes G1–G9 · fix-arc fba7b13 (SessionStart) — Wave-1 n=1 COMPLETE |
| C (#164) | closed 9e6ceb6 · legs {b-hub,e,g} built, rest evidenced · Done-when amended on record (fan-out → Wave arcs) · C-S3v2 matrix 7/8 · polish filed #298 |
| Consolidation | #294–#297 filed from gap-notes · census docs/handoffs amendment recorded · QA premise-grep (no QA role exists; TDD council-rejected; ADR-81 test-first contract is the nearest construct) |

### Done (unplanned, absorbed)
QA-bundle slug incident remediation (ephemeral pattern) · WMI machine fix (elevated, verified on real path) · git mid-merge incident recovery (in flight) · G8/G9 · temp-repo rule → machine memory.

### NOT done (carried forward)
| Item | Why | Carries to |
|---|---|---|
| F-S1 SEED-6 boundary triage | eaten by incidents | next architect session buffer |
| Step-6 educate/close + handoff | pending recovery + lived-QA returns + P7 | session close |
| P7 operator content verdict (3 modes) | operator's one-liner outstanding | closes EPIC C formally |

### Incident register (I*) — QA-intake EVIDENCE SET
| I | Incident | Lesson class |
|---|---|---|
| I1 | C-S3v1 shallow test (no matrix, no quality rubric) — caught by operator, not mechanism | test-depth unenforced |
| I2 | G8: runbook verify used shim interpreter, hook runtime uses .venv | verify ≠ runtime path |
| I3 | G9: WMI hang — import works, CLI hangs; machine-scoped | env-layer testing gap |
| I4 | dateless slug sailed through every gate (architect-authored) | convention without teeth |
| I5 | F-A: session reported "merged, GREEN" over an uncommitted MERGE_HEAD | premature closure / claim-vs-disk |
| I6 | F-B: maintenance commit in live checkout finalized foreign merge | session isolation unenforced |

---

## §B — PROGRAM STATE (epics)

| Epic | State |
|---|---|
| A visibility | ✅ CLOSED |
| B Wave-1 | B-S1 ✅ · B-S2 corp-monorepo NEXT SESSION (precondition: G8 runbook fix — layer-6 verify must invoke the hook's own command line) |
| C generator | ✅ technically closed · P7 operator verdict pending · #298 polish pegged |
| D e2e test | D-S1 evidence live (pilot + lived-QA exercise in flight) · D-S2 dedicated pass session +2 — MERGES INTO EPIC G protocol once QA role lands (no duplicate test doctrine) |
| E Wave-2 | unchanged; BLOCKED-BY EPIC I (hermetization) by design |
| F architect buffer | carried |
| **G — QA role (NEW)** | intake session = operator's next move (boot printed, evidence I1–I6 + requirements OD2 ready) → technical decomposition → ADR (role, protocol, report-gate) → build → FLEET CARRIER (PLAYBOOK + runbook legs, so every onboarded repo inherits it) |
| **H — subagent/model-routing doctrine (NEW)** | research spike (Task-subagent capabilities/costs/parallelism) → PLAYBOOK doctrine: default routing Opus=orchestration/judgment · Sonnet=bounded probes/mechanical · Haiku=cheap fan-out where quality floor allows → binds EPIC G's protocol (QA runs are the first consumer) |
| **I — docs hermetization (NEW, filed)** | ADR arc: sanctioned top-level set · per-class name grammar `<date>-<class>-<slug>` (audit classes: technical/functional/qa/census/verification) · pre-commit refusal gate · sub-rulings: d(i) runbooks location · d(ii) mode-boot bundle home · d(iii) audit classes. PEG: BEFORE Wave-2 |

## §C — Decisions register (delta)
| ID | Decision | State |
|---|---|---|
| D1 | docs/runbooks location | DEMOTED to interim-keep → final in hermetization ADR d(i) |
| D6 | life-architect privacy gate | STANDING (unchanged, hard) |
| D7 | terminal-setup in Wave-2 | standing recommendation: include |
| **D8** | night-layer go/no-go: after #270 lands + intake-8 triage; unattended = proposal classes only, NEVER autonomous merges | operator rules at that gate |
| P7 | 3-mode content verdict | OPERATOR — one line, closes EPIC C |

## §D — NEXT SESSION PLAN (architect, fresh chat via generated architect bundle)
| Step | What | Notes |
|---|---|---|
| 0 | Boot from /handoff architect bundle (dogfood) + probes | |
| 1 | G8 runbook fix (small, serial) | gates B-S2 |
| 2 | B-S2 corp-monorepo onboarding (dedicated chat, plan-first) | n=2 runbook gate · D4 surface · #262 tool-managed n≥1 target · runs the SEEDER (leg-b fan-out first consumer) |
| 3 | ∥ hub: QA intake decomposition (after operator's functional session) → ADR draft + EPIC G stories | admission: #270 re-enters (unblocks OD4) |
| 4 | ∥ hub: hermetization ADR (EPIC I) if capacity | else session +2, still before Wave-2 |
| 5 | F-S1 SEED-6 boundary (carried) | buffer |

## §E — Session close conditions (this session)
Recovery report GREEN + pushed · lived-QA exercise report reviewed · P7 received · educate artifact delivered · architect close-out handoff generated (dogfood) — then this chat wraps per context self-eval (a).
