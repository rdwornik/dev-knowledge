---
id: "[#345]"
title: "Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermetization.py`"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: pre-commit-config
source: BACKLOG.md
derived: true
---

- [#345] [P2][M] Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermetization.py` (realizes the ADR-101 two-tier amendment) — move `SANCTIONED_TIER1_DIRS`/`_FILES`/`SANCTIONED_GENRES`/`AUDIT_CLASS_ENUM` out of the script into a standalone single-responsibility `ecosystem/<name>.yaml` (home + naming rule + `{kind,repo,ref}` source; NOT in `parity-surfaces.yaml`); refactor the gate to read it (single source of truth — collapses the script+test+ADR+template lockstep); generalize Rule-B naming beyond `docs/audits/` to every registered class (ADR/intake/…). Replication-ready so a consumer carries its own copy; deploy carrier = P6. New registry-file creation needs an explicit operator-authorization line (predates its own pattern). · Done when: registry ships + gate reads it (frozensets gone), a compliant path per class passes + a violation blocks, lockstep collapsed, with tests · refs ADR-101 §3, #306, #344, ADR-103, scripts/validate_hermetization.py · kill-candidates: none — realizes the ADR-101 two-tier amendment; #306 built the bare gate, this externalizes+generalizes it, none subsumes it · serialize-group: pre-commit-config
