# B2 lane 4 — hook role review: 39 classified, 13 re-armed at the commit layer

> BUILD MODE batch B2, lane 4. Scope: `.pre-commit-config.yaml`, `.claude/settings.json`,
> `plugins/tier1-lifecycle/hooks/hooks.json`. Part B method:
> `uv run --locked pre-commit run <id> --hook-stage manual --all-files` (commit-msg trio via
> `--hook-stage commit-msg --commit-msg-filename <scratch>`), timed on the tree as found, no
> fixes applied to hook targets. 15s bar. Push/CI hooks untouched.

## Part A — every hook in the register

Columns: (a) condition guarded · (b) DET(erministic)/JUDGEMENT · (c) layer · (d) REFUSAL or
AFFORDANCE-mis-built · (e) counter+expiry today (before this lane).

| id | (a) condition | (b) | (c) | (d) | (e) |
|---|---|---|---|---|---|
| block-commit-on-main | no direct non-merge commit lands on `main` | DET | commit | REFUSAL | no |
| normalize-dated-headers | dated-log headers rewritten to canonical `###` form | DET | commit | AFFORDANCE (auto-rewrites, never refuses) | no |
| codemap-freshness | ARCHITECTURE.md codemap matches `scripts/` | DET | commit | REFUSAL | no |
| toc-freshness-playbook | PLAYBOOK.md TOC matches its headings | DET | commit | REFUSAL | no |
| roster-freshness | `.claude/methodology-roster.md` matches the manifest | DET | commit | REFUSAL | no |
| claude-rosters-freshness | the two `@`-imported CLAUDE.md fragments match disk | DET | commit | REFUSAL | no |
| doc-counts-pytest-freshness | `doc-counts.md`'s test-count claim matches `pytest --collect-only` | DET | commit | REFUSAL | no |
| audit-index-freshness | `docs/audits/README.md` matches the generator | DET | commit | REFUSAL | no (pre-existing) |
| audit-title-gate | every indexed audit (20-file baseline) carries a `#` heading | DET | commit | REFUSAL | no |
| organ-index-freshness | `ecosystem/organ-index.md` matches its sources | DET | commit | REFUSAL | no (pre-existing) |
| quality-requirements-freshness | schema + organ resolution + ARCHITECTURE section agree | DET | commit | REFUSAL | no |
| validate-hermetization | staged ADDs obey ADR-101's seal + audit-name grammar | DET | commit | REFUSAL | no |
| intake-index-freshness | intake README Contents block matches the generator | DET | commit | REFUSAL | no |
| check-seal-identity | a staged handoff bundle's slug matches its own dir name | DET | commit | REFUSAL | no |
| validate-backlog | `BACKLOG.md`/`tasks/` obey the ADR-66 schema | DET | commit | REFUSAL | no |
| row-archive-proof | archived row bodies stay byte-identical, legs A-E | DET | commit | REFUSAL | no |
| prepend-order | LESSONS/JOURNAL/TOKEN-LOG stay append-only / newest-first | DET | commit | REFUSAL | no |
| provider-registry-agreement | every checked site agrees with the provider registry | DET | commit | REFUSAL | no |
| lane-contract-check | a generator-emitted `LANE-*.md` has its sections + tier agreement | DET | commit | REFUSAL | no |
| derived-copies-rebind | a staged source's derived copy moved with it; every delegated hook exists | DET | commit | REFUSAL | no |
| graph-rebuild | the persisted FPG-1 store is written and readable | DET | commit | AFFORDANCE (refuses only on its own write/read failure) | no |
| graph-orphan-census | no process node is unreachable-and-undispositioned | DET | commit | REFUSAL | no |
| graph-task-coverage | every staged file has an `implements` edge from an OPEN row | DET | commit | REFUSAL | no |
| graph-process-list | ARCHITECTURE.md names no process the graph lacks | DET | commit | REFUSAL | no |
| impacted-tests-guard | a changed `scripts/*.py` selects >=1 test | DET | commit | REFUSAL | no |
| graph-edge-class-census | no module newly computes a five-kind edge outside the register | DET | commit | REFUSAL | no |
| decision-coverage | every in-era decision has a row or a disposition | DET | commit | REFUSAL | no |
| dispatch-conformance | the generator and the ruled `dispatch` verb agree on fence/location/model | DET | commit | REFUSAL | no |
| audit-health | `audit.py health`'s FAIL-tier findings are clear | DET | commit | REFUSAL | no |
| coherence-nudge | a registered spec changed without a version bump | DET | commit | AFFORDANCE (always exits 0; a nudge) | no |
| backlog-id-on-close | a commit removing a task line carries `[#id]` | DET | commit-msg | REFUSAL | no |
| backlog-filing-backpressure | a commit adding a task id carries `kill-candidates:` | DET | commit-msg | REFUSAL | no |
| commit-message-type-prefix | the message carries a `type`/`type(scope)` prefix | DET | commit-msg | REFUSAL | no |
| ruff | staged Python obeys the pinned lint ruleset | DET | commit | REFUSAL | no |
| block-ff-push | no non-merge commit lands on main's spine via push | DET | push | REFUSAL | no (pre-existing) |
| block-unanchored-push | pushed range carries >=1 JOURNAL-anchor SHA | DET | push | REFUSAL | no (pre-existing) |
| arm_hooks.py (SessionStart) | this checkout's git hooks are pre-commit-installed | DET | agent-loop (session) | AFFORDANCE (self-arm; always exits 0) | n/a |
| session_end_backpressure.py (Stop) | JOURNAL/BACKLOG/dirty-tree/freshness, at turn-Stop | DET | agent-loop (session) | AFFORDANCE since ADR-85 (advisory only; hard block retired 2026-08-03) | n/a |
| deny_and_point.py (PreToolUse) | a raw Bash/PowerShell/Grep search resolves to a process FPG-1 already holds | DET | agent-loop (tool-call) | **AFFORDANCE MIS-BUILT AS REFUSAL** — class (d) below | no |
| propose_closures.py (plugin Stop) | proposes Tier-1 closures for the session | DET | agent-loop (session) | AFFORDANCE (non-blocking; always exits 0) | n/a |

39 hooks reviewed (35 pre-commit-config + 4 session/plugin). **Column (b) is uniform: every
hook is DETERMINISTIC.** No LLM-judgment hook exists in either register — the "JUDGEMENT
hooks are wrong by construction" branch has no live instance. `deny_and_point.py` plays that
role instead: a deterministic PREDICATE encoding a *judgment call* ("is this a governed
question") that is often wrong in practice — the wrongness is in shape (d), not (b).

## Class (d) — affordance mis-built as refusal (the SKILL candidate)

**`scripts/hooks/deny_and_point.py`**, wired as `.claude/settings.json` `PreToolUse` on
`Bash|PowerShell|Grep`. **Live-witnessed mid-lane**: it refused this lane's own
`find plugins/tier1-lifecycle -iname propose_closures.py` as "a raw search over a GOVERNED
question ... Run the organ instead" — exactly the over-block risk its own docstring names as
"a known and expensive failure mode." Per BUILD-MODE.md rule 8 ("Refusals ONLY at git
boundaries ... inside the agent loop, nothing but path protection ... A PreToolUse hook hung a
session for twelve hours; a pre-commit hook cannot") this is now **UNWIRED** from
`.claude/settings.json` (script kept on disk). The right shape is an organ call SHORTER than
the raw search, offered proactively — a SKILL at prompt-time, not a tool-call gate that
misfires and teaches avoidance of the tool it gates. No other hook here matches this shape:
every other REFUSAL blocks on a real, narrowly-computed defect, not a guess about intent.
`graph-rebuild`/`normalize-dated-headers` are AFFORDANCEs but not mis-built: one refuses only
on its own write/read failure, the other never denies.

## Part B — commit layer, armed this lane

**Method note:** bare `uv run --locked python -c "print(1)"` measures ~2.5s here; the 10-20s
figures below are `pre-commit run`'s own overhead (env resolution + full-tree diffing), paid
once per hook *however invoked* — including at a real `git commit`, where each hook's
`entry:` is its own `uv run --locked` subprocess. So the 15s bar is real commit-time cost, not
a proxy. Live-verified from `logs/TELEMETRY.db`: `codemap-freshness` runs in **592ms**;
`row-archive-proof` in **1250ms** — armed, then re-run dozens of times during verification.

**Counter + expiry.** `scripts/telemetry_emit.py` (extended, not a new file) gained a `wrap`
CLI: `... wrap <hook-id> -- <python-args...>` runs the check via `sys.executable` (no nested
`uv run --locked`), times it, records one `hook_run(hook_id, pass|block, duration_ms)` row to
the existing gitignored `logs/TELEMETRY.db` ([#529]'s store; already wired in-process into
`audit.py`/`block_ff_push.py`/`block_unanchored_push.py`/`block_commit_on_main.py` — this
lane adds the first CLI entry-point, for an arbitrary hook `entry:`'s subprocess).
`pass_filenames: true` hooks are unaffected. Verified live: two real runs, two real rows.
**Expiry 2026-09-25** (one week), per-hook in `.pre-commit-config.yaml`: **zero `block` rows
in the window -> REMOVE at expiry, do not tune** — BUILD-MODE.md's own rule for itself.

### ARMED (13; clean + <=15s; `stages: [manual]` removed / -> `[commit-msg]`)

| id | stage | measured |
|---|---|---|
| codemap-freshness | pre-commit | 14.3s |
| roster-freshness | pre-commit | 13.6s |
| claude-rosters-freshness | pre-commit | 11.9s |
| quality-requirements-freshness | pre-commit | 9.7s |
| validate-hermetization | pre-commit | 10.7s |
| intake-index-freshness | pre-commit | 12.8s |
| row-archive-proof | pre-commit | 12.9s |
| provider-registry-agreement | pre-commit | 14.0s |
| impacted-tests-guard | pre-commit | 12.0s |
| dispatch-conformance | pre-commit | 11.6s |
| backlog-id-on-close | commit-msg | 11.2s |
| backlog-filing-backpressure | commit-msg | 12.1s |
| commit-message-type-prefix | commit-msg | 13.7s |

The commit-msg trio was measured against a synthetic non-triggering message
(`docs(test): ... kill-candidates: none`) — real, but it does not exercise their block path.

### NOT armed — BROKEN on this tree (fails today; arming would wedge every commit)

- `doc-counts-pytest-freshness` — stale claim (6497 vs actual 6503); also exceeds the 40s cap.
- `check-seal-identity` — real pre-existing bundle defect (`...architect-2` slug/dir mismatch).
- `validate-backlog` — 3 hard fails ([#664] in-place resolved task, [#906] grammar x2).
- `lane-contract-check` — 5 legacy `LANE-*.md` files predate the `**Kind:**` requirement.
- `graph-rebuild` — exits 1 here (also 32.2s); blocks the whole graph-* chain regardless.
- `decision-coverage` — times out past 40s.
- `audit-health` — `health: DEGRADED` (skip-guarded proof-layer findings); also 32.1s.

### NOT armed — clean but SLOW (>15s; overhead, not the check)

`block-commit-on-main` 18.1s · `normalize-dated-headers` 31.0s · `toc-freshness-playbook`
16.4s · `audit-title-gate` 15.4s · `prepend-order` 15.6s · `graph-orphan-census` 16.9s ·
`graph-task-coverage` 15.9s · `graph-process-list` 35.9s · `graph-edge-class-census` 15.8s.

### NOT armed — structural / by design

- `ruff` — clean, 11.7s, but a `language: python` pre-commit-MANAGED venv isolated from this
  repo's `uv` env; `wrap` can't import `scripts/telemetry_emit.py` from inside it without
  converting the hook to `language: system` — out of scope. Follow-up lane.
- `coherence-nudge` — always exits 0 by design; fails "genuine REFUSAL". Left as-is.
- `derived-copies-rebind` — FAILS today: 2 of 3 delegates now armed, but
  `toc-freshness-playbook` (clean, 16.4s, excluded by the bar) is not.

### Pre-existing armed state, unchanged (flagged, not touched)

`audit-index-freshness`, `organ-index-freshness` (pre-commit), `block-ff-push`,
`block-unanchored-push` (pre-push): active before this lane, no counter/expiry — the same
rule-7 gap this lane closes for its own 13. Out of scope (push/CI untouched).

## Agent tool-loop — now EMPTY except path protection

`PreToolUse` `deny_and_point.py` UNWIRED from `.claude/settings.json` (script kept; class (d)
above). `SessionStart` `arm_hooks.py` and `Stop` `session_end_backpressure.py` / plugin
`propose_closures.py` remain: none DENIES a tool call — the first two always exit 0, and
`session_end_backpressure.py` is advisory-only (`additionalContext`, never `decision:block`)
since ADR-85. Session lifecycle hooks, not tool-call refusals — the one hook that denied a
call is gone, which is rule 8's bar.
