# RESULT -- P1 dispatch modelled twice (B: python-statemachine, C: BPMN 2.0 on SpiffWorkflow), dry-run against `dispatch.py`

Lane `lane-dz-0-spike-b-vs-c`, scratch branch `worktree-lane-dz-0-spike-b-vs-c`, never merged. Served model: claude-sonnet-5-5. This is a PROPOSAL for an ADR the operator ratifies; nothing here decides structure.

## 1. Recommendation: B, with one cheap borrow from A. C did not earn a measured win.

Recommendation: **B** (one executable state machine per process, in code), keeping the generated Mermaid export (`b_statemachine/out/p1_dispatch_b.mmd`) as the Option-A artefact for free. No separate YAML-to-Mermaid generator is needed.

Evidence rows it rests on (all in section 3 unless noted):
- Same behaviour: both forms ended in the same terminal node in all 10 scenarios; in the 5 scenarios the real `launch_lane` can answer (S1, S3, S4, S7, S8), both agreed with it, including its exit codes 0, 5, 5, 5, 8. Section 4.
- C costs more for the same result: 44 flow nodes vs 30 states, 51 flows vs 38 transitions, 12 054 vs 22 066 bytes of process definition, one compiled dependency (lxml, 11.9 MiB on disk) vs none, LGPL-3.0 vs MIT.
- C has no renderer: SpiffWorkflow draws nothing, and a hand-written `.bpmn` has no layout, so bpmn.io cannot open it as-is. `bpmn-auto-layout` 1.3.0 laid out 46 shapes but only 1 edge (cause not investigated), so a bpmn.io-rendered picture is UNVERIFIED. I wrote an 84-line BPMN-to-DOT pass instead; B's export was 51 lines and native.
- A BPMN gateway cannot compute, so every decision needs a separate service task first (5 extra "read X" tasks in C: dependency, serialize-group, substrate, cap/RAM, held-by; plus one after start). A state in B can compute and branch.
- Fit with Conductor E (R105): B leaves the phase table alone and owns the `[#669]` transitions; C would have to wrap or replace it (section 3, row e).

What would change the recommendation (any one is enough to reopen it):
- The operator wants non-coders to edit the process in bpmn.io. That is the one thing C has and B lacks, and this spike did NOT test whether the file opens there (UNVERIFIED).
- The operator needs BPMN features this process did not exercise: timers, human tasks, call activities across L1 diagrams, message correlation. C expresses those natively; B would hand-roll them. Measured here: only message events, error boundary events and an event-based gateway.
- `bpmn-auto-layout` (or another tool) turns out to produce a complete layout, which removes the renderer cost.
- LGPL-3.0 is accepted as a core dependency and a single-file exchange format outranks 8 extra nodes per process.
- The completeness rule ("every node binds to a `file:line` and a test") is judged better enforced on an XML file than on class attributes. In this spike it was equally easy on both (row h).

## 2. Setup actually run (so every number below can be reproduced)

- B: `python-statemachine 3.2.2` in `/tmp/spike/venv-python_statemachine` (+ `pydot 4.0.1`, `pyparsing 3.3.3` for the diagram, + system `graphviz 2.43.0` installed with apt in this throwaway box). Chosen over `transitions 0.9.3` because 3.x has eventless guarded transitions (a gateway is a state whose outgoing transitions carry guards and no event name), a Mermaid export that needs no graphviz, and no hard dependency. `transitions` was tried only on a 4-state toy (its `GraphMachine` exported DOT fine with the `graphviz` pip package) and has no eventless transition, so each gateway would need an explicit trigger: that is the whole reason, and the full model was NOT built in `transitions` (UNVERIFIED beyond the toy).
- C: `spiffworkflow 3.2.0` (+ `lxml 6.1.3`) in `/tmp/spike/venv-spiffworkflow`, `SpiffBpmnParser`, service tasks through `TaskDataEnvironment.call_service`, error boundary events on an embedded sub-process, an event-based gateway with three message catch events.
- Both call the same `common/services.py`, which runs REAL verbs in dry-run: `dispatch.py queue --dry-run`, `dispatch.py launch --dry-run`, `dispatch.py plan`, `claim.py claim|release` on a throwaway transport, plus `common/probe.py` for the pure functions that have no CLI dry-run surface (`dependency_status`, `serialize_group_clear`, `decide_lane`, `_held_by`, `_identify`, `_write_launch_records`). The oracle row calls the real `launch_lane` with only the spawn seam faked (the same seam `tests/test_dispatch_launch.py` fakes). No `claude`, `codex` or `gh` was started; every receipt went to a throwaway `HARNESS_RECEIPTS_DIR` that is removed on exit.
- Synthetic contracts: `contracts/LANE-spike-{clean,refused,dep,codespace}.md`.
- `moment:pre-launch` was NOT run (its organs read live worktrees and sessions): its verdict is injected per scenario and the trace marks it `injected`. UNVERIFIED against the real organs.

## 3. Grading table

| Criterion | B python-statemachine | C BPMN + SpiffWorkflow |
|---|---|---|
| a. gateways bound to `file:line` with a test | 11 of 11 | 12 of 12 (11 exclusive + 1 event-based) |
| a. all nodes bound | 27 of 30 (3 HOLES) | 39 of 44 (5 HOLES) |
| a. check output | `b_statemachine/check_bound.py` | `c_bpmn/check_bound.py` |
| b. node count (flow nodes) | 30 | 44 (incl. 2 boundary events, 2 inner error ends, the sub-process, 3 catch events) |
| b. edge count | 38 transitions (39 DOT edges incl. the initial arrow) | 51 sequence flows |
| b. rendered files | `b_statemachine/out/p1_dispatch_b.{png,svg,dot,mmd}`, 964 x 2399 px | `c_bpmn/out/p1_dispatch_c.{png,svg,dot}`, 1891 x 3680 px |
| b. edges into END REFUSED | 8 | 8 (7 flows + 1 boundary) |
| b. can a reader follow the error paths | B: yes, edges are labelled with the guard name, one column; the 8 refusal edges are long. C: yes, flows are labelled with the condition, the sub-process is a labelled box; the 2 boundary events float beside it, not on its border (my renderer, not BPMN). I judged this by reading both images; no reader test was run: UNVERIFIED | |
| c. REFUSED (exit 5) | expressed; scenarios S2, S4, S7 | expressed; S2, S4, S7 |
| c. already-launched `[#1572]` | expressed; S3 | expressed; S3 |
| c. job-unresolved (exit 8, found while reading) | expressed; S8 | expressed; S8 |
| c. reaped (RAM) | expressed, model-only (M1) | expressed, model-only (M1) |
| c. END-EARLY | expressed, model-only (M2) | expressed, model-only (M2) |
| c. native error-boundary construct | none: a guarded transition to the end state | yes: 2 error boundary events on the launch window (S7, S8 go through them) |
| d. colour by zone from node attributes | yes: `export_diagram.py` post-pass over pydot nodes, about 14 lines | yes, but only through my own renderer (84 lines); bpmn.io colouring would need `bioc:fill` written into the DI: UNVERIFIED |
| d. distinct border for TODAY-GLUE | yes: red dashed, 6 nodes | yes: red dashed, 9 nodes |
| d. hand-drawing | none | none |
| e. fit with Conductor E (R105) | see below | see below |
| f. package versions | python-statemachine 3.2.2; pydot 4.0.1, pyparsing 3.3.3 (diagram only) | spiffworkflow 3.2.0; lxml 6.1.3 |
| f. licence | MIT (python-statemachine, pydot); pyparsing UNVERIFIED | LGPL-3.0 (`spiffworkflow` METADATA: `lGPLv3`); lxml BSD-3-Clause |
| f. install size on disk (`du -sk`) | 1 012 KiB, + 232 + 489 KiB for the diagram | 2 188 KiB, + 11 856 KiB lxml |
| f. transitive dependencies | 0 (2 for the diagram) | 1 (lxml, a compiled wheel) |
| f. system dependency | `dot` for PNG/SVG (apt `graphviz`, Installed-Size 3 064 KiB); Mermaid needs none | `dot` for my renderer |
| f. import time, median of 7 (`-X importtime`, cumulative) | `statemachine` 58.1 ms; with `.contrib.diagram` 74.4 ms | `SpiffWorkflow.bpmn` 46.5 ms; `SpiffWorkflow.spiff.parser` 65.8 ms; `lxml.etree` 21.4 ms |
| f. the other B candidate | `transitions 0.9.3` + `six`: 598 + 71 KiB, MIT, import 18.8 ms (44.1 ms for `.extensions`) | n/a |
| g. process definition | `p1_dispatch.py`: 210 lines, 172 code lines, 12 054 bytes (38 transitions, 17 guards, 16 action hooks) | `p1_dispatch.bpmn`: 163 lines, 146 non-comment, 22 066 bytes (51 flows, 15 service tasks, 14 condition expressions) |
| g. driver + loader + renderer | `run_scenarios.py` 32 + `check_bound.py` 8 + `export_diagram.py` 51 code lines | `run_scenarios.py` 71 + `check_bound.py` 12 + `render.py` 84 code lines |
| g. tests | 19 (17 branch cases, 2 attribute checks), 0.09 s | 19 (the same matrix), 0.23 s |
| g. shared by both | `common/`: services 155, probe 105, completeness 58, model_matrix 34, report 30 code lines | same |
| h. completeness check | see below | see below |

Row e, Conductor E (read `scripts/conductor.py` and `ecosystem/harness.yaml`). Conductor E has two parts. (1) The phase table: one row per delivery stage over `tasks/<row>.md` `phase:`, a read-only gate, and a docstring that says it fires no `[#669]` transition. (2) `conductor.py lane`: one `doit` run per round over the harness `phases:` table P1..P7 (spec, red, implement, constraints, qa, review, judge) with receipts and C-* constraints. P1 dispatch is in neither. The name "P1" in this contract collides with harness phase P1 (spec); the contract's "P1" is process 1 of the process map.
- B wraps nothing and replaces nothing. The dispatch machine owns the `row + contract -> dispatched` transition that `[#669]` reserves, keeps state in the repo (receipts, the `tasks/` phase field), and sits beside `doit` stages (stage 11 already runs `dispatch.py plan`).
- C would either wrap the phase table (the engine runs the lane loop and the table becomes a view over engine state) or replace it. Both put process state in a SpiffWorkflow instance, which has its own serializer and task states, while decision E says state stays in the repo. I did not test persisting an instance, so how much of that conflict is real is UNVERIFIED. This is the T2 decision the contract names.
- Neither form touches the harness `phases:` table P1..P7; that is a lane-internal loop, not a process-map process.

Row h, completeness check. Shared half is `common/completeness.py` (58 code lines): bind line exists and is non-blank, test function exists in the named file, and a static AST call graph maps each `@cli.command` entry point to a node. Only the loader differs:
```
# B (8 code lines): the nodes are class attributes
nodes = [{"id": s.id, "kind": s.kind, "bind": s.bind, "test": s.test} for s in P1Dispatch.states]
raise SystemExit(report("B", nodes))
# C (12 code lines): parse the file, read the dz: attributes
DZ = "{https://dev-knowledge.invalid/spike/dz}"
nodes = [{"id": e.get("id"), "kind": "gateway" if etree.QName(e).localname.endswith("Gateway") else "other",
          "bind": e.get(DZ + "bind"), "test": e.get(DZ + "test")}
         for e in etree.parse(BPMN).iter() if isinstance(e.tag, str) and e.get("id") and etree.QName(e).localname.endswith(("Event", "Gateway", "Task", "subProcess"))]
raise SystemExit(report("C", nodes))
```
Result on both: every bound node resolves; both report the same 6 LEFTOVER entry points (no node reaches them): `repair_cmd`, `codespace_exec_cmd`, `codespace_observe_cmd`, `codespace_harvest_cmd`, `codespace_stop_cmd`, `codespace_delete_cmd`. Those belong to other processes (repair, codespace lifecycle), so for P1 alone they are expected, and they show the check works. Mapped: `launch_cmd`, `queue_cmd`, `plan_cmd`, `govern_cmd`.

## 4. Scenario traces (full state-by-state traces with each verb's exit code: `b_statemachine/out/traces.md`, `c_bpmn/out/traces.md`)

| Scenario | What it feeds | B ends in | C ends in | Real `launch_lane` (spawn faked) |
|---|---|---|---|---|
| S1 clean launch | `LANE-spike-clean.md`, nothing live, pre-launch injected PASS | end_launched | end_launched | launched, exit 0: AGREE |
| S2 refused | Dispatch block says effort low, table says high | end_refused (parse, `launch --dry-run` exit 1) | end_refused | no comparable call |
| S3 already launched | planted receipt + a live listing entry | end_already_launched | end_already_launched | already-launched, exit 5: AGREE |
| S4 pre-launch refused | pre-launch injected REFUSED | end_refused | end_refused | refused, exit 5: AGREE |
| S5 dependency hold | `Starts after spike-clean`, nothing MERGED | end_hold (WAITING) | end_hold | no comparable call |
| S6 codespace route | claude head + `substrate: **codespace**` note | end_routed_codespace (`plan --substrate codespace` printed 12 steps) | end_routed_codespace | no comparable call |
| S7 spawn fails | spawn returns exit 1 | end_refused | end_refused (through the error boundary) | refused, exit 5: AGREE |
| S8 job unresolved | spawn exit 0, listing empty | end_unresolved | end_unresolved (through the error boundary) | LaunchIncomplete, exit 8: AGREE |
| M1 reaped | clean launch, then a synthetic `lane_reaped` | end_reaped | end_reaped | model-only: nothing in the code produces it |
| M2 END-EARLY | clean launch, then a synthetic `lane_ended_early` | end_early | end_early | model-only |

State sequences (B; C is the same with 6 extra tasks (one after start, five "read X" before the dependency, serialize-group, substrate, cap/RAM and held-by gateways) and, on the launch path, the sub-process wrapper nodes `w_start`, `w_end`, `launch_window` and the event-based gateway):
- S1: start > parse > g_agree > valid > g_valid > tier > claim > g_claim > g_dep > g_serial > g_substrate > g_capram > prelaunch > g_prelaunch > g_held > spawn > g_spawn > identify > g_identify > receipt > running > end_launched (22 states; C 32)
- S2: start > parse > g_agree > end_refused (4; C 5)
- S3: ... g_prelaunch > g_held > end_already_launched (16; C 22)
- S5: ... claim > g_claim > g_dep > end_hold (10; C 12)

Wall time per scenario was 0.7 to 4.2 s on both forms and is dominated by `uv run` start-up, so it does not separate them.

## 5. HOLES (nodes with no code to bind; listed, not invented)

| Node | What was found |
|---|---|
| R101(a) tier refusal (`tier`) | Owed: `STANDING_RULINGS.md` R101(a) says `lane_boot` must refuse a tier above the distiller's output, "a mechanism owed". `scripts/dispatch.py` has no such check. Both models pass it through by default. |
| `end_reaped` | No code detects or raises a RAM reap of a launched lane. The nearby code only prevents it (`decide_lane` RAM floor, `dispatch.py:1664`; `scripts/memory_admission_gate.py`) or shows its symptom (`end_unresolved`, `dispatch.py:1196`). |
| `end_early` | No code. The open row `[#1621]` owes a report convention (first line `END-EARLY <reason>`), which is a template and a lint, not a dispatch node. |
| substrate `cloud` | `SUBSTRATES = ("local", "codespace")` at `dispatch.py:137`; `plan --substrate cloud` exits 2 ("not one of 'local', 'codespace'"). Both models route it to END REFUSED. |
| `moment:pre-launch` on the codespace path | Confirmed hole: `run_prelaunch` is referenced only from `launch_lane`'s default (`dispatch.py:1129`) and `launch_cmd` (`:1909`); the codespace route (`codespace_exec`) never calls it. |
| `c_reaped`, `c_early` (C only) | The two catch events for the two holes above. |

## 6. DIVERGENCES between the contract's order and the code (measured; the models follow the contract except where marked)

| Contract says | Code does | Model |
|---|---|---|
| substrate gateway after cap/RAM | `decide_lane` routes a codespace lane BEFORE cap/RAM (`dispatch.py:1657` before `:1661`; test `test_decide_lane_routes_codespace_before_cap_or_ram_ever_apply`) | follows the code |
| claim before the gates | no claim in `dispatch.py` at all; `claim.py` runs as the lane's own first turn, after the spawn (`templates/batch-common-rules-template.md` section 3). Marked actor `seat`, TODAY-GLUE | contract order |
| pre-launch before already-launched? | `launch_lane` checks `_held_by` first (`dispatch.py:1136`) and pre-launch second (`:1145`) | contract order; same outcome on S3 and S4 |
| parse (table = block) covers the pipeline | `dispatch.py plan` accepts the S2 contract (exit 0): it takes its head from `--provider` and ignores the block's effort. Only `launch`/`queue` (`request_from_contract`) refuse it (exit 1) | parse is `launch --dry-run`, valid is `plan` |
| REFUSED = exit 5 | exit 5 is only `LaunchRefused` from `launch_lane`; every parse-time refusal exits 1 (`DispatchRefused`); a started-but-unidentified lane exits 8 (`LaunchIncomplete`) | one node `END REFUSED (exit 5)`; S2 really exits 1: the label is imprecise |
| dependency / serialize-group / cap / RAM are part of dispatch | they exist only in `queue` (`decide_lane`); a hand-run `launch` never checks them | modelled as one path |
| verb `codespace-plan` | there is no such verb: `codespace_plan()` (`dispatch.py:1978`) is reached through `plan --substrate codespace --repo owner/name` | used that |
| a Dispatch-Codespace head reaches the substrate gateway | `launch --dry-run` refuses a `Dispatch-Codespace` head at parse (exit 1, measured); `queue` reads the substrate from the raw text first | S6 uses a claude head with the `substrate: **codespace**` label |
| `[#1572]` already-launched | `queue_cmd`'s `do_launch` (`dispatch.py:3954`) has no try/except around `launch_lane`, so a `LaunchRefused` propagates out of the pass; the row's title and body read in opposite directions, and the non-dry `queue` was not run (it would launch), so this is read, not executed: UNVERIFIED | end node bound to `dispatch.py:1141` |

## 7. Zone, actor and TODAY-GLUE values are my assignment

The attribute values (`actor`, `zone`, `glue`) are this lane's judgement, not measured and not the operator's. They exist to test the MECHANISM (colouring from attributes), which worked in both forms. Glue nodes: start (seat runs the Dispatch line by hand, `[#1572]`), claim (seat follows prose), dependency (fed by the integrator seat's hand-written STATE lines), running (the dispatcher watches), reaped and END-EARLY (a human notices). No node is colour BROWSER; the zone enum itself is accepted by both (tests check it).

## 8. UNVERIFIED (not run, or run only on a toy)

- Opening `p1_dispatch.bpmn` in bpmn.io, and colouring there.
- A complete bpmn.io layout (1 of 51 edges laid out; cause not looked into).
- `transitions` beyond the 4-state toy.
- The real `moment:pre-launch` organs (injected).
- A non-dry `queue` pass and `[#1572]`'s actual behaviour.
- Persisting a SpiffWorkflow instance against decision E.
- pyparsing's licence.
- Reader comprehension of either diagram.
- Anything about a second process (P2..Pn): this is one process.

## 9. Files

`b_statemachine/{p1_dispatch.py,run_scenarios.py,export_diagram.py,check_bound.py,test_p1_dispatch_b.py,out/}` · `c_bpmn/{p1_dispatch.bpmn,run_scenarios.py,render.py,check_bound.py,test_p1_dispatch_c.py,out/}` · `common/{services,probe,completeness,model_matrix,report}.py` · `contracts/`.

Run: `/tmp/spike/venv-python_statemachine/bin/python -W ignore scratch/b-vs-c-spike/b_statemachine/run_scenarios.py` and `/tmp/spike/venv-spiffworkflow/bin/python scratch/b-vs-c-spike/c_bpmn/run_scenarios.py` (the venvs are throwaway: `uv venv`, `uv pip install python-statemachine pydot` / `spiffworkflow`; `pytest -c /dev/null --rootdir=/tmp` because the hub's `pyproject.toml` adds `-n`).
