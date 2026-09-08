# LANE lane-v-000-offload-admission — Admit the Copilot CLI offload route on seeded defects and verify LIVE that -Model reaches the dispatch line, so the route is gated rather than merely declared.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-offload-admission LANE-v-000-offload-admission.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #000 · lane-v-000-offload-admission]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-offload-admission` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-offload-admission` -> branch `worktree-lane-v-000-offload-admission` -> contract `LANE-v-000-offload-admission.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- the Copilot/offload admission gate and its seeded-defect suite
- read access to `ecosystem/provider-registry.yaml` (`copilot-enterprise`)

**Pinned OUT — another lane owns these, or nobody does:**

- `~/.claude/ROUTING.md` and any L0 surface — operational doctrine and the BILLING VERDICT
  live there, outside this repo, and this lane does not edit global infrastructure
- Copilot BILLING probing — ruled closed 2026-08-29: consumption meters to the enterprise org
  seat, a zero on the user premium-requests meter is CORRECT, and the ruling says
  **NO FURTHER PROBING from our side**
- `provider-registry.yaml` SCHEMA — it is a thin identity surface and forbids extra fields

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **This lane replaced V-7 by `AMEND-BATCH-V-002` §2**, applied before the manifest merged.
  V-7 (FPG-1 + `orphan_census`) was the only lane whose scope grew at step 0 — migration to
  BUILD, because `orphan_census` does not exist (intake #86, DRAFT) — and it would have built
  against an unratified spec. V-7 returns as V+1's first lane; `#86` joins Sitting 1's list.
- **Sitting 1 ratifies `#75`** (`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`).
  This lane is contracted now and its admission is the mechanism `#75` describes.
- Registry entry verified present at step 0: `copilot-enterprise`, `cli: copilot`,
  `version_command: [copilot, --version]`.

## Done-contract (immutable)

1. Copilot CLI admitted from `ecosystem/provider-registry.yaml` (`copilot-enterprise`,
   `cli: copilot`) **on SEEDED DEFECTS**, following the `[#627]` agy/Gemini admission
   precedent — an admission that passes only because nothing was broken proves nothing.
2. **LIVE verification that `-Model` reaches the dispatch line** — witnessed, not read off
   the code. This is a second seam test of the same class as the generator/verb defect: a
   declared-but-unbacked edge, measured rather than asserted.
3. seeded-defect cases that the admission REFUSES **0 -> N, N printed**; a seeded defect the
   route accepts is a FAIL, not a caveat.
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

1. PLAN round: the seeded-defect set, and where the admission gate lives. Those are the TWO
   budgeted forks; a third is a STOP.
2. Read `ecosystem/provider-registry.yaml` `copilot-enterprise` and the `[#627]` row as the
   admission precedent. Operational doctrine is NOT in the registry — it is L0
   (`~/.claude/ROUTING.md`) and out of this lane's reach. **COMMIT** the measurement.
3. Seed the defects and prove the route REFUSES each. An admission suite that only exercises
   the happy path is the thing `[#627]` exists to stop. **COMMIT**
4. Verify LIVE that `-Model` reaches the dispatch line. Witness it; do not infer it from a
   code read. **COMMIT**
5. PRINT N; targeted tests green against the 28-RED baseline; end-of-lane artifact.
   **COMMIT, then STOP.**

## What NOT to do

- Do not admit on a happy path. A seeded defect the route ACCEPTS is a FAIL.
- Do not infer `-Model` arrival from a code read — witness it live.
- Do not touch L0 (`~/.claude/`) or any global-infrastructure surface.
- Do not probe Copilot billing. Ruled closed 2026-08-29.
- Do not add fields to `provider-registry.yaml`; its schema forbids them.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- `ecosystem/provider-registry.yaml` -> `copilot-enterprise`
- `[#627]` — the agy/Gemini admission precedent (open)
- `docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md` (intake #75)
- `to-cc/AMEND-BATCH-V-002.md` §2 · `to-cc/DECLARE-DISPATCH-SEAM-AND-ENTERPRISE-2026-09-08.md`

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state
  predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge; the reviewer model name goes in the tally,
  and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`, as amended by
AMEND-BATCH-V-002 §2. The lane's authoritative surface is THIS file; a correction re-enters
as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*
