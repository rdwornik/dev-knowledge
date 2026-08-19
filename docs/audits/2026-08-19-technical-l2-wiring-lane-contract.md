# LANE L2 — [#529]/[#530] wiring — CONTRACT OF RECORD (ADR-110)

**Lane:** batch lane L2 · worktree `lane-l-529-wiring` · branch `worktree-lane-l-529-wiring`
**Mode:** execute — frozen contract, NO plan-mode · effort high · commit-and-STOP
**Serialize-group:** `audit-py` (sole audit-py lane; the seam lane boots only after this merge)

This file is the ADR-110 contract-of-record: the dispatch wrapper verbatim, plus the pointer to
the contract body it executes. It is committed FIRST, before any work, so what this lane was
told is a committed artifact rather than a recollection.

## Contract body — WHERE IT LIVES

The executable contract is the **item 5 fenced lane contract** inside

    docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md

on `main` (merge `52542a5d`, night-harvest merge of `15e3d861` = night lane N1). It is the fenced
block that opens `# LANE L2 — [#529]/[#530] WIRING: telemetry emission + single-flight call
sites` and runs to the closing `## WHAT NOT TO DO` list — frozen header, PINNED-BY-TESTS,
UNDERSTAND, STEPS 0–9 each with a `COMMIT` marker, FINAL, and 11 refusals.

It is NOT copied here. Copying a frozen contract into a second file creates two texts that can
disagree; the pointer cannot. The spec artifact is immutable (ADR-53 §5 rule 3), so the pointer
is stable.

**Executed verbatim, with the four architect amendments below overriding it on contact.**

## Dispatch wrapper — VERBATIM

```
# LANE L2 — [#529]/[#530] WIRING (executes N1's in-artifact contract, amended)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Your contract body lives IN THE REPO:** open
`docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md` (on `main`, merge `15e3d861`) and
execute its **item 5 fenced lane contract** verbatim — frozen header, PINNED-BY-TESTS,
STEPS 0–9 with COMMIT markers, FINAL, refusals — **with the four architect amendments below,
which override the artifact wherever they touch it.**
**ADR-110:** your STEP 0 contract-of-record commit = this wrapper file AND a pointer to the
artifact's item 5, committed together as
`docs/audits/2026-08-19-technical-l2-wiring-lane-contract.md`.

## ARCHITECT AMENDMENTS (override on contact)
1. **Config-surface ruling (N1 item 2, ruled):** NO new runtime-knobs YAML — adopt the
   `audit.py` precedent: named module constant + click option (default OFF) + env-var switch
   for hook contexts. No ADR-101 Rule A/C event may occur in this lane; a new config file
   appearing anywhere = STOP.
2. **The two MEASURED blockers are in-scope, with the artifact's own stated fixes:**
   (a) `audit.py:283` `basicConfig` — telemetry must NOT push 43 lines to stderr on the
   per-commit gate; apply the artifact's fix. (b) `telemetry_emit._REPO_ROOT` independence —
   wire the sandbox seam so the store is reachable by tests, and REPAIR
   `test_ship_gate_is_readonly` so it passes for the RIGHT reason; state before/after why.
3. **UNVERIFIED rows first:** N1 ran with no gates (no pytest, no pre-commit, Python 3.11 vs
   the >=3.12 floor). Before acting on any row the artifact marks UNVERIFIED, re-verify it on
   this real toolchain; log each verdict (CONFIRMED/CORRECTED + evidence) in your lane
   artifact. A CORRECTED row that changes a step → apply the correction and record it; if it
   changes the CONTRACT's shape → STOP-report.
4. **Serialize-group:** `audit-py` — you are the ONLY audit-py lane running; the seam lane
   boots only after your merge. Do not touch `tests/test_audit.py` (seam leg's surface).

**Closes:** `[#529]` + `[#530]` (verify each Done-when literally before claiming it).
**FINAL:** targeted suites `-n 0` (the artifact's 19 named cases across its 2 NEW test files +
the pinned-by-tests sweep's touched set). Commit-and-STOP; STOP packet = Done-when states,
UNVERIFIED→verdict log, blocker fixes evidence, shas. Never merge, never push main.
```

## Governing rows

- `[#529]` — open leg 1 (wire the call sites) + leg 2 (`.gitignore`). Leg 3 (structlog) stays
  open by the contract's own instruction; the row's Done-when says "via structlog" and structlog
  is absent from `[dependency-groups]`/`uv.lock`, so **this lane does not close `[#529]`**.
- `[#530]` — call sites only. The row's Done-when is already met (`50daad05`); its two open
  defect legs (ABA in `release`, `rev-parse` conflation) are NOT taken here, so **this lane does
  not close `[#530]`** either.

The wrapper's "Closes: [#529] + [#530]" is read as *"verify each Done-when literally before
claiming it"* — which is the same sentence's own instruction. The verification is recorded in the
lane packet, `docs/audits/2026-08-19-technical-l2-wiring-lane-packet.md`.

## Working artifact

Decision log, UNVERIFIED→verdict table, blocker before/after evidence and the STEP-9 store
readback live in `docs/audits/2026-08-19-technical-l2-wiring-lane-packet.md`, written as the lane
proceeds and frozen at STOP. This contract file is written once and not edited again.
