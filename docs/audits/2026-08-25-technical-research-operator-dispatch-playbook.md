# Operator Playbook: Launching & Managing Claude Code (and Peer Coding-Agent CLIs) at Scale on Windows 11 + PowerShell

*Scope: a solo operator driving multi-session, multi-worktree "lane" workflows across three substrates — LOCAL (Claude Code in git worktrees), CLOUD (Claude Code on the web / Anthropic-hosted sessions), and GitHub Codespaces via `gh`. Current as of August 25, 2026. Primary sources: Anthropic Claude Code Docs (code.claude.com), GitHub Docs, GitHub CLI manual.*

## TL;DR

- **The canonical dispatch surface you want already exists in three vendor primitives** — `claude` (LOCAL, with `-p`/`--worktree`/`--output-format json`), `claude --cloud "<task>"` (CLOUD, Anthropic-hosted VM), and `gh codespace create` + `gh codespace ssh -c <name> -- "<cmd>"` (CODESPACES). The friction you feel is not missing tooling; it's the absence of ONE thin wrapper that gives each substrate a single verb with a fixed argument shape and a written receipt.
- **Recommended architecture (a recommendation, not a decision): one self-documenting PowerShell module exposing three verbs** — `Start-Lane` (LOCAL), `Start-CloudLane` (CLOUD), `Start-CodespaceLane` (CODESPACES) — because it is Windows-PowerShell-native, ships tab-completion + `Get-Help` from the same source that runs the command, and avoids the tmux dependency that rules out `claude-squad`/Crystal on native Windows. A `justfile` is the strong runner-up if you want terse `just --list` discoverability and don't mind installing `just`.
- **The dominant failure mode is the silent permission-prompt hang** in non-interactive contexts, plus PowerShell↔bash quoting corruption of prompt strings. Both are fully avoidable: pass prompts via files/stdin, pre-authorize with `--allowedTools`/`--permission-mode`, capture `--output-format json` as a receipt, and treat `--dangerously-skip-permissions` as a container-only flag.

---

## Key Findings

1. **Claude Code has a mature, documented headless surface.** `claude -p`/`--print` runs the full agent loop non-interactively and exits; it reads stdin, supports `--output-format text|json|stream-json`, `--max-turns`, `--json-schema`, `--resume`/`--continue`, and pre-authorization via `--allowedTools`/`--permission-mode`. A new `--bare` flag (recommended for scripts, and slated to become the `-p` default) skips discovery of hooks/skills/MCP/CLAUDE.md for reproducible, faster starts. The Agent SDK (Python/TypeScript) is the alternative to shelling out when you want in-process control.

2. **Native worktree support is now first-class.** `claude --worktree <name>` (short `-w`), shipped in Claude Code v2.1.49 (February 2026), creates an isolated worktree at `<repo>/.claude/worktrees/<name>` on branch `worktree-<name>` and starts the session there — no manual `git worktree add`. This is the LOCAL lane primitive.

3. **CLOUD dispatch is a documented CLI feature.** `claude --cloud "<task>"` creates an Anthropic-hosted VM session that clones your current repo's GitHub remote at your current branch, runs autonomously, and persists across browser/laptop closes. Each `--cloud` invocation is an independent parallel session; follow-ups go via `claude -p "<msg>" --cloud <session-id>` (queue-and-exit, `--output-format json` returns `{ok, session_id, url}`). It requires claude.ai auth (not API key), is in research preview, and shares your account rate limits with no separate compute charge.

4. **Codespaces is fully driveable from `gh`.** `gh codespace create` (with `--machine`, `--idle-timeout`, `--retention-period`, `--devcontainer-path`), `gh codespace ssh -c <name> -- "<command>"` for non-interactive command execution, and `gh codespace cp` for file transfer in/out. Published patterns run `claude -p` headless inside a codespace over SSH. Free tier (personal accounts only): 120 core-hours/month + 15 GB-month storage on GitHub Free; GitHub Pro includes 180 core-hours + 20 GB-month. Default idle timeout 30 min (configurable 5–240 min); stopped ≠ deleted (storage still bills).

5. **The Windows-native orchestration gap is real.** The most-cited multi-agent orchestrators — `claude-squad`, `cmux`, `workmux`, `claude-tmux` — all depend on tmux, which has no native Windows port; they require WSL. Windows-native options are desktop apps (Pane, Vibe Kanban) or your own PowerShell wrappers. This strongly favors a home-grown PowerShell/justfile launcher for a Windows solo operator.

6. **Doc-from-code is achievable on both candidate runners.** PowerShell comment-based help feeds `Get-Help`, and `Register-ArgumentCompleter` gives tab completion; `just --list` prints each recipe's `#` doc comment as a self-generating menu. Either lets the runbook be generated from the launcher itself so it can't drift.

---

## Details

### (a) Claude Code invocation-mechanics reference

All flag descriptions below are quoted/condensed from the **official CLI reference at code.claude.com/docs/en/cli-reference** (page reflects at least v2.1.233, fetched Aug 25 2026) and the **headless docs at code.claude.com/docs/en/headless**.

**Common commands (verbatim official descriptions):**

| Command | Official description | Source |
|---|---|---|
| `claude` | Start interactive session | cli-reference |
| `claude "query"` | Start interactive session with initial prompt | cli-reference |
| `claude -p "query"` | Query via SDK, then exit (print/headless) | cli-reference |
| `cat file \| claude -p "query"` | Process piped content | cli-reference |
| `claude -c` | Continue most recent conversation in current directory | cli-reference |
| `claude -c -p "query"` | Continue via SDK (non-interactive) | cli-reference |
| `claude -r "<session>" "query"` | Resume session by ID or name | cli-reference |
| `claude update` | Update to latest version | cli-reference |
| `claude mcp` | Configure MCP servers | cli-reference |

**Flags (verbatim/condensed official descriptions):**

| Flag | Purpose | Source (dated) |
|---|---|---|
| `--print`, `-p` | Print response without interactive mode; runs full agent loop then exits | cli-reference (Aug 2026) |
| `--output-format` | Output format for print mode: `text`, `json`, `stream-json` | cli-reference |
| `--input-format` | Input format for print mode: `text`, `stream-json` | cli-reference |
| `--model` | Set session model by alias (`sonnet`, `opus`, `haiku`, `fable`) or full name; overrides `model` setting & `ANTHROPIC_MODEL` | cli-reference |
| `--fallback-model` | Auto-fallback to specified model(s) when primary is overloaded/unavailable; comma-separated chain | cli-reference |
| `--permission-mode` | Start mode: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`, or `manual` (alias for default) | cli-reference |
| `--dangerously-skip-permissions` | Skip permission prompts; equivalent to `--permission-mode bypassPermissions` | cli-reference / permission-modes |
| `--allowedTools` / `--allowed-tools` | Tools that execute without prompting; supports permission rule syntax e.g. `Bash(git diff *)` | cli-reference |
| `--disallowedTools` / `--disallowed-tools` | Deny rules; bare name removes tool from context, scoped rule denies matching calls | cli-reference |
| `--max-turns` | Limit agentic turns (print mode only); exits with error at limit | cli-reference |
| `--max-budget-usd` | Stop print-mode execution at approximate dollar budget | cli-reference / headless |
| `--continue`, `-c` | Load most recent conversation in current dir (skips bg/`-p`/SDK sessions unless `-p` also passed) | cli-reference |
| `--resume`, `-r` | Resume specific session by ID/name or interactive picker | cli-reference |
| `--session-id` | Use a specific session ID (valid UUID) | cli-reference |
| `--append-system-prompt` | Append custom text to end of default system prompt | cli-reference |
| `--append-system-prompt-file` | Append system prompt text from a file | headless |
| `--system-prompt-file` | Load system prompt from file, replacing default | cli-reference |
| `--json-schema` | Validate print-mode structured output against a JSON Schema (with `--output-format json`) | headless |
| `--add-dir` | Add additional working directories to read/edit | cli-reference |
| `--mcp-config` | Load MCP servers from JSON files/strings | cli-reference |
| `--verbose` | Verbose turn-by-turn logging | cli-reference |
| `--bare` | Minimal mode: skip auto-discovery of hooks/skills/commands/subagents/plugins/MCP/auto-memory/CLAUDE.md; requires `ANTHROPIC_API_KEY` or `apiKeyHelper` (no OAuth/keychain); recommended for scripts, will become `-p` default | headless (v2.1.81+) |
| `--worktree`, `-w` | Start in isolated worktree at `<repo>/.claude/worktrees/<name>`; accepts `#<PR>` / PR URL / MR URL | cli-reference (v2.1.49, Feb 2026) |
| `--cloud` | Create/target an Anthropic-hosted web session | cli-reference / claude-code-on-the-web |
| `--teleport` | Resume a web session in local terminal | cli-reference / claude-code-on-the-web |
| `--bg`, `--background` | Start as background agent, return immediately; cannot combine with `-p` | cli-reference |
| `--effort` | Session effort level: `low`, `medium`, `high`, `xhigh`, `max`, `ultracode` (model-dependent) | cli-reference |

**Interactive vs print mode for long agentic tasks:** Both run the same engine, tools, and agent loop. The REPL loops until you exit and prompts for tool approvals interactively; `-p` runs and returns, and combined with permission flags is fully non-interactive. Key print-mode behaviors from the headless docs: `-p` rejects `--bg` and `--cloud "<task>"`; background bash tasks are killed ~5s after the final result; SIGTERM yields exit code 143 and leaves the in-progress turn unfinished (resumable), while SIGINT ends the turn; stdin is capped at 10MB; exit code is 0 on success, non-zero on failure. **Critically, without `--bare`, a `-p` session runs a project's `.claude/settings.json` hooks and connects `.mcp.json` MCP servers even in an untrusted folder, with no trust dialog** — a supply-chain sharp edge for scripted runs.

**Scripting/automation guidance (official):** headless mode is the documented foundation; the Agent SDK (renamed from "Claude Code SDK" to "Claude Agent SDK") wraps the same engine as a library for Python/TypeScript. For other languages, Anthropic's own docs say run the CLI as a subprocess with `-p --output-format json`. There is an official GitHub Action (`anthropics/claude-code-action@v1`). `claude setup-token` generates a long-lived OAuth token for CI (requires a subscription). Note: as of June 15, 2026, programmatic usage (SDK, `claude -p`) still draws from subscription usage limits; Anthropic recommends a Claude Platform API key for predictable pay-as-you-go automation.

### (b) Orchestration-tools landscape

| Tool | What it automates | Windows support | Status (2026) |
|---|---|---|---|
| **Claude Code native `--worktree`** | Worktree provisioning + session launch in one flag; subagent `isolation: worktree` | Native (it's the CLI itself) | Actively developed; shipped v2.1.49 Feb 2026, still receiving fixes (e.g., v2.1.218 Jul 22 2026) |
| **claude-squad** (smtg-ai) | TUI managing many agents (Claude Code, Codex, Aider, Gemini, etc.), each in its own tmux session + git worktree; background/auto-accept | **No native Windows** — needs tmux → WSL only | Open source (AGPL-3.0), actively maintained; installs as `cs` |
| **Crystal / Nimbalyst** | Desktop apps, worktree-per-session, visual diff/review | Crystal desktop; Nimbalyst has native Windows build | Nimbalyst active; Crystal maintained |
| **vibe-kanban** (BloopAI) | Kanban board; card = one worktree + one agent + one review; agent-agnostic | Cross-platform (npx) | **Bloop announced shutdown Apr 10, 2026**; now community-maintained, fully local, cloud features removed |
| **cmux / workmux / claude-tmux** | tmux+worktree wrappers with completion (bash/zsh) | tmux-only → WSL on Windows | Community projects, active |
| **Pane** | Desktop app, any CLI agent, worktree isolation without tmux, built-in diff | **First-class native Windows** (unsigned → SmartScreen warning) | Active commercial/OSS |
| **amux** | "Control plane" for fleets of headless `claude -p` sessions; dashboard + iOS monitor | Cross-platform (self-hosted) | MIT, active |
| **PowerShell / justfile DIY wrapper** | Whatever you script: worktree, launch, receipt, teardown | **Native Windows** | You own it |

**What practitioners converge on:** git worktree isolation is universal ("every tool converges on git worktrees"). Anthropic's own team endorses this: Boris Cherny (@bcherny), the creator of Claude Code, wrote in a Jan 31, 2026 X thread, *"Do more in parallel. Spin up 3–5 git worktrees at once, each running its own Claude session in parallel. It's the single biggest productivity unlock, and the top tip from the team."* Per Vibe Coder Blog's account of his setup, Cherny "runs five Claude Code instances in parallel terminal tabs, each with its own git worktree… Then he opens five to ten more sessions on claude.ai/code in his browser. Then he keeps the iOS app open too" — a pattern Anthropic researcher Sholto Douglas calls **"multiplexing,"** and by which Cherny reportedly landed ~150 PRs in a single day. The operator interface splits into three camps: **terminal session managers** (claude-squad), **desktop task boards** (vibe-kanban, Pane), and **DIY one-command-per-lane wrappers**. For a Windows solo operator, camp 1 is blocked by tmux and camp 2 adds a GUI you didn't ask for — pushing toward camp 3.

### (c) Recommended minimal dispatch architecture (a recommendation, with trade-offs — NOT the decision)

**Primary recommendation: a single PowerShell module `LaneKit` exposing one verb per substrate.**

```
Start-Lane          -Repo <path> -Name auth-fix -Prompt <file|string> [-Model opus] [-Print]   # LOCAL
Start-CloudLane     -Repo <path> -Title "auth-fix" -Prompt <file>                                # CLOUD
Start-CodespaceLane -Repo owner/repo -Name auth-fix -Prompt <file> [-Machine standardLinux32gb] # CODESPACES
Get-Lane            # list active lanes across all three (reads a receipts dir)
Stop-Lane           -Name auth-fix
```

- **LOCAL** wraps `claude --worktree <name> --model <m> --output-format json` (or interactive without `-p`), reading the prompt from a file to sidestep quoting, and writing a JSON receipt.
- **CLOUD** wraps `claude --cloud "<task>"`, captures the returned session ID/URL as a receipt, and offers `Send-CloudLane` → `claude -p "<msg>" --cloud <id> --output-format json`.
- **CODESPACES** wraps `gh codespace create … --idle-timeout 30m --retention-period 24h`, `gh codespace cp` the prompt file in, `gh codespace ssh -c <name> -- "claude -p \"\$(cat /workspaces/prompt.md)\" --output-format json > /workspaces/receipt.json"`, then either pushes from inside or `gh codespace cp` the receipt out.

Why this wins for THIS setup:
- **Windows-PowerShell-native**, zero tmux, zero WSL tax.
- **Self-documenting from the same source that runs the command**: comment-based help → `Get-Help Start-Lane -Examples`; `Register-ArgumentCompleter` → tab completion of lane names/models; a `Get-Lane`/`Show-LaneKit` command lists everything. The runbook is generated from the module, so it can't drift.
- **One argument shape across all three verbs** kills the "every session invents a new procedure" problem.

Trade-offs / when to pick differently:
- **justfile** is the runner-up: `just --list` is the single best out-of-the-box "list everything" menu, recipes carry `#` doc comments, and it's cross-platform. Costs: extra `just` install, and on Windows you must `set shell := ["powershell.exe","-c"]` or recipes fail (they default to `sh`, absent on Windows); no `Get-Help`/typed tab-completion.
- **Taskfile (go-task)** — YAML, cross-platform, good if you prefer declarative; weaker discoverability than `just --list`.
- **Make** — avoid on Windows (tab-sensitive, needs a `sh`).
- If you later want a visual board across lanes, layer **vibe-kanban** or **Pane** on top; they don't replace the wrapper, they observe it.

**Benchmarks that would change the recommendation:** if you outgrow ~5 concurrent local lanes and need live monitoring, adopt a control plane (amux) or desktop board (Pane); if you standardize on WSL for dev anyway, `claude-squad` becomes viable and gives you a ready-made TUI.

### (d) Cloud + Codespaces dispatch specifics (commands)

**CLOUD (Claude Code on the web), per code.claude.com/docs/en/claude-code-on-the-web:**
```powershell
# One-time: sync gh token to Claude account
#   run /web-setup inside claude, OR authorize the Claude GitHub App
claude --cloud "Execute the migration plan in docs/migration-plan.md"   # new session; clones GitHub remote @ current branch
claude --cloud "Fix the flaky test in auth.spec.ts"                      # parallel session #2
# follow-up (queue-and-exit; machine-independent; works in PowerShell):
claude -p "also update the changelog" --cloud session_01Di... --output-format json
# pull a cloud session back to local terminal:
claude --teleport                     # interactive picker
claude --teleport <session-id>        # specific
```
Documented capabilities/limits: isolated Anthropic-managed VM per session; repo cloned from GitHub (push local commits first — it clones the remote, not your working copy); limited network access by default; **credentials (git/signing keys) are never in the sandbox** — auth via a secure proxy with scoped creds; requires claude.ai auth (API key/Bedrock/Vertex not supported); one-way CLI handoff (teleport web→terminal; no terminal→web push from CLI); shares account rate limits, no separate compute charge; non-GitHub repos can be sent as a local bundle (<100 MB) but can't push back; IP-allowlisted orgs must exempt Anthropic infra. Local repos without GitHub auto-bundle (`CCR_FORCE_BUNDLE=1` to force). Cloud sessions support most built-in commands; `/clear` and terminal-only pickers don't work.

**CODESPACES via `gh`, per GitHub Docs + GitHub CLI manual:**
```powershell
# Create with cost controls
gh codespace create -R owner/repo -b main `
  --machine standardLinux32gb --idle-timeout 30m --retention-period 24h `
  --display-name "lane-auth-fix"
$cs = gh codespace list --json name --jq '.[0].name'   # capture name
# Push a prompt file in
gh codespace cp .\prompt.md "remote:/workspaces/repo/prompt.md" -c $cs
# Run the agent headlessly (single remote command; note quoting)
gh codespace ssh -c $cs -- "cd /workspaces/repo && claude -p \"`$(cat prompt.md)\" --output-format json --allowedTools 'Read,Edit,Bash' > receipt.json 2>&1"
# Retrieve the receipt (or have the agent git push from inside)
gh codespace cp "remote:/workspaces/repo/receipt.json" .\receipt.json -c $cs
gh codespace stop -c $cs          # stop to halt compute billing (storage still accrues)
gh codespace delete -c $cs        # delete to stop storage billing
```
Notes: `gh codespace ssh -c <name> -- <cmd>` runs a command non-interactively (syntax `ssh [flags] user@host command`); the codespace must run an SSH server (default image does; custom images add the `sshd` devcontainer feature). `--idle-timeout` accepts 5m–240m; `--retention-period` max 30 days. Machine types: `basicLinux32gb`, `standardLinux32gb` (2-core), `premiumLinux`, `largePremiumLinux`. **Cost math (GitHub published rates):** compute is billed at **$0.18/hr for a 2-core machine**, scaling by core count (4-core = $0.72/hr, 16-core = $2.88/hr); storage is **$0.07/GB-month**. 120 free core-hours/month ≈ 60 h on a 2-core, ≈ 30 h on a 4-core; a 4-core left running a full Friday-evening-to-Monday weekend (~60 h × $0.72) costs ≈ **$43** in compute alone. Stopped codespaces still consume the storage quota. Prebuilds cut spin-up time at the cost of ongoing storage. A published pattern (blle.co) wraps exactly this — VPS API → `gh codespace ssh` → `claude -p` → stdout piped back — showing the approach is proven end-to-end.

### (e) Anti-patterns checklist

- **Permission-prompt hang (the #1 killer).** In non-interactive contexts a tool-approval prompt blocks forever — "no timeout and no error; the agent just stops." Fix: always pass `--allowedTools` (scoped, e.g. `Bash(npm test)`) and/or `--permission-mode acceptEdits|dontAsk|auto`; never rely on defaults. `dontAsk` denies anything not allow-listed rather than prompting.
- **`--dangerously-skip-permissions` outside a sandbox.** It auto-approves every bash command, edit, network call, and MCP call, and subagents inherit it with no override. Anthropic's guidance and community consensus: use it **only** inside a container/VM with locked-down network egress (the reference devcontainer with default-deny firewall). A reported bug had it silently override `--permission-mode plan`. On Linux/macOS it refuses to run as root/sudo. Prefer the new **auto mode** (classifier-reviewed) for host use.
- **PowerShell↔bash quoting corruption.** Claude Code runs its Bash tool via Git Bash on Windows; passing PowerShell inline gets `$_`/`$var` expanded by bash before PowerShell sees it, and backslash paths mangled (`C:\Users\cl` → `C:Userscl`). Multiple open GitHub issues (#15471, #55727, #51430). Fix: **pass prompts as files or via stdin, not inline argument strings**; use the stop-parsing token `--%` when you must pass literal args through PowerShell to a native exe; keep prompts in `.md` files under version control.
- **No receipt = no proof of dispatch.** Always capture `--output-format json` (includes `session_id`, `total_cost_usd`, per-model cost — client-side estimates) to a per-lane receipt file; for cloud, capture the `{ok, session_id, url}` JSON; for codespaces, redirect stdout/stderr to `receipt.json` and copy it out or push it. A receipts directory is what `Get-Lane` reads to prove what ran.
- **Zombie sessions / cost leaks.** Local `-p` runs can be held open by never-exiting background bash (capped since v2.1.163/v2.1.182); codespaces left running burn core-hours (a 4-core over a weekend ≈ $43) and stopped ones still bill storage. Fix: set aggressive `--idle-timeout`/`--retention-period`, `gh codespace stop`/`delete` in teardown, and audit `gh codespace list` regularly.
- **Ambient config in scripted runs.** Without `--bare`, `claude -p` silently loads hooks/MCP from the working tree even in untrusted folders. Fix: use `--bare` for CI/scripted lanes and pass only what you need via `--settings`/`--mcp-config`/`--append-system-prompt-file`.
- **tmux-dependent orchestrators on native Windows.** `claude-squad`/`cmux`/`workmux` need WSL; don't build a Windows runbook on them expecting native behavior.

---

## Recommendations

1. **Now (day 1): standardize the prompt contract.** Every lane's task lives in a versioned `prompt.md`. This single change eliminates the quoting class of failures and makes all three substrates take the same input. Benchmark to revisit: if prompts stay <1–2 short lines you may inline them, but files remain safer.
2. **Week 1: build the thin PowerShell module** (`Start-Lane`/`Start-CloudLane`/`Start-CodespaceLane` + `Get-Lane`/`Stop-Lane`) with comment-based help and `Register-ArgumentCompleter`. Wrap the exact vendor commands in section (d); write a JSON receipt per lane to `~/.lanekit/receipts/`. Ship `Get-Help` examples so the runbook self-generates.
3. **Week 1, parallel: set Codespaces cost guards** — default idle timeout 15–30 min, retention 1 day, prefer 2-core, add a `Stop-Lane` that always `gh codespace stop`s. Configure a Codespaces spending budget with "pause at limit."
4. **Week 2: pick your headless safety defaults.** For unattended local lanes use `--bare -p --permission-mode acceptEdits --allowedTools "<scoped>" --max-turns <cap> --output-format json`. Reserve `--dangerously-skip-permissions` for codespaces/containers only.
5. **Evaluate, don't pre-commit, a board/control-plane.** Run the wrapper for two weeks; if you routinely exceed ~5 concurrent lanes or want at-a-glance status, add **Pane** (native Windows, no tmux) or **amux** (headless fleet) as an *observer* over the same receipts. Threshold: > 5 concurrent lanes or > 1 substrate needing live monitoring.
6. **If you adopt `just` instead of/alongside PowerShell**, make `default: @just --list` the first recipe, set the PowerShell shell, and keep a `#` doc comment on every recipe so `just --list` is the runbook.

## Caveats

- **This space changes weekly.** Claude Code shipped `--worktree` in Feb 2026 and was still fixing it in late July 2026; `--bare` is documented to become the `-p` default "in a future release"; Cloud/Remote Control are **research preview**. Re-check code.claude.com before relying on any single flag's behavior.
- **Cloud vs Remote Control are different products** and easy to conflate: `--cloud` runs on Anthropic infra (fresh VM, no local files); `--remote-control` exposes a *local* session to phone/browser (one session at a time, terminal must stay open, ~10-min network-loss timeout). For dispatching work you want `--cloud`.
- **Some flag names appear in community cheatsheets but aren't all in official docs** (e.g., `-n` session-name); where this report cites the official cli-reference/headless pages the flags are confirmed, but treat third-party cheatsheets as unverified.
- **Billing for programmatic use is in flux** (the separate Agent SDK credit pool was paused June 15, 2026). Confirm current terms in Anthropic's Help Center before building always-on automation.
- **Codespaces free-tier numbers are for personal accounts only** (120 core-hours/15 GB on Free, 180/20 on Pro; not included on org/enterprise accounts) and can change; verify against your GitHub billing page.
- The recommended architecture is exactly that — **a recommendation**. The decision on PowerShell-module vs justfile vs a desktop board is yours; the trade-offs above are the inputs.