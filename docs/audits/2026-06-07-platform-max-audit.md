# Audit — Platform-maximization: full Claude Code CHANGELOG + current docs vs our stack

**Date:** 2026-06-06/07 · **Type:** read-only analysis (report persisted post-hoc) · **Session:** terminal A (Opus/xhigh) · **Status:** findings captured to BACKLOG via `docs/audit-trio-capture`; design implications feed Council brief, #84, #91.

---

## COVERAGE

CHANGELOG: 362,560 bytes / 4,259 lines / 310 version headers · range 2.1.167 (newest) → 0.2.21 (oldest); mined in 7 line-range chunks via artifact-reader (filtered to rubric intersections).

DOCS read (artifact-reader, .md via Mintlify): hooks (210KB), settings (153KB), sub-agents (65KB), plugin-marketplaces (60KB), slash-commands/skills (53KB — see note), sandboxing (32KB), common-workflows (18KB), security (10KB), iam (11KB → was Authentication, slug-mismatch). 9 passes. Empty slugs (404): sdk, background-tasks. Worktrees cleanup lives on a dedicated /en/worktrees page (not fetched — changelog+sub-agents already gave the cleanup semantics).

DOC NOTE: doc-slash-commands.md and doc-skills.md are BYTE-IDENTICAL ("Extend Claude with skills"). Slash-command + skill AUTHORING is now ONE doc (reflects 2.1.3 "merged slash commands and skills").

artifact-reader passes: 16 (7 changelog + 9 docs). Structural greps: ~10. Source ingested by subagents ≈ 0.97 MB; main-thread summaries ≈ ~60 KB (artifact-reader kept raw artifacts out of the thread).

FRAMING: the prior 2.1.148–167 windowed capture already annotated #8/#82/#84/#106/#107/#9/#112. This full-history+docs audit's NET-NEW value = (a) STALE-NAMES from PRE-148 renames the window couldn't see, (b) pre-148 hook/billing/worktree capabilities, (c) docs-confirmed CURRENT state. Entries tagged [KNOWN]=already annotated · [NET-NEW]=this audit.

## 1) UNDERUSED-NATIVE (platform has it now; we hand-built or don't use it)

**UN-1 · Billing via settings.json env route** [FIRST CONFIRMED MEMBER — per amendment #1, not re-discovered]
- canonical: `env: {"ANTHROPIC_API_KEY":""}` in settings.json (env applies to session + ALL subprocesses, settings doc L212). Empty = absent → subscription OAuth.
- chain: env key longstanding → load-bearing interaction is 2.1.139 "Remote Control, /schedule, claude.ai MCP connectors… disabled when ANTHROPIC_API_KEY/apiKeyHelper/ANTHROPIC_AUTH_TOKEN is set."
- our artifact: PATH .cmd shim + SessionStart billing sentinel (npm-clobber class).
- so what: env route REPLACES the shim as primary; shim = FALLBACK for launches that bypass settings.json (raw .exe / IDE / desktop); sentinel = retained tripwire.
- [NET-NEW nuance, pre-148]: 2.1.139 makes the empty-key route DOUBLY correct — it is REQUIRED for cloud Routines (ADR-72/73 /schedule) to run. A real API key would SILENTLY break /schedule. This coupling sits below the 148–167 window.

**UN-2 · /stats is gone → /usage** [NET-NEW — pre-148, the windowed mine could not see it]
- canonical: /usage (2.1.118 "Merged /cost and /stats into /usage"). Also a STALE-NAMES hit (see §3).
- our artifact: ENVIRONMENT.md ccusage rationale + ESSENTIALS/PLAYBOOK slash-command refs say "/stats".
- so what: /usage REPLACES interactive /stats+/cost. ccusage --json exporter STILL stands (native /usage is still a TUI, not scriptable) — only the command NAME is stale, NOT the exporter.

**UN-3 · Stop-hook additionalContext (#8)** [KNOWN #8 — this audit confirms shipped + docs-current]
- canonical: hookSpecificOutput.additionalContext on Stop/SubagentStop — continues the turn, shown as feedback NOT error (hooks doc L2134). 2.1.163.
- our artifact: Stop→propose_closures.py plugin hook (writes PROPOSALS-*.md; surfacing is a separate next-session SessionStart nudge).
- so what: COMPLEMENT — the Stop hook can ALSO return additionalContext to surface closure proposals INLINE at session end, collapsing the write-then-nudge-next-session latency. #8 = "emit the field," not "build a mechanism."

**UN-4 · Native managed worktrees (#107 / ADR-61)** [KNOWN #107 — this audit adds full native depth]
- canonical: agent/subagent frontmatter isolation:worktree (sub-agents doc L280: temp worktree branched from default branch, AUTO-CLEANED if no changes); --worktree/-w CLI flag; EnterWorktree/ExitWorktree tools; worktree.baseRef|bgIsolation|sparsePaths; WorktreeCreate/Remove hooks.
- chain: 2.1.49/2.1.50 (isolation:worktree, --worktree) → 2.1.157 (left UNLOCKED on finish so git worktree remove/prune cleans them) → 2.1.133 (baseRef).
- our artifact: PLAYBOOK manual git worktree add/remove/prune; ADR-61 ephemeral audit worktrees; CLAUDE §5 rule-9 "No leftovers" (the .dev-knowledge-* orphan failure).
- so what: COMPLEMENT — audit worktrees run read-only (no changes) → AUTO-CLEAN, directly solving the orphan failure rule-9 guards. #107 convention can become "use isolation:worktree" instead of hand-rolled. RESIDUAL: cross-repo orchestration + manual interactive parallel sessions still need the discipline (native cleanup covers only Claude-managed worktrees).

**UN-5 · Hook shell:"powershell" + args:[] exec-form** [NET-NEW — pre-148 Windows ergonomics]
- canonical: command-hook shell:"powershell" spawns pwsh.exe directly (auto-detect → 5.1 fallback; hooks doc L2979); args:[…] exec-form = no shell, apostrophes/$/backticks pass verbatim (L326-337).
- chain: 2.1.139 (args exec-form) · 2.1.143 (Windows PowerShell tool).
- our artifact: PowerShell hooks (surface-closures.ps1, billing sentinel) — Windows quoting/cmd.exe pain.
- so what: SIMPLIFY — declare shell:"powershell" instead of wrappers; args:[] kills quoting bugs. The .cmd/.bat shim caveat (hooks doc L342: command:"node" + script in args) IS the npm-clobber .cmd class.

**UN-6 · Hook if: conditional filter** [NET-NEW — pre-148]
- canonical: if:"Bash(git *)" / "Edit(*.ts)" — hook only spawns on matching tool calls (hooks doc L300-301). 2.1.85.
- our artifact: PreToolUse guards (OneDrive exclusion, transcripts immutability, C2 shell-write) fire every matching event.
- so what: COMPLEMENT — if: scopes WHEN the guard process spawns (cuts overhead); guard logic unchanged.

**UN-7 · permissions.deny path-globs as defense-in-depth** [NET-NEW framing]
- canonical: deny rules now support path globs + hardened Bash matching (wrapper/redirect/glob) — 2.1.166, 2.1.113; settings doc permissions.deny.
- our artifact: OneDrive-exclusion + transcripts-immutability PreToolUse hooks.
- so what: COMPLEMENT ONLY — deny:["Edit(**/OneDrive - Blue Yonder/**)","Write(…)","Read(…)"] adds a declarative 2nd layer, but the HOOK stays (deny-glob path-matching on arbitrary Bash is historically bypassable — the changelog is full of such CVE-class fixes). Defense-in-depth.

**UN-8 · /context native diagnostic (#17)** [#17-adjacent]
- canonical: /context shows context-heavy tools, memory bloat, capacity warnings + actionable suggestions (2.1.74).
- our artifact: #17 compaction guidance + PLAYBOOK read-scoping + verify skill.
- so what: COMPLEMENT — native self-serve diagnostic alongside the methodology.

(minor) artifact-reader subagent is already a NATIVE subagent but under-configured — could add effort:low / maxTurns frontmatter for cheaper routine extraction. Low value; noted not headlined.

## 2) ADOPT (we lack it; queue it)

**AD-1** · fallbackModel setting (up to 3 fallbacks when primary overloaded/unavailable) — 2.1.166. value: resilience for unattended cloud Routines / long sessions. NOT in settings doc yet (changelog-only → also VERIFY). BACKLOG home: ENVIRONMENT runtime config. No dup with #102–#113.

**AD-2** · Prompt-based / agent-based hooks (type:"prompt" Haiku-eval; type:"agent" multi-turn subagent, experimental). value: the Tier-1 closure/triage loop could evaluate "any closable items?" via a type:prompt hook IN-session instead of a Python shell-out. CAVEAT → VERIFY (amendment #2 auth). BACKLOG home: Tier-1 lifecycle evolution (near #8). New.

**AD-3** · fewer-permission-prompts skill (native; scans transcripts → proposes a prioritized allowlist). value: one-shot to tighten the allow-list under the deny-rule posture; low effort. (Built-in skill.) BACKLOG home: runtime/permissions. New.

**AD-4** · /code-review ultra (cloud multi-agent) — DUP of #82 (native /code-review --fix + /simplify eval). Do NOT re-propose; fold ultra into #82's evaluation. HARD CAVEAT: ultra is Claude — it does NOT replace Codex's cross-vendor heterogeneity (complement, not substitute). See KILL-3.

## 3) STALE-NAMES (concrete drift in OUR live docs — highest-confidence output)

**DRIFT-A · "/stats" → "/usage"** (renamed/merged 2.1.118; /cost+/stats merged into /usage)
- protocols/ESSENTIALS.md:251 — "… /stats (tokens)" (slash-command quick-ref)
- protocols/PLAYBOOK.md:2834 — "| /stats | Check token usage (interactive TUI; use ccusage --json …) |"
- protocols/ENVIRONMENT.md:20 — "Export … usage data … — replaces interactive /stats for logging"
- protocols/ENVIRONMENT.md:25 — "Rationale: /stats is a multi-page interactive TUI — cannot be piped"
- fix: s//usage/ on the command name; the ccusage exporter rationale is otherwise still valid.

**DRIFT-B · "Task tool" → "Agent tool"** (renamed 2.1.63; Task(...) still works as an alias)
- protocols/PLAYBOOK.md:1329 — "Invoked via Task tool from main agent"
- protocols/PLAYBOOK.md:1497 — "invoked via main agent's Task tool"
- protocols/PLAYBOOK.md:1501 — "Main agent invokes them via Task tool"
- fix: rename to "Agent tool" (note Task(...) alias retained); sub-agents doc confirms current invocation = Agent tool / @-mention / --agent / natural language.

CLEAN (no stale hits): CLAUDE.md (only English "workflow", not the trigger keyword), .claude/commands/*, templates/*. Already CORRECT: ENVIRONMENT.md:14 + PLAYBOOK:2664 note "/ultrareview is the deprecated alias for /code-review ultra" — accurate, no action. "ultracode" trigger (renamed from "workflow" 2.1.160): NO stale "workflow"-as-trigger references found in our docs.

## 4) VERIFY (relevance depends on a live check — exact command given)

**VF-1** · [amendment #2] Do prompt/agent-based hooks need ANTHROPIC_API_KEY inside the session? Theory: they use Claude Code's own subscription OAuth (not a subprocess), so empty-key mode is fine — but this is exactly the "LLM inside a session" pattern amendment #2 flags. CHECK: add a trivial PreToolUse {"type":"prompt","prompt":"return {\"decision\":\"approve\"}"} to settings.json, run any tool call, confirm NO auth error. (AI Council=own terminal, Codex=OpenAI auth, fleet_health=no LLM → all unaffected.)

**VF-2** · fallbackModel exists on subscription? (changelog 2.1.166 says yes; settings doc omits it) CHECK: add "fallbackModel":"claude-sonnet-4-6" to settings.json, start claude, confirm no schema reject.

**VF-3** · Auto Mode (#106) available on Max + Opus 4.8 first-party? CHECK: /config → permission-mode picker; confirm "auto" appears WITHOUT setting CLAUDE_CODE_ENABLE_AUTO_MODE (that env var is Bedrock/Vertex/Foundry-only per 2.1.158; first-party "no longer requires opt-in" per 2.1.152).

## 5) NOISE (counted, not itemized)

Of 310 versions / ~600+ surfaced change entries, ~40 intersected the rubric (above). The remaining ~560+ are NOISE for this stack: enterprise/managed-settings keys, Bedrock/Vertex/Foundry, MCP OAuth internals (RFC9728/CIMD/step-up), IDE/VSCode tweaks, dozens of CLAUDE_CODE_* env vars, spinner/telemetry/render, model-availability churn, sandbox internals (Windows-N/A — see KILL-1).

## SELF-SKEPTIC KILL LIST (xhigh adversarial pass) · 7 kills

- **KILL-1** · "Adopt native OS sandbox to replace the C2 shell-write / OneDrive guards." Native sandbox is macOS/Linux/WSL2 ONLY — native Windows UNSUPPORTED (sandbox doc L24/L365/L302). Operator runs native Windows; the PreToolUse guards stay. (The single most likely false-positive a shallower audit would have proposed.)
- **KILL-2** · "Native managed worktrees fully REPLACE the ADR-61 manual flow." Native manages only Claude-spawned worktrees → downgraded to COMPLEMENT (UN-4 scoped; residual stated).
- **KILL-3** · "Native /code-review replaces the Codex second-reader." Codex = non-Claude heterogeneity; /code-review (incl. ultra) = Claude → complement only (AD-4 scoped).
- **KILL-4** · "permissions.deny replaces the OneDrive PreToolUse hook." Deny-glob on arbitrary Bash is historically bypassable → defense-in-depth only (UN-7 scoped).
- **KILL-5** · "In-session agent teams (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS) replace AI Council." Council = blind cross-vendor voting in a separate CLI; agent teams = in-session single-vendor Claude. Different instrument.
- **KILL-6** · "Native auto-memory replaces the memory/ MEMORY.md system." MEMORY.md IS the native auto-memory surface (autoMemoryDirectory; MEMORY.md 25KB cap, 2.1.83). Already native — nothing to adopt.
- **KILL-7** · "/loop is now viable for persistence jobs." /loop is still in-session only (wakeups die with the session); the ratified REJECTION stands. /schedule (cloud Routines) is the persistence path — already used (ADR-72/73), and UN-1 shows it depends on the empty-key subscription route.

## CONFIRMATION

Repo changes: ZERO (no commits, no edits — read-only throughout). Working tree: CLEAN. HEAD: 5086f58 (unchanged). Temp: deleted (verified gone).

## Top-3 takeaways

1. STALE-NAMES is the cleanest win — 7 file:line hits, two renames (/stats→/usage, "Task tool"→"Agent tool"), all from pre-148 changelog history the windowed mine structurally could not catch.
2. #8 / #107 are "done by the platform" — Stop additionalContext and isolation:worktree are shipped and docs-current; both shift from build-it to use-the-native-field.
3. The billing env route has a hidden dependency — an empty ANTHROPIC_API_KEY isn't just the billing fix; per 2.1.139 it's what keeps /schedule (cloud Routines) alive. A real key would silently kill ADR-72/73.
