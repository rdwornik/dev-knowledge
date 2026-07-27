---
id: "[#335]"
title: "Exempt `templates/` from the `reconciled_versions` check"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#335] [P3][S] Exempt `templates/` from the `reconciled_versions` check — a template file's `reconciled_with` intentionally carries the `<version>` fill-in placeholder (the consumer resolves it), so the check flags `templates/CONTRIBUTING-md-template.md` as "malformed" **by construction** (a false-positive). Skip `templates/**` in the `reconciled_versions` organ (or accept a bare `<version>` placeholder for template-genre files). · Done when: `reconciled_versions` no longer flags a `templates/` file carrying a placeholder, with a test, and the standing disposition `warn-reconciled-versions-contributing-template` auto-clears · refs scripts/audit.py, templates/CONTRIBUTING-md-template.md, ecosystem/disposition-register.yaml, ADR-75 · kill-candidates: none — check-precision fix surfaced by the A0-seal ship-gate (its disposition auto-clears on this) · serialize-group: audit-py
