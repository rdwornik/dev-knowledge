# Archive copy of transport file DIGEST-PHASE0-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-PHASE0-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] c9817a2bd9e54ab3. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
supersedes: none
summary: Phase 0 evidence for PLAN-HARNESS r4. CI is RED on 2512b210 and on main b46836c8, and land refuses today. Known-reds compare: 4 regressions on 2512b210, 25 on b46836c8. 21 of the 25 have one cause: the 10-14 bundle's BD-manifest sha mismatch makes handoff_probes hard-fail. ci_verdict.py over-reports (it reads the retired [#802] step). Registry expiry 0, flake 0. manual_until 10-19 hard-blocks nothing on 10-20 (advisory TIER_SHIP only). The R48 registry and print are not built. Registry implement order and the sonnet-5/haiku-4-5 pins mismatch R104. 14 of 16 B-1 lanes have no owning row.
by: CC session 2cbf27b3-4e9c-4968-a3ff-1c76fdb79d49 (Claude Code 2.1.299 bg job 2cbf27b3; served claude-opus-5-5[1m] = Opus 5.5, orchestrating per R104). Read-only subagents: Haiku x4 (F1, E-READ/E7, E2, E9), Sonnet x5 (E0, E3, E4, E5, E6/E8).

# DIGEST — Phase 0 evidence (2026-10-14)

## Failures and contradictions (R46.6)
- **X1. main is RED; land refuses.** `ci_verdict --ref b46836c8` returns state RED (run 38555439522). Only PASS and PRE-EXISTING are landable (`merge_path.py:220`, `:339-341`).
- **X2. One cause behind 21 new reds.** The live `handoff_probes` fails with "BD-manifest toothless in 2026-10-14-dev-knowledge-architect … PASTE_THIS/PROBES/RESIDUAL/SUPPLEMENT (sha mismatch)". A local run of `test_verify_handoff_probes.py::test_registered_check_never_fails_on_live_repo` FAILs at `:766`. The filled bundle (4438afcd/2c4d2a54) is newer than its manifest; this is R103 item 4.
- **X3. ci_verdict reads the wrong step.** `SUITE_GATE_STEP_NAME` (`ci_verdict.py:114`) parses the retired [#802] step (`conductor.yml:165-173`). The verdict is the known_reds step (`:182-197`, `:226`). As a result:
  - it counts 10 reds against 4 real on 2512b210, and 31 against 25 on main;
  - registered ids and witnesses appear as new;
  - entries are duplicated (24 and 133 raw lines).
- **X4. CLAUDE.md §9 vs config.** The parsed `.pre-commit-config.yaml` has 17 armed and 18 manual hooks. §9 says "armed 12" and says ruff blocks, but ruff is manual. block-commit-on-main is armed (E0 said manual; the parse corrects it).
- **X5. Brief premises that do not hold.**
  - `--trial-cut` is at `gen_handoff.py:3528`, not `:3526`.
  - `manual_until` has 90 entries, not 62 (58 dated 10-19).
  - dodo.py and gen_handoff.py do not read `manual_until`.
  - [#1439] is R91 attribution, not D7.
- **X6. Dead reader.** `handoff_state.py:697` `_MANUAL_UNTIL_RE` is `^`-anchored, but harness.yaml uses the key inline. It matches 0 lines, so `verify_handoff_probes.py:1575` always reads "none".
- **X7. Preflight now fails twice.** It counts 148 OPEN decision files (145 at the cut), and 2 QUESTION files have no `disposition:`. `--preflight-only` exits 1.

## F2 / E1 — CI (artifact `known-reds-compare.out`; Linux and Windows identical)
- **2512b210** (run 38440203431): 54 pre-existing, 4 witnesses ([#664]).
  - **4 REGRESSION:** 3 in `test_consumer_at_landing` (live_corpus_measures, live_corpus_verdict@branch_context, main_shaped_control@branch_context). Cause: `LANE-bw-912-known-reds-expiry.md` is unconsumed.
  - The 4th is `test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export`, SIG-CHANGED. The export is now read by `graph_queries.py`, `system-map-record.json` and `harness.yaml`.
- **b46836c8** (run 38555439522): the same 4, plus 21 new: handoff_cut_acceptance ×5, onboarding_items ×3, seat_release_moment ×12, verify_handoff_probes ×1. All raise `PreflightError … handoff_probes` (X2).
- **Class counts:** regression 25, registry expiry 0, flake 0.
  - No expiry: every member expires 2026-10-31 (R98, dc24b371).
  - No flake: the two OS legs are identical.
- **Other jobs on main:** commit-gate, ship-gate and handoff-manifest FAIL. ruff, spine, seal, anchor and phase-gate pass.

## F1 / E1b — manual_until
- **Live reader:** `audit_checks/check_organ_truth.py:317-319` alone, and only for uncalled rows (`:306`). Its tier is TIER_SHIP (`audit.py:5551`).
- **Inert or prose readers:** `handoff_state.py:697` (X6), `generate_organ_index.py:152,489-520` (0 hits), `gen_task_tree.py:206`, `graph_queries.py:600-674`, `fleet_health.py:1191`, `plan_lint.py:218`.
- **On 2026-10-20:** uncalled fates dated 10-19 flip WARN→FAIL "dated debt is now due" (`:341-343`). The comparison is a strict `<` (`:346`), so 10-19 itself stays WARN. Nothing blocks:
  - `audit.py health` runs TIER_COMMIT only (`:6871`);
  - the ship-gate job is `continue-on-error` (`conductor.yml:582`);
  - no stage, cut or commit flips.
- **Already due if uncalled:** `seat_state.py` (10-11), `hook_watchdog.py` (10-14).
- **Moment organs** (`harness.yaml:57-96`; no code reads them): pre-launch 3, lane-start 1, merge 7, teardown 1, lane-end 3, batch-close 2, seat-release 4.
- **Fates** (`:105-174`): 10-19 ×58, 10-15 ×9, 10-14 ×1, 10-11 ×1.
- **Per-name list:** UNKNOWN. No listing tool exists.

## E-READ
- **TOOLS-IN-USE 10-11:** holds. Cites drifted: SIZE_TO_EFFORT is now `gen_lane_contract.py:1695`, DEFAULT_MODEL `:199`.
- **REVIEW-STATUS 10-11:** stale. Worktrees 19→2, local branches 20→7.
- **SPINE-MAP 10-10:** holds. BUILD-LIST is still read (`gen_lane_contract.py:1687`).
- **state-store audits 09-23:** research (27 KB) and debate (150 KB) are present.
- **doc-counts:** 10474 tests, matching `pytest --collect-only`.

## E0 — tools
- **R48 print: NOT BUILT** (R48.5, `STANDING_RULINGS.md:5472`). The nearest tools have no last-ran column:
  - `system_map.py build` (out-dir in scratch): map_sha 88f1bc52, 73 organs, LIVE 52 / DEAD 21;
  - `organ_usage_metric.py census`: 232 processes, CALLED 91 / UNOBSERVED 103 / UNREACHABLE 21.
- **USED:** dispatch, merge_path, merge_receipt, conductor, distill, quota_watch, telemetry_emit, ci_verdict, known_reds, audit, reuse_gate, gen_handoff, assemble_paste, verify_handoff_probes, system_map, no_leftovers, dodo.
- **INERT:** offload_admission, provider_router, provider_bench (09-15), cost_usage_telemetry, required-tools, read_gate, decision_coverage, decision_carriage, transport_lint, batch_janitor, seat_registry, codespace_parity, /lane-boot.
- **MISSING:** lane_report.py (the schema exists). claim.py is UNKNOWN.
- **Diff vs 10-11:** new are system_map, /map, reuse_gate, required-tools and SessionStart-one. Nothing went MISSING.
- **Not effective:**
  - 18 manual hooks;
  - commit-gate and ship-gate are `continue-on-error`;
  - the ruleset is `enforcement: disabled`;
  - the merge moment has left no telemetry since 10-10.

## E2 — ADR-121 / ADR-125
- **ADR-121.** Status: Proposed.
  - Decision: an event log on orphan ref `harness-state`, one writer (the integrator, via state_store), lanes writing their own outbox ref, validated transitions (`:61-75`).
  - Options: O1–O6 plus O3-refined.
  - Evidence: research and debate present; the Codex check is debate §4 (gpt-6-sol). Matrix: absent.
  - Dependents: 52 files (tasks 963/981/984/986/987/1039/1360/1361/1420, ADR-122/123).
  - Partial implementation: `known_reds.py:2`, `harness.yaml:73`. No state_store.
  - C5: `WARN proposed-stale 21d`.
- **ADR-125.** Status: Proposed.
  - Decision: prose is replaced by its kind (rule→gate, fact→data, event→trailer, procedure→skill, reason→ADR), then removed in 5 steps (`:46-60`).
  - Options: P0–P5; P2 chosen at 435/500 (matrix `:130-153`).
  - Evidence: Codex check `docs/audits/2026-09-25-codex-lane-adr-drafts.md:30`. Research and debate: absent.
  - Dependents: 14 files. Implementing rows: none.
  - C5: `WARN proposed-stale 19d`.

## E3 — R103
- **`--preflight-only`:** writes nothing, exit 1. FAIL ship_gate and question_disposition; `p11_carriage: 339 files, 191 resolve, 148 OPEN`.
- **R103 items:**
  1. Trial cut: PARTIAL (preflight rows only, `:1919-1962`).
  2. Generator writes the mechanical parts: PARTIAL. JOURNAL is a printed draft (`:3521`); SUPPLEMENT and publish are absent.
  3. Standing GO: ABSENT.
  4. Seat-release accepts a filled bundle: PARTIAL (`_self_inflicted_bd_manifest`, `:1047-1231`). X2 is the live failure.
  5. janitor --apply: PARTIAL (`transport.py:35-37`, no caller).
- **P11:** `assemble_paste.py:480`, refusal at `:565-575`. It refused because 145 `carried-by: OPEN` files were unnamed in RESIDUAL. The fix named them (RESIDUAL.md:77).

## E4 — gate map
- **task:** code (`gen_task_tree --check`). Stage 1 still reads BUILD-LIST (`harness.yaml:13`).
- **contract:** partial (`lane-contract-check` manual, `.pre-commit-config.yaml:456`).
- **RED test:** nothing.
- **implement:** 17 armed hooks.
- **checks:** CI pytest via known_reds.
- **review:** prose. Nothing reads PLAN-REVIEW.
- **land:** code (`merge_path.py:293-354`), not exclusive; the ruleset is disabled.
- **close:** code (`backlog-id-on-close`).
- **G1–G10:** all OPEN, except G7 partly changed (088ff1c8). `lane_handback_gate.py:262-270` still exits 0 with no session file.
- **R48 registry:** absent; nothing runs it.
- **CI tools:**
  - ruff: `conductor.yml` job ruff (`:229`);
  - mutmut: `report-only-wall.yml` mutation-pilot, report-only;
  - deptry: not in CI (spine stage 6);
  - import-linter, mypy: not configured.

## E5 — routing vs R104
- **distill:** UNKNOWN. "no single BUILD-LIST row matches subject 'BACKLOG'", so no tier or vendor line came out.
- **provider_router:** reads the registry order (`provider_router.py:192,295`).
  - implement: anthropic, copilot, xai (not-admitted).
  - review: openai, xai (not-admitted), anthropic.
  - Gemini has no route in either.
- **provider-registry.yaml:**
  - orchestrate `:631` and plan `:650` = claude-opus-5-5. OK.
  - **MISMATCH:** implement `:672-705` is sonnet-5 first; R104 puts Copilot first.
  - **MISMATCH:** review `:730-766` ends with sonnet-5; R104 has Copilot non-Anthropic, then Gemini.
  - dispatcher `:837-839` = sonnet-5 (an R22 override?).
  - **`claude-sonnet-5` pins** where 5-5 exists (`:1087` "ROWS-OWED"): `:673,766,798,813,839`, dispatch.py ×7, plan_lint.py ×8, routing_agreement.py ×4.
  - **Haiku** is `claude-haiku-4-5-20251001` (`:978`, `dispatch.py:363`).
- **Models:**
  - `/model opus`: settings has `opus[1m]`, and this session is served claude-opus-5-5[1m]. Yes.
  - Copilot dot-form ids: UNKNOWN (no catalog in `--help`).
- **Cost:**
  - An Agent-tool result gives tokens, tool_uses and duration, **no USD**.
  - `claude -p` `total_cost_usd`: parsed at `provider_bench.py:643`. Whether it is an API estimate: UNKNOWN (not run).
- **quota_watch:** `Codespaces 47.10/180 core-hours / Actions 10921/3000 min (364%) / Copilot 5356/20000 credits (26.8%)`.

## E6 — logistics
- **Seat id:** the last id is Tech-Architect-44 (`seat-ids.yaml:16`), so 45 by sequence. Nothing assigns it. The file is generated by `transport.py seat-ids --write` (`:1599,1720`) from `by:` pairs.
- **Overlap:**
  - lane_boot: W0-1 and W0-2 only.
  - dispatch.py: L2a hunks 619-870, 1415-1500, 2170-2260; L4 hunks 1964-2701 (codespace_exec). Adjacent near 2170-2390; no trial merge was run.
  - gen_handoff: L7 (1907-1970, 3558-3865), then L8.
  - merge_path: L2a only (247-457).
  - provider-registry: L4 (+37) and W0-2.
- **Resources:** RAM free 13.0/27.7 GB, CPU 66% on 16 logical processors. Ceiling: reserve 2.00 GB (`resource_lifecycle.py:115`), 17 more seats, floor 200 MB (`:125`). No lane-cap constant.

## E7 — boot drift
- **f74d1c4c** as HANDOFF_BOOT's last change: confirmed.
- 81 files changed since. Not named in the boot: session_start, hook_launcher, reuse_gate, merge_path, row_close, system_map, transport_lint, harness_probes, decision_carriage, check_rulings_carried, seat-ids.yaml, the lane_report schema, `/map`.
- **Citations:** all ADRs and R30/34/41/46/47 resolve. R45 and R48 resolve only to boot summaries (`:116-121`).
- The boot's line 150 calls R30 "standing", but it is batch-scoped (`STANDING_RULINGS.md:5060`).

## E8 — what bit
- **Fixture writing seat rows:** nothing (plan line only). Site: `test_seat_registry.py:317/482/519` uses `CLAUDE_PID=os.getpid()`.
- **Background job surviving a restart:** nothing (`batch_janitor.py:244` runs `claude stop`).
- **Midnight cut:** nothing (`gen_handoff.py:1288-1309`).
- **P11 on 145:** nothing exact; adjacent rows [#1332], [#887], [#1432].

## E9 — ownership (grep over tasks/; `gen_task_tree` has no query mode)
- **Owned:**
  - L7 = [#1450], partial ("HANDOFF_BOOT states the R80 order… a test finds both").
  - L10 = [#603], probable.
- **No owner:** W0-1…W0-6, L2a, L2b, L1b, L3, L4, L5, L8, L9. Traps: [#1374] is the dispatch shim, not D1's 3 HIGH; [#1439] is R91.
- **Proposed intakes:**
  - W0-1: lane_boot refuses a contract with no [#id] or Done-when — Done when: a RED test refuses both.
  - L8: R103 into --trial-cut, generator-written parts, seat-release taking a filled bundle — Done when: a fixture trial cut on a filled bundle passes.
  - L9: boot-drift gate at batch close — Done when: an unexplained system_map diff FAILs it.

## Transport lint
`transport_lint.py check` printed ok for BATCH-PHASE0-EVIDENCE-2026-10-14.md, PLAN-HARNESS-2026-10-14.md and RATIFICATION-2026-10-14.md (exit 0). This file keeps the brief's name; lint ok.

usage: orchestrator UNKNOWN (not readable in-session); 9 subagents = 738,542 tokens (source: Agent-tool `subagent_tokens` fields)
