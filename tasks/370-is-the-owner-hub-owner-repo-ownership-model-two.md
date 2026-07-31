---
id: "[#370]"
title: "Is the `owner=hub` / `owner=repo` ownership model two-state-complete?"
status: closed
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: claude-md
generates: BACKLOG.md
---

- [#370] [P3][S] **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — **RULED 2026-07-28 (operator word, architect session): NO — a third ownership state EXISTS, named `owner=user`.** Anchors: `deploy/manifest-v1.4.0.yaml` splits `implemented:` from `deferred_deployables:`; CLAUDE.md §5 rule 7 routes executable rules to `~/.claude/`; core-invariant #6 makes global-infra a class the hub may neither hold nor edit; `~/.claude` carries its own remote (`dot-claude.git`) outside every fleet repo. The symptom that raised it (CLAUDE.md §7/§8 user-level lines `:122-124`/`:140-145`, outside the Form-A regions, ruled OUT of [#352] clause (f)) is superseded; git holds it. **Follow-up, explicitly NON-BLOCKING:** what `owner=user` GOVERNS vs merely CONTAINS — `~/.claude/night-agent/` (97 files) and `archive/` (24) are gitignored, untracked even by `dot-claude.git`. · Done when: the marker/template/test work the ruling now calls for is ruled into this row or into a follow-on · refs CLAUDE.md §7/§8, templates/claude-regions/, #400, #352, #312 · kill-candidates: none — the ruling split this cell from [#400]'s, which stays open · serialize-group: claude-md
