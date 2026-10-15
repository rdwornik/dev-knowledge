# Archive copy of transport file DIGEST-VERIFY-handoff-tools-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-handoff-tools-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 13af4efb157dbc6d. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-c-handoff-transport (claude-sonnet-5-5)

# DIGEST VERIFY handoff-tools (V4) @ origin/main b46836c8

Run from the lane worktree, `uv run --locked python scripts/<x>.py`, each under `timeout`. Classes: WORKS / BROKEN / DEAD / DUPLICATE / UNRUN.

| element | class | witness | caller |
|---|---|---|---|
| gen_handoff.py --help | WORKS | `--help` -> "Generate a v5 handoff bundle from committed repo state.", exit 0 | /handoff, scripts/audit.py |
| gen_handoff.py --mode architect --preflight-only | WORKS | ran ~4 min (first 300 s try hit timeout, retry at 590 s ok): `preflight -- pre-handoff hygiene rows`, 1 `[FAIL] ship_gate: 1 hard-fail finding(s) ... (handoff_probes)`, 8 PASS, exit 1 (tool correct, repo verdict FAIL) | /handoff |
| gen_handoff.py --trial-cut | WORKS | help says it writes nothing ("like --preflight-only ... cut nothing"); ran: `batch-close trial cut -- pre-handoff hygiene rows`, ship_gate FAIL, ledger_refreshed/ratification_present `[n/a-reason:TRIAL-CUT-EXCLUDED]`, exit 1; git status stayed empty | batch-close stage |
| gen_handoff.py --dry-cut DIR | BROKEN | help says it skips the cut-boundary gates, but `[error] refusing to cut a bundle: 2 pre-handoff hygiene row(s) FAILED -- [FAIL] ship_gate ...`, exit 1; PREMISE-FAILED, no bundle written | none found beyond help |
| assemble_paste.py --help / --pin-only | WORKS | `--pin-only` -> `ROLE PIN - HANDOFF_BOOT.md @ handoff-process v7.1.0` + `sha256: 3b097159...c9c746`, exit 0 | gen_handoff.py, /boot-session |
| verify_handoff_probes.py <bundle> | WORKS | on docs/handoffs/2026-10-14-dev-knowledge-architect: `verify_handoff_probes: 42 probe(s) - 38 pass, 1 fail, 3 warn`, exit 1; first 100 s try timed out (SLOW probes), retry ok. Fail = `BD-manifest 5 file(s) differ from the generation manifest` (HANDOFF_BOOT, PASTE_THIS, PROBES, RESIDUAL, SUPPLEMENT sha mismatch) | /handoff-verify, audit.py |
| gen_seat_boot.py verify --bundle <b> | WORKS | `P12: PASS -- 5 seat boot(s) equal a fresh render from Ch8`, exit 0. Bare `verify` -> `Error: Missing option '--bundle'`, exit 2 (needs flag) | PLAYBOOK Ch8, audit |
| gen_seat_boot.py write | UNRUN | writes SEAT-BOOT files; R105 D6 freeze | PLAYBOOK Ch8 |
| handoff_state.py | BROKEN | prints 5+ state rows then `UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 200` (handoff_state.py:852) under cp1252 console, exit 1 | handoff boot, gen_handoff |
| boot_frontier.py --frontier | BROKEN | default console: `UnicodeEncodeError: 'charmap' ... '→'` (boot_frontier.py:315), exit 1; with PYTHONIOENCODING=utf-8 it lists rows `[#720] ...`, exit 0 | /boot-session, fleet_health.py |
| /handoff (.claude/commands/handoff.md) | WORKS | command file present, "Generate or complete a handoff per HANDOFF_PROCESS.md v7"; grep refs to gen_handoff/assemble_paste: 14 in file. Not invoked (would cut) | operator |
| /handoff-verify (.claude/commands/handoff-verify.md) | UNRUN | command cut-day only; its engine verify_handoff_probes WORKS above | operator |
| /boot-session | WORKS | file present; calls `boot_frontier.py` (line 81) | operator |

## CHECKER

vendor: OpenAI via `codex exec -m gpt-5.6-terra` (common rules §4 over the contract's gpt-6-astra: PREMISE-FAILED). Served model id reported by the tool: `gpt-5`. stdin closed. `uv run --locked` was blocked for the checker (uv cache access denied), so it used the checked-in .venv interpreter.
AGREE: gen_handoff --help; assemble_paste --pin-only (sha 3b097159...c9c746); gen_seat_boot verify (`P12: PASS -- 5 seat boot(s)`); /handoff; /handoff-verify; /boot-session (line 81).
INDETERMINATE (checker could not complete): handoff_state.py, boot_frontier.py -- BROKEN rows are confirmed by my own two runs only; checker read source lines 852 / 315 as consistent. NOT RE-RUN by checker: verify_handoff_probes (uv blocked), preflight, trial-cut, dry-cut (skipped by instruction), gen_seat_boot write (UNRUN). So only 4 table rows were re-run with output; this is short of the 5-row bar, and BROKEN rows are not independently confirmed. Status: PARTIAL check.

## USAGE

Claude tokens: lane_cost.py not run (no answer sought). agy calls: 0 (all reads were single --help/grep lookups). Copilot substitutions: 0. Other-vendor calls: see CHECKER.
