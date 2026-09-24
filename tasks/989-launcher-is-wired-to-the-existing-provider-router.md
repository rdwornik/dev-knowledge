---
id: "[#989]"
title: "Launcher is wired to the existing provider_router -- routing stops living in prose and hard-coded models"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#989] [P1][M] **Launcher is wired to the existing provider_router -- routing stops living in prose and hard-coded models** - D16/D17/D32/O-4b (correction in `docs/audits/2026-09-23-technical-window-defects-amend.md`): `scripts/provider_router.py` and `ecosystem/provider-registry.yaml` already exist and gate admission per role -- nothing new needs to be built. The defect is that `scripts/dispatch.py launch` bypasses the router entirely and every contract hard-codes `--model`; separately, the `opus` alias now resolves to Opus 5.5 while the registry pins an older Opus, so 'ordered opus' silently 'ran 5.5' at the alias level · Done when: `dispatch.py launch` asks `provider_router.py` for role, size and kind and resolves an explicit model id from the registry -- never an alias; `scripts/plan_lint.py` refuses a contract's Dispatch block that names a model directly instead of a role; a witness contract naming only role+size launches with the router-resolved model recorded in its receipt · implements: ADR-120 · refs `scripts/dispatch.py`, `scripts/provider_router.py`, `ecosystem/provider-registry.yaml`, `scripts/plan_lint.py`, `docs/audits/2026-09-23-technical-window-defects-amend.md`, `docs/audits/2026-09-23-technical-handoff-readiness.md` §6 · kill-candidates: none -- no open row wires the launcher to the router; this row folds D16, D17 and D32 (superseded/re-scoped by the AMEND) and discharges S3 §6's O-4b together, since all four name the same mechanism
