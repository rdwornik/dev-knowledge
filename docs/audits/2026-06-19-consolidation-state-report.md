<!-- scope: meta -->

# Consolidation state report — 2026-06-19

> **Point-in-time inventory** at the close of the 2026-06-19 "doc-currency seal + whole-flow
> verification" session, following the morning's enforcement-layer seal (C1 JOURNAL gate,
> #140 `doc_rot`, #187 dedup, #186 floor-sync). Audience: the next session, which starts the
> #131 ai-council onboarding and the visual workflow/dependency dashboard. This is the **text
> precursor** to that dashboard — a clear *sealed / open / sequenced* picture. Immutable
> (dated audit, ADR-60); supersede with a new dated report, never edit in place.

---

## 1. Sealed — done **and** verified

| Item | Evidence | Verified |
|---|---|---|
| **C1 per-session JOURNAL gate** — push-boundary → session-boundary anchor | `session_end_backpressure.py::check_journal_sha_anchor` (merged 2026-06-19 AM); ADR-85 amendment 2026-06-19 | `test_e2e_cross_session_miss_blocks` + 38 sibling tests PASS (39/39); the gate fired live this session (blocked on 6 unjournaled commits) |
| **DEFINITION_OF_DONE synced to C1** | `1bf8fdb` (this session) — boundary description rewritten push→session; `last_reviewed` 06-16→06-19 | the canonical "done" doc no longer mis-describes its own gate |
| **#140 `doc_rot` grooming checker** (ADR-88 FC4 deterministic trigger) | `validate_doc_rot.py` + `check_doc_rot`; `ALL_CHECKS` → 21 | `audit.py checks` == **21**; 5 live loci grandfathered + dispositioned |
| **#187 dedup-on-entry** (hub) | `_check_duplicate_titles` in `validate_backlog.py` | `validate_backlog: OK`, 0 warnings |
| **#186 floor-sync** of the #156 task-graph checks into the plugin floor | `plugins/tier1-lifecycle/scripts/validate_backlog.py` | **7/7** floor tests pass; child-shaped dangling-edge fixture caught |
| **ESSENTIALS under the freshness gate** (check #10) | `9e16a3d` (this session) — frontmatter + `_FRESHNESS_FILES`; PLAYBOOK L864 + CLAUDE §4 ripple (four→five); `test_freshness_includes_essentials` | ESSENTIALS drift is now check-#10-detectable; previously invisible |
| **5 LESSONS entries** (this session's generalizable lessons) | `95f0006` (this session) | newest-first; C1 boundary, worktree n=3, git-log lever, verify-from-live-state, closure-surfacing |
| **Closures #187 / #186 / #140** | done-items-leave (AM); evidence SHAs re-verified | left `BACKLOG.md` per ADR-65 |
| **file #191** — `file_path` PreToolUse guard for the P0 OneDrive zone (Audit Finding 1 from #188) | merge `de7d040` (pre-session) | Finding 1 was filed + shipped, not left dangling |

**Live gate status (re-confirmed this session, post-edits):** `audit.py checks` == **21** · `health` **OK** · `ship-gate` **GREEN** (6 WARN dispositioned: #77 + 5 `doc_rot`) · `validate_reconciliation` 1 edge / 0 mismatch · `validate_doc_claims` 4 claims match (pytest_collected **667/667**) · full suite **666 passed / 1 skipped** · ruff clean.

---

## 2. Open — closeable soon

- **#188 — hook-completeness audit** — OPEN by operator choice; the audit shipped (`docs/audits/2026-06-19-hook-completeness-audit.md`, refs-only). Operator ratifies closure separately. Finding 1 (the P0 `file_path` guard) already shipped as **#191** — so the residual #188 scope is the *record*, not new build.
- **`_DEPENDS_CLAUSE_RE` hub↔floor twin parity-check** — the mechanical hub↔floor parity check (ADR-88) is queued per the 2026-06-19 JOURNAL but is **genuinely untracked** (no BACKLOG id; confirmed — no `parity`/`_DEPENDS`/`twin` match in `BACKLOG.md`). The #186 carrier-doctrine twin-marker (ADR-78) flags the drift edge by hand; **recommend filing it** so the parity check isn't lost between grooms. (Distinct from **#190**, which is the *intra-file* duplication detector — `serialize-group: audit-py`, tracked.)

---

## 3. Open — flow-enforcement gaps (from the Part B lifecycle walk)

These are not defects to fix this session — they are honest coverage limits worth seeing in one place. **Do NOT add a pytest hook this session** (a separate friction decision).

- **(a) Unit-test PASS/FAIL is NOT commit-gated.** Only the test *count* is gated (via `doc_claims` check #17, `pytest --collect-only`). There is **no pytest pre-commit hook**, so a commit whose tests *fail* is not blocked at commit time. `audit-health` (the commit gate) checks structure, not test outcomes. Mitigation today: the per-step `pytest -x` cadence (manual / `verify` skill) + the `ship-gate`.
- **(b) Empirical / e2e** — no hard gate; advisory only.
- **(c) Review (`/codex-review`, `/code-review`)** — operator-invoked; advisory only (no gate forces a review before merge).

### Lifecycle organ map (which stage actually fires what)

| Stage | Organ | Enforcement |
|---|---|---|
| Planning | `validate-backlog` (pre-commit) — schema + #156 dep-graph + #187 dedup | **GATED** (schema/graph); plan *quality* advisory |
| Empirical / e2e | — | advisory (gap b) |
| Unit test | `pytest` (manual / `verify` skill); count via `doc_claims` #17 | count **gated**; **PASS/FAIL not commit-gated** (gap a) |
| Review | `/codex-review` (command), `/code-review` (skill) | advisory (gap c) |
| Journal | `session_end_backpressure` C1 Stop hook | **HARD-GATED** (blocks turn-end; `/override` only escape) |
| Closure | `propose_closures` (Stop) → `/review-closures` (command) | propose auto; **close human-gated** |
| Ship | `audit.py ship-gate` (verification-organ gate, #147) | **HARD-GATED** (RED blocks `/ship`) |

### Skills / guards (Part B reconciliation)
- **Skills present:** `verify`, `check-against-spec` (`.claude/skills/`). **`handoff` is a command** (`.claude/commands/handoff.md`), not a skill. **No `cc-prompt` skill exists** anywhere — the prompt skeleton lives in **PLAYBOOK §2 + `templates/prompt-template.md`**. The task's "cc-prompt / handoff skills load" is a **naming discrepancy**, not a missing organ.
- **PreToolUse guards:** `block_immutable_edits.py` (in-repo, tested, ADR-77 transcript zone) + the global `~/.claude` `block-onedrive` P0 guard (command-string-scoped per the #188 audit) + the new **#191** `file_path` guard (closes the Edit/Write `file_path` blind spot for the P0 OneDrive zone).

---

## 4. Open — gated / future-arc (report open; do NOT fabricate-resolve)

- **ADR-88 `Proposed` → `Accepted`** — the file-oriented-dependency capstone is `Proposed`; promotion is a Council/operator step (the `doc_rot` arc already cites it as a forward-pointer, which is correct for a Proposed ADR).
- **Handoff-machinery arc (#159 / #164, Finding B = supplement↔state reconcile)** — both tracked in `BACKLOG.md` (handoff serialize-group). The boot-time stale-PROBES concern: `audit.py health` reports **`handoff_probes`: 10 probes bind to live state** (2026-06-18 bundle), so the probe teeth are currently sound; the supplement↔state reconcile (Finding B) is **not yet closed** — report **open, not corrected** (the prior sessions surfaced/worked-around the PROBES-vs-state seam rather than mechanically closing it).
- **Encapsulation-gate → #131 pilot** — the next session's onboarding (ai-council) is the first deployment test of the unified, self-enforcing methodology. Out of scope here.
- **Conformance dashboard** — tracked ids confirmed: **#168** (build), **#169 / #171** (reparent/build cluster), **#170** (traceability-spine ADR that promotes ADR-85's BACKLOG leg advisory→hard), **#183** (reparent under coherence doctrine). Sequenced **post-pilot**. ADR-86 already located the dashboard.
- **Conformance harness** — the broader self-conformance test surface; future-arc.

### C6 — nightly conformance digest: **investigated, NOT a silent skip**
The suspicion that the nightly "silently skipped since 2026-06-14" is **refuted by live state**: the docs/audits/ gap on `main` after 06-14 is the **ADR-84 relocation** — the digest no longer commits to `main`, it diverts to `origin/automation/conformance-digest`, which carries digests **06-15, 06-16, 06-17, 06-18** (latest commit 2026-06-18 01:13 UTC). So the loop is healthy through 06-18. **Residual sub-item:** the **06-19** run is unconfirmed from local state (`origin/` may be unfetched; the run window may be ongoing) — confirm via a `git fetch` of the automation branch or the cloud Routine panel. (This is the second inherited-framing refutation this session — see Appendix.)

---

## 5. Appendix — inherited framings refuted by reading live state

This session re-applied the verify-from-live-state discipline (now LESSONS 2026-06-19) and overturned three load-bearing claims it inherited:

1. **"PLAYBOOK prompt-format lags ADR-87" (the task's stated highest-value update)** — REFUTED. PLAYBOOK §2 ("Architect output vs CC consumption-spec", L2012–2020) already carries the ADR-87 contract verbatim (landed 2026-06-18, `25e64e2`). The real highest-value laggard was **DEFINITION_OF_DONE** (pre-C1 push-boundary). The session was re-scoped accordingly.
2. **"The nightly digest may have silently skipped since 06-14" (task C6)** — REFUTED — ADR-84 relocation to `automation/conformance-digest`, healthy through 06-18 (§4 above).
3. **"C1 gate-logic merge conflict hazard" (AM integration contract)** — REFUTED in the AM arc; no base commit touched the gate code, so the only merge conflict was JOURNAL stacking.

**Takeaway:** a task's framing of what is stale/risky is a *hypothesis to verify against the repo*, not a finding.

---

## Merged-but-undeleted branches (operator cleanup)

Merged to `main`, deletable at operator discretion (branch drops are operator-gated): `docs/dod-c1-sync`, `feat/essentials-freshness-gate`, `lessons/2026-06-19-consolidation`, `docs/adr-88-file-oriented-deps`, plus the AM `worktree-seal-hooks` / `worktree-seal-dedup`.
