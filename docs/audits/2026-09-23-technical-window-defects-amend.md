# AMEND — defect register: routing exists but is bypassed; tool changes adopted as mechanisms

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN`. Source: `to-cc/AMEND-WINDOW-DEFECTS-2026-09-23.md`. Amends
> `2026-09-23-technical-window-defects.md` (adds D30-D34; corrects D16/D17).
> Carrier rows: one row per D30-D34 item, filed by `lane-landing-window` (D30 folds into the O-4a
> row where the two mechanisms coincide; see this contract's Done-contract item 1): D30 `[#988]`,
> D31 `[#990]`, D32 `[#989]`, D33 `[#991]`, D34 `[#992]`.

carried-by: OPEN
lands-via: LANE-5A-5 (the same rows as the register) and the night batch
date: 2026-09-23
amends: to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md (adds D30-D34; corrects D16/D17)
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)
basis: DIGEST-OPUS55-HARNESS-2026-09-23 (S1), DIGEST-HANDOFF-READINESS-2026-09-23 (S3)

## Correction to D16 and D17

`scripts/provider_router.py` and `ecosystem/provider-registry.yaml` already exist, and they gate
provider admission per role. **Nothing new is to be built.** The defect is that the launcher does not
consult the router, and the registry's data is stale. DECLARE-MODEL-AGNOSTIC is re-scoped from
"build a router" to "wire the launcher to the existing router".

## New items

| # | Area | Defect (evidence) | Mechanism | Wave |
|---|---|---|---|---|
| D30 | routing | Registry says Copilot is not admitted and not licence-cleared. Evidence of its admission (lanes ab-828/ab-832 on 2026-09-16, JOURNAL lines 962 and 1113, `to-cc/run-lane-copilot.ps1`) and the operator's licence ruling O-3 are not landed. The router therefore blocks it. | Registry entry with `decided_by: operator`, `decided_on`, and evidence, following the pattern of the existing admitted rows | **5a (tonight)** |
| D31 | routing | The alias `opus` now resolves to Opus 5.5 (CC 2.1.280), while the registry pins an older Opus. S2 ordered opus and ran 5.5. Ordered is not ran, at the alias level. | The launcher passes explicit model ids from the registry, never aliases. Add an Opus 5.5 rate row for cost telemetry. Run the admission A/B for orchestrate/plan (the operator rules). | rate row and A/B **5a**; launcher wiring 5b |
| D32 | routing | The launcher bypasses the existing router. Contracts hard-code `--model`. | `dispatch.py launch` asks `provider_router.py` for role, size and kind. Plan lint forbids model names in contracts. | 5b |
| D33 | knowledge | `/changelog-review` ran after a 2.5-month gap (77 CC versions), because it is operator-invoked. | A conductor schedule runs it weekly. Its ADOPT seeds become rows automatically. | 5b |
| D34 | context | Every subagent and reviewer loads the large governance `CLAUDE.md`; unused skills cost context. Per the course, our context per task is several times a peer's. | Run `/skill-doctor` and `/doctor` (trim proposal) and record the numbers. `omitClaudeMd` for bounded roles (reviewer, reader). Prune skills on the measured data. | measurement **5a**; adoption 5b |
