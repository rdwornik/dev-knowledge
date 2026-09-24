> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-browser/DIGEST-ORGAN-TRIAGE-2026-09-24.md` (a Drive transport path, not retained in
> this repo — verifiable against the bytes landed below by their hash,
> `sha256:6c9776322aae8375b90e29f2acb26ec8c2d2b02f4c8bbce9852355e977151269`, 12,124 B, computed by
> this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-digest-organ-triage.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: the operator's per-item GO in the morning review; no repo change was made
date: 2026-09-24
from: night-readonly (BATCH-NIGHT-READONLY-2026-09-23 Part 1, job a58f3cec, Opus 5.5), read-only on main @ 4667f731 (clean before and after)

# DIGEST — organ triage of the 97 UNOBSERVED + UNREACHABLE organs

**Source list:** S3's census on this same SHA (`organ_usage_metric.py census`, 30 d window, S3 job tmp `census.out`), INHERITED, not re-run. 80 REACHABLE-BUT-UNOBSERVED + 17 UNREACHABLE = 97.
**Evidence method (MEASURED):** a word-boundary `git grep` of every organ's stem across all wiring surfaces, then real-importer greps, then the file's own docstring and its `ecosystem/harness.yaml` `fates:` line. Nothing was deleted or edited.

## Headline

- **RETIRE: 2 claims survive, and both collide with a standing ruling.** 4 claims went to Codex. The routed checker, `gpt-5.6-sol`, confirmed C1 and C3 and rejected C2 and C4. A first run served `gpt-5.6-terra`, the configured default: a SUBSTITUTION, recorded. Terra rejected all 4.
- **WIRE: 77.** 74 of them are already wired, and the census cannot see the surface they are wired through: an import chain, a git hook, the consumer-side `.pre-commit-hooks.yaml`, `.devcontainer`, a SessionStart/Stop hook, or a harness moment. 3 are PROPOSED new wirings. 3 already-wired hooks are proposed for re-wiring, and `plan_lint` (outside the 97) for a moment. Each proposal needs a GO.
- **KEEP-MANUAL: 18,** each with a reason and a date. Most dates are `2026-10-05`, aligned with the existing `fates:` block (pre-authorized ruling 2a).
- **Defects the census exposed (not organs):**
  - D1: two stale `fates:` lines. `harness.yaml:103` (codespace_regime) and `:123` (surface_triage) say "hook off since 09-17", but `.claude/settings.json` arms both at SessionStart today (W4B-0 re-arm).
  - D2: `surface_triage.ps1` is wired but times out on 252 of 262 runs (96%, boot banner). Wired is not working.
  - D3: `lane_end_guard.py` runs as bare `python`, not `uv run --locked` (`.claude/settings.json` Stop hook; `/doctor` flagged it too).
  - D4: the census over-counts UNREACHABLE because FPG-1 has no stage/moment→script edge (S3 Track B #1). 3 of the 17 UNREACHABLE organs are argv at a moment today.

## RETIRE (operator GO per item; nothing deleted)

- **C1 `scripts/export_backlog_view.py` — RETIRE-CLAIM, sol CONFIRMED, terra NOT-CONFIRMED.** Sol cites `scripts/graph_queries.py:437`: consumerless by design, and a test asserts that nothing reads the export. Terra cites the docstring (`:5`): the external Backlog.md board/UI is the consumer. **Collides with the `[#563]` ADOPT-VIEW-LAYER ruling (2026-08-19).** Retiring it reverses that ruling, so the GO is a ruling, not a cleanup. 0 calls in 30 d.
- **C3 `scripts/offload_admission.py` — RETIRE-CLAIM, sol CONFIRMED, terra NOT-CONFIRMED.** No caller (`harness.yaml:114`: "unwired by design"). It is the admission gate for a role row (intake #75) that the operator has not created. **If the offload role is dead, RETIRE; if it is only deferred, KEEP-MANUAL.** The operator owns that routing decision.
- C2 `context_reclamation.py`: NOT CONFIRMED by both models. `tests/test_codespace_regime.py:164` imports it as a reference implementation. → KEEP-MANUAL.
- C4 `propose_row_closures.py`: NOT CONFIRMED by both models. The operator reads its output (`graph_queries.py:593-599` disposition); `propose_closures` does not supersede it. → KEEP-MANUAL.
- **Why so few:** `[#734]` deleted two census "orphans" with invisible callers: `desired_state_loader.py` (loaded by importlib in a test; restored) and `cloud_provisioning.py` (called by path from `provision.sh`; re-filed as `[#746]`). This triage applied that lesson: a census zero is never evidence alone.

## WIRE — PROPOSED (needs GO; moment + evidence)

- `scripts/handback.py` → **moment `lane-end`** (`harness.yaml` lane-end organ list). It writes the SESSION handback line that `lane_end_guard.py` reads (`handback.py:326-340`). Its fate (`:111`) already says "a moment declaration is owed by the next wave".
- `scripts/lane_boot.py` → **moment `pre-launch`**. It is `/lane-boot`'s pre-flight (`.claude/commands/lane-boot.md:64`) and runs before any worktree exists, as the other pre-launch organs do.
- `scripts/plan_lint.py` (CALLED, but an orphan-census finding) → **moment `pre-launch`, batch-scoped**. WAVE5A step 0 already runs it by hand. **Caution (Digest MEASUREMENTS §3):** it refuses every live WAVE5A contract, because they carry no ``slug `<slug>` `` line and use `**Owns:**` where it reads `**Files you own:**`. Fix its grammar before wiring it.
- `scripts/block_commit_on_main.py` → **pre-commit default stage** (today `stages: [manual]`). Core-invariant #5 PREVENT is inert (S3 §2). The pre-push `block-ff-push` catches the push, but nothing catches the commit.
- `scripts/surface_triage.ps1` and `scripts/billing_leak_sentinel.ps1` → stay at SessionStart, **ported to `uv run --locked python`**. This fixes D2's timeouts and the container blocker (Digest SELF-PROPOSALS §a, top-1).
- `scripts/lane_end_guard.py` → the Stop hook command becomes `uv run --locked python …` (D3).

## WIRE — already wired; the census is blind to the surface (74)

**Import chain from a CALLED organ** (import → CALLED importer):
- `scripts/audit_checks/*` — 25 files, including `_common.py` and `registry.py`. All come in through `registry.py` → `audit.py` (CALLED 316). Moment: `merge/gates` (`harness.yaml:62`, where `gates.py` runs `audit.py health` + `ship-gate`).
- `backlog_source` (`audit.py:4723`, `conductor.py:56`) · `canonical_docs` (`audit.py:236`) · `gitenv` (`audit.py`, `fleet_parity.py`, `batch_manifest.py`) · `governance_health` (`audit.py:135`) · `generated_artifact_freshness` (`audit.py:245`, ship tier `:5377`).
- `scan_undeclared_edges` (`audit.py:219`) · `validate_doc_code_edge` (`audit.py:153`, `file_purpose_graph.py:143`) · `validate_no_ff` (`audit.py:112`).
- `validate_adr_status` (`check_adr_status_grammar.py:21`) · `validate_reconciliation` (`check_reconciled_versions.py:17`) · `dispatch_drift` (`check_dispatch_drift.py:57`).
- `coherence_enumerator` (`scan_undeclared_edges.py:61`, check-against-spec skill) · `handback_schema` (`handback.py:63`, `transport_report.py:63`, `lane_end_guard.py:192`).
- `reverse_dep_oracle` (`safe_remove.py:73`) · `seat_ch8` (`gen_seat_boot.py:54`) · `provider_registry` (`changelog_sentinel.py:39`, `check_provider_registry` hook).
- `generate_floor` (`check_floor_integrity.py:22`, `deploy/carrier_floor.py:79`) · `enforcement_coverage` (`deploy/carrier_precommit.py:65`, `deploy/floor_mechanisms.py:90`).
- `scripts/codemap/{__init__,ast_walker,check,generator,mermaid_emit,text_emit}.py` → `codemap/cli.py`, run by the default-stage `codemap-freshness` hook.
- `scripts/toc/{__init__,check}.py` → `toc/cli.py` (hub hook manual; consumer hook below).

**Git hooks** (hook runs leave no transcript interpreter line, so the census cannot count them):
- Default stage: `telemetry_emit` wraps 10 hook entries (`.pre-commit-config.yaml:77…`); `dispatch_conformance`.
- commit-msg: `check_backlog_commit_msg`, `check_backlog_filing`.
- pre-push: `block_ff_push`, `block_unanchored_push`. `block_unanchored_push` also runs in CI.

**Consumer-side hooks** (fire in child repos, never in hub transcripts):
- `codemap_hook.py` and `toc_hook.py`: `.pre-commit-hooks.yaml:26,35,44,52`, deployed through `deploy/manifest-v1.5.0.yaml:265-266`.
- `canonical_freshness_gate.py`: `deploy/carrier_mesh.py:61`, roster `canonical_freshness`.
- `plugins/tier1-lifecycle/scripts/validate_backlog.py`: the floor copy. It DIFFERS from `scripts/validate_backlog.py` by design.

**Session hooks** (`.claude/settings.json`):
- SessionStart: `arm_hooks`, `changelog_sentinel`, `conductor`, `codespace_regime`, `billing_leak_sentinel.ps1`, `surface_triage.ps1`.
- Stop: `session_end_backpressure`, `lane_end_guard`, and the plugin's `propose_closures.py` (`plugins/tier1-lifecycle/hooks/hooks.json`). S3 records that nothing reads what `propose_closures` writes; that is a consumer gap, not a caller gap.

**Other surfaces:**
- `provision_legs.py` → `.devcontainer/provision.sh:450-469`, the codespace create moment. It was restored by `[#746]` after exactly this misread.
- `fleet_analytics.py` → CI only (`report-only-wall.yml:65,254`, mutation scope). It has no scheduled caller. **Borderline:** re-check at the 10-05 fate sweep.

**Declared at a moment, census/graph blind (D4):**
- `go_reader.py` → `merge` (`harness.yaml:60`).
- `lane_digest.py` → `batch-close` (`harness.yaml:78`).
- `dodo.py` → the moments runner itself (`harness.yaml:26`).

## KEEP-MANUAL (reason · date)

- `plugins/tier1-lifecycle/scripts/review_closures.py`: the ratification act via `/review-closures`; no event should fire it · 2026-10-05 (`harness.yaml:101`).
- `scripts/review_closures.py` and `scripts/propose_closures.py`: derived-copy sources of the plugin copies (`ecosystem/derived-copies.yaml`) · 2026-10-05.
- `scripts/codespace_state.py`: unwired by directive until intake 102 settles who observes · 2026-10-05.
- `scripts/context_reclamation.py`: a seat calls it at its own checkpoint; `[#791]` owns the initiator; imported by `tests/test_codespace_regime.py:164` (both Codex models agree) · 2026-10-05.
- `scripts/cost_usage_telemetry.py` and `scripts/provider_router.py`: waiting on `[#691]` Half B (non-Claude routing) · 2026-10-05.
- `scripts/desired_state_loader.py`: pinned by `tests/test_membership_agreement.py` (importlib); `[#734]` deleted it once and it was restored · 2026-10-05.
- `scripts/propose_row_closures.py`: the operator reads its on-demand witness report (`[#730]`); both Codex models agree · 2026-10-05.
- `scripts/provider_bench.py`: a paid one-off measurement; a commit-tier trigger would bill per commit (`[#785]`, owner `[#676]`) · 2026-10-05.
- `scripts/setup-fleet-scheduler.ps1`: a one-shot installer. The task it registers is live (`schtasks`: `fleet-baseline` Ready, next run 2026-09-24 09:00) · 2026-10-05.
- `scripts/gen_dashboard.py`: a library of `propose_row_closures.py`. `ecosystem/conformance.md` was last regenerated 2026-09-05, and `conformance.html`'s "MIGRATE-not-delete" question is open (`HANDOFF_PROCESS.md:1230`) · 2026-10-05.
- `scripts/hooks/deny_and_point.py`: PreToolUse UNWIRED by the B2 lane4 rule-8 review 2026-09-18 (`.claude/settings.json:120`) · 2026-10-05.
- `scripts/hooks/bounded_hook.py`: routing held by operator ruling 2026-09-17 (`.claude/settings.json:30`) · 2026-10-05.
- `scripts/hooks/block_immutable_edits.py`: the ADR-77 guard stays off (`[#863]`; `.claude/settings.json:35`) · 2026-10-05.
- Pre-commit `stages: [manual]` organs: `normalize_headers.py`, `check_derived_copies.py`, `coherence_nudge.py`. Held manual by the B2 lane4 review; decide at the counter verdict · **2026-09-25**. Note that the counter is per-checkout, so a zero reads UNMEASURED, not REMOVE (S3 §2).

## Counts (by construction from the lists above)

- RETIRE 2 (C1, C3), both ruling-conflicted.
- WIRE 77:
  - 74 already wired, including the 3 re-wirings of already-wired hooks (surface_triage, billing_leak_sentinel, lane_end_guard);
  - 3 proposed new wirings (handback, lane_boot, block_commit_on_main).
  - `plan_lint` is CALLED and not in the 97, so it is not counted here.
- KEEP-MANUAL 18.
- Total 97. Checked mechanically: every organ in `census.out`'s two states appears in this file by name or by its package line.

## Routing record (what served)

- orchestrate: claude-opus-5-5 (this session).
- evidence sweep: done in-session by deterministic `git grep`; no sub-agent was needed for Part 1.
- RETIRE re-check: `codex exec -s read-only`. Run 1 served **gpt-5.6-terra** (SUBSTITUTION: the default config, not sol; 51,246 tok). Run 2 used explicit `-m gpt-5.6-sol`, which **served sol** (48,720 tok). The verdicts above are sol's, with terra's recorded as dissent.
- Gemini/agy: not used. No source over 50 KB was read (the largest was 48 KB).

DONE 2026-09-24 00:25
