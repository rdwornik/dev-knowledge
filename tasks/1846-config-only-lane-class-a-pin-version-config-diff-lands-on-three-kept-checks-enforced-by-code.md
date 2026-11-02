---
id: "[#1846]"
title: "config-only lane class: a pin/version/config diff lands on three kept checks, enforced by code"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1846] [P2][M] **config-only lane class: a pin/version/config diff lands on three kept checks, enforced by code** - a pin or version commit has no landing path of its own: `subst_gate.handback_problems` demands a MODELS block and a LAUNCH receipt a config-only change has no use for, so the integrator waives them by hand (`to-cc/INTEGRATOR-PIN-WAIVER-2026-11-01.md`) · Done when: a registry (the row defines it) names the registered config paths; a diff that touches only those paths is a config-only lane; its landing runs exactly three kept checks - `codespace_parity.py` pin check against the laptop on the integration tip, integration CI shows no new red against its base, one OpenAI-family review - and replaces the MODELS-block and LAUNCH-receipt demands, all enforced by code, not by the integrator's hand · owner: the integrator · touches: `scripts/subst_gate.py`, `scripts/land_lane.py`, `scripts/codespace_parity.py`, `tests/test_subst_gate.py`, `tests/test_land_lane.py` · kill-candidates: none -- no open row covers a config-only landing class · source: `LANE-e30-seat-registry-binds.md` (GO-E3.0 C1), evidence `to-browser/DIGEST-RULING-PIN-COMMIT-AND-DEFECT-33-2026-11-01.md` Ruling 1, `to-cc/INTEGRATOR-PIN-WAIVER-2026-11-01.md`, `to-browser/QUESTION-E3.0-2026-11-01-pin-commit-landing-path.md` · filing only, E3.2, not built by the lane that filed it · refs scripts/subst_gate.py, scripts/land_lane.py, scripts/codespace_parity.py
