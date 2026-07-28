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

- [#370] [P3][S] **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — a third content class demonstrably exists. `CLAUDE.md` §7/§8 user-level lines (`:122-124`, `:140-145`) name `~/.claude/` surfaces (`/session-summary`, `/codex-review`, `gotchas`): `owner=hub` is false (the hub does not carry them), `owner=repo` is false (the repo does not own `~/.claude/`). Surfaced as a render gap in [#352] clause (f) — those lines fall outside the Form-A roster regions — but that is the **symptom, not the subject**; operator-ruled 2026-07-20 as OUT of (f)'s scope. **No owner is nominated** — naming a third class, or ruling the model complete with those lines correctly unmarked, is the operator's call. **RULED 2026-07-28 (operator word, architect session): the model is NOT two-state-complete — a third ownership state EXISTS, named `owner=user`.** Anchors: the hub's own `deploy/manifest-v1.4.0.yaml` splits `implemented:` from `deferred_deployables:` (a declared surface the hub does not itself hold); CLAUDE.md §5 rule 7 routes executable rules to `~/.claude/` with `verify:` lines; core-invariant #6 makes global-infra edits exception-with-ruling — a class the hub may neither hold nor edit; and `~/.claude` carries its own remote (`dot-claude.git`) outside every fleet repo. **Follow-up sub-question, recorded here and explicitly NON-BLOCKING on this ruling:** what `owner=user` GOVERNS vs merely CONTAINS — `~/.claude/night-agent/` (97 files) and `~/.claude/archive/` (24) are gitignored and untracked even by `dot-claude.git`, so containment is demonstrably not governance. **Closure posture:** the ruling clause of the Done-when is satisfied and recorded; whether the marker/template/test work the ruling now calls for sits inside this row or a follow-on is the operator's call at `/review-closures` — no closure taken here. · Done when: the operator rules on the model's completeness and the ruling is recorded; marker/template/test changes follow only if it calls for them · refs CLAUDE.md §7/§8, templates/claude-regions/, docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md, #352, #312 · kill-candidates: none — an ownership-model completeness question surfaced by [#352]; no open task covers the two-state model's adequacy · serialize-group: claude-md
