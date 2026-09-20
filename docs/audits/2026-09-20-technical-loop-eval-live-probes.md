# LIVE-PROBES — the loop's candidate mechanisms, run live (LANE-loop-eval, step 3)

> **Status:** record of four probes (B1-B4) run on 2026-09-20 from `worktree-lane-loop-eval`, carrier row `[#929]`.
> Rulings: `to-cc/DECLARE-LOOP-EVAL-2026-09-20.md` R1, R2, R7. Companion record: `2026-09-20-technical-loop-eval-mapping.md`.
> **Scope:** evidence only. Nothing was built, fixed, wired or re-armed. Probe scripts are scratch (kept in the job's
> scratch dir, outside the repo, so the tree stays clean) and are reproduced **inline** below; they are not tools.
> **Environment:** Windows 11, `claude` 2.1.278, `codex-cli` 0.155.0, `claude-agent-sdk` 0.2.157 installed **ephemerally**
> (`uv run --no-project --with claude-agent-sdk`) — `pyproject.toml` and `uv.lock` were not touched; `git status` was clean after every probe.

## Verdict table

```
probe  question                                                            verdict
B1     SDK: does the Python hook fire+deny; does the budget end the run     PASS
       and report its cost?
B2     codex exec (terra): prompt in -> result + usage out, in B1's shape?  PARTIAL
B3     pydoit: does a re-run skip completed stages?                         FAIL  (re-executes every stage, by design)
B4     a --bg spawn from inside a session gets an Agent View row + record?  PASS
```

---

## B1 — Claude Agent SDK `query()` on haiku, a Python PreToolUse hook, a budget below need

**Question.** Does the hook fire and deny, and does the budget end the run, reporting its cost? (main thread only.)

**Command** (run twice: budget `0.02` = below need, budget `0.06` = control that completes):

```
uv run --no-project --with claude-agent-sdk python b1_sdk_probe.py 0.02
uv run --no-project --with claude-agent-sdk python b1_sdk_probe.py 0.06
```

**Script** (`b1_sdk_probe.py`, scratch, inline in full):

```python
import asyncio, json, sys, time
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher, query
from claude_agent_sdk import AssistantMessage, ResultMessage, ToolUseBlock

BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 0.02
DENY = "probe-forbidden"
HOOK_LOG = []

TASK = (
    "Do these steps in order, one tool call at a time, and do not skip any:\n"
    "1. Read scripts/dodo.py (first 30 lines).\n"
    "2. Run the Bash command: echo PROBE_OK\n"
    f"3. Run the Bash command: echo {DENY}\n"
    "4. Then read scripts/dispatch.py, scripts/audit.py, scripts/gen_task_tree.py and scripts/file_purpose_graph.py "
    "(first 60 lines each) and write a two-sentence summary of each.\n"
)

async def pre_tool_use(input_data, tool_use_id, context):
    entry = {"t": round(time.time() % 1000, 2), "tool": input_data.get("tool_name"), "input": input_data.get("tool_input")}
    cmd = json.dumps(input_data.get("tool_input", {}))
    denied = DENY in cmd
    entry["decision"] = "deny" if denied else "allow"
    HOOK_LOG.append(entry)
    print("HOOK", json.dumps(entry)[:300], flush=True)
    if denied:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": f"probe policy: '{DENY}' is refused"}}
    return {}

async def main():
    opts = ClaudeAgentOptions(
        model="haiku",
        cwd=r"C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\lane-loop-eval",
        allowed_tools=["Read", "Bash"],
        permission_mode="dontAsk",
        max_budget_usd=BUDGET,
        setting_sources=[],
        hooks={"PreToolUse": [HookMatcher(matcher="Read|Bash", hooks=[pre_tool_use])]},
    )
    result = None
    try:
        async for msg in query(prompt=TASK, options=opts):
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, ToolUseBlock):
                        print("TOOL_USE", b.name, json.dumps(b.input)[:120], flush=True)
            if isinstance(msg, ResultMessage):
                result = msg
    except Exception as e:  # the budget trip arrives as a raised ResultError
        print("RAISED", type(e).__name__, str(e)[:200])
        for k, v in vars(e).items():
            print("  ATTR", k, json.dumps(v, default=str)[:600])
        r = getattr(e, "result", None)
        if isinstance(r, ResultMessage):
            result = r
    print("HOOK_CALLS", len(HOOK_LOG))
    if result:
        print("RESULT", json.dumps({
            "subtype": result.subtype, "is_error": result.is_error, "num_turns": result.num_turns,
            "total_cost_usd": result.total_cost_usd, "stop_reason": result.stop_reason,
            "terminal_reason": result.terminal_reason, "errors": result.errors,
            "model_usage": result.model_usage, "permission_denials": result.permission_denials,
            "duration_ms": result.duration_ms}, default=str))

asyncio.run(main())
```

*(A first attempt at budget `0.02` without the `try/except` tripped after the first tool call and surfaced only
`claude_agent_sdk._errors.ResultError: Claude Code returned an error result: Reached maximum budget ($0.02)` — the
traceback carried no cost; the `except` block above is what recovers it. That first run is why the script has the block.)*

**Verbatim load-bearing output — budget 0.02 (below need):**

```
HOOK {"t": 37.66, "tool": "Read", "input": {"file_path": "...\\scripts\\dodo.py", "limit": 30}, "decision": "allow"}
HOOK {"t": 39.74, "tool": "Bash", "input": {"command": "echo PROBE_OK", ...}, "decision": "allow"}
HOOK {"t": 48.38, "tool": "Bash", "input": {"command": "echo probe-forbidden", ...}, "decision": "deny"}
HOOK {"t": 51.23, "tool": "Read", "input": {"file_path": "...\\scripts\\dispatch.py", "limit": 60}, "decision": "allow"}
HOOK {"t": 53.55, "tool": "Read", "input": {"file_path": "...\\scripts\\audit.py", "limit": 60}, "decision": "allow"}
RAISED ResultError Claude Code returned an error result: Reached maximum budget ($0.02) (exit code: 1)
  ATTR subtype "error_max_budget_usd"
  ATTR errors ["Reached maximum budget ($0.02)"]
  ATTR terminal_reason "budget_exhausted"
HOOK_CALLS 5
RESULT {"subtype": "error_max_budget_usd", "is_error": true, "num_turns": 5, "total_cost_usd": 0.025860200000000007,
 "stop_reason": "tool_use", "terminal_reason": "budget_exhausted", "errors": ["Reached maximum budget ($0.02)"],
 "model_usage": {"claude-haiku-4-5-20251001": {"inputTokens": 1050, "outputTokens": 902, "cacheReadInputTokens": 127182,
   "cacheCreationInputTokens": 3791, "costUSD": 0.025860200000000007, "canonicalModel": "claude-haiku-4-5", "provider": "firstParty", "costBasis": "list"}},
 "permission_denials": [{"tool_name": "Bash", "tool_input": {"command": "echo probe-forbidden", ...}}], "duration_ms": 19532}
```

**Control — budget 0.06 (completes):** `HOOK_CALLS 7`, the same deny on `echo probe-forbidden`, then
`RESULT {"subtype": "success", "num_turns": 8, "total_cost_usd": 0.054383100000000004, "terminal_reason": "completed", ...}`.

**Verdict: PASS.**
- The Python `PreToolUse` hook fired on **every** tool call (5 of 5 before the trip, 7 of 7 in the control) and the `deny`
  was honoured: `echo probe-forbidden` never ran, and the denial is reported twice — in the hook log and in
  `permission_denials` of the result.
- The budget **ended the run** (`terminal_reason: budget_exhausted`, `subtype: error_max_budget_usd`) mid-task, and **reported its cost**
  (`total_cost_usd` and per-model `model_usage`, model id `claude-haiku-4-5-20251001`).
- **Two facts an adapter must absorb:** (1) the cap is checked **between turns**, so cost overshoots it —
  `0.02` cap, `0.0259` spent (29 % over); (2) the SDK **yields the `ResultMessage` and then raises** `ResultError` from the
  same iterator, so a stage-13 adapter that does not `catch` sees a crash instead of a cost. Also: `dontAsk` + an
  explicit `allowed_tools` list gave a closed tool surface with no prompt.
- **What B1 did not test** (Codex adversary, finding 12): it exercised one `query()` process with two tools, one hook and one budget. Process-tree teardown when the adapter itself dies, cancellation, crash recovery, a durable run identity, and cap enforcement after the adapter's death were **not** probed — the properties a RUN stage needs so that a writing agent is never left alive. "Adapter-shaped" is what B1 shows; "works as the stage-13 adapter" is not shown.

---

## B2 — `codex exec` as a subprocess, model pinned to terra

**Question.** Does a prompt go in and a result plus usage come out, in B1's shape?

**Routing source.** `ecosystem/routing-table.yaml` `roles.reviewer`: `cli: codex`, `model: gpt-5.6-terra`.

**Command** (PowerShell; stdin closed with `< NUL` because `codex exec` otherwise waits on stdin; read-only sandbox; no commit):

```
codex exec -c model=gpt-5.6-terra --sandbox read-only --json --skip-git-repo-check -o b2-last.txt "Do these steps in order: 1. Read the first 30 lines of scripts/dodo.py. 2. Run the shell command: echo PROBE_OK. 3. Reply with exactly two sentences: what scripts/dodo.py is, and the output of step 2. Do not modify any file." < NUL > b2-events.jsonl 2> b2-err.txt
```

**Verbatim load-bearing output** (exit 0, 20.0 s, 9 JSONL events; stderr was one line, `Reading additional input from stdin...`):

```
{"type":"thread.started","thread_id":"01a0bee6-4d09-7613-8b50-e351f8f22b98"}
{"type":"item.started","item":{"id":"item_1","type":"command_execution","command":"\"C:\\\\Program Files\\\\PowerShell\\\\7\\\\pwsh.exe\" -Command 'Get-Content -LiteralPath scripts/dodo.py -TotalCount 30'", ...}
{"type":"item.completed","item":{"id":"item_2","type":"command_execution","command":"...pwsh.exe\" -Command 'echo PROBE_OK'","exit_code":0,"status":"completed"}
{"type":"item.completed","item":{"id":"item_3","type":"agent_message","text":"scripts/dodo.py is a doit adapter for the ecosystem harness stage table.  \nThe command output was PROBE_OK."}}
{"type":"turn.completed","usage":{"input_tokens":36311,"cached_input_tokens":24064,"cache_write_input_tokens":0,"output_tokens":219,"reasoning_output_tokens":13}}
```

The `-o` file held the same two sentences. Each shell command's `aggregated_output` began with two `profile.ps1: Cannot dot-source this command because it was defined in a different language mode` lines before the real output.

**Verdict: PARTIAL.**
- **Works:** a prompt goes in; a final result comes out (`agent_message` and the `-o` file); a usage object comes out (`turn.completed.usage`); every tool call is an event with `exit_code`. An adapter can wrap it.
- **Not in B1's shape:** (a) **no cost** — tokens only, so the price must be computed from a rate table; (b) **no model id** in any event, so "RAN terra" cannot be proved from the output, only from the flag that was passed; (c) **no budget cap**, so B1's stop-loss has no equivalent — the only bound is a wall-clock timeout the caller must impose; (d) **no hook seam** — there is no pre-tool deny point, only the sandbox mode; (e) `codex exec` **blocks on stdin** unless it is closed, and prints a `Reading additional input from stdin...` line even then; (f) the sandboxed shell prints profile noise into every command's output.

---

## B3 — pydoit resume: run the spine as recorded, then re-run it unchanged

**Question.** Does doit skip the completed stages, or re-execute them? (stage 7 was **not** fixed.)

**Command** (run twice, back to back, unchanged):

```
$env:HARNESS_KIND='WIRE'; $env:HARNESS_SUBJECT='dispatch'
uv run --locked doit -f scripts/dodo.py spine
```

**Disclosure — a first run stopped at stage 3, for a reason this lane caused.** With `[#929]` filed as a task file but not yet registered in `tasks/manifest.json` (the contract forbids index regeneration; the integrator does it once), stage 3 `gen_task_tree.py --check` refused:

```
.  stage:03-carrier-row
gen_task_tree: check FAIL: retired allocation record is not marked terminal: 929-the-spine-is-the-whole-work-loop-map-every-organ-onto-stages-1-16-and-run-the-mechanisms-live.md (status: 'open'; expected one of closed, retired, superseded) — ADR-107 §6.3 ...
TaskFailed - taskid:stage:03-carrier-row
```

That is a finding in its own right (see the MAPPING record): **a lane that files a row without its manifest node makes spine stage 3 refuse.** To answer the actual question the row was registered *in scratch* (a manifest node inserted after task 928 by a scratch script, then `gen_task_tree.py --emit-source`), the two runs below were made, and **every touched file was then restored** (`git restore BACKLOG.md tasks/manifest.json tasks/929-*.md`; `git status` clean afterwards).

**Verbatim load-bearing output** (run 1 started 14:53:08.101, exit 1 at 14:53:37.855; run 2 started 14:53:37.861, exit 1 at 14:54:07.637):

```
=== spine run 1 start                   === spine run 2 start
.  stage:01-kind-subject                .  stage:01-kind-subject
.  stage:02-prior-art                   .  stage:02-prior-art
.  stage:03-carrier-row                 .  stage:03-carrier-row
.  stage:04-change-kind                 .  stage:04-change-kind
.  stage:05-dependencies                .  stage:05-dependencies
   nodes    : 3010                         nodes    : 3010
.  stage:06-library-first               .  stage:06-library-first
   Scanning 184 files...                   Scanning 184 files...
   Success! No dependency issues found.    Success! No dependency issues found.
.  stage:07-substrate                   .  stage:07-substrate
validate_substrate.py: error: the following arguments are required: paths
TaskFailed - taskid:stage:07-substrate
Command failed: '['uv', 'run', '--locked', 'python', 'scripts/validate_substrate.py', '--rules']' returned 2
```

**Verdict: FAIL — as wired, the spine has no resume.** Both runs re-executed stages 1-6 in full (30 s each, no speed-up, stage 5 and 6 re-emitted their output) and both halted at stage 7 with exit 2. The cause is on the page in `scripts/dodo.py:75`: every stage task is declared `"uptodate": [False]`, which tells doit the task is **never** up to date. The file states no reason for it (recomputing is a defensible default for a check against live state, since a cached "pass" can be stale, but that is an inference, not a recorded policy), and the effect is that the answer to "do interrupted runs resume without a lost step" is **no**: a run that stops at stage N restarts at stage 1. doit's state db (`dodo.py:29-35`, in the system temp dir keyed by the checkout path) records task results, but no stage consults it. Resume, if wanted, is a design decision — either drop `uptodate: [False]` for the deterministic stages and key it on input hashes, or keep the recompute and pay the ~30 s per restart — and neither has been made. **Not probed** (Codex adversary, finding 10, UNVERIFIED): the state db is one file per checkout path (`dodo.py:29-38`), so two spine runs in the same checkout would share it; whether doit serialises or corrupts that is not measured here.

---

## B4 — one `--bg` spawn from inside a session (DECLARE R7 / AMEND A4)

**Question.** Does a background job spawned from inside a session get its own Agent View row and job record?
(AM-5 premise: it does not; measured false twice before — 2026-08-15 container CLI 2.1.233, 2026-09-19 host job `4c128d01` CLI 2.1.278.)

**Command:**

```
claude --bg --model haiku "Reply with the single word DONE and do nothing else. Use no tools."
claude agents --json          # the row
Get-ChildItem C:\Users\1028120\.claude\jobs\0cac8686        # the job record
claude rm 0cac8686            # teardown: that job's own id only
```

**Verbatim load-bearing output:**

```
backgrounded · 0cac8686
  claude agents             list sessions
  claude attach 0cac8686    open in this terminal
  claude logs 0cac8686      show recent output
  claude stop 0cac8686      stop this session
```

Its row in `claude agents --json`, ~15 s later:

```
{"pid":16924,"id":"0cac8686","cwd":"C:\\Users\\1028120\\Documents\\Dev\\.dev-knowledge\\.claude\\worktrees\\lane-loop-eval","kind":"background","startedAt":1789909202955,"sessionId":"0cac8686-4248-4f5e-bb9d-e19c267798a0","name":"conversation interaction labeling","status":"busy","state":"working"}
```

Its job record `C:\Users\1028120\.claude\jobs\0cac8686\` held `state.json` (`"template": "bg"`, `"respawnFlags": ["--model","haiku","--permission-mode","default"]`,
`"intent": "Reply with the single word DONE and do nothing else. Use no tools."`) and `timeline.jsonl`:

```
{"at":"2026-09-20T13:00:10.355Z","state":"done","detail":"user request completed","text":"DONE"}
{"at":"2026-09-20T13:00:19.381Z","state":"working","detail":"Reading JOURNAL.md","text":""}
```

Teardown, verified by the record itself:

```
removed 0cac8686
record dir exists: False
row still listed: False
remaining ids: dc092468,90ac7484,a04ed419,6bb0f2c7,9c53bd44,bc6e739e      (the six ids present before the spawn; none touched)
```

**Verdict: PASS — the AM-5 premise is false again, a third time.** A `--bg` job spawned from inside a session **did** get its own Agent View row (own id, own session id, `kind: background`) and its own job record, on the host, CLI 2.1.278, at 2026-09-20 14:59. `claude rm` on its own id removed both and left every other row alone.
**One thing the probe surfaced that the question did not ask:** after answering `DONE` the job did not stay done — 9 seconds later it went back to `working` and began `Reading JOURNAL.md`, because a session started in the repo boots on `CLAUDE.md`'s §6 session-start protocol. A "trivial" spawned job is not trivial unless it is launched with a contract that stops it; `--bg` spawn is proven, cheap-and-quiet is not.
This record re-witnesses the premise; **it re-rules nothing** (DECLARE R7): AM-5 binds for everything else until the seat re-rules it.
