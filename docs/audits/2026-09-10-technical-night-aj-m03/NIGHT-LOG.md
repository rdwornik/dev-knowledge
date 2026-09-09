# NIGHT-LOG — 2026-09-09 Architekt Jutra M03 + Maister vs our harness

PROMPT-SHA256: `c1c77598850b7e492bb416544e3c50b92bbe4f032bca79db451ffb1a9e052224`
(over `docs/audits/2026-09-10-technical-night-aj-m03/MISSION-PROMPT.md`, this bundle's verbatim
copy of the mission prompt — the hash is of that file, which is the only byte-exact rendering of
the prompt this run had.)

Append-only. One line per leg. Newest at the bottom.

Legend — ORDERED = the reader the mission named · CORRECTED = same ordered reader, invocation
fixed after a recorded failure (the `[#676]` discipline: a mis-invocation is not a dead tool) ·
SUBSTITUTED-PENDING-OPERATOR = a different reader was used, R1 applies.

```
2026-09-09T22:22:04+02:00 | SETUP    | worktree            | EnterWorktree name=night-aj-m03-review -> branch worktree-night-aj-m03-review | OK | NOTE: mission said branch `night-aj-m03-review`; the closed branch-prefix enum (AGENTS.md "Landing a change") admits only worktree-<name> for a machine-provisioned lane, so the branch carries the prefix and the WORKTREE carries the mission's name. Flagged, not silently renamed.
2026-09-09T22:22:04+02:00 | PROBE    | agy                 | agy --print="Reply with exactly: PROBE_OK" --model gemini-3.8-flash-low --dangerously-skip-permissions | OK 9s | PROBE_OK, exit 0
2026-09-09T22:22:21+02:00 | PROBE    | codex               | codex exec -c model=gpt-5.6-sol -s danger-full-access "Reply with exactly: PROBE_OK" | OK 11s | PROBE_OK, exit 0, model gpt-5.6-sol confirmed in banner
2026-09-09T22:22:42+02:00 | PROBE    | grok                | grok -p "Reply with exactly: PROBE_OK" | OK 24s | PROBE_OK
2026-09-09T22:23:15+02:00 | PROBE    | cursor-agent        | absolute path C:\Users\1028120\AppData\Local\Programs\cursor-agent\cursor-agent.exe -p --trust | FAIL 0s | "No such file or directory" — the path in the mission's shape does not exist on this host
2026-09-09T22:23:30+02:00 | PROBE    | cursor-agent        | Get-Command cursor-agent -> C:\Users\1028120\AppData\Local\cursor-agent\cursor-agent.ps1 | OK | REAL path is a .ps1 under AppData\Local\cursor-agent, NOT AppData\Local\Programs\...\.exe
2026-09-09T22:23:36+02:00 | PROBE    | cursor-agent        | & "C:\Users\1028120\AppData\Local\cursor-agent\cursor-agent.ps1" -p --trust "Reply with exactly: PROBE_OK" | OK 21.2s | PROBE_OK
2026-09-09T22:24:25+02:00 | INPUT C  | git                 | git clone --depth 1 https://github.com/SkillPanel/maister | OK | CLAUDE.md docs LICENSE Makefile platforms plugins README.md
2026-09-09T22:24:50+02:00 | INPUT B  | git                 | git clone --depth 1 https://github.com/Architekt-Jutra/architekt-jutra-code | OK | 1044 files; Java/Maven + litellm + mcp-server + plugins + week7..week10
2026-09-09T22:25:30+02:00 | INPUT A  | Expand-Archive      | AJ_M03_transkrypcje.md.zip -> 1 clean file, 91,413 B, 353 lines | OK | .md unzipped clean, so the PDFs were NOT used (mission: "prefer the .md if it unzips clean")
2026-09-09T22:25:40+02:00 | INPUT A  | split               | 6 lessons: L01 1-28 · L02 29-108 · L03 109-178 · L04 179-238 · L05 239-300 · L06 301-353 | OK | LOCATOR CAVEAT: the .md carries NO page numbers and NO timestamps. Locators for leg 1a are therefore LINE NUMBERS in the split file. The mission asked for "page/timestamp"; that granularity does not exist in the chosen source. Recorded, not silently swapped.
2026-09-09T22:26:33+02:00 | 1a L01   | agy ORDERED         | agy --model gemini-3.8-flash-low --print-timeout=15m --dangerously-skip-permissions --add-dir . --print="<per-lesson table prompt>" | OK 322s | 18 claim rows, stdout; table emitted 3x by the streaming client, deduped by hand on capture
2026-09-09T22:32:xx+02:00 | 1a L02   | agy ORDERED         | as L01, file-write variant -> ../out/1a-L02.md | running |
2026-09-09T22:32:xx+02:00 | 1a L03   | agy ORDERED         | as L01, file-write variant -> ../out/1a-L03.md | running |
2026-09-09T22:32:xx+02:00 | 1a L04   | agy ORDERED         | as L01, file-write variant -> ../out/1a-L04.md | OK | landed
2026-09-09T22:34:xx+02:00 | 1a L05   | agy ORDERED         | as L01, file-write variant -> ../out/1a-L05.md | OK 8933 B | landed via agy's own file-write tool
2026-09-09T22:32:xx+02:00 | 1a L06   | agy ORDERED         | as L01, file-write variant -> ../out/1a-L06.md | running |
2026-09-09T22:33:xx+02:00 | 1b       | agy ORDERED         | agy ... --add-dir . --print="<repo B audit prompt>" -> ../out/1b-ajcode.md | running |
2026-09-09T22:33:40+02:00 | 1c       | codex ORDERED       | codex exec -c model=gpt-5.6-sol -s danger-full-access "<spine derivation, write to out/1c-codex-spine.md>" | FAIL-TO-DELIVER | Ran to completion, 85,017 tokens, exit 0, then: "BLOCKED: Repository policy restricts Codex to read-only review, so I cannot create the requested output file." NOT a provider failure and NOT an auth failure — OUR OWN L0 reviewer doctrine (~/.codex/AGENTS.md, the read-only reviewer role that AGENTS.md "Precedence" names) forbids the write. 85k tokens of real derivation were done and discarded.
2026-09-09T22:41:xx+02:00 | 1c       | codex CORRECTED     | same model/sandbox, deliverable changed to "PRINT your entire answer to stdout; READ-ONLY - do not create or modify any file" | running | Correction stays inside the ordered reader AND inside its L0 role. Not a substitution.
2026-09-09T22:33:50+02:00 | 1d       | grok ORDERED        | grok -p "<census prompt, write to out/1d-grok-census.md>" | FAIL-TO-DELIVER | exit 0 after TWO assistant turns, 304 B of stdout, no table, no file. Last words: "Next I'll list every scripts/ file and trace callers". CAUSE, from `grok --help`: `-p, --single <PROMPT>  Single-turn prompt. Prints the response to stdout and exits`. `-p` is SINGLE-TURN BY CONSTRUCTION; a census needs many tool turns, so the run was structurally incapable of finishing. Indistinguishable from a dead provider from the outside — the exact collapse `[#676]` was filed about.
2026-09-09T22:42:xx+02:00 | 1d       | grok CORRECTED      | grok --always-approve --max-turns 80 --output-format plain -p "<census prompt, print to stdout>" | running | Correction stays inside the ordered reader. Not a substitution.
2026-09-09T22:36:xx+02:00 | 1e       | cursor-agent ORDERED| & cursor-agent.ps1 -p --trust "<quality/cannot-fail-test audit>" | running |
2026-09-09T22:37:xx+02:00 | 1f       | claude sonnet       | Agent(subagent_type=general-purpose, model=sonnet) model-agnosticism audit, read-only | running | ORDERED by the mission as a Claude Sonnet subagent
2026-09-09T22:44:xx+02:00 | D-prep   | claude sonnet       | Agent(model=sonnet) extract prior conclusions: census 160/24/32 + 32 orphans, 16-stage map, conductor E + AMEND-001, five dead PLAYBOOK sections, the "nothing beyond a spine" claim | running | Support leg for Phase 2, not a Phase 1 reader
2026-09-09T22:44:xx+02:00 | D-prep   | claude sonnet       | Agent(model=sonnet) extract M01/M02 practices from intake #20 + the 2026-09-06 erratum | running | Support leg for Phase 2, not a Phase 1 reader
2026-09-09T22:42:xx+02:00 | 1c       | codex CORRECTED     | codex exec -c model=gpt-5.6-sol -s danger-full-access "<spine derivation, PRINT to stdout>" | OK, 92,866 tokens | DELIVERED. 14-phase Maister spine + 8-phase ours + DIVERGENCE + ATTACK + STATE-CARRIER-DELTA, all with locators. ATTACK verdict: REFUTES.
2026-09-09T22:46:xx+02:00 | 1d       | grok CORRECTED      | grok --always-approve --max-turns 80 --output-format plain -p "<census prompt>" | **FAILED — R1** | Ran 3 turns, then: "You've reached your free Grok Build usage limit for now. Get SuperGrok for much higher limits, or try again later". A QUOTA refusal, NOT an invocation error and NOT a corrupt binary. The corrected invocation was right; the account cannot pay for the work. **LEG 1d IS UNFULFILLED. Marked SUBSTITUTED-PENDING-OPERATOR — and per R1, NO substitute reader was run for it.** See "R1 register" below.
2026-09-09T22:47:xx+02:00 | 1a L03   | agy CORRECTED       | as L01 but stdout-only (file-write proved unreliable, see below) | rerun launched | First attempt died: "the connection to the agent was interrupted before the response finished: subscriber fell behind updates, stalled for 5s" — a CLIENT-SIDE streaming stall under six concurrent agy processes, not a model failure
2026-09-09T22:48:xx+02:00 | 1a L04   | agy CORRECTED       | as L01 but stdout-only | rerun launched | First attempt printed DONE at exit 0 and WROTE NO FILE
2026-09-09T22:48:xx+02:00 | 1b       | agy CORRECTED       | as 1b but stdout-only | rerun launched | First attempt printed DONE at exit 0 and WROTE NO FILE
```

## R1 register — substitutions and unfulfilled legs

| LEG | ORDERED READER | STATUS | EXACT COMMAND | EXACT RESPONSE | DISPOSITION |
|---|---|---|---|---|---|
| 1d | `grok` | **UNFULFILLED** | `grok --always-approve --max-turns 80 --output-format plain -p "<census prompt>"` (run from the worktree root) | `You've reached your free Grok Build usage limit for now. Get SuperGrok for much higher limits, or try again later: https://grok.com/supergrok?referrer=grok-build` then `Error: <same>`, exit 0 | **SUBSTITUTED-PENDING-OPERATOR.** No other reader was run in its place. The Phase-2 census diff is therefore built from an IN-REPO source instead — lane v-664's own re-measurement — which is not a substitute reader but our own dated artifact, and is stated as such wherever it is used. |
| 1e | `cursor-agent` | **UNFULFILLED** | attempt 3: `& "C:\Users\1028120\AppData\Local\cursor-agent\cursor-agent.ps1" -p --trust "<quality audit, print to stdout>"` with `$env:CLAUDE_PROJECT_DIR` set to the worktree root | `ActionRequiredError: You've hit your usage limit Get Cursor Pro for more Agent usage, unlimited Tab, and more.` exit 1 | **SUBSTITUTED-PENDING-OPERATOR.** No other reader was run in its place. The "cannot-fail test" scan the mission wanted from this leg is therefore ABSENT from the DELETE LIST, and the DELETE LIST says so in place of guessing. |

### Leg 1e, in full — it failed three times, for three different reasons

1. **Attempt 1** (write a file): `SUBSTITUTED-PENDING-OPERATOR: cannot write 1e-cursor-quality.md — Write/Shell/Task blocked by PreToolUse (python C:\scripts\fleet_health.py → ENOENT). Audit completed in-session; disk deliverable blocked.`
2. **Attempt 2** (print to stdout instead): still blocked — `Every repo tool call (Read, Shell, Glob, Grep, Task) is blocked by a broken PreToolUse hook: can't open file 'C:\\scripts\\fleet_health.py'`. The reader then **refused to fabricate**: *"Without real locators I will not invent table rows."* Correct behaviour, recorded as such.
3. **Attempt 3** (with `CLAUDE_PROJECT_DIR` exported): quota refusal, above.

**The cause of 1 and 2 is ours, and it is a model-agnosticism defect found by execution.**
`.claude/settings.json:21` declares a `PreToolUse` hook with matcher `"*"`:

```
"command": "python \"$CLAUDE_PROJECT_DIR/scripts/fleet_health.py\" --prompts-guard"
```

`cursor-agent` **honours the hook file** but does not define `$CLAUDE_PROJECT_DIR`. The variable
expands to empty, the path becomes `\scripts\fleet_health.py` → `C:\scripts\fleet_health.py`,
the interpreter exits non-zero, and because the matcher is `"*"` **every tool call in the session
is refused with no in-session escape.**

That is the recorded `pretooluse-match-all-wedges-session-no-escape` failure — except it is now
wedging a *different vendor's* CLI, which nothing in the repo anticipated. A swap of reader does
not merely lose Claude-specific features; **our own guard converts into a total refusal for the
new reader, and presents as the reader being broken.** This is filed as finding MA-1 in
MATRIX.md's MODEL-AGNOSTIC section and is, in the mission's own terms, the sharpest thing the
night produced about model-agnosticism — because it was measured, not read.

**Contamination note, recorded for honesty:** `MISSION-PROMPT.md` was committed into the tree the
readers were auditing before legs 1d/1e ran. Attempt 1's reply quotes the mission's own phrase
`SUBSTITUTED-PENDING-OPERATOR`, which is proof it read the mission prompt. Later invocations
told the reader to ignore that directory. No leg's *findings* are known to be affected, but the
possibility is on the record rather than assumed away.

**A registry correction falls out of this and is recorded here rather than acted on.**
`ecosystem/provider-registry.yaml` records grok as **PAY-PER-CALL** ("one small test cost
**$0.037**, with the credential proven by a server round-trip", measured 2026-08-26). The
refusal this run received names a **free tier with a usage limit** ("free Grok Build usage
limit", upsell to SuperGrok). Those two cannot both describe the account in use tonight.
Either the credential changed, or the 2026-08-26 cost note describes a different route
(the raw-HTTPS route the registry itself says the A/B runs used) than the CLI does. **Not
repaired here** — this bundle writes no registry change; it is evidence for `[#676]`, whose
Done-when already requires the four outcomes (absent · corrupt · mis-invoked · answered) to
be discriminated. Tonight adds a **fifth**: *reachable, correctly invoked, and refused for
quota* — which the current four-way split would file as "answered" or "unreachable", both wrong.

## Reader-reliability observations (evidence for `[#676]`, gathered incidentally)

| READER | FAILURE OBSERVED | LOOKS LIKE | ACTUALLY IS |
|---|---|---|---|
| `cursor-agent` | mission's absolute path `...\Programs\cursor-agent\cursor-agent.exe` does not exist | provider absent | wrong path — real one is `...\AppData\Local\cursor-agent\cursor-agent.ps1`, a **.ps1, not an .exe** |
| `codex` | 85,017 tokens spent, exit 0, no artifact | task failure | **our own L0 doctrine** — `~/.codex/AGENTS.md`'s read-only reviewer role forbids the write. The caller was never warned; the money was spent first. |
| `grok` (1st) | exit 0 after 2 turns, 304 B, no answer | dead provider | `-p/--single` is **single-turn by construction**; a multi-turn census cannot complete in it |
| `grok` (2nd) | exit 0, quota refusal | dead provider | free-tier quota exhausted — a **fifth** outcome the `[#676]` four-way split does not carry |
| `agy` | printed `DONE`, wrote no file (2 of 6 legs) | success | **silent write failure reported as success** — the worst shape, because nothing downstream can tell |
| `agy` | `subscriber fell behind updates, stalled for 5s` | model/network failure | client-side streaming stall under 6 concurrent processes — a **concurrency ceiling**, recoverable by serialising |

## Running notes

- **Free RAM at start:** 4.83 GB. Abort floor is 1 GB.
- **Wall cap:** 6 h from 2026-09-09T22:20+02:00 → hard stop 2026-09-10T04:20+02:00.
- **No commit to main.** All work on `worktree-night-aj-m03-review`.
- **Two invocation-shape failures in the first hour, both on the ordered reader, both recovered
  without substitution.** They are not incidental to this mission — they are evidence for the
  mission's own subject. `[#676]` predicted exactly this collapse and both instances are new
  data for it. One of them (`codex`) is a **model-agnosticism finding in its own right**: our L0
  reviewer role makes an ordered reader structurally unable to produce an artifact, and nothing
  warned the caller in advance.
