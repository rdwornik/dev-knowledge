# Archive copy of transport file DIGEST-VERIFY-ci-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-ci-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 03cfb9687e3739fd. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-b-ci-gates (Sonnet 5.5), V3 CI and known reds, base b46836c8

Main's last push run, conductor 38555439522 on b46836c8: failure. The required-check ruleset is `enforcement: disabled`, so no job blocks a merge today.

| element | class | witness | caller |
|---|---|---|---|
| scripts/ci_verdict.py | WORKS | `--ref main --timeout 0` -> `"state": "RED"`, "133 new red(s) ... baseline c5108329" | verify_handoff_probes, gen_handoff, merge_path |
| scripts/known_reds.py | WORKS | `--help` lists refresh/compare/compare-hook/attribute | conductor.yml:192, :553 |
| logs/KNOWN-REDS-REGISTRY.json | BROKEN | `baseline_id 2026-10-04-fdf4f4952211` but ci_verdict names baseline c5108329; all 61 entries expire 2026-10-31 (not 11-01); one windows member expires 2026-10-19 | known_reds.load_registry |
| job pytest (ubuntu-latest) | BROKEN | run: failure, new reds in test_seat_release_moment, test_onboarding_items, test_handoff_cut_acceptance | conductor.yml; ruleset |
| job pytest (windows-latest) | BROKEN | run: failure; 133 new reds over both OS | conductor.yml; ruleset |
| pytest inner step "-n 4" | WORKS | step `continue-on-error: true`; job fails on the later `exit ${{ steps.known_reds.outputs.exit }}` | conductor.yml |
| jobs ruff, seal, spine, anchor | WORKS | each success in the run; `ruff check` locally "All checks passed!" | ruleset |
| job commit-gate | BROKEN | job-level coe true; `orphan-census: REFUSED -- 15 finding(s)`, `task-coverage: REFUSED -- 9`, audit-health exit 1; orphan-census reproduced locally | conductor.yml |
| job ship-gate | BROKEN | job-level coe true; `[!!] canonical_freshness: CLAUDE.md last_reviewed 2026-10-05 predates last edit 2026-10-13` | conductor.yml |
| job handoff-manifest | BROKEN | blocking, failed; local `audit.py health`: `BD-manifest ... 5 file(s) differ` | conductor.yml |
| job phase-gate | WORKS | success; two inner steps coe true, so it cannot go red on the evaluation | conductor.yml |
| job terra | DEAD | success in 6 s; prints "terra review NOT RUN -- no provider credential" | conductor.yml |
| report-only-wall.yml | WORKS | push run 38555439545 and schedule 09:00: success | push, schedule |
| job mutation-pilot | UNRUN | `if: workflow_dispatch or schedule`; absent from the push run | report-only-wall.yml |
| substrate-heartbeat declaration | WORKS | run 38558284096: success | schedule, push |
| substrate-heartbeat container | BROKEN | same run: "devcontainer build + L1 marker verify" failure; 10-13 schedule run failed too | schedule |
| deploy/conductor-required-checks.ruleset.json | DEAD | `"enforcement": "disabled"` (also via `gh api .../rulesets`); 6 contexts | none; operator arms |

PREMISE-FAILED: registry expiry is 2026-10-31, not 2026-11-01.
OPERATOR-ACTION: renew the 2026-10-19 windows entry first.
DECIDED-BY-LANE: workflows parsed with PyYAML, not agy (exact structure).

CHECKER
vendor: OpenAI Codex CLI, served model gpt-5.6-terra (log header), stdin closed, session 01a13c5b; draft sha256 375C0029...0477. Its rows verbatim; DISAGREE stands beside mine.

scripts/ci_verdict.py | UNRUN | `.venv\Scripts\python.exe scripts\ci_verdict.py --ref main --timeout 0` → `"state": "GH-UNAVAILABLE"` (network blocked).
logs/KNOWN-REDS-REGISTRY.json | AGREE | `Get-Content ...KNOWN-REDS-REGISTRY.json` → `"baseline_id": "2026-10-04-fdf4f4952211"`; entries include `expiry: "2026-10-31"`.
job pytest (ubuntu-latest) | UNRUN | `gh run view 38555439522 --json jobs` → GitHub API proxy connection refused.
job pytest (windows-latest) | UNRUN | `gh run view 38555439522 --json jobs` → GitHub API proxy connection refused.
job pytest, inner step “pytest, pinned at -n 4” | AGREE | `Select-String conductor.yml 'pytest, pinned|continue-on-error'` → `continue-on-error: true`.
job commit-gate | AGREE | `Select-String conductor.yml 'commit-gate|continue-on-error'` → job-level `continue-on-error: true`; local orphan census → `REFUSED -- 15 finding(s)`.
job ship-gate | AGREE | `Select-String conductor.yml 'ship-gate|continue-on-error'` → `continue-on-error: true`.
job handoff-manifest | UNRUN | local `audit.py health --parallel` could not produce a result within the sandboxed run; GitHub run unavailable.
job terra | AGREE | `rg -n 'terra review NOT RUN' conductor.yml` → `terra review NOT RUN -- no provider credential`.
workflow report-only-wall.yml | AGREE | `Select-String report-only-wall.yml 'recorded, never blocking'` → `pytest (recorded, never blocking)`.
job mutation-pilot | AGREE | `Select-String report-only-wall.yml 'mutation-pilot|workflow_dispatch|schedule'` → conditional admits `workflow_dispatch` or `schedule`.
substrate-heartbeat.yml, job container | UNRUN | `gh run view 38558284096` unavailable due blocked GitHub API; static workflow confirms scheduled container job.
deploy/conductor-required-checks.ruleset.json | AGREE | `Get-Content ...ruleset.json` → `"enforcement": "disabled"`.

USAGE
Claude: lane_cost not run; agy 0; Copilot substitutions 0; Codex 1 call (79k tokens).
