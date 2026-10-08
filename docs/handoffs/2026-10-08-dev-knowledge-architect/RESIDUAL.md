# Residual — 2026-10-08-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers, which CC re-derives from PROBES.md. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-10-02-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**UNJUDGED — every flag in this section.** At this cut CC rules none of them a decision or a defect: the incoming seat judges each one together with CC after its teach-back (R76; `to-cc/PLAN-HANDOFF-2026-10-04.md` v5 §2). The evidence is by reference; P7/P4 re-derive the live values, and none is stated here.

- **`reconciled_versions` — UNJUDGED.** Evidence: this window's diff touched two of the surfaces it reads, `CLAUDE.md` and `docs/handoffs/README.md`. Re-derive: `git diff --name-only` from the commit that added `docs/handoffs/2026-10-02-dev-knowledge-architect/` to `HEAD`, over `protocols/HANDOFF_PROCESS.md templates/prompt-template.md docs/handoffs/README.md CLAUDE.md`; P7 carries the organ's live finding.
- **`fleet_parity` — UNJUDGED.** Evidence: this window's diff touched surfaces under all four roots it reads — among them `.claude/commands/handoff.md`, `deploy/conductor-required-checks.ruleset.json`, `ecosystem/provider-registry.yaml`, `ecosystem/transport-registry.yaml` and the `templates/handoff/` set (R66 retirements). Re-derive: the same diff over `ecosystem/ deploy/ .claude/ templates/`; P7 carries the organ's live finding.
- **The register-dispositioned family above — UNJUDGED for a new evidence signature.** The register dispositions only a matching signature; whether any live finding from those organs carries a new one is P7's answer, judged with CC.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
This is a terse map. The detail is in `JOURNAL.md` 2026-10-02..2026-10-04 (w) and in the transport digests
`to-browser/DIGEST-FOUNDATION-2026-10-03.md` and `to-browser/DIGEST-B2-W1-2026-10-04.md`. Re-derive anything from `git log --first-parent main`.

- **The 2026-10-02 window's architect bundle** was cut and verified, with R53 and R54 recorded in its residual.
- **FOUNDATION** merged and closed (`to-browser/STATE-BATCH-FOUNDATION.md`): the known-reds registry owned and ratcheted, cheap reds fixed by cause, the handoff boot teaching the onboarding items (R35-R54 verbatim), CI speed, Codespace parity and toolset, test isolation, model currency from served evidence, R66 template retirement (ADR-116 withdrawn), harness-report hygiene.
- **B2-W1** merged and closed (`to-browser/STATE-BATCH-B2-W1.md`, CLOSED 2026-10-06T15:51Z): row close on merge, the merge gate (FLAG pre-existing, REFUSE new and non-pass), R55-R79 as `protocols/STANDING_RULINGS.md` §AR with the `rulings_carried` gate, handoff hardening, Codespace 1:1 and close-out, transport probe and lint, CI poll, dispatch-local-sole, branch-context tests, integrator liveness, the known-reds re-sign; rows `[#1383]`-`[#1386]`, `[#1421]` and `[#1422]` filed. W1-13 and the dispatcher seat row are archived as tags (§4).
- **B+ step 2** (R90, 2026-10-08; branch `worktree-b-plus-step-2`, carried by this bundle's branch): the nine P13 dispositions the seat ruled ESTABLISHED, rendered by the new `scripts/decision_carriage.py` (the seed of the batch-close dispositions gate); rows `[#1423]`-`[#1437]` (W1-13 follow-on superseding `[#1376]`, FOUNDATION lane 12, the handoff tooling defects, R90 fixes (a)-(c)); `[#1366]` implements AMEND-B2-W1-4.
- **This cut** files `[#1438]` (W2-22 boot teaching), `[#1439]` (R91), `[#1440]` (pinned readiness) and `[#1441]` (the NEW reds) on the bundle's branch.

**Carried WARN debt.** `journal_spine_anchor` is carried. It is dispositioned in `ecosystem/disposition-register.yaml` ("anchored by mention, not by record"; provenance `[#524]` leg c; review 2026-11-14) and is ADVISORY BY DESIGN. P7 re-derives the live WARN set. No WARN was silenced to make a gate pass.

**Carried questions** (`question_disposition` CARRIED leg). Each is named with the OPEN row that owns it:
- `QUESTION-github-private-now.md` ← [#887]
- `archive/2026-09-07/QUESTION-dispatcher-N2.md` ← [#610], [#642]
- `archive/2026-09-07/QUESTION-dispatcher-T.md` ← [#628]
- `archive/2026-09-07/QUESTION-integrator-N2-win-tooling-merge.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-t-000-reds-spine.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-adr-carrier-split.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-branch-enum-parity.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-carrier-floor-v150-mechanisms.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-deploy-tool-consumer-override.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-dispatch-receipt-is-work.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-handoff-v71-build.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-000-shape-spec-finalize.md` ← [#642]
- `archive/2026-09-07/QUESTION-lane-u-628-release-commit.md` ← [#642]

**Carried decisions (`carried-by: OPEN`).** They are named here because the residual is their only carrier (P11 leg 2). Each one states an OPEN carrier and has no repo home yet. The next session either lands each one or re-declares the carriage:

- to-cc/AMEND-B2-W1-1-2026-10-04.md
- to-cc/AMEND-B2-W1-2-2026-10-04.md
- to-cc/AMEND-B2-W1-3-2026-10-04.md
- to-cc/AMEND-B2-W1-4-2026-10-05.md
- to-cc/AMEND-B2-W1-5-2026-10-05.md
- to-cc/AMEND-BATCH-FOUNDATION-2-2026-10-03-v1-superseded.md
- to-cc/AMEND-BATCH-FOUNDATION-2-2026-10-03-v2-superseded.md
- to-cc/AMEND-BATCH-FOUNDATION-2-2026-10-03.md
- to-cc/AMEND-BATCH-FOUNDATION-2026-10-03.md
- to-cc/AMEND-BATCH-FOUNDATION-3-2026-10-03.md
- to-cc/AMEND-BATCH-FOUNDATION-4-2026-10-03.md
- to-cc/AMEND-BATCH-FOUNDATION-5-2026-10-03.md
- to-cc/AMEND-BATCH-LAUNCH-SEATS-2026-09-29.md
- to-cc/AMEND-BATCH-WAVE5B-N2-LANE8-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE2-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE3-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE4-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE5-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N4-HANDOFF-MIN-2026-09-27.md
- to-cc/AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28.md
- to-cc/AMEND-BATCH-WAVE5B-N5-2026-09-29.md
- to-cc/AMEND-BATCH-WAVE5B-N5-R-CYCLE-2-2026-09-29.md
- to-cc/AMEND-BATCH-night-2026-09-17.md
- to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md
- to-cc/AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md
- to-cc/AMEND-HANDOFF-REDESIGN-BUILD-2026-10-01.md
- to-cc/AMEND-INTEGRATOR-MERGE-PATH-2026-09-29-withdrawn.md
- to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md
- to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md
- to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md
- to-cc/AMEND-ORGAN-USE-2026-09-17.md
- to-cc/BATCH-AJ-ALL-MODULES-2026-09-29.md
- to-cc/BATCH-AUDIT-OPEN-LOOPS-2026-09-26.md
- to-cc/BATCH-AUDIT-SPINE-AND-TOOLS-2026-10-04.md
- to-cc/BATCH-AUDIT-TRANSPORT-2026-10-04.md
- to-cc/BATCH-B2-PREP-2026-10-03-v1-superseded.md
- to-cc/BATCH-B2-PREP-2026-10-03.md
- to-cc/BATCH-B2-W1-2026-10-04.md
- to-cc/BATCH-BOOT-TEST-GRADE-2026-10-04.md
- to-cc/BATCH-CAPABILITY-MAP-2026-09-25.md
- to-cc/BATCH-CI-TRIAGE-2026-10-03.md
- to-cc/BATCH-CLEANUP-SESSIONS-2026-09-29.md
- to-cc/BATCH-CODESPACE-SECRETS-2026-10-04.md
- to-cc/BATCH-COMMON-B2-W1-2026-10-04.md
- to-cc/BATCH-COMMON-FOUNDATION-2026-10-03.md
- to-cc/BATCH-COMMON-HANDOFF-REDESIGN-BUILD-2026-10-01.md
- to-cc/BATCH-COMMON-HANDOFF-UNBLOCK-2026-09-30.md
- to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24.md
- to-cc/BATCH-COMMON-WAVE5B-N2-2026-09-25.md
- to-cc/BATCH-COMMON-WAVE5B-N3-2026-09-26.md
- to-cc/BATCH-COMMON-WAVE5B-N4-2026-09-26.md
- to-cc/BATCH-COMMON-WAVE5B-N5-2026-09-29.md
- to-cc/BATCH-COMMON-WAVE5B-N5-R-2026-09-29.md
- to-cc/BATCH-DECIDE-FALSE-POSITIVE-DEFENSE-2026-10-03.md
- to-cc/BATCH-DECIDE-FALSE-POSITIVE-DEFENSE-V2-2026-10-03.md
- to-cc/BATCH-DECIDE-MERGE-LATENCY-2026-10-05.md
- to-cc/BATCH-DECIDE-R59-REV3-2026-10-04.md
- to-cc/BATCH-DECIDE-THROUGHPUT-2026-10-03-v1-superseded.md
- to-cc/BATCH-DECIDE-THROUGHPUT-2026-10-03-v2-superseded.md
- to-cc/BATCH-DECIDE-THROUGHPUT-2026-10-03.md
- to-cc/BATCH-DECISION-AJ-M06-2026-09-28.md
- to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26.md
- to-cc/BATCH-DECISION-HANDOFF-REDESIGN-2026-09-30.md
- to-cc/BATCH-DECISION-HANDOFF-SYSTEM-2026-09-26.md
- to-cc/BATCH-DECISION-HANDOFF-SYSTEM-V2-2026-09-28.md
- to-cc/BATCH-DECISION-LANE-RUNTIME-2026-09-28.md
- to-cc/BATCH-DECISION-MEMORY-RESILIENCE-2026-09-27.md
- to-cc/BATCH-DECISION-OWN-TOOLS-2026-09-26.md
- to-cc/BATCH-DECISION-OWN-TOOLS-REVISION-2026-09-26.md
- to-cc/BATCH-DECISION-PROCESS-ENGINE-2026-09-29.md
- to-cc/BATCH-DECISION-REMOTE-OBSERVABILITY-2026-09-26.md
- to-cc/BATCH-DECISION-SELF-MAINTAINING-REPO-2026-09-29.md
- to-cc/BATCH-DECISION-TOKENS-AND-MERGE-2026-09-29.md
- to-cc/BATCH-ENV-GLOBALS-2026-09-23.md
- to-cc/BATCH-EVAL-CODEX-FALSE-POSITIVE-DEFENSE-2026-10-03.md
- to-cc/BATCH-EVAL-R59-V2-ROUND3-2026-10-04.md
- to-cc/BATCH-FOUNDATION-2026-10-03.md
- to-cc/BATCH-GEMINI-READ-DIAG-2026-10-03.md
- to-cc/BATCH-HANDOFF-BOOT-TEST-2026-10-03.md
- to-cc/BATCH-HANDOFF-CUT-2026-09-28.md
- to-cc/BATCH-HANDOFF-CUT-2026-10-06.md
- to-cc/BATCH-HANDOFF-REDESIGN-BUILD-2026-10-01.md
- to-cc/BATCH-HANDOFF-UNBLOCK-2026-09-30.md
- to-cc/BATCH-HARNESS-STATE-2026-09-30.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-27.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-29.md
- to-cc/BATCH-LAUNCH-SEATS-WAVE5B-N5-2026-09-29.md
- to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md
- to-cc/BATCH-MEMORY-DIAG-2026-10-03.md
- to-cc/BATCH-NIGHT-2026-10-04-v1-superseded.md
- to-cc/BATCH-NIGHT-2026-10-04.md
- to-cc/BATCH-NIGHT-AJ-BENCHMARKS-2026-10-03.md
- to-cc/BATCH-NIGHT-CONSOLIDATION-2026-09-30.md
- to-cc/BATCH-NIGHT-LESSONS-CEREMONY-2026-10-03.md
- to-cc/BATCH-ONBOARDING-CHECK-2026-10-02.md
- to-cc/BATCH-OPERATOR-QUESTIONS-2026-09-30.md
- to-cc/BATCH-P0-GATHER-2026-09-25.md
- to-cc/BATCH-PRECUT-VERIFY-2026-10-01.md
- to-cc/BATCH-RATIFICATION-PACK-2026-09-26.md
- to-cc/BATCH-RATIFY-PACKET-2026-09-29.md
- to-cc/BATCH-RECOVERY-WAVE5B-N2-2026-09-26.md
- to-cc/BATCH-REMOVAL-INVENTORY-2026-10-03.md
- to-cc/BATCH-REPO-CLEANUP-2026-10-05.md
- to-cc/BATCH-RESEARCH-HANDOFF-2026-09-24.md
- to-cc/BATCH-RETRO-DEBATE-HANDOFF-2026-10-02.md
- to-cc/BATCH-RETRO-WINDOW-2026-09-28.md
- to-cc/BATCH-REVIEW-LANE-REPORTS-2026-09-30.md
- to-cc/BATCH-ROW-BROWSER-SEAT-PROBLEM-2026-09-29.md
- to-cc/BATCH-SEAT-EXAM-GRADE-2026-10-04.md
- to-cc/BATCH-SPINE-STEP0-2026-10-04.md
- to-cc/BATCH-STATUS-CYCLE-2-2026-09-29.md
- to-cc/BATCH-VALUE-AUDIT-2026-09-29.md
- to-cc/BATCH-VERIFY-ANSWERS-2026-10-03.md
- to-cc/BATCH-VERIFY-CHECKLIST-2026-09-30.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24.md
- to-cc/BATCH-WAVE5B-N2-2026-09-25.md
- to-cc/BATCH-WAVE5B-N3-2026-09-26.md
- to-cc/BATCH-WAVE5B-N4-2026-09-26.md
- to-cc/BATCH-WAVE5B-N5-2026-09-29.md
- to-cc/BATCH-WAVE5B-N5-R-CYCLE-2-2026-09-29.md
- to-cc/BATCH-WAVE5B-N5-RECKONING-2026-09-29.md
- to-cc/BATCH-dispatch-order-2026-09-17.md
- to-cc/BATCH-night-2026-09-17.md
- to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md
- to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md
- to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md
- to-cc/DECLARE-OPERATOR-FEEDBACK-2026-09-24.md
- to-cc/DECLARE-SEAT-KNOWLEDGE-2026-09-24.md
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The outgoing seat's "why" is the filled SUPPLEMENT — a verbatim transcription of `to-cc/PLAN-HANDOFF-2026-10-04.md` v5 §4. **Read `to-browser/DIGEST-HANDOFF-ADDENDUM-2026-10-06.md` right after the SUPPLEMENT**: its eight open threads are not in §4.

**Open threads — FIRST: `main` carries NEW reds, and the B+ step-2 landing caused all of them.** Owner: row `[#1441]` (P1, the W2 first-wave integrator).
- **Pin.** This cut ran on `350c07f7`, the step-2 merge. Its completed CI run is **37790704091**, RED. The only first-parent commit between it and the green base run 37490604437 (`6d79ef0`) is that merge.
- **NEW tests, both OS** (`known_reds.py compare`: REGRESSION 3 against registry baseline 2026-10-04-fdf4f4952211):
  - `test_decision_coverage.py::test_the_live_rows_this_lane_filed_sit_in_its_id_block`
  - `test_funnel_lifecycle.py::test_live_tree_leg_c_measures_zero_so_arming_cannot_red_a_clean_tree`
  - `test_loop_declaration.py::test_the_fates_cover_every_organ_the_census_names`
- **NEW gate findings:**
  - ship-gate hard-fails rose from 14 to 28: 13 rows `[#1425]`-`[#1437]` with unresolvable `refs`, and `organ_truth` on `scripts/decision_carriage.py`.
  - commit-gate: orphan-census, edge-class-census and task-coverage on `scripts/decision_carriage.py` and its test.
- **Every other red is registered** (known-red or witness) **or was already red on the base run.** Every red is listed, each one marked, in `to-browser/DIGEST-CI-REDS-350c07f-2026-10-08.md`.
- **What BD-ci's "42 new red(s)" counts:** repeated names against the 2026-09-17 frozen suite baseline, not the registry. `[#1426]`, `[#1427]` and `[#1440]` own it. Nothing is masked (R59). Triage this before any dispatch.

**Then:**
- `archive/b2-w1-dispatcher-seat-row-cycle-22` — the unlanded B2-W1 dispatcher seat cost row. W2's first landing.
- `archive/b2-w1-13-codespace-subscription-auth` — W1-13, Codespace sign-in by subscription (R87, R88). Row `[#1423]` carries it (it supersedes `[#1376]`). Its first step is unsetting `CODEX_API_KEY` for codex and proving a served id.
- `to-browser/DIGEST-HANDOFF-ADDENDUM-2026-10-06.md` — **read right after the SUPPLEMENT.** It covers:
  - the THROUGHPUT ADR and the cloud-leg ADR (R75);
  - the removal engine, the retire list and the ceremony removals;
  - registry currency;
  - demo-prep's unpushed commits and the empty job directories;
  - the browser-seat memory file at its cap, and the user-level hook flag.

  Verify every status with CC before acting (R76).
- `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` — **read after the addendum.** It holds every failure of the readiness dry run, the twelve P13 decisions, and the three-part fix (R90). B+ step 2 filed them as:
  - `[#1425]`-`[#1434]`: tooling defects;
  - `[#1435]`: write-time validators;
  - `[#1436]`: the readiness gate;
  - `[#1437]`: the batch-close dispositions gate.
- **Filed at this cut:**
  - `[#1438]` W2-22 boot teaching: SEAT-LESSONS and the seat exam join HANDOFF_BOOT's reading path.
  - `[#1439]` R91: every transport file names its seat, with a per-seat index.
  - `[#1440]`: readiness pins the commit and a completed CI run across dry run and cut, and every gate condition must be satisfiable after the steps it gates.
  - `[#1441]`: the NEW reds above.
- The rest of §4's open-threads table stands as written there and is not restated here.

**Executor-side residue observed at this cut (witnessed):**
1. **The cut runs on the local date, 2026-10-08, with no `--date`.** BD-dates reads the local clock (`[#1425]`), so the cut-day files are dated 2026-10-08 (R90, `RATIFICATION-2026-10-08`).
2. **The condition "BD-ci equals dry run #2" was withdrawn** (RATIFICATION v2). Landing step 2 moved `main`, so that condition could never hold. Dry run #2 read `e2b9d4a7`; this cut reads the pin above (`[#1440]`).
3. **ADR-129's 120 s bound did not hold** (`[#1434]`): `--preflight-only` took 502 s wall-clock on this box at this cut (the readiness dry run measured 484 s).
4. **The v5 §4 transcription passes `assert_supplement_fixed_slots`**, checked before the finalising re-render.
5. **A background seat still has no sanctioned fill path** (`[#1433]`). This cut was made in the primary checkout on the bundle's branch, filled by scripts, with no linked worktree present.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
