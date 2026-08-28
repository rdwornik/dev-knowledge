---
id: "[#335]"
title: "Exempt `templates/` from the `reconciled_versions` check"
status: closed
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#335] [P3][S] Exempt `templates/` from the `reconciled_versions` check — a template file's `reconciled_with` intentionally carries the `<version>` fill-in placeholder (the consumer resolves it), so the check flags `templates/CONTRIBUTING-md-template.md` as "malformed" **by construction** (a false-positive). Skip `templates/**` in the `reconciled_versions` organ (or accept a bare `<version>` placeholder for template-genre files). · Done when: `reconciled_versions` no longer flags a `templates/` file carrying a placeholder, with a test, and the standing disposition `warn-reconciled-versions-contributing-template` auto-clears · refs scripts/audit.py, templates/CONTRIBUTING-md-template.md, ecosystem/disposition-register.yaml, ADR-75 · kill-candidates: none — check-precision fix surfaced by the A0-seal ship-gate (its disposition auto-clears on this) · serialize-group: audit-py · **VERIFIED-THEN-CLOSED 2026-08-28** — the K4 verdict was verify-then-close on the premise that the false positive *"may already be gone"*. One live run REFUTED that: `check_reconciled_versions(Path('.'))` returned `warn: templates/CONTRIBUTING-md-template.md: malformed (reconciled_with not '<spec-id>@<version>')`. So the row was landed, not closed on a stale premise. `validate_reconciliation.is_template_placeholder` now exempts a `templates/` path whose value still carries an angle-bracket placeholder; narrow on BOTH axes (a resolved template edge stays checked, a placeholder outside `templates/` still WARNs) so the exemption cannot hide genuine drift. Same run after: `pass: 8 reconciled_with edge(s) match`. Three tests in `tests/test_validate_reconciliation.py` pin all three branches. The standing disposition `warn-reconciled-versions-contributing-template` is REMOVED from `ecosystem/disposition-register.yaml` — its `auto_clearable_by: "#335"` is documentary (no script reads the key), so the clear is this deletion · CLOSED 2026-08-28
