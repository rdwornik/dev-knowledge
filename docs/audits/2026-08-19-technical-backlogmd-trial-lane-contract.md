# LANE N — BACKLOG.MD ADOPTION TRIAL (Tier-M, sandbox, bounded)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Worktree lane — but the TRIAL runs in a THROWAWAY CLONE outside the repo** (e.g.
`$env:TEMP\backlogmd-trial\`): `git clone <repo-path>` there, experiment freely, delete at end.
**Your worktree exists ONLY to commit the evaluation artifact** to `docs/audits/`. NOTHING from
the trial (no `backlog/` dir, no config, no npm state) ever touches the real repo or your
worktree beyond the artifact — a `backlog/` directory appearing in the repo = Rule C event =
you failed the contract.
**ADR-110:** commit this prompt first as
`docs/audits/2026-08-19-technical-backlogmd-trial-lane-contract.md`.

## CONTEXT (operator's ask, verbatim intent)
The operator demands library-first for the management loop itself: "intake→ADR→archive, backlog,
user stories, epics — this is not rocket science; there must be libraries." Candidate:
**Backlog.md** (github.com/MrLesk/Backlog.md, MIT) — markdown-native tasks with
acceptance-criteria + DoD per task, dependencies/milestones, decisions + archive folders,
terminal Kanban + board export, local web UI, MCP + CLI (Claude Code / Codex / Gemini CLI).
Secondary candidates for a paragraph each, not a full trial: `veggiemonk/backlog` (Go), `tkr`.

## TRIAL PROTOCOL (measure, don't vibe)
1. Install per its docs in the sandbox (`npm i -g backlog.md` or bun); `backlog init`; record
   versions + any Windows friction verbatim.
2. **Import a REAL slice:** convert 15 representative rows from our `tasks/` (mix of sizes,
   one with serialize-group, one with kill-candidates, one with a ruled leg like #533's shape,
   one closed row) into Backlog.md tasks via its CLI. Record per-field mapping: what maps
   cleanly / what has no home (serialize-group? reserved-id blocks? `· Done when:` clauses?
   source/refs/footprint?) / what Backlog.md has that we lack (DoD checklist, dependencies,
   milestones, drafts→archive lifecycle).
3. **Drive it as an agent would:** create/edit/close via CLI + `--json`; run `backlog board`,
   `backlog board export`, `backlog browser` (screenshot-in-text what the operator would see).
4. **Decisions lifecycle:** model our intake→ADR→archive gate in its decisions/archive
   structure; state precisely where it fits and where it cannot express our rules.
5. **Coexistence probe:** can it run as a VIEW/UI layer over a one-way export from our
   generator (our tasks/ stays source of truth), without owning the data? Prototype the
   export mapping for the 15 rows; state the sync hazards.

## VERDICT (three-value enum + evidence, architect ratifies)
`ADOPT-WHOLESALE (migration plan sketch + what we delete)` ·
`ADOPT-VIEW-LAYER (export mapping + what stays bespoke and why)` ·
`REJECT (the measured divergence, recorded so it is not relitigated)`.
Score against the operator's four pains: task status visibility · human release notes ·
intake→ADR/archive gate · epics/stories structure.

## OUTPUT
`docs/audits/2026-08-19-technical-backlogmd-trial.md` — protocol results, field-mapping table,
verdict + evidence, secondary-candidates paragraphs, exact commands. Commit-and-STOP; sandbox
clone deleted (verified). Packet: verdict line + top-3 evidence + shas.

## WHAT NOT TO DO
No install into the real repo/worktree beyond the artifact · no migration of real data · no
touching tasks/, BACKLOG.md, scripts/ · no adoption verdict presented as ruled (architect +
operator ratify) · no merge.
