---
id: "[#600]"
title: "Delete P10 from the shipped probe manifest and gate the boundedness condition"
status: closed
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#600] [P2][S] **Delete P10 from the shipped probe manifest and gate the boundedness condition** — P10 asks the incoming seat, at boot, to classify **every open item** as live, dead or awaiting-ruling. `HANDOFF_PROCESS.md` section 5 condition 4 rejects exactly that shape — *"a probe whose honest answer requires unbounded judgment over an open set is an arc, not a probe, and is rejected"* — and **names P10 as its own origin**. The condition was ratified at the v6 cut and P10 survived it, so the spec has been shipping a probe its own prose rejects. Deleting the row is the small half; the rung that makes it unrecurrable is the other. · Done when: the P10 row is out of `templates/handoff/v5/PROBES.md.tmpl`, `verify_handoff_probes` FAILs an unbounded probe row (row-scoped and era-judged, so sealed older bundles are not retro-REDed), and the RED-first test lands **before** the removal · refs docs/audits/2026-08-26-technical-handoff-census.md (b7 and delta D1), docs/intake/2026-08-26-tech-handoff-mechanization.md (intake #55), protocols/HANDOFF_PROCESS.md section 5 condition 4, templates/handoff/v5/PROBES.md.tmpl, scripts/verify_handoff_probes.py, #506 · source: intake #55, census row R3 · kill-candidates: #506 — that row exists to discharge P10's whole-set grooming binding (*"no open `#id` may pass unreconciled"*), so if the probe that creates the obligation is deleted as an arc shipped as a probe, the row discharging it loses its origin and becomes a discretionary hygiene arc. Proposal only, never a removal: grooming may still be wanted on its own merits, and that is the operator's call · serialize-group: handoff · **CLOSED 2026-09-16** — evidence b14306bc
