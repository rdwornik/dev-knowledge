---
id: "[#522]"
title: "A re-cut handoff sibling carries its predecessor's payloads — the thinner-refill hole"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: handoff
generates: BACKLOG.md
---

- [#522] [P2][M] **A re-cut handoff sibling carries its predecessor's payloads — the thinner-refill hole** — `gen_handoff.py --allow-suffix` (`_resolve_bundle_dir`) writes a fresh `-2`/`-3` sibling with **FILL-IN regions re-rendered EMPTY**; the flag prevents a worse failure (silent suffixing once wrote into an existing bundle, with real data loss). A `-2` sibling nearly shipped four unfilled regions and was refused by `residual_completeness` at `86078062` — the gate working. **The gate catches only the EMPTY case:** the validator states its own limit at `:25-33` — placeholder-replaced, never value-present — so a region refilled **thinner** passes, and nothing names a re-cut's predecessor or carries its payloads. · Done when: (a) `--allow-suffix` **refuses unless a predecessor is named** (e.g. `--carry-from <predecessor-bundle>`); (b) a test proves the refusal; (c) a test proves the carry — a re-cut sibling's FILL-IN regions are non-empty and reference the predecessor's payloads; (d) the validator's stated limit is closed for the re-cut path or re-annotated · refs `scripts/gen_handoff.py`, `scripts/validate_residual_completeness.py:25-33`, `86078062`, [#310], [#422] · kill-candidates: none — Sheet E records eight rows read and rejected as owner · serialize-group: handoff
