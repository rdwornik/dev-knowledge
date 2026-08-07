---
id: "[#490]"
title: "Parity-manifest 9/9 — fleet-green currently measures a third of the fleet"
status: closed
priority: P2
size: M
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
generates: BACKLOG.md
---

- [#490] [P2][M] **Parity-manifest 9/9 — fleet-green currently measures a third of the fleet** — `ecosystem/parity-surfaces.yaml` resolves 5 of the 9 ADR-104-declared members, and the membership_agreement check reports the split in the open: registry-md 9/9, index-yaml 6/9, deployed-versions 5/9, parity-surfaces 5/9, onboarding-rulings 4/9, state-dirs 0/9. **Two of those figures were stale when the row was written and are corrected here at close (2026-08-07), from a live `membership_agreement` read: state-dirs was 6/9, not 0/9; parity-surfaces is now 9/9.** Until the manifest covers all nine, every "fleet parity GREEN" verdict is a claim about a subset while reading as a claim about the fleet. **Precondition to any further [#383] wave** — a wave that walks a partial fleet cannot produce a fleet done-signal. · Done when: all 9 declared members resolve on the parity surface, or each absent member carries a declared reason the check reads rather than a silent gap · refs ecosystem/parity-surfaces.yaml, ADR-104, scripts/fleet_parity.py, #383 · kill-candidates: none — [#383] owns the per-surface waves, not the manifest's own coverage
