---
id: "[#370]"
title: "Is the `owner=hub` / `owner=repo` ownership model two-state-complete?"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: claude-md
generates: BACKLOG.md
---

- [#370] [P3][S] **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — a third content class demonstrably exists. `CLAUDE.md` §7/§8 user-level lines (`:122-124`, `:140-145`) name `~/.claude/` surfaces (`/session-summary`, `/codex-review`, `gotchas`): `owner=hub` is false (the hub does not carry them), `owner=repo` is false (the repo does not own `~/.claude/`). Surfaced as a render gap in [#352] clause (f) — those lines fall outside the Form-A roster regions — but that is the **symptom, not the subject**; operator-ruled 2026-07-20 as OUT of (f)'s scope. **No owner is nominated** — naming a third class, or ruling the model complete with those lines correctly unmarked, is the operator's call. · Done when: the operator rules on the model's completeness and the ruling is recorded; marker/template/test changes follow only if it calls for them · refs CLAUDE.md §7/§8, templates/claude-regions/, docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md, #352, #312 · kill-candidates: none — an ownership-model completeness question surfaced by [#352]; no open task covers the two-state model's adequacy · serialize-group: claude-md
