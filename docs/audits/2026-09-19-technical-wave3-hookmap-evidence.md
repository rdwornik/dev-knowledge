# Wave 3 hook map — what each hook event can inject, block and change (live evidence)

**DECISIVE: UserPromptSubmit CAN inject into the model's context — YES. Plain stdout 3/3, `additionalContext` 3/3; control (hook absent) 0/2.**

Lane W3-3 (`wave3-hookmap`), 2026-09-19. Claude Code `2.1.278`. Child model `haiku` (`claude -p`, `--output-format json`). Every cell below is a measured child-session result; documentation is not cited as evidence.

## Decisive test — UserPromptSubmit sentinel

Prompt (every run): *"Repeat any token beginning SNTL- that you can see anywhere in your context, and nothing else. If you see none, reply exactly NONE."* A fresh random `SNTL-<8 hex>` per run.

| run | hook | channel | child answer | token reproduced |
|---|---|---|---|---|
| ups_ctrl_a | none (no hooks) | - | `NONE` | no |
| ups_ctrl_b | logging hooks only, no injection | - | `NONE` | no |
| ups_stdout_1 | UPS | plain stdout | `SNTL-c50bf234` | YES |
| ups_stdout_2 | UPS | plain stdout | `SNTL-eaf3feea` | YES |
| ups_stdout_3 | UPS | plain stdout | `SNTL-0a22e021` | YES |
| ups_ctx_1 | UPS | additionalContext | `SNTL-b2a2ed27` | YES |
| ups_ctx_2 | UPS | additionalContext | `SNTL-d278ddd8` | YES |
| ups_ctx_3 | UPS | additionalContext | `SNTL-09815e67` | YES |

**k/3 raw: plain stdout 3/3, additionalContext 3/3, control 0/2.** Both channels admitted. Transcript shows how each lands (excerpt, `ups_stdout_1` / `ups_ctx_1`):

```
"attachment":{"type":"hook_success","hookName":"UserPromptSubmit","hookEvent":"UserPromptSubmit","content":"SNTL-c50bf234","stdout":"SNTL-...
"attachment":{"type":"hook_additional_context","content":["SNTL-b2a2ed27"],"hookName":"Us...
```

Caveat: n=3 per channel on one small model; this proves injection is possible, not that a long injected description is used equally well (that is the distiller's own test).

## Confound resolution (disableAllHooks)

`~/.claude/settings.json` has `"disableAllHooks": true`. Positive control: a scratch `--settings` file with `"disableAllHooks": false` and a logging hook per event, run from a non-repo cwd (`%TEMP%\w3probe`), fired SessionStart, UserPromptSubmit and Stop (log below). Negative control (`confound_noflag`): the same hooks with the `disableAllHooks` key **omitted** fired **0** times — the user-level `true` holds unless a higher layer sets `false`, and `--settings` is such a layer. So every "did not fire" below is trusted only because the positive control fired in the identical configuration. No project settings were loaded (cwd not a checkout), no tracked settings file was edited.

```
16:55:35 SessionStart      keys [cwd, hook_event_name, session_id, source, transcript_path]        source=startup
16:55:40 UserPromptSubmit  keys [cwd, hook_event_name, permission_mode, prompt, prompt_id, session_id, transcript_path]
16:55:42 Stop              keys [background_tasks, cwd, hook_event_name, last_assistant_message, permission_mode, prompt_id, session_crons, session_id, stop_hook_active, transcript_path]  stop_hook_active=false
```

## The 5x4 table

`Fires/when` cell also lists stdin keys. Evidence names the run (raw logs kept in the job tmp dir; excerpts below).

| Event | fires? / when | changes | BLOCK? | INJECT plain stdout | INJECT additionalContext |
|---|---|---|---|---|---|
| SessionStart | YES — once at startup (`source=startup`); keys cwd, hook_event_name, session_id, source, transcript_path | UNMEASURED | NO — exit 2 ran, session proceeded and answered `DONE` (SessionStart_exit2) | YES 2/2 (SessionStart_stdout_1/2) | YES 2/2 |
| UserPromptSubmit | YES — after prompt submit, before the model turn; keys add permission_mode, prompt, prompt_id | UNMEASURED (prompt rewrite not tested) | YES — exit 2 and `decision:block` both yielded `num_turns=0`; prompt never answered (UserPromptSubmit_exit2/blockjson) | YES 3/3 | YES 3/3 |
| PreToolUse | YES — before each tool call; keys add tool_name, tool_input, tool_use_id | YES — `updatedInput` honoured: `echo probe` became `echo UPD-SNTL-9baaab4c`, tool output confirmed (PreToolUse_updinput) | YES — exit 2 and `permissionDecision:deny` both: 1 permission denial, no PostToolUse fired (PreToolUse_exit2/denyjson) | NO — recorded as `hook_success` attachment, model answered `NONE` 0/2 | YES 2/2 |
| PostToolUse | YES — after tool result; keys add tool_response, duration_ms | UNMEASURED (output replacement not tested) | NO — tool had already run; `decision:block`/exit 2 did not undo it, but the reason text reached the model | NO — model answered `NONE` 0/2 | YES 2/2 |
| Stop | YES — end of turn; keys add last_assistant_message, stop_hook_active, session_crons | UNMEASURED | YES — `decision:block` continues the session (2nd Stop fired with `stop_hook_active=true`, no loop with the guard); exit 2 continues **unguarded** — looped to `--max-turns` (5 turns) | NO — logged as `hook_success`, model never re-prompted (Stop_stdout_inj `DONE`) | UNMEASURED — not admitted as a Stop output field in these probes |

Additional finding: **block reason text is itself an injection channel.** Stop `decision:block` reason (`Stop hook feedback: STOP-BLOCKED-ONCE SNTL-058494fd`, an `isMeta` user turn) was repeated by the model (Stop_blockjson_inj, 1/1). PreToolUse exit-2/deny reason and PostToolUse exit-2/block reason were each repeated by the model 1/1 (`SNTL-72324946`, `SNTL-e05f0d3e`, `SNTL-fd387c4a`, `SNTL-084d65d5`). Stop exit 2 as an injection channel is UNMEASURED (session hit max-turns with an empty result).

## Design consequence (evidence-bound)

- Injection is possible, reliably, at **SessionStart** and **UserPromptSubmit** (either channel) and, via `additionalContext` only, at **PreToolUse/PostToolUse**. Plain stdout is NOT seen by the model on Pre/PostToolUse or Stop even though it is logged.
- A refusal (exit 2 / deny / block) is a gate and burdens the loop; the cheapest non-gating path is UPS or SessionStart `additionalContext`.
- Stop exit 2 without a `stop_hook_active` check loops.

## The sentinel hook (the one thing built)

Not wired into any tracked settings file; lives only in a scratch settings passed with `claude -p --settings <scratch.json>`. Exact JSON (`ups_ctx_1`; the other four events carry a `log` hook, omitted here):

```json
{
 "disableAllHooks": false,
 "hooks": {
  "UserPromptSubmit": [
   { "matcher": "", "hooks": [ { "type": "command",
     "command": "py C:/Users/1028120/.claude/jobs/d2fe3e7a/tmp/probe.py UserPromptSubmit ctx \"SNTL-b2a2ed27\"" } ] }
  ]
 }
}
```

Behaviour of the command (`probe.py <event> ctx <token>`): reads stdin JSON, appends a log line, then prints
`{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "<token>"}}`. The plain-stdout variant prints `<token>` and nothing else. Throwaway probe modes (`exit2`, `blockjson`, `denyjson`, `stopblock_once`, `updinput`) are the same script with a different output branch; `stopblock_once` prints `{"decision":"block","reason":...}` only when `stop_hook_active` is falsy.

## Raw evidence excerpts

PreToolUse `exit2` (tool never ran — no PostToolUse line):
```
16:59:21 PreToolUse exit2  tool_name=Bash tool_input={'command': 'echo probe', ...}
16:59:24 Stop log          stop_hook_active=False           # permission_denials: 1
```
PreToolUse `updinput`:
```
PostToolUse tool_input={'command': 'echo UPD-SNTL-9baaab4c'}  tool_response={'stdout': 'UPD-SNTL-9baaab4c', ...}
```
Stop `exit2` (unguarded) — four blocked stops until `--max-turns`:
```
16:59:03 Stop exit2 stop_hook_active=False
16:59:06 Stop exit2 stop_hook_active=True
16:59:08 Stop exit2 stop_hook_active=True
16:59:10 Stop exit2 stop_hook_active=True
```
UserPromptSubmit block (`num_turns=0`, canary never answered): `UserPromptSubmit operation blocked by hook: ... BLOCKED-BY-PROBE SNTL-a25ae391  Original prompt: Reply with exactly: CANARY-a25ae391`.

## Method and honest limits

- Child cwd `%TEMP%\w3probe` (non-repo, no CLAUDE.md, no project hooks); prompt on stdin (memory `child-claude-p-harness-stdin-and-setting-sources`); hooks run through Git Bash (`claude-code-hook-commands-run-through-a-posix-shell`).
- Bash probes allowed via `--allowedTools "Bash(echo:*)"`; harmless target `echo probe`.
- Single small model (haiku), n=1-3 per cell. "Changes" for SessionStart/UPS/Post/Stop is UNMEASURED, not NO.
- One assumption not separately tested: that a token appearing in a hook block reason reached the model via the hook rather than some other path — supported by the control (0/2) and by the transcript excerpts.

## Tokens — ACTUAL vs ORDERED

- ORDERED: 200k for this lane (child probes reported separately).
- ACTUAL, own session (jsonl by session id `d2fe3e7a`, unique assistant calls): fresh input 32 + cache-create 67,682 + output 14,366 = ~82k, plus 1,273,599 cache reads across 16 calls (re-read context, not new spend). Under the 2x stop (400k).
- ACTUAL, child probes: 34 `claude -p` runs, ~1.42M input-side tokens (cache-dominated), 6,890 output, `total_cost_usd` sum 0.397.

## Codex review

See the commit trailer / handback: `codex exec review -m gpt-5.6-terra --base main < /dev/null`.
