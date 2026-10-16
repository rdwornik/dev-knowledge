# PROCESS MATRIX (PART 9) - repo snapshot night-archive-2026-10-15, as of 2026-10-16
Sources: ecosystem/harness.yaml, .pre-commit-config.yaml, .claude/settings.json, .claude/commands/*.md, .github/workflows/*.yml, docs/audits/2026-10-15-technical-verified-harness-map.md (+ the 10 verify digests). Verdicts REUSED from the map, not re-derived. Receipts (logs/receipts/MOMENT-*.json) are gitignored: absence in the repo is not proof of no fire; where I say DEAD for a moment, the witness is the absence of a recorded step plus the operator register line.

## A. ROWS (90) with trigger, applies-to, status, witness
### A1 harness.yaml moments (7) - trigger quoted
| moment | trigger (quoted) | status | witness |
|---|---|---|---|
| "pre-launch" | "the launcher (`dispatch.py launch`), before it spawns the lane" | WORKS | scripts/dispatch.py:902 argv `doit ... moment:pre-launch`; BU `queue --watch` "fired 4" (token-burn inventory) |
| "lane-start" | "the lane's own first turn, inside the lane" | DECLARED-ONLY | no caller: grep moment:lane-start hits only dodo.py:41 docstring + worktree_occupancy.py:32 comment |
| "merge" | "integrator command, immediately after each `git merge --no-ff`" | DEAD (no fire evidenced) | caller lane-integrate.md:179 exists, but MERGE-RECEIPTS 51 rows 10-01..10-15 carry no `assemble` step; operator-asks-register:46 "BW did not run the moments"; how-work-runs:31 G15 `merge_receipt.models needs contract and it is unset` |
| "teardown" | "integrator command, after merge and push" | WORKS | lane-integrate.md:192; MERGE-RECEIPTS steps `teardown` x2 since 10-01 |
| "lane-end" | "Claude Code Stop hook, once: at the first turn end after the lane wrote its HANDBACK line" | WORKS (hook), organs unverified | settings.json Stop lane_end_guard.py; hooks-gates digest rc=0 |
| "batch-close" | "integrator command, after the last merge of the batch" | DECLARED-ONLY | only prose caller templates/integrator-order-template.md:131; BACKLOG #1028 "digest organ reads no receipt"; no receipt |
| "seat-release" | "the operator's own act ... run by hand" | DECLARED-ONLY | callers are prose in handoff.md:15-18 / handoff-verify.md:64; no receipt |
All 21 moment organs carry manual_until <= 2026-10-05 (expired, not re-dated); HANDOFF_BOOT.md:99 "dodo.py ignores it, so nothing flips on the date".
### A2 spine / phases (3)
| process | trigger | status | witness |
|---|---|---|---|
| /spine, stages 1-12 (kind-subject..contract) | by hand, change kind + subject | WORKS (list only; a run is UNRUN) | `doit -f scripts/dodo.py list` ec=0 (spine-engine digest) |
| phases P1-P7 `doit round` | conductor.py:902, per round | DECLARED-ONLY | harness.yaml:152-ish run_phase.py "manual_until 2026-11-15 ... until the lane phases run it live"; phase-gate: "NOT GATED (1): #689 build" |
| constraints C-TASK/SCOPE/RED/VENDOR/CLEAN | `conductor.py lane --constraint` per round | DECLARED-ONLY | same: no live round has run |
### A3 pre-commit (35)
Armed (17) WORKS: pre-commit x12 {block-commit-on-main, codemap-freshness, roster-freshness, claude-rosters-freshness, audit-index-freshness, organ-index-freshness, quality-requirements-freshness, validate-hermetization, intake-index-freshness, row-archive-proof, provider-registry-agreement, impacted-tests-guard} (each "Passed", 11-24 s; hooks-gates digest); commit-msg x3 {backlog-id-on-close, backlog-filing-backpressure, commit-message-type-prefix} (bad message refused); pre-push x2 {block-ff-push, block-unanchored-push} (local UNRUN, but CI jobs spine/anchor run them: success).
Manual (18, run only in CI job commit-gate via `pre-commit run --hook-stage manual`, conductor.yml:526): WORKS 9 {toc-freshness-playbook, audit-title-gate, validate-backlog, prepend-order, derived-copies-rebind, coherence-nudge, doc-counts-pytest-freshness, graph-process-list, graph-edge-class-census}; BROKEN 6 {graph-orphan-census "REFUSED -- 15 finding(s)"; check-seal-identity "SEAL-IDENTITY FAIL ... slug mismatch" (checker could not reproduce); lane-contract-check "no Kind line found"; decision-coverage "REFUSED -- 1 decision(s)"; audit-health rc=1 "health: DEGRADED"; graph-task-coverage CI "task-coverage: REFUSED -- 9" (local pass)}; UNRUN 2 {graph-rebuild, normalize-dated-headers: write}; DUPLICATE 1 {ruff: stages manual, CI job ruff does the work}.
### A4 .claude/settings.json hooks (12)
WORKS 6: PreToolUse scope_guard, PreToolUse reuse_gate (new file under scripts/ or .claude/ in a lane; "allow-and-log" outside a lane or when the contract is in the prompt dir), SessionStart session_start (nine entries folded to one), Stop session_end_backpressure, Stop lane_end_guard, Stop lane_handback_gate.
BROKEN 1: plugin Stop propose_closures "385/780 bypassed (49%) -- OVER THE BAR", DECLARED BROKEN 2026-09-17.
DEAD 5: block_immutable_edits.py, fleet_health.py --prompts-guard, logs_retention.py (all removed from hooks{}, expiry 2026-10-08 lapsed, not re-dated), deny_and_point.py (UNWIRED 2026-09-18), scripts/hooks/hook_watchdog.py (logs/HOOK-WATCHDOG-KILLS.jsonl is 0 bytes).
### A5 commands/skills (16 besides /spine)
WORKS 13: /boot-session, /decide, /handoff-verify, /handoff, /lane-boot, /lane-integrate (51 merge receipts), /map, /preflight ("wired into no gate"), /why, skills aj-scan, check-against-spec, verify, plugin /review-closures. UNRUN 3: /changelog-review, /save, plugin /ship. All are operator-invoked; none is called by a gate except /lane-integrate -> moments.
### A6 CI jobs (16)
conductor.yml (on push main|worktree-**|epic/**, PR to main, cron 05:00, dispatch): ruff, seal, spine, anchor, phase-gate WORKS; pytest, commit-gate, ship-gate (canonical_freshness: CLAUDE.md last_reviewed 2026-10-05 < edit 2026-10-13), handoff-manifest ("BD-manifest ... 5 file(s) differ") BROKEN; terra DEAD ("terra review NOT RUN -- no provider credential"). report-only-wall.yml (push main, cron 03:37): changes, record WORKS; mutation-pilot UNRUN (schedule/dispatch only). substrate-heartbeat.yml (cron 06:05, push on substrate paths): declaration WORKS; container BROKEN. deploy/conductor-required-checks.ruleset.json: DEAD ("enforcement": "disabled").
### A7 scripts (map, 153 elements REUSED): 89 WORKS / 25 BROKEN / 6 DEAD / 2 DUPLICATE / 31 UNRUN. Plus 70 harness.yaml `fates:` entries (manual_until, no moment trigger) = one DECLARED-ONLY bucket row; 11 of them dated <= 2026-10-15 (expired): ci_red_age, hook_watchdog, learning_distiller, seat_state, transport, quota_watch, codespace_admission, quota_daily, carrier_landed_check, claim, platform_skip_ratchet.
### scripts/impacted_tests.py
NOT called by any .github workflow (grep -rn impacted .github/ = 0 hits). Callers: pre-commit impacted-tests-guard (always_run, `impacted_tests.py guard`), harness.yaml stage 10 (`select --ref main`), .claude/skills/verify/verify.py, ci_verdict.py, gates.py, test_pairing.py. CI runs the full pytest suite. BACKLOG #1560 (Tier-1 impacted on push), #1561 (workflow/ecosystem-data and removed-module selection), #1568 (removal leaves orphan tests) are all status: open.
### FPG-1 / file-purpose graph and /why
Used by gates, not only by hand: reuse_gate.py (PreToolUse; denies a new file unless a `why` search covers its neighbours; settings.json comment R96-D7), scope_guard.py, deny_and_point.py (unwired), harness stage 5 `file_purpose_graph.py stats`, CI-manual hooks graph-rebuild/orphan-census/task-coverage/process-list/edge-class-census, substrate-heartbeat path trigger. /why itself is a by-hand command (harness.yaml fates:113 "whether a fresh session calls it unprompted is [#924]'s measurement -- no census row yet").

## B. MATRIX: artifact x operation -> process(es) that fire
| artifact | create | update | delete | read/query |
|---|---|---|---|---|
| feature code | reuse_gate + scope_guard (PreToolUse, lane only); impacted-tests-guard (scripts/*.py only); codemap-freshness; organ-index-freshness; CI ruff, pytest; graph-orphan-census (CI, BROKEN) | impacted-tests-guard (only if zero tests selected); codemap; ruff; pytest | graph-orphan-census (BROKEN); NONE for orphan tests / removed module (#1561, #1568 open) | /why, file_purpose_graph why |
| test | CI pytest; doc-counts-pytest-freshness (count); quality-requirements trip test; C-RED (DECLARED-ONLY) | pytest; known_reds compare | NONE ([#1568] open; only doc-counts count drift) | known_reds, ci_verdict |
| ADR | claude-rosters-freshness (recent-adrs); decision-coverage (BROKEN); /decide (by hand) | claude-rosters-freshness; decision-coverage; check-against-spec (by hand) | NONE (ADR-125 "superseded means code removed" not enforced; operator-asks-register:36 "7 Proposed-stale, 84 Accepted with no evidence", controller D1 HELD) | decision_coverage.py |
| backlog row (tasks/) | validate-backlog (CI); backlog-filing-backpressure (commit-msg); stage 3 gen_task_tree --check; graph-task-coverage (CI, REFUSED 9) | validate-backlog; backlog-id-on-close (commit-msg); row_close.py (by hand, fates) | row-archive-proof (armed) | /boot-session, boot_frontier |
| intake | intake-index-freshness (armed); NONE for intake-to-row | intake-index-freshness | intake-index-freshness (index drift only) | aj-scan (by hand) |
| docs / protocols | audit-title-gate + audit-index-freshness (docs/audits only); NONE for protocols/ | toc-freshness-playbook (PLAYBOOK); coherence-nudge (HANDOFF_PROCESS); prepend-order (LESSONS/JOURNAL/TOKEN-LOG); ship-gate canonical_freshness (CLAUDE.md, BROKEN); roster-freshness; check-against-spec (by hand) | NONE | /why |
| dependency (uv.lock) | NONE (no add process) | NONE except implicit `uv run --locked` / `uv sync --locked` failing on stale lock; pyproject.toml touches codemap + doc-counts regex | NONE | dependency-baseline.yaml read by fleet_parity.py and gen_handoff.py only |
| CI workflow | NONE | NONE (impacted_tests does not select for workflows, #1561 open; the push itself runs conductor); substrate-heartbeat path trigger for its own files | NONE | merge_path.py ruleset check (ruleset DEAD) |
| release / tag | NONE | NONE | NONE | decision_carriage.py reads `archive/*` tags only |
| handoff / boot | /handoff, gen_handoff.py (--dry-cut refuses: ship_gate FAIL); moment:seat-release (DECLARED-ONLY) | check-seal-identity (BROKEN); CI handoff-manifest (BROKEN); restamp (HANDOFF-RESTAMP-RECEIPTS 10-14, R107) | NONE | /boot-session, /handoff-verify, handoff_state.py + boot_frontier.py (both UnicodeEncodeError) |

## C. Counts (my 90 rows)
WORKS 57 / BROKEN 12 / DEAD 8 / DECLARED-ONLY 6 / UNRUN 6 / DUPLICATE 1. Declared total 90 (+153 script elements from the map, +70 fated scripts).
