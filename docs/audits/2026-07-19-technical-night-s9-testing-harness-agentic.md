# Testing harness & agentic testing audit — the missing dynamic-test stage

Night-audit cycle-close · Stream S9 · ADR-101 class `technical`; read-only; measured numbers

## 1. Current mechanism

Measured this session (`pytest --collect-only -q`, wall time via `time`; each repo's own interpreter — hub system Python, consumer `.venv`):

| Repo | Tests collected | Collect cost (pytest-reported / wall) | pytest floor | ruff floor | xdist | Coverage | Marker tiering |
|---|---|---|---|---|---|---|---|
| hub (`.dev-knowledge`) | **1598** | 3.89s / 6.23s | `minversion=9.0` | `required-version>=0.15.5`, `target-version=py311`, `line-length=120` | `pytest-xdist>=3.8` dev-dep; invoked **manually** at `/ship` pre-flight only (`-n auto --dist worksteal`), not in `addopts` | no `pytest-cov` dep, no `[tool.coverage]` — **absent** | `live_repo` (docs-only pre-flight subset) + `slow` (opt-in gauntlet) markers, `pyproject.toml` L26-29 |
| corp-monorepo | **2735** | 18.65s / 24.11s | `minversion=9.0` | `required-version>=0.15.5` (SHAPE-equalized); lint posture diverges (`select=["E","F","I"]`, `ignore=["E501"]`, declared REPO-PERSONAL) | `pytest-xdist>=3.8` dev-dep; **no `addopts` wiring found** (grep) — latent, unused by default | `pytest-cov>=4.1` dep declared; **no `[tool.coverage]` section** — declared but unconfigured | none found (`addopts="-v"` only, no markers list in `[tool.pytest.ini_options]`) |
| ai-council | **549** | 4.92s / 7.91s | `minversion=9.0` | `required-version>=0.15.5` (SHAPE-equalized) | **no `pytest-xdist` dependency at all** (grep, 0 hits) | `pytest-cov>=5.0` **and** `[tool.coverage.run]`/`[tool.coverage.report]` wired — the only one of the three with live coverage config | `integration` / `envcheck` markers (require real API keys) |

Full-suite runtime — **not re-run tonight** (corp's 2735 tests would run multiple minutes; instruction is to avoid a minutes-long full run). Using the repo's own documented measurements instead:
- Hub full serial: **~9m42s** (`pyproject.toml` L33, 2026-07-05 profile). Hub full parallel (`/ship` code-diff pre-flight, `pytest -n auto --dist worksteal -x --tb=short`): **~2m05s wall**, "floor-bound by one 90s E2E test" (`plugins/tier1-lifecycle/commands/ship.md` L37-39, measured 2026-07-05). Hub docs-only fast path (`pytest -m live_repo -q && ruff check`): **~21s tests + ~13s ship-gate ≈ 34s** (ship.md L32-36).
- corp-monorepo / ai-council: no documented full-suite wall-time figure found in `CLAUDE.md` or `pyproject.toml`; both `CLAUDE.md`s cite only the command (`pytest -x --tb=short`), not a measured cost.

Slowest-test profile (cheap proxy — subprocess-spawn count per file, hub only, `grep -c "subprocess.run\|subprocess.Popen"`): `tests/test_audit.py` (9 spawns, 2230 lines, 164 test functions — largest file both ways), `tests/test_e2e_consumer_lifecycle.py` (8 spawns, opt-in `RUN_E2E=1`-gated), `tests/test_carrier_hooks_source.py` (8 spawns), `tests/test_block_ff_push.py` (7 spawns, real git pushes).

## 2. Designed/intended shape

The operator's stated engineering loop (mission brief): **intake → functional-req → ADR → implementation → sandbox/console DYNAMIC testing → review → close.** The repo's own documented loop (`ARCHITECTURE.md` Ch6 L564-571) is close but not identical: `Lessons → Decision/ADR → Conventions → Enforcement → Dissemination → (run in live sessions → new friction) → back to Lessons` — it names no explicit dynamic-testing stage between Enforcement and Dissemination.

The verification mesh (`ARCHITECTURE.md` Ch6 L577-583, five layers) is the closest existing structure:

| Layer | Organ | Dimension |
|---|---|---|
| In-session | `verify` skill (pytest+ruff+git) | step passes its own gates |
| Pre-merge | `/codex-review`; `/ship` gate | code-diff correctness; branch discipline |
| Nightly (cloud) | conformance Routine | claims-vs-docs coherence |
| Nightly (local) | `fleet_health.py`/`audit.py run` | structural + freshness health |
| Funnel | `surface_triage.ps1` + morning triage | operator ratifies findings |

None of the five layers **executes new functionality live and requires the output as merge evidence** — `/codex-review` is a static read-only diff review (PLAYBOOK L3371, "read-only sandbox"), not dynamic execution.

ADR-81 leg (e) — "functional proof" (`PLAYBOOK.md` Ch12, L1653: *"a mechanism is not done on presence or configuration alone... closure requires demonstrated enforcement-in-effect... a test observing the gate block/trigger, or an observed in-situ firing"*) is the doctrinal ancestor of gap (a) — it demands firing-evidence for **enforcement organs**, generalized to consumer-mesh transfer at L1659 ("configured → armed → proven"). It does not yet generalize to arbitrary **new functionality** (a feature, not a gate).

"What every routine must meet" (`PLAYBOOK.md` L1628-1636, ADR-80, 7 points: self-containment, declared output channel, `Routine:` trailer, per-stage model pins, fail-soft/catch-up, funnel-review, n=2 graduation) is the standard any configured agentic-testing workflow (gap b) must satisfy to graduate from ad-hoc to standing.

`docs/intake/2026-07-08-func-night-routines-suite.md` (intake-id 8) names the gap directly: *"the subagent-army pattern (Sonnet/Haiku swarms for micro-specific tasks) is currently underused and has no home in the night suite's design"* (L17-18) — a Should-tier FR (L45-47) with acceptance criterion 4 ("one demonstrated swarm run against such a task") still unmet.

BACKLOG chain: `#348` (P3, night routines + configured multiagent workflows, 2026-07-18) depends-on `#270` (P1, load-gauge, open) and refs `#271` (P3, nightly proposal loop) and `#324` (P3, Phase-6 axis-2, "night-batch (Codex review + audit fan-out) as a standing scheduled routine" — **charter-only, codification explicitly deferred**, `BACKLOG.md` L101).

## 3. Gap

**(a) Dynamic/sandbox pre-merge testing stage — absent as a general gate.** Proof of absence:
- Zero hits for `dangerouslyDisableSandbox` anywhere in the repo (grep).
- Zero `/run`-skill-relevant conventions (this repo is Layer-2 governance/validators-only — CLAUDE.md §3 "NOT a code project"; `/run` targets an *app*, which corp-monorepo/ai-council are and this repo is not).
- `deploy/lived_sandbox/` (`arc.py`, `cli.py`, `consumer.py`, `isolation.py`, `observe.py`, `oracle.py`, `spawn.py`) **is** a real live-fire mechanism — it spawns isolated `claude -p` subprocess sessions and derives a verdict from three EXTERNAL evidence channels only (transcript-events / hook-stdout / git-state, never inner-session narration — `test_lived_sandbox_observer.py` L1-6, "C1"). But it is scoped narrowly to proving the METHODOLOGY'S OWN hook-firing behavior for deploy/carrier verification — not a general "did this new feature work when exercised live" gate.
- `tests/test_e2e_consumer_lifecycle.py` (239 lines, 11-stage consumer-lifecycle gauntlet, `docs/audits/2026-07-12-technical-night-e2e-evidence.md`) is the fullest lived-workflow proof that exists — but it is **opt-in** (`RUN_E2E=1` env var, `slow` marker) and grep confirms **zero references** to `lived_sandbox`, `RUN_E2E`, or `live-fire` in `scripts/audit.py` or `.claude/commands/*.md` — it never gates a merge.
- `docs/audits/2026-07-17-technical-night-live-fire-sheet.md` is the closest prior art: a manual, read-only, one-night exercise (mutate config → observe organ fires → revert, in throwaway sandbox clones under `scratchpad/`) proving that seven **existing** gate mechanisms fire correctly. It is not a repeatable pre-merge requirement, and it proves gate-firing, not new-feature-correctness.
- Conclusion: **no enforcement site anywhere requires live/dynamic-execution evidence as a precondition for merging a code-impact change.** Pre-merge today is entirely static (pytest + ruff + `audit.py ship-gate`, all evaluate code/config without executing the changed feature against a live console).

**(b) Agentic testing — improvised per session, not configured.** Proof: no BACKLOG item, workflow-spec file, or `protocols/*.md` doc currently names a Sonnet-run / Haiku-fan-out / Codex-adversarial-derivation workflow as configuration. `docs/intake/2026-07-08-func-night-routines-suite.md` explicitly flags the subagent-army pattern as homeless (above). `#324`'s Codex-review-fan-out charter is deferred, not built. `#348` is the ticket that would close this — open, P3, gated behind `#270` (also open). No workflow-spec-file convention exists to hold such a definition yet: grep for `workflow-engine`/`.js` workflow files/`.claude/workflows/` returns zero hits in this repo; the only related doctrine is the (cloud-only, currently unavailable) "Native Workflow launcher" and its "spec-orchestration" fallback (`PLAYBOOK.md` L1594), plus the T-shirt model-pin convention (S=Haiku/M=Sonnet/L=Opus, Appendix B) that a configured workflow would need to reuse per the "per-stage model pins" routine-standard point (L1633).

**(c) Optimization** — see section 4.3 for concrete seeds (not abstract): zero shared `conftest.py`, 18 duplicated git-helper implementations, xdist wired only at one enforcement site, uneven coverage posture across the fleet.

## 4. Proposed MECHANISM

**(a) The sandbox/dynamic-test gate.**
- **Isolation primitive (reuse, don't reinvent):** generalize `deploy/lived_sandbox/spawn.write_isolated_config` (already proven in `test_lived_sandbox.py` — isolated `settings.json` + isolated `PRE_COMMIT_HOME`) from "prove a hook fires" to "prove a changed feature executes correctly," run inside a worktree (`.claude/worktrees/<slug>` — the exact convention this probe itself runs under).
- **Evidence artifact:** reuse the two existing captured-evidence shapes rather than inventing a third — `docs/audits/*-e2e-evidence.md` (precedent: `2026-07-12-technical-night-e2e-evidence.md`) or `docs/audits/*-live-fire-sheet.md` (precedent: `2026-07-17-technical-night-live-fire-sheet.md`).
- **Enforcement site:** extend `plugins/tier1-lifecycle/commands/ship.md` step 4 (the diff-shaped classifier at L26-42, currently docs-only vs code-diff) with a **code-impact** tier (touches `scripts/`, `deploy/`, or a child repo's `src/`) that additionally requires a same-arc-or-newer `*-e2e-evidence.md`/`*-live-fire-sheet.md` artifact. Concretely: a new `audit.py ship-gate` check (e.g. `dynamic_test_evidence`, alongside the existing hub-only checks at step 5) — **WARN-only first**, per the repo's own n=2 graduation discipline (PLAYBOOK L1636) and the routine-standard's evidence-gate-before-doctrine rule, promoted to FAIL only after two demonstrated runs.
- This composes with ADR-81 leg (e) rather than duplicating it: leg (e) is the qualitative "must fire" standard for enforcement organs; this gate is its concrete pre-merge enforcement for code-impact arcs generally.

**(b) The configured agentic-testing workflow.**
- **Config home:** new `protocols/AGENTIC_TESTING.md` (or a Council-routed ADR if contested) — the hub may only hold the *definition*, never execute it (CLAUDE.md §5 item 4 / ADR-28/36, "Layer 2 never executes"); a child repo or the cloud Routine runtime is the executor.
- **Structure**, satisfying the 7-point routine standard (PLAYBOOK L1628-1636):
  1. **Sonnet test runs** (M-tier) — executes the actual new-functionality pass.
  2. **Haiku fan-out collection** (S-tier) — parallel result-gathering/summarization (this very S1-S9 probe fan-out is the dogfood precedent, proven tonight).
  3. **Codex adversarial test derivation** for critical paths — reuses the *existing* sanctioned interim producer-lane pattern (PLAYBOOK L3395: "Codex fully specifies... writes nothing to the tree") repurposed to derive adversarial test cases, staying inside Codex's current read-only reviewer role — no need to wait on the gated producer lane (`#341`).
  4. Output → morning funnel (existing consumer, L1635) — proposals only, never auto-applied.
  5. Explicit `depends-on #270` per `#348`'s own declared dependency; folds `#324`'s Codex-fan-out charter in rather than duplicating it.

**(c) Optimization seeds** (concrete, witnessed):
1. **Zero `conftest.py`** anywhere under `tests/` (Glob `**/conftest.py` → no hits) — yet **18 files** independently define their own `_git()`/`_run_git()`/`_make_git_repo()`/`_init_repo()` helper: `test_audit`, `test_block_ff_push`, `test_canonical_freshness_gate`, `test_carrier_hooks_source`, `test_coherence_nudge`, `test_deploy_mesh`, `test_e2e_consumer_lifecycle`, `test_enforcement_coverage`, `test_fleet_parity`, `test_fleet_parity_events`, `test_floor_conformance`, `test_lived_sandbox_observer`, `test_merge_serialization`, `test_propose_closures`, `test_safe_remove`, `test_validate_git_backlog`, `test_validate_hermetization`, `test_validate_no_ff` (grep-confirmed). A shared `tests/conftest.py` git-repo fixture is the highest-value, lowest-risk seed.
2. **`tests/test_audit.py`** — 2230 lines / 164 test functions / 9 subprocess spawns — the largest file by every measure; a split-by-concern candidate (it covers the ~30-check `ALL_CHECKS` battery + ship-gate + index regeneration in one file).
3. **xdist is already wired**, but only at one enforcement site (`/ship` code-diff pre-flight) — measured ~2m05s parallel vs 9m42s serial (4.6x), yet "floor-bound by one 90s E2E test" (ship.md L39) that dominates wall time even under `-n auto`; profiling/isolating that test (subprocess-spawn ranking points to `test_carrier_hooks_source.py` or `test_block_ff_push.py`) is the highest-leverage remaining speed seed. It is **not** the pytest default (`pyproject.toml` has no `addopts="-n auto"`), so a bare `pytest -x --tb=short` (the CLAUDE.md §Testing convention) runs serial.
4. **corp-monorepo** declares `pytest-xdist>=3.8` but has zero `addopts` xdist wiring (grep-confirmed) — same latent-but-unused pattern as the hub pre-`/ship.md`-tiering state; a directly transferable seed once corp adopts an analogous pre-flight tiering step.
5. **Coverage posture is uneven fleet-wide**: hub has no `pytest-cov` at all; corp declares `pytest-cov>=4.1` with zero `[tool.coverage]` config; ai-council is the only repo with both the dep and live `[tool.coverage.run]`/`[tool.coverage.report]` config. Worth a `fleet_parity`-style follow-up if coverage posture is ever declared a MUST.

## 5. BACKLOG seed

- [SEED] [P3][M] Dynamic-test pre-merge gate + configured agentic-testing workflow — close S9's two named gaps: (a) extend `plugins/tier1-lifecycle/commands/ship.md` step 4 with a code-impact tier requiring fresh `docs/audits/*-e2e-evidence.md`/`*-live-fire-sheet.md` evidence (WARN-first, promoted to FAIL after n=2 per PLAYBOOK L1636), generalizing `deploy/lived_sandbox/spawn.py`'s isolation scaffold beyond hook-firing proofs; (b) author `protocols/AGENTIC_TESTING.md` naming the Sonnet-run/Haiku-fan-out/Codex-adversarial-derivation workflow, model-pinned per Appendix B, satisfying the 7-point routine standard, depends-on `#270`, folding in `#324`'s deferred Codex-fan-out charter · refs #348, #270, #271, #324, docs/intake/2026-07-08-func-night-routines-suite.md, ARCHITECTURE.md Ch6, PLAYBOOK.md Ch12 (ADR-81 leg e), docs/audits/2026-07-12-technical-night-e2e-evidence.md, docs/audits/2026-07-17-technical-night-live-fire-sheet.md, plugins/tier1-lifecycle/commands/ship.md, deploy/lived_sandbox/ · kill-candidates: none — no existing ticket names the pre-merge dynamic-test gate or the agentic-workflow spec-file home specifically; #348/#270/#271/#324 are the adjacent night-routine chain this seed extends, not a subsuming duplicate · Done when: a code-impact arc lacking fresh dynamic-test evidence fails (or WARNs, pre-graduation) `audit.py ship-gate`, AND `protocols/AGENTIC_TESTING.md` (or successor ADR) names the three agentic roles + model pins + funnel consumer, AND a shared `tests/conftest.py` git-repo fixture replaces at least one of the 18 duplicated `_git()` helpers as the first optimization payoff
