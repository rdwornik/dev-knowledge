# Archive copy of transport file DIGEST-HANDOFF-GAPS-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-HANDOFF-GAPS-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 1f7e731abd83315d. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-1450-f-handoff-gaps (Sonnet 5.5), base b46836c8; V11 of batch NV. Reading was Copilot (claude-sonnet-5.5), NOT Gemini: SUBSTITUTION below.

# DIGEST-HANDOFF-GAPS — what a fresh seat must know vs what boot and bundle give

Headline: the seat cycle is mostly given. The **flow (Conductor E)**, the **reading rule**, the **per-substrate start lines** and the **dated rulings** are not. The 10-14 bundle also still carries unfilled FILL-INs.

## Q1/Q2 — one row per item (G=given, P=partial, M=missing)
| # | item | v | evidence | fix | carrier |
|---|---|---|---|---|---|
| 1 | flow (Conductor E, #689/#669) | M | no hit in the bundle, protocols/HANDOFF_BOOT.md, PROCESS, README; flow taught only as lane-HANDBACK-serial merge, protocols/HANDOFF_BOOT.md:178-210 | FLOW row from the conductor registry | boot v2 [#1450] |
| 2 | substrates + start on each | P | bundle HANDOFF_BOOT.md:24 lists them; local `dispatch <FILE.md>` SEAT-BOOT-dispatcher.md:199; codespace "launch it yourself" dispatcher-order-template.md:60; no cloud start line anywhere; PROCESS:238-246 local only | one start line per substrate | boot v2, R103 |
| 3 | seat cycle | P | order+serial land protocols/HANDOFF_BOOT.md:191-209; lane stop SEAT-BOOT-lane.md:42; rotation integrator-order-template.md:167-173 (3 h) vs dispatcher-order-template.md:120-127 (2 h); none for the architect seat | role-by-role cycle; reconcile 3 h/2 h | boot v2 |
| 4 | plan, ledger, maps | P | plan+ledger protocols/HANDOFF_BOOT.md:34-35; map only the /map skill, RESIDUAL.md:52-54 unfilled; no MAP-DISPATCH pointer | Plan/Ledger/Map rows | boot v2 |
| 5 | reading rule agy first, <=20 KB/turn | M | only "about 20 KB per review" SUPPLEMENT.md:73; route shown bundle HANDOFF_BOOT.md:30-31, no rule | state it in BOOT-DATA | boot v2, R103 |
| 6 | operator standing rules | P | pointer protocols/HANDOFF_BOOT.md:32; scattered integrator-order-template.md:30-31, SUPPLEMENT.md:148-151 | generated STANDING block | boot v2 |
| 7 | open rulings + dates | P | R100-R102 not landed, bundle HANDOFF_BOOT.md:24-27; "next dated fates none" :28 while ecosystem/harness.yaml:105+ has manual_until 2026-10-19 rows | date-carrying ruling rows | boot-drift gate |
| 8 | main red: triage first; BW-FINISH practice | P | red-first given protocols/HANDOFF_BOOT.md:85-86; BW-FINISH practice absent (ANSWERS:234) | add the practice line | boot v2 |

## Q3 — stale and contradictory
- Version: only 7.1.0 is current (PROCESS:10). v5/v6 live-looking: PROCESS:58 ("In v5/v6"), :289-305 (v6 per-probe boot), :932 (`/handoff v5 <mode>`), :964 ("A v5 bundle carries four"); README:32, :85 ("P0 (v6 bundles)").
- R30 conflict: README:130 "browser does not run the gate at boot" vs README:84, PROCESS:289+, bundle HANDOFF_BOOT.md:51-53.
- Four seats: protocols/HANDOFF_BOOT.md:173, PROCESS:64-75, README:268 vs one chat per window (bundle Forms card 6). Five SEAT-BOOT-*.md ship; nothing says which one the architect reads.
- Queue verb: SEAT-BOOT-dispatcher.md:199 `dispatch <FILE.md>` vs dispatcher-order-template.md:49 `queue --watch` vs protocols/HANDOFF_BOOT.md:198 "one-shot, not --watch".
- Model: SEAT-BOOT-dispatcher.md:229-231 routes opus by default vs R101 (SUPPLEMENT.md:85).
- Dead: scripts/seed_runbook.py (README:14, PROCESS:977) absent; DIGEST-HOW-WORK-RUNS not on transport; DECLARE-BROWSER-TOPOLOGY sits in to-cc/, cited as to-browser (BOOT:140). VISION.md (PROCESS:704, 1139) is disputed: see Codex.
- Unfilled: bundle HANDOFF_BOOT.md:36-37, RESIDUAL.md:45,53,61, PASTE_THIS.md:73 (spot-checked: P0c in PROBES.md:19 wants Purpose filled).
- Generator prose: 6,324 of 12,972 B of the bundle HANDOFF_BOOT.md repeats byte-identical in all four bundles (Forms 0-6, teardown, filename grammar).

## Q4 — generator gaps (scripts/gen_handoff.py, found by grep -n)
- `grep -inE "conductor|substrate|dispatch.map"` hits only comments (:121, :820, :2167): no code writes Flow or maps.
- `boot_data_rows` :2519 writes Slug..Harness plus `state_rows`; Substrates is already a state row (handoff_state.py:223 `row_substrates`). Add Flow/Reading/Standing/Map rows there or in handoff_state, one authority.
- `dispatch_form` :2310 — per-substrate start lines.
- `standing_vs_new` :2256 — dated rulings.
- `detect_fill_state` :2337 / `_splice_fill_regions` :2469 — purpose/destination FILL-INs never derived.
- `_write_seat_boots` :3067 — emits five boots with no "architect reads this" marker.
- `_render` :2887 — repeated Forms prose should become a pointer.

## CODEX OBJECTIONS (listed separately; not merged)
- CRITICAL: the bundle fails its own boot contract (unfilled Purpose HANDOFF_BOOT.md:37, PROBES.md:19 P0c; destination :38; RESIDUAL.md:45,53,61). Promote above stale notes.
- Item 2: the registry row lists FOUR substrates, not three; the fix needs four start lines.
- Item 8 NO is wrong: red-first is given at protocols/HANDOFF_BOOT.md:85-86 (adopted above as P).
- Item 3 YES unsupported: cycle exists only for integrator and dispatcher, 3 h vs 2 h (adopted above as P).
- VISION.md is not dead: PROCESS:704 re-pointed, :1139-1144 documents the hub relocation. (Not adopted; both readings stand.)
- Generator: Substrates is a delegated state row; do not duplicate it (adopted in Q4).
- ANSWERS:237 is not a bundle locator; cite ecosystem/harness.yaml:105+ (adopted in row 7).
- README:32 and PROCESS:964-978 are qualified, not flat contradictions (not adopted; both readings stand).

## CHECKER
vendor: OpenAI via codex exec. Served model, from the tool's own header: gpt-5.6-sol (reasoning effort low); the answer text called itself "GPT-5 Codex". Content hash returned: c22b1e1fab. Session id 01a13c5b-be1f-7183-b75d-11b14fb65cba. Spot-checks I ran: PROCESS:932,964 and README:32,85 confirm; protocols/HANDOFF_BOOT.md:85-86, handoff_state.py:223 and PROBES.md:19 confirm Codex.

## USAGE
- Claude: lane_cost 35 calls, 3.52 M tokens (claude-sonnet-5-5, UNPRICED, USD not shown).
- agy: 1 call, gemini-3.8-flash-high, empty at the 600 s timeout (process killed).
- SUBSTITUTION: agy -> copilot for both reads; Copilot served claude-sonnet-5.5 per its log. Not a different vendor, so it does not count as the check.
- Codex: 1 call, 85,466 tokens.
