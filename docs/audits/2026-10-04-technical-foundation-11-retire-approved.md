# Run record and removal ledger — foundation-11-retire-approved (R66)

- **Lane:** `LANE-FOUNDATION-foundation-11-retire-approved` (batch FOUNDATION night lane, `to-cc/AMEND-BATCH-FOUNDATION-5-2026-10-03.md` §"Lane 11")
- **Authority:** R66 §2 (`to-browser/RATIFICATION-2026-10-03.md`): the operator's deletion act for the approved rows, conditional on the dynamic-use check reading DEAD (`to-browser/DIGEST-B2-PREP-2026-10-03.md` Part 1, table `…-TABLE.md` §4). Reading rule N1: only a verdict that reads DEAD qualifies.
- **Base:** `origin/main` `31c791ae9e82eb499c0831631d552d916700882e` (merged at step 0; the sha every RED below was measured on)
- **Served model:** `claude-sonnet-5-5`

## The removal ledger (R56, N4)

One line per item, in the fixed form.

### Removed

```
REMOVED templates/handoff/01_ROLE.md.tmpl | verdict: DEAD (table §4 A2d) | evidence: "DEAD as files (no code opens them); prose and sibling-template references only" | sha 055bf91d
REMOVED templates/handoff/03_PROJECT.md.tmpl | verdict: DEAD (table §4 A2d) | evidence: same row; base re-check: no hit outside the template set, protocols/archive/HANDOFF_PROCESS_v4.4.md, check_handoff_bundle_structure.py:21 and test_audit.py:973 (the last two name BUNDLE files under docs/handoffs/*, not the template) | sha 055bf91d
REMOVED templates/handoff/04_RECENT.md.tmpl | verdict: DEAD (table §4 A2d) | evidence: same row; base re-check as above (check_handoff_bundle_structure.py:22,88-95 and test_audit.py:995 read the bundle file docs/handoffs/*/04_RECENT.md) | sha 055bf91d
REMOVED templates/handoff/05_NOW.md.tmpl | verdict: DEAD (table §4 A2d) | evidence: same row; base re-check: protocols/HANDOFF_PROCESS.md:628 and protocols/SESSION_SETUP.md:236 name `05_NOW` as an anti-pattern / "is gone", prose only | sha 055bf91d
REMOVED templates/handoff/06_QUESTIONS.md.tmpl | verdict: DEAD (table §4 A2d) | evidence: same row; base re-check as for 03 | sha 055bf91d
REMOVED templates/workspace-L.code-workspace | verdict: DEAD (table §4 A2e) | evidence: "DEAD (no executable reacher); doctrine mention only"; base re-check: literal `workspace-L` has 0 hits outside docs/audits and prose; only protocols/PLAYBOOK.md:1147 names the brace form `workspace-{S,M,L}` | sha 055bf91d
REMOVED templates/workspace-M.code-workspace | verdict: DEAD (table §4 A2f) | evidence: "DEAD (same as L)"; base re-check: literal `workspace-M` has 0 hits | sha 055bf91d
```

**Base re-check method (N1).** The table's literal-stem search, run on `31c791ae`:
`rg --hidden -uu -F -n` over the whole tree excluding `.git`, `.venv`, `.claude/worktrees`, `JOURNAL.md`, `LESSONS.md`, `docs/**`, `BACKLOG.md`, `logs/**`, `tasks/**`, `ecosystem/organ-index.md`, for each of `01_ROLE`, `03_PROJECT`, `04_RECENT`, `05_NOW`, `06_QUESTIONS`, `workspace-L`, `workspace-M`, `workspace-{S`, `workspace-S`; then the directory-level reachers (`templates/handoff` outside `v5|epic|functional|seats`, `\.tmpl`, `code-workspace`, `workspace-`, `glob(`/`rglob(` over `scripts tests deploy .github .claude plugins ecosystem config`).

- **Positive control:** `desired_state_loader` was still found, 20 hits in 12 files, including the real dynamic user `tests/test_membership_agreement.py:209` `dsl = _load("desired_state_loader")` (`_load` = `importlib.util.spec_from_file_location`). The method sees a string-argument dynamic load; so the zero code hits below are real.
- **No code, test, CI step, deploy manifest, parity row or hook opens any of the seven files.** The surviving hits are: the template set naming each other; `.claude/commands/handoff.md` prose; `protocols/archive/HANDOFF_PROCESS_v4.4.md` (immutable); bundle-file names in `check_handoff_bundle_structure.py` / `tests/test_audit.py`; prose in `protocols/`.
- **Directory-level reachers read only as generic scans** and tolerate the files being gone: `tests/test_residual_completeness.py:92` (`rglob("*.tmpl")` keeps FILL-IN carriers only; 41 tests pass), `ecosystem/fleet-shape-spec.yaml:253-254` (lists the directory and `templates/handoff/*`; `tests/test_fleet_shape_spec*.py` pass), `scripts/silent_rule_detector.py:137-138` (globs `templates/**/*.tmpl`; `tests/test_silent_rule_ratchet.py` passes). No deploy manifest carries `templates/handoff/*` (only `templates/child-methodology-floor.md.tmpl`).
- **No hit made any item UNKNOWN.**

### Kept (listed untouched; N1: not DEAD)

```
KEPT A1 propose_closures (plugin Stop hook) | verdict: ALIVE (plugins/tier1-lifecycle/hooks/hooks.json:10; enabled in 3 repos) | reason: not DEAD (N1)
KEPT A2a /save (.claude/commands/save.md) | verdict: ALIVE-TEST-ONLY plus declared surfaces | reason: not DEAD (N1)
KEPT A2b aj-scan (skill + scripts/aj_scan.py) | verdict: ALIVE (skill invokes the script), on demand | reason: not DEAD (N1)
KEPT A2c /handoff-verify | verdict: ALIVE (pinned by tests and declared surfaces) | reason: not DEAD (N1)
KEPT A5a offload_admission | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5b context_reclamation | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5c export_backlog_view | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5d carrier_landed_check | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5e platform_skip_ratchet | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5f ci_red_age | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5g hook_expiry_verdict | verdict: ALIVE-TEST-ONLY | reason: not DEAD (N1)
KEPT A5h cost_usage_telemetry | verdict: ALIVE (path-loaded by scripts/provider_router.py:100) | reason: not DEAD (N1)
KEPT A7 coherence-nudge | verdict: ALIVE in CI only (manual stage) | reason: not DEAD (N1)
KEPT B2 scripts/hooks/block_immutable_edits.py | verdict: ALIVE-TEST-ONLY plus declared surfaces; unwired | reason: not DEAD (N1)
KEPT B3 scripts/logs_retention.py | verdict: ALIVE-TEST-ONLY; unwired | reason: not DEAD (N1)
```

All paths above exist on the base and are unchanged by this lane. Out of this lane by its Do-not list: A3/A4 (lane 12), C1/C2, A6, A8, B1, and B1's prompts guard.

### ADR statuses (N3, R66 C3)

```
ADR-82 -> Accepted (unchanged; PREMISE-FAILED at render, confirmed: docs/decisions/ADR-82-handoff-process-v5-model-c.md:3 reads "Accepted (ratified 2026-08-04 ...)") | cited by: tasks/547 (open)
ADR-116 -> Explored, not adopted (withdrawn under R66, 2026-10-03: no open row cites it) | cited by: none | sha 35e06455
ADR-117 -> Proposed (kept) | cited by: 642, 650 (both status: open)
ADR-118 -> Proposed (kept) | cited by: 640, 664, 674, 755, 839, 963 (all status: open)
```

**How each was decided.** A case-insensitive search `adr[- _]?<n>\b` over `tasks/*.md` (open rows live directly under `tasks/`; `tasks/archive/` holds relieved bodies of rows that are still open and was searched by the same pattern: 0 hits for ADR-116, -117 and -118). `status: open` was read from each cited row's frontmatter. The render's list also named rows 640, 642, 650, 664, 674, 755, 839 and 963: all are open, and each cites ADR-117 or ADR-118 (none cites ADR-116). `tasks/manifest.json` carries one ADR-117 mention and none for 116 or 118.

**Withdrawal form.** The status enum (`scripts/validate_adr_status.py:114-122`) has no `Withdrawn`; the render's DECIDED-BY-AMEND-SESSION ruling takes `Explored, not adopted` with the reason on the status line. Only the status line and the README index entry changed (ADR-94); `validate_adr_status.py` reports no `enum` or `coherence` defect for ADR-116 and its warnings are the baseline's.

## RED first, then GREEN (Done-contract 3)

Outcome tests (existing files, no new test path: the contract creates no other paths): `tests/test_residual_completeness.py` (R66 block, 12 tests: absence per retired path, no dangling stem in the four referencing files, the `/handoff` command no longer claims the templates are retained live) and `tests/test_validate_adr_status.py` (R66 C3 block, 7 tests: citation scan not vacuous, ADR-116 status line, index row, validator clean, ADR-117/118 kept while cited, ADR-82 Accepted; the first was added after the review, `docs/audits/2026-10-04-codex-foundation-11-retire-approved.md`).

RED on `31c791ae` (commit `ed9180d0`, before any removal):

```
FAILED tests/test_residual_completeness.py::test_r66_retired_path_is_absent[...] x7 (every retired path)
FAILED tests/test_residual_completeness.py::test_r66_no_surviving_reference_to_a_retired_template[...] x4
FAILED tests/test_residual_completeness.py::test_r66_handoff_command_no_longer_claims_the_templates_are_retained_live
FAILED tests/test_validate_adr_status.py::test_r66_adr_116_index_row_carries_the_withdrawn_status
FAILED tests/test_validate_adr_status.py::test_r66_adr_116_is_withdrawn_because_no_open_row_cites_it
14 failed, 4 passed in 8.66s
```

(The 4 that pass on the base are the guards that stay true: validator clean for ADR-116, ADR-117 and -118 kept, ADR-82 Accepted. They are the "do not over-remove" side of the contract. The 19th test, the non-vacuous scan guard, was added after the review and has no RED run: it is a guard on the other tests, not an outcome.)

GREEN after the removal and the ADR-116 edit: `tests/test_residual_completeness.py` + `tests/test_validate_adr_status.py` = 248 passed.

## Dangling references (N2) and rows owed

- Fixed in this lane, citing R66: `templates/handoff/02_METHODOLOGY.md.tmpl` (2 lines), `07_ASK_BACK.md.tmpl` (3 lines), `README.md.tmpl` (paste sequence, drift note, contents table, plus a retirement comment), `.claude/commands/handoff.md` (`:170-177` and the twin block at `:318-322`, which also called the five templates "retained live"). The contract names `:170-177`; the twin block names the same files in the same file, so it is fixed too (DECIDED-BY-LANE).
- ROWS-OWED: PLAYBOOK still names the retired workspace templates — `protocols/PLAYBOOK.md:1147` ("`workspace-{S,M,L}.code-workspace`") and `:1150` copies `workspace-S`; `workspace-L` and `workspace-M` no longer exist. Not edited (N2: any commit to PLAYBOOK reds the canonical-docs freshness tripwire). Check: `rg -n "workspace-\{S,M,L\}" protocols/PLAYBOOK.md`.
- ROWS-OWED: PLAYBOOK also names the v4 bundle files as history at `:1237` and `:1398` (accurate as history; listed so the same re-read covers them).
- ROWS-OWED: a real home for a removal ledger. None existed (`grep -ri "removal ledger\|REMOVAL-LEDGER"` over the tree: 0 before this file); this run record is the ledger. Check: `rg -il "REMOVAL-LEDGER" .` returns a registry once one exists.
- Left stale on purpose: `ecosystem/conformance.md` / `.html` list ADR-116 as Proposed. They are generated, last regenerated 2026-09-05 (`HEAD c579e3e777fe`), commit-gated by nothing and not in this lane's ownership; `python scripts/gen_dashboard.py --write` refreshes them.
- Left stale for the integrator (common rules §0 (d)): `docs/audits/README.md`.

## Regenerated indexes (Done-contract 2)

Methodology roster, CLAUDE.md fragments and organ index were already current (the files this lane changed are not inputs of those generators except as shown); `ecosystem/doc-counts.md` was stale by exactly the tests added (`pytest_collected` 8851 -> 8869, then 8870 with the review-fix test) and was regenerated in `716a85b3` and `555f98cd`. Check outputs are in the session file.
