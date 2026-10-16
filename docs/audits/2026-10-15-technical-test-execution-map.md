# Archive copy of transport file DIGEST-TEST-EXECUTION-MAP-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-TEST-EXECUTION-MAP-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 7d5774d06a44c645. Content below the rule is unchanged except CRLF->LF.

---

<!-- scope: meta -->
by: integrator-bu (CC seat 3cdb5b69)
date: 2026-10-15

# TEST EXECUTION MAP — 2026-10-15

Line numbers are at b6161972. Times in seconds, from `gh api .../actions/jobs/<id>` step timings.

## (a) Lane local
- rule: Tier A targeted per step; full suite once at integration (PLAYBOOK.md:993-1000, :1071-1073; batch-common-rules-template.md:84)
- selection: `/verify` -> verify.py:53-59 `impacted_tests.select`, falls back to full suite (verify/SKILL.md:14-19)
- parallelism: template placeholder "memory gate | -n <k>" (batch-common-rules-template.md:84); default addopts `-n auto` (pyproject.toml:324)
- integrator `merge_path verify-local` -> gates.py:176-181: audit-health, ship-gate, ruff, impacted-tests (`pytest -x` over the selection; refuses "# FULL SUITE", gates.py:157-169)

## (b) Pre-commit
- local stages: only the hooks with no `stages: [manual]`; header says all other hooks moved to CI (.pre-commit-config.yaml:19-30)
- impacted-tests-guard: live, always_run, `impacted_tests.py guard` (:677, :715); static coverage check, starts no pytest (impacted_tests.py:736-800)
- doc-counts-pytest-freshness: `stages: [manual]` (:198-199); runs `pytest --collect-only`, measured 29 s (:213); runs in CI commit-gate (conductor.yml:526)

## (c)(d)(f) CI — conductor.yml
- triggers: push main/`worktree-**`/`epic/**` (:74), PR main (:76), cron 05:00 UTC (:81)
- command: `uv run --locked pytest -q --tb=short -n 4 --dist loadgroup -m "not operator_host"` (:163); full suite, marker filter only, no path filter
- OS legs: ubuntu-latest, windows-latest, fail-fast false (:105-106); the raw exit is continue-on-error (:150), the verdict comes from the known-reds compare (:182-193, :226-227)
- ship-gate job: `audit.py ship-gate`, advisory, job continue-on-error (:587, :606)

| run | event | ubuntu setup/tests | windows setup/tests | ship-gate step |
|---|---|---|---|---|
| 38656374259 | push main 50013d6f | 16/751 | 29/1555 | 66 (fail) |
| 38725590391 | push worktree-integrate-bu b6161972 | 13/544 (red) | 24/1551 (red) | 70 (fail) |
| 38713361053 | schedule 50013d6f | 16/770 | 17/1163 | job 98 (fail) |

- newest push-to-main 38728894892 (b6161972): in progress at read time
- report-only-wall.yml (push main, cron 03:37, :18-26): `uv run --locked pytest -q --tb=line` (:149), ubuntu only, addopts -n auto; last schedule 38706597567: pytest 915 s, never blocking (:145)

## (e) merge_path.py land
- runs no tests; pushes the sha to `worktree-integrate-<batch>`, polls CI (timeout 900 s, merge_path.py:263-264)
- verdict: `ci_verdict.verdict_for(sha, baseline=base, required_contexts)` (merge_path.py:228-239); 6 contexts, 2 pytest legs (actions_verdict.py:97-98)
- failing pytest leg compared test by test against the same-named leg of the base run (actions_verdict.py:502-505)
- known reds: `logs/KNOWN-REDS-REGISTRY.json` read at the BASE sha (actions_verdict.py:99-101); head registry checked for expiry (ci_verdict.py:487-495)

## Answers
- pytest-xdist in uv.lock: yes, 3.8.0 (uv.lock:994-995)
- pytest-testmon in uv.lock: no (grep empty); named as a rejected alternative only (impacted_tests.py:18)
- impacted_tests.py callers: .pre-commit-config.yaml:715 (guard); gates.py:150 (select); verify.py:53; test_pairing.py:125 (that stage is skipped by decision, integrator-order-template.md:84); deny_and_point.py:602 is pointer text; no caller in .github/ or templates/
- mutmut: [tool.mutmut] pyproject.toml:198, source_paths scripts (:236), tests test_fleet_analytics.py (:238), `-n 0` (:259); CI job mutation-pilot report-only-wall.yml:235-290, `--with mutmut==3.7.0`
- mutmut last run: 38706597567 (2026-10-15 schedule), mutmut step 163 s; 2077 of 2291 executed: 863 killed, 1210 survived, 4 timeout, 214 no tests (job 116327524000 log). Baseline logs/MUTATION-BASELINE.json = run 38073707389, identical totals (commit 028b1f58)
- ship_gate_diff timing: not in MERGE-RECEIPTS (0 matches, b6161972). Run-events file `%LOCALAPPDATA%/dev-knowledge/MERGE-PATH-RUN-EVENTS.jsonl` has 26 events; the last 10 (2026-10-05..10-10) are all `fail`, 655-1146 s, mean 899 s; none after 2026-10-10T20:08. Moved to batch close (STANDING_RULINGS.md:5257)
- ship_gate_diff catches: not recorded. Events hold only organ/outcome/duration; receipts have no such step
- last 10 kind:merge receipts: `suite` step (CI read) 11-30 s; suite_verdict PRE-EXISTING 8, none 2; flagged_reds 0/0/0/0/0/6/8/8/0/0
