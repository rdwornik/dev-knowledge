# Archive copy of transport file DIGEST-VERIFIED-HARNESS-MAP-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFIED-HARNESS-MAP-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] e3db2ec7bd7df85b. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: integrator-nv (CC seat 4e51a080, Opus 5.5), batch NV, base b46836c8

# VERIFIED HARNESS MAP — batch NV (2026-10-14 night)

Source: the 11 lane digests only (DIGEST-VERIFY-{dispatch,land,ci,hooks-gates,handoff-tools,transport,telemetry,providers,commands-skills,spine-engine}-2026-10-14.md, DIGEST-HANDOFF-GAPS-2026-10-14.md), 52,062 B total.
SUBSTITUTION: agy -> copilot (agy gemini-3.8-flash-high empty output: headless mode auto-denied its file-read tool permission). Copilot extracted with a line-quoted PROOF per file; integrator spot-checked lines 310 and 449 and two BROKEN quotes with grep -n: all match.
Lanes: 6 of 6 REPORTED, 0 FAILED (purity clean, every digest lint ok, every digest carries a non-Anthropic CHECKER).

## Counts per area

| FILE | WORKS | BROKEN | DEAD | DUPLICATE | UNRUN |
|---|---|---|---|---|---|
| V1 dispatch | 10 | 2 | 2 | 0 | 4 |
| V2 land | 10 | 0 | 0 | 0 | 6 |
| V3 ci | 7 | 7 | 2 | 0 | 1 |
| V7 hooks-gates | 9 | 6 | 1 | 1 | 2 |
| V4 handoff-tools | 8 | 3 | 0 | 0 | 2 |
| V5 transport | 12 | 1 | 0 | 0 | 1 |
| V6 telemetry | 8 | 2 | 0 | 0 | 3 |
| V10 providers | 5 | 2 | 1 | 0 | 2 |
| V8 commands-skills | 15 | 1 | 0 | 1 | 4 |
| V9 spine-engine | 5 | 1 | 0 | 0 | 6 |
| V11 handoff-gaps | n/a (G/P/M table) | | | | |
| **Total (153 rows)** | **89** | **25** | **6** | **2** | **31** |

## BROKEN items

**V1 dispatch**
- substrate codespace, last run: `"failure": "the lane returned no handback"`, `"fate": FAILED`, receipt.json `"handback": {"present": false}`
- scripts/dispatch_surface.py check / resolve: `model 'claude-sonnet-5-5' is outside the enum {opus | opusplan | sonnet | haiku}`

**V3 ci**
- logs/KNOWN-REDS-REGISTRY.json: `baseline_id 2026-10-04-fdf4f4952211` but ci_verdict names baseline c5108329. All 61 entries expire 2026-10-31, and one windows member expires 2026-10-19.
- job pytest (ubuntu-latest): `run: failure, new reds in test_seat_release_moment, test_onboarding_items, test_handoff_cut_acceptance`
- job pytest (windows-latest): `run: failure; 133 new reds over both OS`
- job commit-gate: `orphan-census: REFUSED -- 15 finding(s)`, `task-coverage: REFUSED -- 9`, audit-health exit 1
- job ship-gate: `[!!] canonical_freshness: CLAUDE.md last_reviewed 2026-10-05 predates last edit 2026-10-13`
- job handoff-manifest: `BD-manifest ... 5 file(s) differ`
- substrate-heartbeat container: `"devcontainer build + L1 marker verify" failure`

**V7 hooks-gates**
- graph-orphan-census: `REFUSED -- 15 finding(s)`, e.g. scripts/system_map.py "reached by no wiring surface"
- check-seal-identity: `SEAL-IDENTITY FAIL: refusing to seal docs\handoffs\2026-08-01-dev-knowledge-architect-2: slug mismatch`
- lane-contract-check: `no Kind line found` (archived v-000, t-000, z-4 contracts)
- decision-coverage: `REFUSED -- 1 decision(s)` (to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99 has no OPEN row)
- audit-health: `rc=1, "health: DEGRADED"; handoff_probes: BD-manifest ... 5 file(s) differ`
- [hook-rate] declarations: `9 hooks DECLARED BROKEN`, all "Disabled: NO"; propose_closures 49% bypassed

**V4 handoff-tools**
- gen_handoff.py --dry-cut DIR: `[error] refusing to cut a bundle: 2 pre-handoff hygiene row(s) FAILED -- [FAIL] ship_gate ...`, exit 1
- handoff_state.py: `UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 200` (handoff_state.py:852)
- boot_frontier.py --frontier: `UnicodeEncodeError: 'charmap' ... '→'` (boot_frontier.py:315), exit 1

**V5 transport**
- transport_report.py --help: `{"delivered": false, ... "reason": "unexpected SystemExit: 0"}` and `NOT delivered`

**V6 telemetry**
- lane_cost.py lane (price leg): `lane lane-nv-929-d-telemetry-providers USD 0.00 over 9 call(s)` and `claude-sonnet-5-5: UNPRICED ... carries no rates: block`
- logs/MERGE-RECEIPTS.jsonl newest 3: `empty: ['ordered_model', 'ran_model']` on all three

**V10 providers**
- grok -p --max-turns 1: `Max turns reached` / `Error: max turns reached`
- provider_bench census: ollama: `Warning: could not connect to a running Ollama instance`

**V8 commands-skills**
- plugin Stop hook propose_closures: `cmd:propose_closures.py: 385/780 bypassed (49%) -- OVER THE BAR`; `DECLARED BROKEN 2026-09-17`

**V9 spine-engine**
- scripts/dodo.py `--help`: `python scripts/dodo.py --help` prints nothing, ec=0

## DEAD and DUPLICATE removal candidates

| FILE | Item | Class | CHECKER verdict |
|---|---|---|---|
| V1 | substrate cloud (Dispatch-Cloud) | DEAD | AGREE: `dispatch.py --help` exposes no cloud verb |
| V1 | substrate interactive | DEAD | UNRUN: "files not read" |
| V3 | job terra | DEAD | AGREE: `terra review NOT RUN -- no provider credential` |
| V3 | deploy/conductor-required-checks.ruleset.json | DEAD | AGREE: `"enforcement": "disabled"` |
| V7 | scripts/read_gate.py | DEAD | AGREE: only harness/manual record and source references; no hook wiring |
| V7 | ruff pre-commit id | DUPLICATE | AGREE: `id: ruff`, `stages: [manual]`; supports duplicate/manual classification |
| V10 | provider_bench census: aider, llm, amp | DEAD | DISAGREE (sandbox): `uv` cache error, `Access is denied` |
| V8 | validate_backlog.py (plugin copy) | DUPLICATE | AGREE: `diff` shows `### [S<n>] <User story>` vs `### <User story>` |

## V9 engine answer

- **Workflow can gate, with a caveat.**
  - The gate was a JS `if` in the lane's script.
  - The exit code reached the script only as an LLM-relayed field (the agent reported 1 via schema), not as a process status.
  - Marker files confirm what ran.
  - Cost: 2 agents, about 122k subagent tokens, 22 s for a 2-row table.
- **doit gates natively.**
  - It halts at the first failing task and itself exits 1, with no model call.
  - `scripts/dodo.py` already builds on it.
  - For `[#689]` the evidence favours reusing doit with the phase table as tasks, with Workflow as an optional wrapper.
- **/loop cannot be a phase-table driver.** It has no per-step exit-code gate, and the lane did not run it.
- This is two toy runs, not a decision.
- Checker: AGREE on `toy phase1=True phase2=True phase3=False` and `doit p1=True p2=True p3=False`.

## V10 provider table

| element | class | witness | caller |
|---|---|---|---|
| claude -p --json-schema --model claude-sonnet-5-5 | WORKS | nonce NONCE-41950 back: `"structured_output":{"nonce":"NONCE-41950"}`; served `modelUsage` key `claude-sonnet-5-5`; `total_cost_usd":0.224222`. Stray `'m' is not recognized` cmd-shim line on stderr | provider_router, dispatch |
| codex exec -m gpt-6-astra | WORKS | nonce NONCE-60144 back; header `model: gpt-6-astra`, `provider: openai`; 19,268 tokens | reviewer role |
| copilot -p -s --model gpt-5.6-terra | WORKS | nonce NONCE-43970 back; served id not disclosed in its log (requested id only) -> UNATTESTED | plan-review fallback |
| copilot Enterprise model list | UNRUN | no CLI verb lists the catalog; asking the model returned only `gpt-5.6-terra` (a self-report, not a catalog) | n/a |
| grok -p --max-turns 1 | BROKEN | `Max turns reached` / `Error: max turns reached`, no nonce | contract invocation shape |
| grok -p --max-turns 2 | WORKS | `**NONCE-12946**`; `grok models` default `grok-4.20-0309-non-reasoning` (not echoed by the run, UNATTESTED) | substitute reviewer |
| agy -p (stdout) | WORKS | nonce NONCE-90904 back; log: `selected model override ... label="Gemini 3.8 Flash (High)"` | bulk reading |
| provider_bench census: gemini 0.56.0, cursor-agent 2026.09.08 | UNRUN | PRESENT in census, not in the contract's probe list | n/a |
| provider_bench census: ollama | BROKEN | `Warning: could not connect to a running Ollama instance` | none found |
| provider_bench census: aider, llm, amp | DEAD | `ABSENT`; caller search: `provider_bench census` lists them, nothing probes them | n/a |

## V11 headline

- **Given: 0. Partial: 6** (items 2, 3, 4, 6, 7, 8). **Missing: 2** (items 1 and 5).
- **Top three gaps:**
  1. **Flow (Conductor E, #689/#669)** is missing. It is taught only as the lane-HANDBACK-serial merge.
  2. **Reading rule (agy first, ≤20 KB/turn)** is missing. Only "about 20 KB per review" appears, at SUPPLEMENT.md:73.
  3. **Per-substrate start lines** are partial. Local and codespace have one; there is no cloud start line anywhere, and the registry lists four substrates.
- **Next gaps in the digest:** dated rulings (R100-R102 not landed; "next dated fates none" despite `manual_until 2026-10-19` rows), and the 10-14 bundle's unfilled FILL-INs.
- **Codex objection:** it rates the unfilled FILL-INs CRITICAL.

## Usage

Claude tokens (`lane_cost.py lane --slug`, all claude-sonnet-5-5, UNPRICED: no `rates:` block in the provider registry, so no USD):
- lane-nv-929-a-dispatch-land: 8,300,586 tokens, 68 calls
- lane-nv-929-b-ci-gates: 6,514,637 tokens, 54 calls
- lane-nv-929-c-handoff-transport: 5,931,824 tokens, 51 calls
- lane-nv-929-d-telemetry-providers: 3,143,373 tokens, 31 calls
- lane-nv-689-e-skills-engine: 6,317,111 tokens, 55 calls
- lane-nv-1450-f-handoff-gaps: 4,576,069 tokens, 43 calls
- total: 34,783,600 tokens, 302 calls (cache-read dominant)

agy calls: lanes 1 (V10 probe) + 1 (V11, empty at timeout) + integrator 1 (empty, permission-denied) = 3, 1 useful.
Other-vendor calls: Codex checker on every lane (~9 exec runs incl. sandbox retries), Copilot 2 (V10) + 2 (V11 substitution) + 1 (integrator substitution), grok 2 (V10).

Cost line (`quota_watch.py line`): [quota] / Codespaces 49.38/180 core-hours used, 130.62 remaining / Actions 11234/3000 min used / Copilot 6361/20000 credits used (31.8%) / cloud sessions: not recorded

## Checker DISAGREE rows (both readings)

| FILE | Item | Lane reading | Checker reading |
|---|---|---|---|
| V1 | dispatch.py queue --dry-run | 929-a is first in the 6-lane order | Exit 0, but order starts `lane-nv-1450-f...`, `689-e...`, `929-a...`, so 929-a is third. The lane says this is argument order. |
| V1 | scripts/codespace_admission.py | Exit 1 with 5 refusals | Exit 1, but it also refuses `git_remote_reachable`. The lane says this is the checker sandbox's blocked network. |
| V7 | check-seal-identity | `SEAL-IDENTITY FAIL ... slug mismatch` | Exit `0` on the current unstaged tree; the committed-bundle failure was not reproduced. |
| V5 | transport.py inventory | `2219 live file(s)` | `2221 live file(s)`. The lane says the live transport gained 2 files. |
| V5 | transport.py query | First run found no rows, exit 1 | 4 LANE_END rows, exit 0. The lane's re-run agrees, so the row is reclassed WORKS-unstable. |
| V6 | lane_cost.py lane (price leg) | `USD 0.00 over 9 call(s)` | `USD 0.00 over 26 call(s)`; USD agrees, only the call count differs. |
| V10 | grok --max-turns 2 | `**NONCE-12946**` | `FS_PERMISSION_DENIED: Couldn't create session` (sandbox) |
| V10 | copilot | NONCE-43970 returned | No response before the 30 s runner cutoff |
| V10 | agy -p | NONCE-90904 returned | `Authentication required` (expired token or network refusal) |
| V10 | claude -p | Nonce returned | `'m' is not recognized as an internal or external command` (the cmd-shim noise the lane also saw) |
| V10 | census ollama | `Warning: could not connect to a running Ollama instance` | `uv` cache init failed, `Access is denied` |
| V10 | census aider/llm/amp | `ABSENT` | Same `uv` cache error |
| V9 | dodo.py (list) | ec=0 | ec=1, `FileNotFoundError: No usable temporary directory found` (no temp dir in the checker sandbox) |
| V9 | dodo.py `--help` | Prints nothing, ec=0 | Same temp-dir error; did not reproduce |
| V9 | organ_usage_metric.py census | Completed in the lane | No output after its 30 s window |

- **V3, V4, V8:** these checkers have no DISAGREE rows. V3's CHECKER lists rows as UNRUN (ci_verdict `GH-UNAVAILABLE`, pytest jobs, handoff-manifest, heartbeat container). V4 marks handoff_state and boot_frontier INDETERMINATE.
- **V11:** Codex's "not adopted" objections are the two-readings-stand cases: VISION.md is not dead; README:32 and PROCESS:964-978 are qualified, not flat contradictions.
- **V2:** all checked rows AGREE.

## MORNING

**V3 ci**
- `PREMISE-FAILED: registry expiry is 2026-10-31, not 2026-11-01.`
- `OPERATOR-ACTION: renew the 2026-10-19 windows entry first.`
- `DECIDED-BY-LANE: workflows parsed with PyYAML, not agy (exact structure).`

**V7 hooks-gates**
- `OPERATOR-ACTION: decide whether the 9 DECLARED BROKEN hooks keep running.`
- `DECIDED-BY-LANE: stdin payloads as files (guard refuses pipes); script reading, not agy.`

**V6 telemetry**
- `DECIDED-BY-LANE: lane_cost price leg classed BROKEN (zero USD for a priced-in-use model), not WORKS, because the value line is "a cost meter that reads nothing".`

**V10 providers**
- `PREMISE-FAILED: contract "grok `--max-turns 1`" -> one turn cannot return text; 2 turns can.`
- `PREMISE-FAILED: contract "agy 1.2.2" in provider_bench report -> census shows agy 1.3.5.`
- `DECIDED-BY-LANE: one retry used on grok only (turns 1 -> 2).`
- `OPERATOR-ACTION: re-run the provider checker unsandboxed or from a lane with a writable uv cache (the checker cannot reach the user dirs these CLIs write to).`

**V8 commands-skills**
- `PREMISE-FAILED: "fleet_health.py --help" and "validate_reconciliation.py --help" do not print help; neither has argparse. They ran their normal read-only report (ec=0).`

**V11 handoff-gaps**
- `- SUBSTITUTION: agy -> copilot for both reads; Copilot served claude-sonnet-5.5 per its log. Not a different vendor, so it does not count as the check.` (starts with a bullet marker)

V1, V2, V4, V5 and V9 have no line that starts with a tag. QUESTION appears nowhere in the file.

Tags that appear inline rather than at line start:
- V1: SUBSTITUTION (retry via the venv interpreter).
- V2: SUBSTITUTION (retry via the venv interpreter).
- V1, V8, V9: PREMISE-FAILED, SUBSTITUTION and DECIDED-BY-LANE inside table cells or bullets.
- V4 and V5: PREMISE-FAILED on the gpt-6-astra contract, and on `--dry-cut`.
- V6: PREMISE-FAILED on the telemetry_emit docstring.
- V7: PREMISE-FAILED on AGENTS.md calling ruff a pre-commit gate.
- V8 and V9: DECIDED-BY-LANE "bulk reading -> targeted greps and `--help`".

Integrator additions:
- OPERATOR-ACTION: lane c worktree husk `.claude/worktrees/lane-nv-929-c-handoff-transport` (empty, unregistered, branch deleted) could not be removed: "Device or resource busy" — a stopped lane process still holds it; `rmdir` it once the handle drops (see close note).
- TRANSPORT-LINT: lane SESSION files of a, c, e, f carry no `by:`; LANE-END-* files written by the Stop-hook writer carry no `by:` (script-written kind) — a writer defect, not a lane one.
- Receipt times: lane fire-to-handback 21–32 min; lane b heartbeats mislabel local time as `Z`.
- QUESTION: none left by any lane.
