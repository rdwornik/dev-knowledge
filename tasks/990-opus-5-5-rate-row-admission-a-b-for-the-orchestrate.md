---
id: "[#990]"
title: "Opus 5.5 rate row + admission A/B for the orchestrate/plan role"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#990] [P2][M] **Opus 5.5 rate row + admission A/B for the orchestrate/plan role** - D31: Claude Code 2.1.280 made `claude-opus-5-5` the default Opus alias (1M context, $4/$20 per Mtok) while `ecosystem/provider-registry.yaml` still pins `claude-opus-4-8` for the non-rerankable orchestrate/plan role; no rate row or A/B exists to let the operator rule on a swap (`docs/audits/2026-09-23-technical-opus55-harness.md` Part C) · Done when: `ecosystem/provider-registry.yaml` carries an Opus 5.5 rate row for `cost_usage_telemetry.py`/`lane_cost.py`; the orchestrate/plan A/B (real recent artifacts, scored on the architect's existing rubric, per `docs/audits/2026-09-11-technical-batch-x-manifest.md`'s pattern) is run and its result is recorded for the operator's ruling · implements: ADR-120 · refs `ecosystem/provider-registry.yaml`, `docs/audits/2026-09-11-technical-batch-x-manifest.md`, `docs/audits/2026-09-23-technical-opus55-harness.md`, `docs/audits/2026-09-23-technical-window-defects-amend.md` · kill-candidates: none -- no open row adds the Opus 5.5 rate row or runs the A/B
