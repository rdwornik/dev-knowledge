---
id: "[#604]"
title: "Admit win-tooling and terminal-setup to the deploy registry and rule their onboarding profiles"
status: open
priority: P2
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: architecture
generates: BACKLOG.md
---

- [#604] [P2][S] **Admit win-tooling and terminal-setup to the deploy registry and rule their onboarding profiles** — the deploy tool rejects an unregistered repo before anything else runs (`deploy/tool.py:253`), and `ecosystem/satellite-onboarding-rulings.yaml` carries no entry for either repo, so nothing says which gate set they should receive. Both are declared fleet members and neither is reachable by the mechanism that would onboard them. **The win-tooling half is DONE by the lane that filed this row** — registry key and profile ruling both landed — so what remains is `terminal-setup`, plus the correction this row exists to preserve: **adding a registry key does not flip a parity role**. `ecosystem/parity-surfaces.yaml` declares `role:` as hand-maintained data, so the role flips when a deploy actually lands, not when a key appears; the recon's step-2 claim to the contrary was measured false at HEAD and the reason string was corrected in the same act. · Done when: `terminal-setup` carries a null-valued key in `ecosystem/deployed-versions.yaml` **and** an entry in `ecosystem/satellite-onboarding-rulings.yaml` naming `full` or `floor-only` with `ruled_by` and a date, `validate_onboarding_rulings.py` reports no schema defect, and each admitted repo's `parity-surfaces.yaml` reason states its true registry state · refs docs/audits/2026-08-26-technical-w3prep-recon.md (steps 2-3, blockers B2 and B9), docs/intake/2026-08-26-tech-wave3-wintooling.md (intake #56), ecosystem/deployed-versions.yaml, ecosystem/satellite-onboarding-rulings.yaml, ecosystem/parity-surfaces.yaml, deploy/tool.py · source: intake #56, recon row W3-2 · kill-candidates: none — no open row owns deploy-registry membership; `[#462]` registered terminal-setup in the ecosystem registry, a different register with a different consumer, and it is closed · serialize-group: architecture
