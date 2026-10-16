# Archive copy of transport file DIGEST-VERIFY-transport-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-transport-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] d2e8ee19a9691002. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-c-handoff-transport (claude-sonnet-5-5)

# DIGEST VERIFY transport (V5) @ origin/main b46836c8

Transport root `H:\My Drive\CLAUDE PROMPT DIR`. Classes: WORKS / BROKEN / DEAD / DUPLICATE / UNRUN.

| element | class | witness | caller |
|---|---|---|---|
| transport.py --help | WORKS | lists report,strays,derive,inventory,index,seat-ids,query,janitor; exit 0 | harness |
| transport.py report | WORKS | JSON with `"stray_count": 128`, exit 0 | audit, humans |
| transport.py strays | WORKS | `"stray_count": 128 ... "unclassified_count": 117`, exit 1 (gate fires: 128 strays on live transport) | gate |
| transport.py derive | WORKS | `"missing_from_registry": []`, exit 0 | registry check |
| transport.py inventory (no --write) | WORKS | `inventory: 2219 live file(s) ... not written (use --write)`, exit 0 | landing inventory |
| transport.py index --check | WORKS | `index: STALE (run index --write)`, exit 1; tool correct, INDEX is stale | integrator |
| transport.py index (build, print) | UNRUN | would print a ~345 KB INDEX; --check proves the builder runs | integrator |
| transport.py seat-ids --check | WORKS | `seat-ids: STALE or empty (run seat-ids --write)`, exit 1 | index, query |
| transport.py query --kind LANE_END --date 2026-10 | WORKS | first run `query: no INDEX row matches (status=current)`, exit 1; re-run after the checker disagreed: 4 rows (`to-browser/LANE-END-lane-bw-1450-boot-teaching.md \| LANE_END ... 2026-10-13`), exit 0. Result is not stable across runs while INDEX is STALE and the transport moves | seats |
| transport.py janitor (dry run) | WORKS | default dry run, lines `skipped: to-browser/LEDGER-...-superseded... (UNATTRIBUTED)`, `... (unregistered)`, exit 0; --apply not used | operator |
| transport_lint.py --help | WORKS | subcommands check, sweep; exit 0 | lanes |
| transport_lint.py sweep --since 2026-10-14 | WORKS | reports e.g. `ANSWER-...: wrong-folder: kind ANSWER belongs in to-cc/` and `no-by` on 4 SESSION/SUPPLEMENT files, exit 1 | lanes |
| transport_report.py --help | BROKEN | prints help then `{"delivered": false, ... "reason": "unexpected SystemExit: 0"}` and `NOT delivered`; --help is treated as a failed delivery | lane-end hook |
| to-browser/INDEX.md size | WORKS | `wc`: 345506 bytes, 2886 lines | humans, query |

## CHECKER

vendor: OpenAI via `codex exec -m gpt-5.6-terra` (R104 default; contract text said gpt-6-astra, common rules §4 wins: PREMISE-FAILED, contract superseded). Served model id reported by the tool: `gpt-5` (header line `model: gpt-5.6-terra`). stdin closed. Checker used `uv run --no-cache`.
Rows re-run: 9. AGREE: --help, report, strays, derive, index --check, seat-ids --check, transport_report --help (BROKEN row confirmed: `NOT delivered`, exit 1).
DISAGREE (both readings stand): inventory -- checker `2221 live file(s)` vs mine `2219` (live transport gained 2 files between runs; not a tool fault). query -- checker got 4 LANE_END rows, exit 0; mine first got none; my re-run agrees with the checker, row reclassed WORKS-unstable.
Checker verbatim excerpt: `| transport_report.py --help -- BROKEN | AGREE | Printed help, then JSON with "reason": "unexpected SystemExit: 0" and transport_report: NOT delivered; exit 1.`

## USAGE

Claude tokens: lane_cost.py not run. agy calls: 0. Copilot substitutions: 0. Other-vendor calls: see CHECKER.
