# LANE lane-g-000-autonomy-synthesis — Read all five AUTONOMY research artifacts TOGETHER and emit ONE synthesis: funnel reconcile, overlap adjudication, unknowns, a ranked decision table, and the equilibrium checkpoint list scored against live organs.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-g-000-autonomy-synthesis LANE-g-000-autonomy-synthesis.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-g-000-autonomy-synthesis · lane-g-000-autonomy-synthesis]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-g-000-autonomy-synthesis` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-g-000-autonomy-synthesis` -> branch `worktree-lane-g-000-autonomy-synthesis` -> contract `LANE-g-000-autonomy-synthesis.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

**ONE new file only:** `docs/audits/2026-08-29-technical-autonomy-synthesis.md`.

This lane is READ-ONLY over everything else. It **proposes**; the integrator's filing pass acts.
**ZERO rows born** — no `tasks/` edit, no intake, no ADR, not even a draft. If a hook or closure
proposal invites one, decline and say the lane is read-only by contract.

## Done-contract (immutable)

1. **ONE synthesis artifact** carrying all five sections below. Its inputs are the five AUTONOMY
   artifacts on `main`, read TOGETHER — the whole point is what no single lane could see:
   `docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md`,
   `-aut-r2-decision-quality-frameworks.md`, `-aut-r3-repo-as-reinforcement-environment.md`,
   `-aut-r4a-harness-evals-observability.md`, `-aut-r4b-orchestration-memory-loop.md`.
   Each carries a PROVENANCE header naming its receipt id; cite artifacts by filename.
2. **(a) PER-FINDING FUNNEL RECONCILE.** Every proposal in the five gets exactly one verdict:
   **already-in-intake** (candidates include #62 L0-as-governed-layer, #63 per-repo learning loop,
   #38 root-contract, #17, #22, #29 — resolve each by reading `docs/intake/`, do not trust this
   list), **already-in-ADR**, **already-a-row** (candidates include `[#616]` flip-condition,
   `[#617]` file-distillation, `[#619]` FM coupling — again, verify), or **TRUE GAP**. Cite the
   object for the first three. A verdict with no locator is not a verdict.
3. **(b) OVERLAP ADJUDICATION.** R3's library-first appendix and R4-B overlap on several
   candidates. **Apply R4-B's own trust paragraph** — find it, quote it — to pick the deeper
   verdict per candidate, and **SAY WHICH ARTIFACT WAS USED** for each. Do not average them.
4. **(c) THE THREE UNKNOWNS — PPI, nasde, tracys — carried VERBATIM**, each marked RESOLVED (with
   what resolved it) or UNKNOWN. Do not quietly drop one, and do not invent a resolution.
5. **(d) DECISION TABLE for the architect:** each proposed adoption with its verdict enum, the
   **cheapest ADR-112 experiment** that would settle it (Tier-L evaluate / Tier-S try-and-delete),
   and **Windows-wheel + pinned-`uv` installability** (`required-version = "==0.11.19"`; the
   `rustworkx` precedent is the bar). **Ranked by fit x value.**
6. **(e) THE EQUILIBRIUM CHECKPOINT LIST from R3, scored against LIVE organs**, each PRESENT (with
   a locator) / PARTIAL (with what is missing) / ABSENT. **BLIND SPOTS FIRST** — the ABSENT column
   leads the section. Do not pad the PRESENT column; an over-generous score makes it useless.
4. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Read all five artifacts and take notes; do not start writing until all five are read. **COMMIT**
   is not taken at this step — nothing has changed yet.
2. Write the synthesis, section by section, resolving each funnel verdict against the live tree as
   you go rather than from memory of the artifacts. **COMMIT**
3. Re-read your own decision table against the repo one final time: every cited object resolves,
   every verdict has a locator, every unknown is marked. Fix what does not. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
