# Changelog review — 2026-09-23

<!-- scope: meta -->

- **Model in effect:** Sonnet 5 (`claude-sonnet-5`), effort high, background session `postwave-changelog`.
- **Trigger:** PUSH — operator paste of `POSTWAVE-CHAIN-2026-09-22.md` §S1 Part B ("`/changelog-review` exactly as the skill defines itself"). SessionStart sentinel had already nudged (claude-code installed 2.1.281 > last-reviewed 2.1.204).
- **Tools + ranges reviewed:**
  - claude-code **2.1.205 → 2.1.281** (77 versions; last-reviewed 2.1.204 @ 2026-07-09 — a 2.5-month gap, the widest this review has ever covered)
  - codex **0.144.0 → 0.156.1** (~30 stable releases; last-reviewed 0.143.0 @ 2026-07-09; installed still behind, reviewed-ahead is intended per this skill's contract)
- **Bucket counts (claude-code):** ADOPT **3** (+2 minor) · OBSOLETES-WORKAROUND **0** · STALE-NAMES **0** (two near-misses ruled out — see below) · VERIFY **3** · NOISE **~2,000+** entries across 77 versions
- **Bucket counts (codex):** ADOPT **0** · OBSOLETES-WORKAROUND **0** · STALE-NAMES **0** · VERIFY **0** · NOISE — all ~30 stable releases (Guardian auto-review internals, sandbox/Windows hardening, TUI/voice/themes — irrelevant to our read-only, non-interactive `codex exec` reviewer usage)
- **SEED doc:** `docs/intake/2026-09-23-changelog-review-seeds.md`, intake-id **105** (3 ADOPT findings)

---

## Headline

77 versions of drift accumulated because the operator's standing request to run this review went unactioned for 2.5 months (recorded verbatim in `to-cc/RATIFICATION-2026-09-23-copilot.md` O-4: "he has asked for several windows that ... it was not [put to work]" — the same neglect pattern applies here). The dominant themes across the range are **background sessions, worktree isolation, hooks, sandboxing, and Windows hardening** — this fleet's exact daily-driver pattern — so most of the ~2,000 entries are reliability fixes that already benefit us automatically, no action needed. Three items are genuine **ADOPT** candidates directly relevant to this repo's own stated pain point (CLAUDE.md/skill byte-and-token budget). Two renames looked like STALE-NAMES risks and were checked against this repo's live files — both are false alarms (see below). Three items need a live VERIFY, one of them prompted by something that happened *in this very session* (see V3).

## ADOPT (3 major + 2 minor)

- **A1 — `/skill-doctor` (2.1.261): shows which loaded skills go unused and what they cost in context.** Directly on point for this repo's own §"Anti-patterns" concern about duplicated/stale content and the `.claude/skills/` roster's growth. No config needed — it's a command. **Candidate home:** run it opportunistically; if it surfaces unused skills, file a row to prune them.
- **A2 — `/doctor` check that proposes trimming checked-in CLAUDE.md by cutting content Claude could derive from the codebase (2.1.206).** This repo's own `CLAUDE.md` carries an explicit `≤24,576 B` budget gate (`tests/test_claude_md_byte_cap.py`) and a documented anti-pattern against restating counts/rosters in prose — this is a native tool that does exactly what our doc-rot tooling already polices by hand. **Candidate home:** run `/doctor` against `CLAUDE.md` and diff its proposal against the current byte count before the next `CLAUDE.md` edit.
- **A3 — `omitClaudeMd` agent frontmatter / `--agents` JSON key (2.1.271-ish range): lets a subagent run without loading user/project/local CLAUDE.md.** This hub's `CLAUDE.md` is large by design (governance doctrine for every session); a read-only research subagent or a bounded external producer (the Copilot-as-producer pattern this same POSTWAVE CHAIN's Part A is trying to stand up) does not need the full governance doctrine loaded to do bounded work. **Candidate home:** the `[#75]`/Copilot-offload intake line (`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`) or a new row under the dispatch/lane-contract surface.
- *(minor)* **A4 — `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (2.1.269).** Only relevant if a workflow run ever needs to exceed the `workflowSizeGuideline`; we already run at "medium" by policy, so this is a lever to know about, not one to pull now.
- *(minor, dogfood-signal)* **A5 — Claude Opus 5.5 (2.1.280): now the default Opus model, 1M context, $4/$20 per Mtok, $0.20/Mtok cache reads.** Covered in full under Part C of this session's own digest (`to-browser/DIGEST-OPUS55-HARNESS-2026-09-23.md`) — not re-litigated here.

## OBSOLETES-WORKAROUND (0)

None found. Closest candidate considered and rejected: "Improved `/batch` to run where a WorktreeCreate hook provides the agent worktrees, not only inside a git repository" (2.1.281-range) — doesn't retire anything of ours, since every lane we run is already inside a git repo.

## STALE-NAMES (0) — two near-misses checked and ruled out

- **Removed the deprecated TaskOutput tool** (2.1.277; "Claude reads a background task's output file with Read instead"). Checked: `TaskOutput`/`taskOutputMaxChars`/`TASK_MAX_OUTPUT_LENGTH` appear nowhere in this repo's live scripts, hooks, or docs (only in `tests/fixtures/lived-workflow/*.jsonl` fixture data, which is fixture content, not a live reference to the tool). **No drift.**
- **Removed the deprecated `codex exec --full-auto` flag** (codex ~0.144.0; "use `--sandbox workspace-write` instead"). Checked: `--full-auto` appears only in two immutable historical audit docs (`docs/audits/2026-06-07-codex-max-audit.md`, `docs/audits/2026-08-28-technical-nb2-f-packet.md`), never in live config or a script we run. **No drift** — those audits are historical record, not live surface.

## VERIFY (3) — live check before assuming impact

- **V1 — Task/Todo tools on Sonnet 5 / Opus 5.5.** 2.1.232: *"Todo/task-tracking tools (TaskCreate/Get/Update/List, TodoWrite) are no longer available on Opus 4.8, Sonnet 5, Fable 5, Mythos 5, and newer models; set `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` to bring them back."* This session runs on Sonnet 5 and the deferred-tools list still offered `TaskCreate`/`TaskGet`/`TaskList`/`TaskUpdate`. Neither this repo's `.claude/` nor `scripts/` sets `CLAUDE_CODE_ENABLE_TODO_TOOLS` (grepped clean), so either the flag is set at the L0 `~/.claude/settings.json` layer (outside this repo, operator-checkable) or the restriction has since been narrowed. **Command:** operator runs `Select-String CLAUDE_CODE_ENABLE_TODO_TOOLS ~/.claude/settings.json` (or equivalent) to confirm the source.
- **V2 — Monitor's `persistent` option was removed (2.1.269): watches now always have a deadline (≤30 min; 10 min in single-prompt `-p` runs), and Claude must re-arm.** No repo hook or script references a Monitor `persistent` flag by name, but any lane pattern that assumed an unbounded Monitor watch (e.g. long-running background lane surveillance) should be re-checked against the new ceiling. **Command:** grep any `.claude/skills/*/SKILL.md` or `scripts/*` for a Monitor invocation with an implied long-running watch and confirm it re-arms rather than assuming persistence.
- **V3 — worktree-isolation Bash-command false positives, several rounds of fixes across the range (2.1.256/2.1.257/2.1.267/2.1.274/2.1.281 all touch this).** This session itself hit a worktree-isolation refusal on a plain `curl ... -o file 2>&1` command inside a worktree ("names git in a form too complex to verify"), which is *not* one of the documented fixed shapes (those cover Bash loops, xargs, heredocs, nested shell expansions, redirect-with-no-redirect false positives — not a bare `curl -o` + stderr redirect). **Command:** reproduce `curl -s <url> -o <file> 2>&1` inside a fresh worktree session on 2.1.281 and, if it still refuses, file a fresh gotcha (this is a NEW false-positive shape, not one already covered).

## NOISE — counted, not itemized

The ~2,000 entries not called out above split roughly into: VSCode-extension-only UI/accessibility polish; Claude Tag (Slack) admin/connector features; Claude Code on the web (cloud/routines/admin) features; Bedrock/Vertex/Foundry/Claude-apps-gateway enterprise deployment plumbing; Code Review (GitHub PR bot) polish; terminal rendering, vim-mode, and keybinding fixes; MCP transport/OAuth edge cases; and a long tail of Windows/background-session/worktree reliability fixes that land free and require no action (they hit the exact failure modes this fleet's own LESSONS/gotchas already document, and each fix narrows, not widens, that surface). Codex's ~30 stable releases in range are dominated by its "Guardian" automatic-approval-review subsystem, voice mode, a new fullscreen TUI, and further Windows sandbox hardening — none of it touches our narrow, non-interactive `codex exec`-as-reviewer usage.

## Operator routing

**Three ADOPT items filed to intake #105** for architect triage: `/skill-doctor` and the CLAUDE.md-trim `/doctor` check are both zero-cost to try immediately; `omitClaudeMd` is a design lever worth folding into the Copilot-offload / bounded-producer intake line already open. **No OBSOLETES-WORKAROUND, no STALE-NAMES action needed.** Three VERIFY checks are CC-runnable spot-checks (V1, V2) or already flagged as a fresh gotcha candidate (V3) — none block anything. State bumped: claude-code → 2.1.281, codex → 0.156.1.
