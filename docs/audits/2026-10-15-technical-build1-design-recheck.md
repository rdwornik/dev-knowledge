# Archive copy of transport file DIGEST-BUILD1-DESIGN-RECHECK-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-DESIGN-RECHECK-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] e4769eafca010c34. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 step 1)
summary: verbatim Codex sol re-check of the outer-loop design rewrite (to-browser/DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md); VERDICT REJECT; dispositions in DIGEST-BUILD1-READY-2026-10-15.md.
served-model: gpt-5.6-sol
run: codex exec -m gpt-5.6-sol -s read-only, stdin closed; 2026-10-15T09:23:55Z-09:25:04Z; exit 0

# Design re-check (Codex sol), verbatim

```
SHA16: fcae08fc38973357
LINE3: by: design-outer-loop (Claude Code claude-opus-5-5 high; contract to-cc/BATCH-DESIGN-OUTER-LOOP-2026-10-14 v2)
O1 | HIGH | B2 is specified against nonexistent rulings R100-R108, so no carrier row or executable Done-when can be derived | evidence: protocols/STANDING_RULINGS.md:6307 — “There is no R100: the operator ruling batch BW's D7 waits on has not been given.” | fix: remove B2 until those rulings exist; do not file a speculative twin or claim R100-R108 coverage
O2 | HIGH | B4 does not complete [#689]: the row requires GitHub Actions, required checks, a SessionStart hook, and movement in four outcome metrics, while B4 builds a local doit loop and labels itself only “a step” | evidence: tasks/689-conductor-e-is-decided-and-unbuilt.md:12 — “Runner is GitHub Actions” and “Done when: the four numbers…move” | fix: either amend [#689] through an actual ratified ruling before design freeze or give B4 the row’s complete existing Done-when and required Actions surfaces
O3 | HIGH | B3 claims to carry [#863] in full but omits `scripts/billing_leak_sentinel.ps1`, even though the Done-when requires proving its ran-then-blocked mode and re-arming the sentinel | evidence: tasks/863-hook-processes-are-created-suspended-and-never-resumed.md:12 — “the billing-leak sentinel [is] re-armed only under (2)” and refs `scripts/billing_leak_sentinel.ps1` | fix: add the sentinel file and separate ran-then-blocked witness to B3’s scope, or stop claiming [#863] is carried in full
O4 | HIGH | B3 truncates [#912]’s Done-when: “45 ids green or owned” omits the required restoration of the integrator’s plain-green merge check with no paired-baseline subtraction | evidence: tasks/912-main-is-red-on-its-own-45-live-state-tests-fail-i.md:12 — “the integrator's merge check is plain ‘impacted set green’ again, with no paired-baseline subtraction” | fix: add that merge-check restoration and its test to B3’s Done-when and owned files
O5 | HIGH | B5 omits [#669]’s required named telemetry consumer; “telemetry consumer” is a placeholder, and neither the lane Done-when nor file list identifies an implementation that reads emitted telemetry | evidence: tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md:12 — “emitted telemetry has a named consumer that reads it on the merge leg” | fix: name the consumer, its input/output contract, owned module, and trip-test in B5
O6 | MEDIUM | The digest cites `dodo.py:4` as proof that doit stops at the first failure, but that line is module documentation and the actual ordering mechanism is the `task_dep` chain | evidence: scripts/dodo.py:330-345 — `task_stage` chains each stage to `prior_name`; `task_spine` depends on all stage tasks | fix: cite the dependency-chain implementation and add a witness showing a failed stage prevents the next stage from running
O7 | MEDIUM | The steel-thread “plant” validates only non-crashing cp1252 output decoded with replacement, so it cannot establish the claimed UTF-8 property and deliberately passes on base | evidence: tests/test_verify_handoff_probes.py:2929-2935 — stdout is decoded as `cp1252` with `errors="replace"` and only exit status plus summary are asserted | fix: keep the plant solely as a halt-control test and require the real RED test to assert strict UTF-8 bytes containing `→` before B6 is dispatchable
VERDICT: REJECT
```
