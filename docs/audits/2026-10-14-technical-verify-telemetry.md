# Archive copy of transport file DIGEST-VERIFY-telemetry-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-telemetry-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] dc597de2356d47d1. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-d-telemetry-providers (claude-sonnet-5-5), V6 telemetry and cost

| element | class | witness | caller |
|---|---|---|---|
| scripts/telemetry_emit.py | WORKS | `--help` -> `usage: telemetry_emit.py wrap <id> [receipt options] -- <python-args...>`; `pytest tests/test_telemetry_emit.py tests/test_cost_usage_telemetry.py tests/test_quota_watch.py` -> `104 passed`. PREMISE-FAILED: docstring says "wires nothing / grep returns nothing" -> 6 importers | audit.py:126, block_commit_on_main.py:66, block_ff_push.py:88, governance_health.py:633, hook_expiry_verdict.py:40, cost_usage_telemetry.py:137 |
| scripts/cost_usage_telemetry.py | WORKS | library, no CLI: `--help` prints nothing, exit 0; tests in the 104 above pass | provider_router.py:100 (`_sibling`); harness.yaml:131 `manual_until: 2026-10-19`, "untriggered only because that caller is [#691] Half B" |
| quota_watch.py line | WORKS | `[quota] / Codespaces 49.38/180 core-hours used ... / Actions 11159/3000 min used / Copilot 6019/20000 credits used (30.1%)` | digest cost line |
| quota_watch.py report | WORKS | `actions_minutes: 11,159.00/3,000.00 minutes (372.0%), burn 858.385/day, exhaustion 2026-10-14` (data finding: Actions quota exhausted) | operator |
| quota_watch.py check | UNRUN | `Error: Missing option '--projected-core-hours'`; a value would be a guess | none run |
| quota_watch.py record | UNRUN | contract bars `record` (writes ledger) | n/a |
| provider_bench.py census | WORKS | `provider-bench: claude PRESENT 2.1.300 (Claude Code)`; aider/llm/amp ABSENT | operator |
| provider_bench.py report | WORKS | `claude: 10/10 pass ... served_model : claude-opus-5`; `agy: served_model : UNATTESTED` | operator |
| provider_bench.py traps | UNRUN | re-spawns provider probes; the lane may not run a benchmark | n/a |
| lane_cost.py lane (price leg) | BROKEN | `lane lane-nv-929-d-telemetry-providers USD 0.00 over 9 call(s)` and `claude-sonnet-5-5: UNPRICED ... carries no rates: block`; the meter reads zero for the model this lane runs on | /lane-integrate, receipts |
| logs/MERGE-RECEIPTS.jsonl newest 3 | BROKEN | 149 lines; newest 3 parse, 21 fields each; `empty: ['ordered_model', 'ran_model']` on all three (batch BW, 2026-10-13) | merge_receipt.py models |
| merge_receipt.py median | WORKS | `merge-y-750: missing required step(s): handback, merge, suite, teardown` (excludes incomplete receipts by design) | integrator |
| organ_usage_metric.py census | WORKS | `organ_invocation_census: generated 2026-10-14T21:26:17+00:00 (window: 30d)` | audit.py |

DECIDED-BY-LANE: lane_cost price leg classed BROKEN (zero USD for a priced-in-use model), not WORKS, because the value line is "a cost meter that reads nothing".
No DEAD or DUPLICATE element found.

CHECKER
vendor: OpenAI via codex exec; served model (header line): `model: gpt-5.6-terra`; stdin closed. A first run with `--sandbox read-only` failed every row with `Access is denied` on uv's temp dir (sandbox artifact, discarded); this is the one retry, default workspace-write.
rows re-run: 6 (every BROKEN row plus 4 others)
- telemetry_emit.py | AGREE | usage: telemetry_emit.py wrap <id> [receipt options] -- <python-args...>
- cost_usage_telemetry.py | AGREE | [no output; exit 0]
- quota_watch.py check | AGREE | Error: Missing option '--projected-core-hours'.
- lane_cost.py lane (price leg) | DISAGREE | `USD 0.00 over 26 call(s)`: the USD 0.00 agrees, only the call count differs (the lane kept running); both readings stand
- MERGE-RECEIPTS newest 3 | AGREE | 149 lines; newest 3 parse, 21 fields empty=['ordered_model', 'ran_model']
- merge_receipt.py median | AGREE | merge-y-750: missing required step(s): handback, merge, suite, teardown

USAGE
lane_cost.py lane --slug lane-nv-929-d-telemetry-providers: 9 calls, 782,400 tokens, USD unpriced. agy calls: 0 (reads were short targeted). Copilot substitutions: 0.

