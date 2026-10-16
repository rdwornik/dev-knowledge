# Archive copy of transport file DIGEST-VERIFY-spine-engine-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-spine-engine-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 32fe3bc0e7269896. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-689-e-skills-engine (Sonnet 5.5), base b46836c8

# V9 spine, conductor and the engine question

| element | class | witness | caller |
|---|---|---|---|
| scripts/dodo.py (list) | WORKS | `uv run --locked python -m doit -f scripts/dodo.py list` ec=0: "spine  The whole run: every stage in order, stopping at the first that does not exist." Also lists moment:lane-start, moment:merge, organ:*, stage:01..06 | /spine, /handoff, /lane-integrate |
| scripts/dodo.py `--help` | BROKEN | `python scripts/dodo.py --help` prints nothing, ec=0; the entry is `doit -f scripts/dodo.py`, not the script | none |
| dodo spine / moment run | UNRUN | organs write receipt files, so a run leaves files; the lane may write none | /spine |
| conductor.py phase-gate | WORKS | "NOT GATED (1): #689 build ... verdict : PASS (0 failure(s))" | conductor.yml, SessionStart |
| conductor.py session-start, metrics, suite-gate | UNRUN | `--help` lists them (ec=0); session-start calls `gh run list`, suite-gate needs a pytest run | SessionStart hook |
| harness_probes.py check | UNRUN | `--help` ec=0 ("check   Validate the receipts in PATH"); no receipts PATH located in the lane | ADR-123 |
| harness_probes.py remote | UNRUN | needs a codespace; none open ("[codespace] no open container") | ADR-123 |
| system_map.py build | UNRUN | `--help` ec=0; build writes the map JSON and HTML | /map |
| organ_usage_metric.py census | WORKS | "states over 30 days, of 215 observable: CALLED 95 / REACHABLE-BUT-UNOBSERVED 101 / UNREACHABLE 19"; commands and skills listed "NOT observable ... NEVER reported as zero" | organ-index |
| ENGINE (i) Workflow, 2 agents | WORKS | toy table in job tmp, run `wf_8dac8083-c4e`: result `[{"phase":1,"exit":0},{"phase":2,"exit":1}]`; marker files p1, p2 exist, p3 absent: phase 3 did NOT run | this lane |
| ENGINE (ii) /loop | UNRUN | a /loop re-fires a prompt on an interval or via ScheduleWakeup; it has no per-step exit-code gate, so it cannot be a phase-table driver. Answered from the tool docs and `.claude/workflows/conformance-hub.js` (phases are JS code over agent() calls); not run, to leave nothing scheduled | none |
| ENGINE (iii) doit toy table (added) | WORKS | `python -m doit -f <tmp>/toy_dodo.py`: "TaskFailed - taskid:phase2 ... returned 1", DOIT_EXIT=1, p3.ran absent: phase 3 did not run | scripts/dodo.py uses doit |

# Engine answer

- **Workflow can gate, with a caveat:** the gate was a JS `if` in my script. The exit code reached the script only as an LLM-relayed field (agent reported 1 via schema), not as a process status. Markers confirm what ran. Cost: 2 agents, about 122k subagent tokens, 22 s for a 2-row table.
- **doit gates natively:** halts at the first failing task and itself exits 1; no model call. `scripts/dodo.py` already builds on it, so for `[#689]` the evidence favours reuse of doit with the phase table as tasks, with Workflow as an optional wrapper.
- This is two toy runs, not a decision.

# CHECKER

- vendor: OpenAI, `codex exec -m gpt-5.6-terra -s read-only`; served model `gpt-5.6-terra` (tool header); output sha256 prefix 0ff5a6d363122519; first pass hit a uv sandbox block, second pass used the venv python
- dodo.py (list) DISAGREE ec=1 `FileNotFoundError: No usable temporary directory found` (checker sandbox has no temp dir; my run was outside it, ec=0)
- dodo.py `--help` DISAGREE same temp-dir error, so it did not reproduce the empty-output ec=0 witness
- conductor.py phase-gate AGREE ec=0 `verdict : PASS (0 failure(s))`
- organ_usage_metric.py census DISAGREE no output after its 30 s window (my run completed in the lane; both readings stand)
- ENGINE (i) Workflow AGREE `toy phase1=True phase2=True phase3=False`
- ENGINE (iii) doit toy table AGREE `doit p1=True p2=True p3=False`

# USAGE

- Claude tokens: not queried; one Sonnet 5.5 seat plus the 2-agent Workflow (subagent_tokens 121692).
- agy calls: 0. DECIDED-BY-LANE: bulk reading -> targeted `--help` and greps.
- Other-vendor and Copilot calls: see CHECKER.
