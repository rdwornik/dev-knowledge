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

## §A — THE ARC (what ARC 4 is)

Bring the Wave-1 consumers (**corp-monorepo**, **ai-council**) into methodology parity with
the hub — harvest their lessons, then propagate. This is the ecosystem crossing from
**hub-only enforcement to a fleet mesh** (ADR-28 Layer-2). The enabling doctrine is **RULING-W**:
the read-only hub becomes one that can WRITE into consumers under a **mechanism-first**
discipline.

**Hard opening constraint (RULING-W).** The FIRST step of ANY consumer leg is to **codify the
consumer-write mechanism as the ADR-36/41 amendment** — mechanism before act. No equalization
edit into a consumer tree happens before that amendment lands. Every consumer write goes
**separate worktree/branch → report**, never a direct push into a consumer checkout.
**Re-witness each consumer live** before touching it — state may have moved since the last window.

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
| #300 | Hermetization residual (d.i runbooks / d.ii mode-boot home / d.iii audit-class grammar) | DEFER — peg BEFORE Wave-2 |
| triage | 15 nightly findings await (#47…#19, Issues tab) | night-triage backlog; surface + triage |

## §E — SESSION CLOSE CONDITIONS
Consumer legs each reported (worktree/branch → report, RULING-W) · ADR-36/41 amendment landed
before any consumer edit · ship-gate GREEN · JOURNAL entry with session SHAs · architect
close-out handoff generated (dogfood) · RETROSPECTIVE fill deferred to the #301 generator build.
