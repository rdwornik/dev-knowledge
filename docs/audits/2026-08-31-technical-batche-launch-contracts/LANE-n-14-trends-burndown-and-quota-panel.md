# LANE batch-e-n-14-trends-burndown-and-quota-panel (HY-4) - the TRENDS burn-down panel (done vs remaining per north-star arc over time) PLUS the quota panel, folded in by ruling CUT-5.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-n-14-trends-burndown-and-quota-panel LANE-n-14-trends-burndown-and-quota-panel.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-n-14-trends-burndown-and-quota-panel` -> branch `worktree-lane-n-14-trends-burndown-and-quota-panel` -> contract `LANE-n-14-trends-burndown-and-quota-panel.md`

## Write-scope (frozen)

- `scripts/gen_trend_dashboard.py`
- `tests/test_gen_trend_dashboard.py`

## Done-contract (immutable)

1. **A burn-down panel: done vs remaining, per north-star ARC, over time.** The arcs are declared
   in `scripts/gen_north_star.py`; read them from there rather than restating them, so the panel
   cannot drift from the arc set.
2. **THE QUOTA PANEL IS FOLDED IN HERE - architect ruling CUT-5.** No new row, no new intake, no
   ledger spend. HY-4 already owns a panel-shaped deliverable and already reads the trend store;
   a second panel is a second section, not a second lane.
3. **THE QUOTA PANEL STATES ITS OWN LIMIT, IN THE PANEL.** It can show **provider and credits**.
   It **CANNOT attribute a lane to a MODEL**, because `[#615]` (MODEL ATTRIBUTION - the
   model+version commit trailer) is open and deliberately UNFUNDED in this batch. The panel says
   so in its own text rather than rendering a column that looks whole and is not.
   **A partial series that looks complete is worse than an absent one** - that is `[#615]`'s own
   reasoning, applied to its own absence.
4. **Every series is DERIVED.** No number is typed in; each cites the surface that computes it.

## Steps

1. Read the arc declarations and the trend store's existing panels first.
2. Build both panels RED-first (ADR-108 section B).
3. Regenerate the dashboard. **Expect `test_export_backlog_view` to RED - it is a known
   dashboard-regeneration false positive, not this lane.** Say so rather than chasing it.
4. Run the TARGETED tests for this diff. Commit and STOP.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
