# Archive copy of transport file DIGEST-VERIFY-land-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-land-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 2e9a4dbf12a25150. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-a-dispatch-land (Sonnet 5.5), base b46836c8, area V2 land and merge

| element | class | witness | caller |
|---|---|---|---|
| merge_path.py (group --help) | WORKS | exit 0; commands: integration-name, land, ruleset, seal-base, target-line, verdict, verify-local | /lane-integrate |
| merge_path.py integration-name | WORKS | `integration-name --batch NV` exit 0: `worktree-integrate-nv` | /lane-integrate |
| merge_path.py seal-base | WORKS | exit 0: `b46836c81589bb1fd0f726279d8d17d9ddb7d5e6` (= origin/main) | integration-branch push |
| merge_path.py target-line | WORKS | `target-line --tip b46836c8...` exit 0: `refs/heads/main b46836c8... refs/heads/main b46836c8...` | server-side spine/anchor organs |
| merge_path.py ruleset check | WORKS | exit 0: `ruleset: OK (deploy/conductor-required-checks.ruleset.json)` | /lane-integrate |
| merge_path.py ruleset apply / rehearse | UNRUN | apply forbidden by contract; rehearse records a verdict (a write); `--help` exit 0 | integrator |
| merge_path.py verdict | UNRUN | `--help` exit 0; every verb emits a run event to the private state home, outside job tmp; no NV merge sha exists | land |
| merge_path.py land | UNRUN | forbidden by contract (pushes; `--no-push` still writes a run event) | integrator |
| merge_path.py verify-local | UNRUN | runs the whole gate list and writes a run event; not a read | integrator |
| merge_receipt.py (group --help) | WORKS | exit 0; 10 verbs: actions, close, median, models, open, push, race, require, summary, time | merge_path.py land, integrator |
| merge_receipt.py median | WORKS | exit 0: `per merge 12.4, 16.9, 17.6, 18.3, 67.9, 804.5`, `quartiles 17.1 / 17.9 / 55.5 min` | integrator |
| logs/MERGE-RECEIPTS.jsonl (newest record) | WORKS | `tail -n 1` parses as JSON: `"batch": "BW", "closed": "2026-10-13T16:57:40+00:00", "concurrent_seats": 17`, with `flagged_reds` listing two pytest (windows-latest) reds | merge_receipt close |
| merge_receipt.py actions / require / open / close / push / race / models / summary / time | UNRUN | `actions` and `require` `--help` exit 0; the rest write the ledger or run commands; none are reads | integrator |
| /lane-integrate | UNRUN | .claude/commands/lane-integrate.md exists and cites PLAYBOOK Ch8; a command that walks a merge queue from the primary on main, cannot run from a worktree with no NV merges | operator |
| scripts/no_leftovers.py verify | WORKS | `verify` (no --lane) exit 0: `husk scan of ...\.claude\worktrees: CLEAN (no husk)` | doc'd Stop/teardown checks |
| ruleset state on GitHub | WORKS | `gh api repos/rdwornik/dev-knowledge/rulesets` exit 0: one ruleset `conductor-e-required-checks`, `"enforcement":"disabled"` (matches the payload arriving disabled) | merge_path.py ruleset |

## CHECKER
vendor: OpenAI Codex CLI 0.155.0, `codex exec -m gpt-5.6-terra -s read-only`. Served model: tool header `model: gpt-5.6-terra` (the body self-reported `gpt-5`). Attempt 1 ran through uv and failed: uv cache access denied, and `gh api` refused (proxy). SUBSTITUTION: retried once through the venv interpreter. Retry verdicts, verbatim (table sha256 0C86135A...F33685):

merge_path.py (group --help) | AGREE | exit 0; lists 7 documented commands
merge_path.py integration-name | AGREE | `worktree-integrate-nv`
merge_path.py seal-base | AGREE | `b46836c81589bb1fd0f726279d8d17d9ddb7d5e6`
merge_path.py target-line | AGREE | `refs/heads/main b46836c8 refs/heads/main b46836c81589bb1fd0f726279d8d17d9ddb7d5e6`
merge_path.py ruleset check | AGREE | `ruleset: OK (deploy/conductor-required-checks.ruleset.json)`
merge_receipt.py (group --help) | AGREE | exit 0; lists 10 documented verbs
merge_receipt.py median | AGREE | `per merge 12.4, 16.9, 17.6, 18.3, 67.9, 804.5`
scripts/no_leftovers.py verify | AGREE | `no-leftovers husk scan ...: CLEAN (no husk)`
ruleset state on GitHub | UNRUN | not queried
logs/MERGE-RECEIPTS.jsonl (newest record), /lane-integrate | UNRUN | not read

8 rows re-run, all AGREE. This table has no BROKEN or DEAD rows. The GitHub ruleset state and the newest receipt rest on my witness alone (single vendor).

## USAGE
Claude tokens: not measured. agy calls: 0. Copilot substitutions: 0. Other vendor: 2 codex calls (attempt 1 failed on uv, one retry), about 37k and 34k tokens.
