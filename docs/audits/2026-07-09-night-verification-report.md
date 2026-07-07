# Night verification report — 2026-07-08/09

<!-- scope: meta -->

- **Model in effect:** Opus 4.8 (`claude-opus-4-8[1m]`), effort HIGH — named per ADR-80 §5 (silent-swap class). No mid-mission model swap observed.
- **Run window:** night of 2026-07-08 (grooming-apply arc + this verification audit, single continuous CC session).
- **HEAD audited:** `cb18ef2` (Merge feat/grooming-apply — leg-c grooming full ruling pass 124→74), branch `audit/2026-07-09-night-verification` off `main`.
- **Method:** adversarial re-verification from live disk/git — session reports were NOT trusted; every claim was re-run.

## Verdict

**Repo is GREEN and next-session-ready. No P0.** Two P1 findings (one a false-premise closure with live data-loss risk; one a confirmed latent parser bug), four P2 notes. The grooming-apply arc reconciles EXACTLY to its frozen ruling (independently verified — 74 tasks, 0 deviations).

---

## Phase 0 — ground truth

First-parent spine since `68c4705` (matches the day's reports, no deviation):

```
cb18ef2  Merge feat/grooming-apply -- leg-c grooming full ruling pass (124->74)   <- this audit's base
bfe2b12  Merge chore/doc-counts-union -- pytest_collected 1422->1424
32db7eb  Merge feat/wave1-prep -- onboarding runbook + v1.3.x contract + 3-stage floor arm [#131][#215][#275]
7f4b566  Merge feat/cadence-teeth -- filing-backpressure + intake-WARN + overdue-groom escalation
4f4948e  Merge docs/2026-07-08-global-infra-incident -- demo-prep incident + hub ratify-or-revert ruling
7aa24f5  Merge fix/265-worktree-registry-keying -- deployed_methodology_version by repo root [#265]
```

Tree clean at audit start.

## Phase 1 — gate battery (deterministic)

| Gate | Result |
|---|---|
| pytest (`-n auto`) | **1422 passed / 2 skipped** (2:16); = 1424 collected, matches `doc-counts.md` |
| ruff | All checks passed |
| `audit.py ship-gate` | **GREEN**, 11 WARN dispositioned, **0 stale** |
| validate_backlog | OK (7 themes / 20 stories / **74 tasks** / 0 warn) |
| validate_git_backlog | OK — no closed-but-present drift |
| validate_doc_claims | match (14 pre-commit hooks; pytest_collected 1424; roster) |
| validate_doc_rot | only BACKLOG#262 + #278 (both dispositioned; reasons refreshed to the leg-c outcome) |
| verify_handoff_probes (latest bundle) | 10 pass / 0 fail / 0 warn |
| roster / claude-rosters / audit-index `--check` | all clean (fresh) |

No non-GREEN gate.

## Phase 2 — heterogeneous code review (Codex 0.141.0, read-only, high effort)

Reviewed the day's code diff `68c4705..HEAD` (481 insertions across `check_backlog_filing.py`, `fleet_health.py`, `audit.py` #265, `carrier_floor.py`, tests). Codex findings **verbatim** + my triage:

1. **HIGH** `deploy/carrier_floor.py:218/275/360` — a stale one-stage `settings.json` still passes detect/verify and `_ensure_settings()` no-ops (only checks for `check_floor_hash.py`), so existing consumers are not upgraded to 3-stage arming.
   - **Triage: AGREE — already TRACKED by #290** (the `#275b` residual I filed today; the wave1-prep contract deferred this deliberately — a DRIFTED verdict without the self-heal reports drift `apply` can't repair, and no consumer deploys from that lane). Strong cross-vendor confirmation of a known, filed gap. No new action.
2. **MED** `scripts/fleet_health.py` groom parser counts a `Next quarterly:` date as a completed groom once that date is in the past, masking overdue-groom escalation after a missed target.
   - **Triage: AGREE — CONFIRMED real (latent).** `validate_doc_rot._latest_groom_date` with a past `Next quarterly: 2026-07-01` returns `2026-07-01`, not the actual groom date. Not currently active (today's footer has a *future* 2026-10-08). → **P1 finding F2.**
3. **MED** `check_backlog_filing.py:35` — `kill-candidates:` accepts bare `none` and any `#id`, so the gate can be satisfied without a real reason or an existing candidate.
   - **Triage: PARTIAL — lenient by design.** The hook is a proposals-only *nudge*, not a validator (its docstring: "never removes or closes anything"). Optional low-value hardening. → P2 F3.
4. **LOW** `check_backlog_filing.py:41/76` — any occurrence of "intake" suppresses the L-epic WARN, so "needs intake" would falsely pass.
   - **Triage: AGREE — LOW**, advisory-only (WARN never blocks). Optional tightening to `intake-id`/`SEED-N`. → P2 F4.

## Phase 3 — functional re-proof (live state, sandboxed + reverted)

| # | Mechanism | Evidence | Verdict |
|---|---|---|---|
| 3.1 | Filing-backpressure | scratch branch: `#999` add w/o `kill-candidates` → **BLOCKED**; with line → **PASSED**; full reset, 0 residue | **PROVEN** |
| 3.2 | Groom-escalation | live digest: no overdue line (footer reset); parser newest = 2026-07-08 (future 2026-10-08 excluded); positive fires on injected-stale | **PROVEN** (+ Codex #2 confirmed) |
| 3.3 | #265 worktree keying | from worktree `wt-265`: `deployed_methodology_version` = `[--] .dev-knowledge: unset` (repo-root keyed, NOT the worktree dirname); teardown clean | **PROVEN** |
| 3.4 | #275b 3-stage arm | sandbox: deleted pre-commit/commit-msg/pre-push, ran carrier arm cmd (`carrier_floor.py:109`) → all three returned; sandbox removed | **PROVEN** |
| 3.5 | OneDrive guard v3 | direct-guard matrix, **15/15** cases matched: T0 enum→allow (4), T1 content→block (3), T2 write/delete/Edit/Write/NotebookEdit→block (4), unknown-head→block, redirection→block, non-zone→allow (2) | **PROVEN** |
| 3.6 | Runbook conformance cmds (#215) | `audit.py health` OK · `audit.py repo` writes report · `fleet_health` runs · `floor_conformance` 18 passed · `enforcement_coverage --fire --run-date` runs | **PROVEN-WITH-NOTES** (F5) |
| 3.7 | Grooming-apply reconciliation | independent subagent: **RECONCILIATION CLEAN** — 74 tasks, all 8 checks pass, 0 deviations (every KILL absent, every MERGE absorbed w/ target note, every DEFER pegged, all 9 CLOSE `closes [#id]`-referenced, both filings w/ kill-candidates) | **PROVEN** |
| 3.8 | Cross-repo spot checks | fleet arm-check **PASS** (8 repos; corp-monorepo 3/3 via importable venv python); **corp-ops remote FAIL**; **corp-sca push FAIL** | **FAILED-REPROOF** → F1 |

## Findings (tiered)

### P0 — blocks next session
**None.**

### P1 — fix-soon (real risk)

**F1 — #284 was CLOSED on an unverified premise; the data-loss risk it targeted PERSISTS.**
The leg-c ruling closed #284 with reason "corp-ops remote added + corp-sca branch pushed (2026-07-08)". Live state contradicts both:
- `git -C corp-ops remote -v` → **empty** (no remote configured).
- `git -C corp-sca-time-automation branch -vv` → `feature/tenrox-loader 3661b3a` has **no upstream / unpushed** (only `main` tracks origin).

The backup posture #284 was meant to establish does not exist; both repos remain single-disk with unpushed work. The grooming arc faithfully applied the ruling — the *ruling's factual premise* was wrong (exactly what "trust no report" is for). Child-repo + operator-decision scope (ADR-41; #284 was PENDING-OPERATOR), so **proposal only**, no fix applied.
*Proposed ready-to-file task (do not auto-file):* `[P2][S] Backup posture — corp-ops has no git remote and corp-sca feature/tenrox-loader is unpushed (the #284 closure premise is false on live state 2026-07-09). Operator: add a corp-ops remote (or accept local-only) AND push corp-sca's feature branch (or accept). · Done when: corp-ops has a tracking remote and corp-sca's branch has an upstream, or both are recorded accept-local · refs #284, docs/audits/2026-07-08-fleet-consistency-census.md`

**F2 — groom-date parser mis-counts a past `Next quarterly:` date as a completed groom (Codex #2, confirmed).**
`validate_doc_rot._latest_groom_date` (mirrored by `fleet_health.groom_escalation_line`) parses ALL dates in the grooming-log line and takes the max ≤ today — including the `Next quarterly:` target once it passes. So a missed quarterly target silently resets the overdue clock. Latent today (footer has a future 2026-10-08); becomes active the moment a `Next quarterly` date passes without a groom.
*Proposed ready-to-file task:* `[P3][S] Harden the groom-date parser — exclude the "Next quarterly:" target date from the newest-groom computation (parse only the "Recent:" segment), so a missed quarterly target does not falsely reset the overdue-groom escalation clock; add a regression test (past Next-quarterly must not count). · Done when: _latest_groom_date ignores the Next-quarterly date, with a test · refs scripts/validate_doc_rot.py, scripts/fleet_health.py, #134`

### P2 — notes / optional hardening
- **F3 (Codex #3):** `kill-candidates:` accepts bare `none`/any `#id` — lenient by design (proposals-only nudge). Optional: require `none -- <reason>` or an existing id. Low value.
- **F4 (Codex #4):** any `intake` substring satisfies the L-epic advisory citation. Optional: tighten to `intake-id`/`#N`/`SEED-N`. Advisory-only.
- **F5:** `check_floor_hash.py --require-present` is **consumer-scoped** — no static hub source (carrier-generated at consumer install); the hub has no installed floor (`floor_integrity [--] skip`). The #215 runbook conformance-verify list should mark hub-runnable vs consumer-only commands, and note `enforcement_coverage --fire` requires `--run-date`.
- **F6:** `~/.claude/hooks/` now holds **3** `block-onedrive.SUPERSEDED*.ps1` backups (`allowlist-v1`, `emptygrant-v2` (2026-07-08), plain) — the grooming brief expected 2. All retained per the no-delete invariant; revisit at #289's build arc.
- **F7 (process, observed during grooming):** across 14 sequential commits the pre-commit **stash/restore cycle silently dropped an unstaged JOURNAL edit** (the held #265 entry) on the final commit; recovered byte-exact from `~/.cache/pre-commit/patch*`. Risk pattern: carrying an unstaged file across many hook-running commits. Mitigation used: explicit per-commit `git add`, and staging the file fully before its own commit. (Also observed: an unrelated uncommitted `~/.claude/settings.json` — #189 territory, left untouched.)

## Day scorecard (plan vs achieved, 2026-07-08)

| Planned | Achieved | Evidence |
|---|---|---|
| leg-c grooming 124/124 ruled | **DONE** 124→74, applied exactly | 3.7 CLEAN |
| cadence mechanism live | **DONE** filing-backpressure + groom-escalation | 3.1/3.2 PROVEN |
| Wave-1 prep (runbook + v1.3.x + #275b) | **DONE** | 3.4/3.6 PROVEN |
| guard v3 (three-tier) | **DONE** | 3.5 15/15 |
| incidents closed (#265, demo-prep) | **DONE** | 3.3 PROVEN; spine 4f4948e |
| SEED 6–9 triage | **deferred** (next architect session) | handoff cut in Phase 5 |
| #164 handoff generator built | **not built** (re-scoped M, remaining scope filed) | BACKLOG #164 |
| a repo onboarded (Wave-1) | **not yet** (runbook ready; ai-council first) | #131/#215 |

Honest gaps carried, no overclaim.
