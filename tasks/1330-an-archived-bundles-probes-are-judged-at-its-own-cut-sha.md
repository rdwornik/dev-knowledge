---
id: "[#1330]"
title: "An archived bundle's probes are judged at its own cut sha"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1330] [P1][M] **An archived bundle's probes are judged at its own cut sha** - R42.3 + R42.4 (`to-browser/RATIFICATION-2026-09-30.md` v2): `handoff_probes` hard-FAILs BD-ci, BD-rulings and BD-capabilities on committed bundle `2026-09-28-dev-knowledge-architect` (cut from `c758fe2f`), because it re-derives the bundle's recorded LIVE-DRIFTS/SLOW values against today's state, so every past bundle turns red with time. This blocks the next cut: the preflight `ship_gate` row (`scripts/gen_handoff.py:986`) accepts only a bundle's own BD-manifest, and the register clears WARNs only. The first work of the next seat, with `[#1329]`, in one handoff-unblock lane. · Done when: RED-first, a committed bundle's BD rows are judged against the sha it was cut at, so the three rows above PASS with no `_BUNDLE_EXCLUDE_DIRS` entry, no disposition and no stopgap (R38); a bundle still uncommitted (being cut) keeps live-state teeth, pinned by a second test · touches: `scripts/audit.py` (`check_handoff_probes`, `_select_active_bundle` :2411), `scripts/verify_handoff_probes.py` (BD re-derivation), `scripts/gen_handoff.py` (`_row_ship_gate`, the `HANDOFF_RECEIPT.json` writer ~:2341 as the recorded cut-sha source), `scripts/audit_checks/registry.py` (`_BUNDLE_EXCLUDE_DIRS` stays unchanged), `templates/handoff/v5/PROBES.md.tmpl` if BD rows must record their cut sha, `tests/test_verify_handoff_probes.py`, `tests/test_seat_release_moment.py` · kill-candidates: none -- no open row tracked this before this entry · refs scripts/handoff_state.py, scripts/verify_handoff_probes.py, tests/test_handoff_state.py, tests/test_verify_handoff_probes.py
