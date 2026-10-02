# Residual — 2026-10-02-dev-knowledge-architect — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-28-dev-knowledge-architect/` was added.

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
**`fleet_parity`** flags from the hub-INVERSE `settings-deny-and-point` row are a decision: the mechanism is working as ruled on 2026-09-19, and `[#727]` stays unwired. Any other `fleet_parity` or `reconciled_versions` flag is a defect.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
This is a terse map. The detail is in `JOURNAL.md` 2026-09-29..10-02 and in the transport digests
`to-browser/DIGEST-HANDOFF-REDESIGN-BUILD-2026-10-01.md`. Re-derive anything from `git log --first-parent main`.

- **The 2026-09-24 window's architect bundle** was cut and verified (`424d6c72`), and the R26 rows' provenance was fixed (R28).
- **WAVE5B-N5** merged and closed with these lanes: ratified-unbuilt (R18-R31 into STANDING_RULINGS), runtime-data-home-2 (R20), handoff-manifest `[#1123]`, handoff-probes `[#1124]`, scope-guard-2/-3 (the R15 PreToolUse guard), python-standard-2, read-gate, handoff-moments (seat-release as one refusing transaction, B1), hook-watchdog `[#863]`, handoff-boot-dispatch (**ADR-128 Accepted**, `[#1037]`), fates-due (R33.3) and claude-md-rulings (R32-R34; `[#1327]` filed).
- **HANDOFF-UNBLOCK** filed `[#1328]` `[#1329]` `[#1330]` (R42.2-R42.4) and merged them closed. It added a codex-review hub carrier, made `consumer_at_landing` read the merge receipt, and judges archived bundles in-era.
- **HANDOFF-REDESIGN-BUILD** (**ADR-129 Accepted**) gates the cut on `audit.handoff_organs()` in parallel. The whole-repository verdict is read from CI and never blocks, `--trial-cut` joins `moment:batch-close`, and `[#1331]` is filed. This bundle is ADR-129's first live cut.

**Carried WARN debt.** `journal_spine_anchor` is carried. It is dispositioned in `ecosystem/disposition-register.yaml` ("anchored by mention, not by record"; provenance `[#524]` leg c; review 2026-11-14) and is ADVISORY BY DESIGN. P7 re-derives the live WARN set. No WARN was silenced to make a gate pass.

**Carried questions** (`question_disposition` CARRIED leg). Each is named with the OPEN row that owns it:
- `QUESTION-github-private-now.md` ← `[#887]`
- `archive/2026-09-07/QUESTION-dispatcher-N2.md` ← `[#610]`, `[#642]`
- `archive/2026-09-07/QUESTION-dispatcher-T.md` ← `[#628]`
- `archive/2026-09-07/` ← `[#642]`: `QUESTION-integrator-N2-win-tooling-merge.md`, `QUESTION-lane-t-000-reds-spine.md`, `QUESTION-lane-u-000-adr-carrier-split.md`, `QUESTION-lane-u-000-branch-enum-parity.md`, `QUESTION-lane-u-000-carrier-floor-v150-mechanisms.md`, `QUESTION-lane-u-000-deploy-tool-consumer-override.md`, `QUESTION-lane-u-000-dispatch-receipt-is-work.md`, `QUESTION-lane-u-000-handoff-v71-build.md`, `QUESTION-lane-u-000-shape-spec-finalize.md`, `QUESTION-lane-u-628-release-commit.md`

**Carried decisions (`carried-by: OPEN`).** They are named here because the residual is their only carrier (P11 leg 2). Each one states an OPEN carrier and has no repo home yet. The next session either lands each one or re-declares the carriage:

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
- to-cc/BATCH-CAPABILITY-MAP-2026-09-25.md
- to-cc/BATCH-CLEANUP-SESSIONS-2026-09-29.md
- to-cc/BATCH-COMMON-HANDOFF-REDESIGN-BUILD-2026-10-01.md
- to-cc/BATCH-COMMON-HANDOFF-UNBLOCK-2026-09-30.md
- to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24.md
- to-cc/BATCH-COMMON-WAVE5B-N2-2026-09-25.md
- to-cc/BATCH-COMMON-WAVE5B-N3-2026-09-26.md
- to-cc/BATCH-COMMON-WAVE5B-N4-2026-09-26.md
- to-cc/BATCH-COMMON-WAVE5B-N5-2026-09-29.md
- to-cc/BATCH-COMMON-WAVE5B-N5-R-2026-09-29.md
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
- to-cc/BATCH-HANDOFF-CUT-2026-09-28.md
- to-cc/BATCH-HANDOFF-REDESIGN-BUILD-2026-10-01.md
- to-cc/BATCH-HANDOFF-UNBLOCK-2026-09-30.md
- to-cc/BATCH-HARNESS-STATE-2026-09-30.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-27.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-29.md
- to-cc/BATCH-LAUNCH-SEATS-WAVE5B-N5-2026-09-29.md
- to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md
- to-cc/BATCH-NIGHT-CONSOLIDATION-2026-09-30.md
- to-cc/BATCH-ONBOARDING-CHECK-2026-10-02.md
- to-cc/BATCH-OPERATOR-QUESTIONS-2026-09-30.md
- to-cc/BATCH-P0-GATHER-2026-09-25.md
- to-cc/BATCH-PRECUT-VERIFY-2026-10-01.md
- to-cc/BATCH-RATIFICATION-PACK-2026-09-26.md
- to-cc/BATCH-RATIFY-PACKET-2026-09-29.md
- to-cc/BATCH-RECOVERY-WAVE5B-N2-2026-09-26.md
- to-cc/BATCH-RESEARCH-HANDOFF-2026-09-24.md
- to-cc/BATCH-RETRO-DEBATE-HANDOFF-2026-10-02.md
- to-cc/BATCH-RETRO-WINDOW-2026-09-28.md
- to-cc/BATCH-REVIEW-LANE-REPORTS-2026-09-30.md
- to-cc/BATCH-ROW-BROWSER-SEAT-PROBLEM-2026-09-29.md
- to-cc/BATCH-STATUS-CYCLE-2-2026-09-29.md
- to-cc/BATCH-VALUE-AUDIT-2026-09-29.md
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
The outgoing seat's "why" is the SUPPLEMENT once it is filled. Until then the §13(d) beat fires in full. Executor-side residue, each item with its owning surface:

**1. CI is RED on `02fb225`** (BOOT-DATA `CI` row: 4 new reds, run 36979022044). The conductor digest shows push failures on the last three merges. ADR-127 makes CI the verdict, so triage these reds before dispatching anything.

**2. `actions_verdict.fetch_run` picks the wrong baseline run.** It read the *schedule* run of `a38b6faf`, not the push run, so a merge receipt's suite verdict can read REGRESSED falsely (JOURNAL 2026-10-02 (b)). This needs a row.

**3. The ADR-129 120 s bound did not hold on this box.** This cut's `--preflight-only` took 2m31s wall-clock. Either the acceptance test measures a different condition, or the bound fails under load. Settle that before treating ADR-129 as delivered.

**4. The OPEN-carrier list is outgrowing the paste ceiling.** It holds 127 `carried-by: OPEN` files, 43 of them `-superseded` versions, and it is inlined in full by the shed. The cold assembly measured 22,309 B against `PASTE_BYTE_CEILING` = 20,000. Options needing a ruling: (a) superseded versions take their successor as carrier on the transport; (b) the shed groups superseded versions; (c) the operator lands the closed batch orders to a repo home.

**5. `--trial-cut` is optional until 2026-10-05,** after which `moment:batch-close` requires it (ADR-129).

**6. The R15 scope guard falsely refused a `grep` regex.** At this cut the PreToolUse guard refused a Bash `grep -o` alternation token (`'+2 more\|to-cc/[A-Za-z0-9._-]*'`), normalizing it to a path under the excluded root. Scope-guard-3 (`9ec8aaf1`) was meant to stop refusing a regex that names no excluded root.

**7. `to-browser/PROBLEM-HANDOFF-CUT-2026-10-02.md` is the input to the next R50 retro+debate run.** Its H1-H6 are unvalidated hypotheses, not decisions. Validate each one before acting on it.

**R53 — the browser seat's rulings at this cut (technical, 2026-10-02):**
- (1) Paste ceiling: **re-ruled as option (c), and applied.** The 43 `-superseded` decision files that carried `carried-by: OPEN` were moved (not deleted) from `to-cc/` to `to-cc/archive/` on the transport. OPEN carriers went from 127 (43 superseded) to 84 (0 superseded), with 0 UNRESOLVED and 0 NO-KEY. Six other `-superseded` files were not OPEN and were left in place. A row for option (a′) is ruled and will be filed in the same landing as (2): P11 and the paste builder treat `-superseded` files as discharged.
- (2) P13: **re-ruled and landed** (`816c7f66`). Archiving removed 3 of the 8 from P13's population. The other 5 are disposed in `DECISION_DISPOSITIONS`, each with its actual closing evidence, and no new rows: `AMEND-BATCH-WAVE5B-N5` -> `to-browser/DIGEST-WAVE5B-N5-2026-09-30.md`; `AMEND-BATCH-WAVE5B-N5-R-CYCLE-2` -> `to-browser/STATE-BATCH-WAVE5B-N5-R.md` (CLOSED, cycle 2) and the cycle-2 integrator receipt; `AMEND-BATCH-LAUNCH-SEATS` -> launcher ce87636a, `to-browser/SESSION-launch-seats-2026-09-29.md`; `AMEND-HANDOFF-REDESIGN-BUILD` -> `to-browser/DIGEST-HANDOFF-REDESIGN-BUILD-2026-10-01.md`; `AMEND-INTEGRATOR-MERGE-PATH-withdrawn` -> refused in writing, withdrawn by R37.2. Two other changes landed in the same commit. The test's named-residual set was emptied, because R26's rows now cover all 16 subjects. The four N2 superseded dispositions the archive move made stale were removed. Row `[#1332]` is filed for option (a′).
- (3) Items 1-3, 6 and 7 above are recorded in this section.

**R54 — the `--filled` waiver covers the whole documented fill step (technical, 2026-10-02):** landed as `8f531a78`, merged as `24bc3d58`. PROBES.md joins `_BD_MANIFEST_FILL_SURFACE`, because `reflow_framing` rewrites it during the fill step. BD-ci and BD-seats may fail under `--filled` only when the recorded row passes an identity check: the CI row names the receipt's `source_sha`, and the Seats row carries a seat_health_line's shape. The waiver now requires every hard-fail to be `handoff_probes`, with a count equal to the bundle's own failing probes. The RED test reproduced this cut's refusal end to end. An isolated `claude-sonnet-5` review returned APPROVE with OPEN P1: 0. Its open P2: the BD-seats identity is shape-only, so a well-formed forged Seats cell passes the gate. That is mitigated because the same re-render rewrites the row from live state. Its open P3: the two tamper guard tests call the waiver directly rather than going through `generate`. A pre-existing red, `test_epic_bundle_has_no_failing_probe` ("assert 6 == 5", an epic bundle missing P11), fails identically on `main`.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
