<!-- scope: meta -->
> **PLAN.md — operator plan of record, copied into this bundle BY HAND.**
> Manual instance of the `#301` session-plan-artifact pattern (mode→artifact symmetry): the
> architect-mode PLAN.md generator feature is filed but NOT yet built (DEFER, peg #298), so the
> plan is hand-authored below. Source: the operator-approved **ARC 4 fleet-equalization prompt
> file** (operator-held, off-repo) + this session's seven operator rulings (carried VERBATIM in
> `SUPPLEMENT.md` ANSWERS). On close, the `#301` pattern calls for a RETROSPECTIVE fill here
> (done / not-done / incidents / carry-forward) — deferred to the generator build; for now the
> plan is read-only. **Never pasted into the browser** — bundle-resident reference only.

---

# PROGRAM PLAN — ARC 4: Fleet Equalization
**Status:** FORWARD PLAN · **Mode:** architect · **Date:** 2026-07-18
**Plan-of-record for:** the next `.dev-knowledge` architect session (successor to the
2026-07-18 serial-integration close-out)
**Binding inputs:** the operator-approved ARC 4 prompt file (off-repo) + rulings RULING-W /
RULING-S / RULING-PY / RULING-CF + the `#329` and `#341-R2` design inputs + the satellite
freeze — all in `SUPPLEMENT.md` ANSWERS (verbatim).

---

## §A — THE GOAL (universalization) and THE ARC (ARC 4 as its first application)

**The goal above all others (operator-dictated, `SUPPLEMENT.md` ANSWERS):** **UNIVERSALIZATION** —
a single fleet-wide pattern for system architecture, file naming, folder structure, and file
structure, AND a universalized DEPLOYMENT of that pattern, so every repo is manageable from the
center and improvable uniformly. Operator's bar: *"I never again want to ask why files differ
between repos."* The methodology ladder has climbed explain→consolidate→document→ENFORCE; this
cycle enters **AUTO-DEPLOY and MANAGE**.

**ARC 4 (equalize corp-monorepo + ai-council) is the FIRST APPLICATION of the pattern, not the
goal itself.** Every align must, where possible, land as **manifest / template / carrier material
that REPLICATES onto the next repo** — not a one-off file fix. Dep/test-library parity counts as
structure (a missing pytest library slowed one repo's tests). This is the ecosystem crossing from
**hub-only enforcement to a fleet mesh** (ADR-28 Layer-2), enabled by **RULING-W**: the read-only
hub becomes one that can WRITE into consumers under a **mechanism-first** discipline.

**The operator priority program** (dictated 2026-07-18, full text in `SUPPLEMENT.md`): (1)
universalization of structure + deployment; (2) formalize the engineering loop end-to-end (intake
→ functional requirements → ADR → implementation → dynamic testing → review → close + REAL
deletion — the junkyard/tombstone pain, a sanctioned safe-deletion pattern wanted); (3) night
routines + configured multiagent workflows + backlog grooming as routine; (4) mechanize
session-discipline inheritance (a fresh browser inherits the test-then-close gate, never operator
reminders); (5) handoff-process refinement — explicitly LAST.

**Hard opening constraint (RULING-W).** The FIRST step of ANY consumer leg is to **codify the
consumer-write mechanism as the ADR-36/41 amendment** — mechanism before act. No equalization
edit into a consumer tree happens before that amendment lands. Every consumer write goes
**separate worktree/branch → report**, never a direct push into a consumer checkout.
**Re-witness BOTH consumers live** before touching them — their HEADs moved repeatedly; never
edit from a stale ledger.

## §B — DECISIONS ALREADY MADE (do not relitigate)

| ID | Decision | State |
|---|---|---|
| RULING-W | Hub MAY/SHOULD write into consumers for methodology/cleanup; worktree/branch → report; mechanism (ADR-36/41 amendment) FIRST | BINDING |
| RULING-S | Every governed file gets reader-visible universal-vs-personal sections; machine markers alone insufficient | BINDING |
| RULING-PY | ruff baseline = py311 (corp floor); "always newest Python" → a filed fleet-upgrade ticket | BINDING |
| RULING-CF | ai-council adopts the conformance workflow | BINDING |
| #341-R2 | Codex producer-activation = sanctioned repo-local `AGENTS.md` override; per-run flag REJECTED (witnessed evidence) | RULED — build, not design |
| #329 | Editor-side background decoration of owner=hub/repo regions via versioned `.vscode` (grey/navy, dark theme) | DESIGN INPUT |
| Satellite wave | FROZEN until corp + ai-council lessons extracted | STANDING |

## §C — NEXT SESSION PLAN (architect, fresh chat via this bundle)

| Step | What | Notes / gate |
|---|---|---|
| 0 | Boot from `PASTE_THIS.md` + work the probes (P1 orient → beat → residual → P2–P9) | dogfood; §13(d) beat NARROWS (supplement filled) |
| 1 | **ADR-36/41 amendment — the consumer-write mechanism (RULING-W)** | the mandatory FIRST consumer-leg step; mechanism before any equalization edit |
| 2 | Re-witness corp-monorepo + ai-council live (git/JOURNAL/BACKLOG/hooks) | consumer state may have moved; read-only until step 1 lands |
| 3 | ARC 4 equalization legs per the operator prompt file — worktree/branch → report per consumer | RULING-CF: ai-council conformance workflow adoption is one leg |
| 4 | RULING-S / #329 — reader-visible governed-file sections + `.vscode` region decoration design | the human-legibility half of the owner=hub/repo boundary (#312) |
| 5 | File the RULING-PY fleet-upgrade ("always newest Python") ticket | not yet filed |

## §D — OPEN QUEUE (execution tickets — advance as ARC 4 bandwidth allows)

| # | Item | Peg / note |
|---|---|---|
| #344 | Session-close gate (Ask 1) + consumer hub-write guard (Ask 2) — NEEDS-RULING | RULING-W defines the write path Ask 2 must ALLOW; `block-onedrive` shape precedent (#289) |
| #341 / #338 | Codex producer-lane (build — R2 ruled) / reviewer-path drift consolidation | disjoint codex threads; #341 = witness `AGENTS.md` precedence + guardrails + PLAYBOOK §16 reconcile |
| #339 | LESSONS legacy-split BUILD leg | ADR-29 chronological-archival amendment ratified in docs; execute the split once (byte-identical, test proving zero entry-body change) |
| #342 | fleet_parity gate-ahead max-fidelity hardening (3 items) | deferred #336/ADR-102; serialize-group audit-py |
| #343 | fleet_parity ship-gate-only perf scoping (RIDER-2) | the ~8s walk should not tax every pre-commit; existing skip-flag pattern |
| #300 | Hermetization residual — **d.i runbooks / d.ii mode-boot home** open; **d.iii audit-class grammar COVERED by ADR-101 → closeable** | DEFER — peg BEFORE Wave-2 |
| triage | 15 nightly findings await (#47…#19, Issues tab) | night-triage backlog; surface + triage |
| new | **Safe-deletion pattern** — sanctioned real-deletion path to end the freeze/tombstone junkyard (extends the proof-then-delete ruling on #122); design question, not yet ruled | priority-2 (loop formalization) |
| new | **Functional-architect role/session** — a functional-requirements session that seeds the BACKLOG (intake → functional reqs leg of the loop) | priority-2 |
| new | **Night-workflow configuration** — configured self-orchestrated Sonnet/Haiku fan-out (no ultracode) + backlog grooming + Q&A as routine, not per-session improvisation | priority-3 |
| new | **Session-discipline inheritance** — a fresh browser inherits the test-then-close gate from a mechanism, never operator reminders | priority-4 |
| new | **fleet-Python-upgrade ticket** (RULING-PY "always newest Python") — unfiled | file next session |

## §E — SESSION CLOSE CONDITIONS
Consumer legs each reported (worktree/branch → report, RULING-W) · ADR-36/41 amendment landed
before any consumer edit · ship-gate GREEN · JOURNAL entry with session SHAs · architect
close-out handoff generated (dogfood) · RETROSPECTIVE fill deferred to the #301 generator build.
