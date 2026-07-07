# Deletion-candidates sweep — 2026-07-08/09

<!-- scope: meta -->

- **Model in effect:** Opus 4.8 (`claude-opus-4-8[1m]`), effort HIGH.
- **Run window:** night of 2026-07-08 (third arc of the session, after grooming-apply + night-verification).
- **Scan scope:** the hub `.dev-knowledge` (branches, `scripts/`+`deploy/` code, `docs/`+`templates/`+`protocols/`, buildup, config) + read-only across 8 fleet repos under `Dev/`. **The `OneDrive - Blue Yonder` zone was excluded from every walk (P0).** `docs/audits/` · `docs/decisions/` · `docs/handoffs/` excluded from doc candidacy (KEEP-ALL by doctrine). **Nothing was deleted, renamed, or modified — propose only.**

## Headline

**Very little to reclaim — the corpus is already lean.** No dead code, no true orphan docs, no large buildup (the 703.87 MB `temp/` was already relocated by #229 — verified empty). The only clean-confidence action is **3 merged-and-undeleted git branches**. The most important thing this sweep surfaces is **not a deletion — it's a backup gap**: three repos have unbacked work on a single disk (corroborates night-audit F1 and adds demo-prep).

---

## RATIFICATION QUEUE (highest-confidence first)

Answer e.g. "1 yes; 2 back-up; 3 no" and the architect converts it to one arc. Commands shown are **NOT executed**.

1. **[LOW] Delete 3 merged-and-undeleted branches** (fully merged into main, 0 ahead — deletion loses nothing):
   - hub: `git -C .dev-knowledge branch -d docs/2026-07-08-architect-handoff worktree-cadence-teeth`
   - demo-prep: `git -C demo-prep branch -d feat/master-deck-audit`
2. **[HIGH-risk, NOT a delete — BACK UP] Three repos have unbacked work on one disk:**
   - `corp-ops` — **no git remote at all** (entire history local-only).
   - `corp-sca-time-automation` — `feature/tenrox-loader` 6 commits ahead, no upstream, never pushed.
   - `demo-prep` — `origin` configured but **nothing ever pushed** (`branch -r` empty); `main` + `fix/audit-needs-input` offsite-unbacked.
   → **TRACKED (partly):** corp-ops + corp-sca are night-audit **F1** (the #284 closure premise is false on live state). **demo-prep is NEW** (not in #284). Operator decision + child-repo scope (ADR-41). Proposed task line at the end.
3. **[MED, verify-then-delete] `origin/automation/conformance-digest`** — dormant since **2026-06-25** (~13 days), remote-only, no local counterpart. **TRACKED by #255** (verify the writer is retired + name its successor organ, THEN delete). Do not blind-delete.
4. **[LOW, push-not-delete] `automation/fleet-audit`** — local branch, recent (2026-07-08), 75 baselines, but **NOT on origin** (`origin/automation/fleet-audit` absent). **TRACKED by #254** (ruled KEEP; its Done-when "origin exists and tracks" is unmet → push for durability). Do not delete.
5. **[UNKNOWN, human decision — do NOT delete] 3 zero-code-referrer modules** — each a runnable CLI / canonical-twin kept by design; the #218 M1 code-ref oracle cannot clear them:
   - `scripts/probe_child_backlogs.py` (DORMANT-by-design, keep-with-reason — 2026-06-26 audit §6)
   - `scripts/review_closures.py` (hub canonical-source twin of the plugin's live copy; hub command deleted #76)
   - `deploy/release_lint.py` (manual lint CLI, live-by-design per #244)
6. **[GATED — do NOT act] v4 numbered handoff templates** (`templates/handoff/0*.md.tmpl` + `README.md.tmpl`, 8 files) — superseded by the v5 generator, BUT **TRACKED/GATED by #164**: its BACKLOG text carries the explicit *ADR-83 LIVE constraint — "the v4 templates stay LIVE for corp's cross-repo path; re-archival gated to #164's close (v5 cross-repo lands + corp migrates off v4)."* Not a free deletion; archive rides #164. (Coherence note: `HANDOFF_PROCESS.md` L245 asserts these are "LIVE" — reconcile that prose when #164 archives them.)
7. **[operator periodic review — out of sweep remit] `docs/archive/` triage-queue** (9 files) — per that folder's own README rule, items past a 2nd review default to deletion; several never got a 2nd pass since "first review 2026-05-28". A scheduled archive-review call, not a night sweep.

**Total reclaim if 1 is ratified:** 3 branches (negligible disk). No file deletions proposed. The session already reclaimed **703.87 MB** via #229 (temp/ relocated, verified empty).

---

## Per-leg detail

### Leg 1+2 — git branches (hub + fleet, 8 repos)

**Safe-delete (merged-and-undeleted, 0 ahead of main):**

```
.dev-knowledge  docs/2026-07-08-architect-handoff   merged, 0 ahead / 39 behind
.dev-knowledge  worktree-cadence-teeth              merged, 0 ahead / 38 behind
demo-prep       feat/master-deck-audit              merged, 0 ahead / 1 behind
```

**Risk-bearing (no-remote / unpushed — back up, do NOT delete):** corp-ops (no remote), corp-sca `feature/tenrox-loader` (6 ahead, unpushed), demo-prep (origin set, nothing pushed).

**Keep / surface-only:** `automation/fleet-audit` (local-only, #254 push-for-durability), `origin/automation/conformance-digest` (dormant 2026-06-25, #255 verify-then-delete), `demo-prep/fix/audit-needs-input` (unmerged but recent + worktree-bound). ai-council / corp-monorepo / life-architect / terminal-setup all single-branch, tracked, clean. **No leftover worktrees or `.dev-knowledge-*` orphan dirs anywhere.**

### Leg 3 — dead code (hub `scripts/` + `deploy/`)

**0 clear candidates.** Enumerated 62 modules; every one has ≥1 code importer OR a hook/CLI/generator entry-point. **3 UNKNOWN** (0 code referrers, prose/config-only — per the #218 boundary the oracle cannot clear them): `probe_child_backlogs.py`, `review_closures.py`, `release_lint.py` (all keep-by-design, item 5 above). A `scripts/safe_remove.py` M1 oracle exists; the sweep did the grep-equivalent (read-only).

### Leg 4 — orphaned docs / templates / protocols

**No true orphans** (the corpus was already justify-or-retire audited 2026-06-26). One THIN cluster (v4 handoff templates, 8 files) → **GATED by #164** (item 6). `AGENT_FRAMEWORK.md` → **TRACKED by #227**. `docs/archive/` triage-queue → operator periodic review (item 7). Everything else is intentional-archive / live-referenced / keep-by-policy (intake docs, canonical protocols, referenced templates).

### Leg 5 — untracked & ignored buildup (hub)

`temp/` **EMPTY** (confirms #229 — 703.87 MB reclaimed). No leftover worktrees. **No files >10 MB.** Caches trivial (`.pytest_cache` 198K, `.ruff_cache` 83K, 9 `__pycache__` dirs — all gitignored, routine). `.claude/settings.local.json` gitignored (expected).

### Leg 6 — config & registry rot

All 10 `.pre-commit-config.yaml`-referenced scripts exist (no dead entries). `tool-versions.yaml` has 2 live watched sources (claude-code, codex); the killed #133 (copilot-collections) left no dead entry. Disposition-register is **0-stale** (reconciled this session). One known stale entry — `doc-code-edge.yaml` `mermaid_theme_directive` — is **TRACKED by #263**. `ecosystem/index.yaml` is a derived cache (regenerated by `audit.py`), not a candidate.

### Leg 7 — cross-check (no forked tracking)

Every candidate was checked against open BACKLOG / rulings: v4 templates→**#164**, AGENT_FRAMEWORK→**#227**, fleet-audit→**#254**, conformance-digest→**#255**, doc-code-edge→**#263**, corp-ops/corp-sca→**#284 / night-audit F1**, release_lint→**#244**, probe_child_backlogs→2026-06-26 audit. Only genuinely-new item: **demo-prep unpushed** (backup gap, below).

---

## Proposed ready-to-file task (do NOT auto-file — proposal only)

`[P2][S] Fleet backup posture — three repos hold unbacked work on one disk: corp-ops (no git remote), corp-sca-time-automation feature/tenrox-loader (6 ahead, unpushed), demo-prep (origin set but nothing pushed). corp-ops+corp-sca are the #284 concern (its closure premise is false on live state, night-audit F1); demo-prep is newly surfaced. Operator: per repo, add/push a remote or record accept-local. · Done when: each of the three has an offsite backup (tracking remote + pushed branches) or a recorded accept-local decision · refs #284, docs/audits/2026-07-09-night-verification-report.md, docs/audits/2026-07-09-deletion-candidates-report.md`
