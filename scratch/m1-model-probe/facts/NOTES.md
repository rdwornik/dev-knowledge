# Facts first (done-contract 1) -- from the installed CLI, 2026-10-18

- `claude --version`: `2.1.302 (Claude Code)`
- `claude --help | grep -A2 effort`: `--effort <level>  Effort level for the current session (low, medium, high, xhigh, max)`
- `copilot --version`: `GitHub Copilot CLI 1.0.98.`

## Which effort levels each model accepts: NOT MEASURED -- the headless login is absent

All 12 one-line calls (`claude -p --output-format json --model <id> [--effort <level>] "reply ok"`, levels low, medium,
high, xhigh, max, plus no flag, for `claude-haiku-5-5` and `claude-sonnet-5-5`) returned, verbatim:

    is_error: true   result: "Not logged in · Please run /login"   total_cost_usd: 0   modelUsage: {}

`claude auth status` in the same shell: `"loggedIn": false, "authMethod": "none"`. The runner log
(`/workspaces/dispatch/run.log`) shows `CLAUDE_CODE_OAUTH_TOKEN set=yes` for the runner, but the variable is not in the
environment of this session's tool shell, and no `~/.claude/.credentials.json` exists. Because the refusal is the login
refusal and not an effort refusal, nothing here says which levels a model accepts: "Haiku highest accepted effort" is
**UNVERIFIED**. Raw files: `effort-<model>-<level>.json/.err/.exit`.
