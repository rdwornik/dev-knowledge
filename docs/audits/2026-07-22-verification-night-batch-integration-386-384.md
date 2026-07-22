# Night-batch integration verification — #386 + #384 landed on main

Write-once verification record · ADR-101 class `verification` · durable home for the
2026-07-22 night-batch integration arc. Absorbs the two ephemeral working logs
(`logs/NIGHT-BATCH-2026-07-22.md`, `logs/CONTINUATION-2026-07-22.md`), which were removed
after this record was committed — nothing is lost. The only repo file mutated to produce
this record is the generated `docs/audits/README.md` index, regenerated in the same commit
(the `audit-index-freshness` gate requires it).

## 0. Outcome (as of the commit that lands this file)
Both lanes are **integrated and pushed** to `origin/main`. The night-batch's single blocker
(a #384 doc-counts drift) was resolved in a follow-up execution session and the integration
completed.

- **`origin/main` @ `a6b326f1`** carries: #386 (delivery-loop codification) + #384 (L5a
  analytics reporter) + the doc-counts fix.
- #386 and #384 both remain **OPEN** by design (see §5) — integrated ≠ closed.

## 1. What each lane is
- **#386** — codifies the proven delivery loop into PLAYBOOK: new `§21` "The delivery loop
  (end-to-end)" spine + four in-place substances (Ch8 unfiltered live-session check, Ch4/§2
  TARGET-REPO guard, §4 prove-then-codify, §8 discharge-with-evidence) + ride-along tickets
  [#389]/[#390]. Docs-only. Pre-merge terra had already fixed 7 HIGH.
- **#384** — `scripts/fleet_analytics.py` (1268-line read-only descriptive fleet reporter:
  hotspots / change-coupling / rot frames via `git log --numstat` + pandas; PyDriller
  deliberately absent, D1/D2 deviations) + `tests/test_fleet_analytics.py` (+64 tests) +
  `pyproject.toml` analytics group + `.gitignore` `logs/FLEET-ANALYTICS.md`.

## 2. Per-phase verdicts + evidence (the night batch)
| Phase | Verdict | Evidence |
|---|---|---|
| Baseline (bare main `2da5da22`) | — | ship-gate undispositioned WARN = {VISION.md [#368] freshness} only. pytest 1666/3. |
| P1 — integrate #386 | **PASS** | `git merge --no-ff docs/playbook-delivery-loop` → **`db878f4c`**. Net-new WARNs 0. pytest 1666/3. |
| P2 — integrate #384 | **STOPPED (then resolved)** | `git merge --no-ff worktree-l5a-analytics` → **`09c50cc0`**. JOURNAL conflict = clean both-added prepend union, resolved newest-first. pytest 1730/3 (+64), reporter clean. BLOCKED by a net-new ship-gate WARN (§3). |
| P3 — push+teardown (night) | did not fire | mission gated push on "both green"; #384 not green. |
| P4 — verification sweep | **PASS (read-only)** | health OK; `ALL_CHECKS`=31 unchanged; `fleet_analytics` correctly NOT a registered check; terra found no integration regression (§4). |
| P5 — continuation pack | written | (this record supersedes it). |
| Resolution (follow-up session) | **LANDED + PUSHED** | fix branch → **`c8de7212`** → merge **`a6b326f1`** → `git push` `2da5da22..a6b326f1` (block-ff-push passed). |

## 3. The blocker and its resolution
- **Blocker:** #384 added 64 tests (collected 1669→1733) but never regenerated
  `ecosystem/doc-counts.md` (line 16: "tests: **1669 collected**"). Surfaced as ship-gate
  `doc_claims: pytest_collected 1669 != 1733`. Confirmed: #384's merge touched 0 lines of
  doc-counts.md. This was the SOLE net-new WARN attributable to the lane (VISION [#368]
  freshness is the pre-existing/expected one).
- **Resolution (deterministic):** `python scripts/gen_doc_counts.py --write` (1669→1733) on
  `fix/doc-counts-384` off `09c50cc0`, `--no-ff` merged. Only the tests line changed (audit
  31 / gates 15 intact). Post-fix: ship-gate net-new WARN 0 (VISION-only), pytest 1730/3,
  ruff clean, health OK.
- **Lesson (for a future test-adding lane):** regenerate `ecosystem/doc-counts.md`
  (`gen_doc_counts.py --write`) IN the lane's own branch. The `doc_claims` count only
  surfaces at integration on merged main, so a commit-and-STOP lane cannot see it pre-merge.

## 4. terra integration review (both lanes, `gpt-5.6-terra`, files named; diff `2da5da22..09c50cc0`)
**No pure integration regression.** Positive confirmations: #386's §21 anchors resolve
(incl. the external ai-council merge `88b0876`); #384's `GIT_*` env-scrub correctly inherits
`audit._git_location_env()` (the GIT_DIR-override hazard is handled); the reporter's only
write target is the gitignored `logs/FLEET-ANALYTICS.md`. Two **ticket-to-file** findings
(filed — see §5):
- **[HIGH]** #384 BACKLOG says "Runs as a nightly lane" but no hook/Routine invokes
  `fleet_analytics.py` — a manual CLI only.
- **[MEDIUM]** `fleet_analytics.py:326` rename-alias loses history on path-reuse (`a→b→a`);
  the global `old→new` alias map can't represent it → undercounts revisions/coupling/edit-age.

## 5. Reporter run + rot-ticket raw material (#384 done-when material)
First live run over 6 repos, 4668 commits (365d): top hotspot `JOURNAL.md` (0.9828), 61
coupled pairs, `parse_anomalies: 0`, state.yaml exclude fired, hub present.
- **corp-sca-time-automation — 3 rot candidates** (stale files still pointed at; oldest edit
  204d > 180d threshold): `config/category_mapping.yaml` (204d, inbound 3, 0.6667);
  `requirements.txt` (199d, inbound 5, 0.3333); `config/excluded.yaml` (203d, inbound 2,
  0.2222). Review queue, NOT a verdict — staleness ≠ rot.
- **corp-monorepo — measurement blind spot:** 311/812 tracked files (38%) have NO
  meaningful-edit record (only ever touched in a wide commit, or <3-line churn) → invisible
  to the rot frame. A coverage gap, not rot.

## 6. Ticket-status cross-check (vs git first-parent spine)
No BACKLOG-vs-git disagreement. #386 and #384 intentionally OPEN (witness / rot-tickets
pending). [E9] S23–S27 / #381–#385 all LIVE + gated; the standing brake holds (no new fleet
machinery before #381 rules).

## 7. Follow-ups filed this session
See BACKLOG under existing stories (filing-only, zero build): the terra [HIGH]/[MEDIUM], the
corp-sca rot review, the corp-monorepo coverage-gap, the `logs/` naming-convention defect,
the `scripts/gitenv.py` extraction, and the `docs/intake/README.md` stale index. Ids in the
session JOURNAL entry.
