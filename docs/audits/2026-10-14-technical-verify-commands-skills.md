# Archive copy of transport file DIGEST-VERIFY-commands-skills-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-commands-skills-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 70de630bdc7944bc. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-689-e-skills-engine (Sonnet 5.5), base b46836c8

# V8 commands and skills

Run: `uv run --locked python scripts/<x>.py --help` (ec=0 every script named) and read-only runs. Callers: `git grep` of the name outside `.claude/commands`, `.claude/skills`, audits, tasks, JOURNAL. Most callers are the generated rosters (`.claude/generated/commands-repo.md`, `.claude/methodology-roster.md`, `ecosystem/organ-index.md`), i.e. self-listing, not a user. `organ_usage_metric census` says a command or skill invocation is NOT observable in transcripts, so "called" cannot be measured.

| element | class | witness | caller |
|---|---|---|---|
| /boot-session | WORKS | assemble_paste, boot_frontier, fleet_health, funnel_lifecycle `--help` ec=0 ("usage: boot_frontier.py [-h] [--repo REPO] [--frontier]") | roster, manifest-v1.5.0 |
| /changelog-review | UNRUN | fetches network and bumps the state file, so not run; its sentinel did fire at SessionStart: "[changelog] claude-code 2.1.300 > last reviewed 2.1.281" | roster, settings.json |
| /decide | WORKS | decide_checks, known_reds, preflight_contract `--help` ec=0 ("usage: decide_checks [-h] [--repo-root REPO_ROOT]") | roster, ADR-128/129 |
| /handoff-verify | WORKS | audit, handoff_state, verify_handoff_probes `--help` ec=0; real run not done | roster, conductor.yml |
| /handoff | WORKS | gen_handoff `--help` ec=0 ("Usage: gen_handoff.py [OPTIONS]"); real run writes a bundle, not run | roster, 86 files |
| /lane-boot | WORKS | lane_boot, id_allocator, single_flight, worktree_seed, worktree_import_proof `--help` ec=0 | roster, intakes |
| /lane-integrate | WORKS | merge_path, merge_receipt, ci_verdict, gates, gen_audit_index `--help` ec=0; real run merges, not run | roster, ADR-110/119/120 |
| /map | WORKS | system_map `--help` ec=0 ("build  Regenerate the map JSON and HTML"); build writes, not run | roster |
| /preflight | WORKS | ran on this contract: "preflight_contract: 6/7 locator claim(s) resolved; 1 FAILED" (contract cites [#717], now CLOSED) | roster, AGENTS.md |
| /save | UNRUN | prompt only, no script; it commits, so not run | roster, CLAUDE.md |
| /spine | WORKS | `python -m doit -f scripts/dodo.py list` ec=0 lists "spine ... stage:01-kind-subject ..."; the run writes receipts, not run | roster, ADR-127 |
| /why | WORKS | ran `file_purpose_graph.py why scripts/dodo.py`: "purpose  : doit adapter for ecosystem/harness.yaml" | roster, ADR-66/98 |
| skill aj-scan | WORKS | aj_scan `--help` ec=0 ("Usage: aj_scan.py [OPTIONS] COMMAND"); a run records a high-water mark, not run | harness.yaml, organ-index |
| skill check-against-spec | WORKS | coherence_enumerator `--help` ec=0; validate_reconciliation ran: "match  CLAUDE.md -> handoff-process (declared 7.1.0 / current 7.1.0)" | CLAUDE.md, organ-index |
| skill verify | WORKS | impacted_tests `--help` ec=0 ("Usage: impacted_tests.py [OPTIONS] COMMAND") | CLAUDE.md, pre-commit |
| plugin /review-closures | WORKS | `review_closures.py --help`: "usage: review_closures [-h] {surface,plan}" | marketplace.json, ARCHITECTURE |
| plugin /ship | UNRUN | prompt only, merges and pushes; refuses in a worktree | roster, CLAUDE.md |
| plugin Stop hook propose_closures | BROKEN | session hook-rate line: "cmd:propose_closures.py: 385/780 bypassed (49%) -- OVER THE BAR"; "DECLARED BROKEN 2026-09-17" | plugin hooks.json |
| workflow conformance-hub.js | UNRUN | spawns Opus and Sonnet agents; the order's one Workflow run was spent on V9 | settings.json, pre-commit |
| validate_backlog.py (plugin copy) | DUPLICATE | `diff scripts/validate_backlog.py plugins/tier1-lifecycle/scripts/validate_backlog.py` differs (line 10: "### [S<n>] <User story>" vs "### <User story>"); the copy has drifted from `scripts/validate_backlog.py` | plugin tests |
| changelog_sentinel.py | WORKS | no argparse; output seen at SessionStart (see /changelog-review) | settings.json |

PREMISE-FAILED: "fleet_health.py --help" and "validate_reconciliation.py --help" do not print help; neither has argparse. They ran their normal read-only report (ec=0).

# CHECKER

- vendor: OpenAI, `codex exec -m gpt-5.6-terra -s read-only`, stdin from file; served model `gpt-5.6-terra` (tool header "model: gpt-5.6-terra"); output sha256 prefix 8ce05a865ea1eafd (the common rules' terra, not the contract's astra: common rules §4 wins)
- first pass (uv blocked by its sandbox, "Failed to initialize cache ... Access is denied"): /why, /preflight, /boot-session, skill verify DISAGREE as sandbox error, not a result; second pass ran the venv python directly
- rows re-run, verbatim:
- /why AGREE `purpose  : doit adapter for ecosystem/harness.yaml` (exit 0)
- /preflight AGREE `preflight_contract: 6/7 locator claim(s) resolved; 1 FAILED`
- /decide AGREE `usage: decide_checks [-h] [--repo-root REPO_ROOT] ...` (exit 0)
- plugin /review-closures AGREE `usage: review_closures [-h] {surface,plan} ...` (exit 0)
- validate_backlog.py (plugin copy) AGREE `diff` shows `### [S<n>] <User story>` vs `### <User story>`
- propose_closures BROKEN AGREE settings says "over the bypass bar", bar is >10% on >=20 runs; the 385/780 count is session hook output, not replayable from a repo file
- note: settings.json records 15% for propose_closures, my witness says 49%; both over the bar, the two figures differ

# USAGE

- Claude tokens: lane_cost not queried; one Sonnet 5.5 seat.
- agy calls: 0. DECIDED-BY-LANE: bulk reading -> targeted greps and `--help` (no document over a few KB was needed).
- Copilot substitutions: see CHECKER.
