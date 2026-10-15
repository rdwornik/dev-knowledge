# Archive copy of transport file DIGEST-NIGHT-READY-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-NIGHT-READY-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] c94da28c42ee1242. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: the night-prep session (CC, Opus 5.5) for Tech-Architect-45, executing `to-cc/BATCH-NIGHT-PREP-2026-10-14.md` v4; nothing launched

# NIGHT-READY — batch NV (NIGHT-VERIFY-2026-10-14)

## Render verdict: GREEN (re-run on the transport copies, origin/main b46836c8)

- plan lint: `plan_lint.py check <6 contracts>` -> `plan-lint: no findings` (0 BLOCKING), exit 0
- contract dry-run: `dispatch.py plan --token-cap 2000000 <c>` -> exit 0 on 6 of 6; argv carries `-n <slug> --model claude-sonnet-5-5 --effort medium`
- queue dry-run: `dispatch.py queue --dry-run --batch NV --cap 6 <6>` -> 6 local lanes in priority order, exit 0
- also PASS: `lane-ceiling` (6 <= 6), `file-collision`, `carried-by`, `transport_lint check` (9 of 9 ok)

## Three deviations from v4 (code over prose, R41 / R105 D1)

1. **11 lanes -> 6.** `seat_refusals.py lane-ceiling` REFUSED 11 against ADR-110's ceiling of 6. Each lane carries one or two areas and still writes one digest per area, so the morning outputs are unchanged.
2. **Lane model Sonnet 5.5, not Opus 5.5.** `gen_lane_contract.py emit --kind text --model opus` REFUSED: "a 'text' lane ... declares 'opus': REFUSED at freeze ([#885] clause 2)". A verify lane changes no code, so calling it `code` would be false.
3. **R106: no new row.** `[#929]` (the spine is the whole work loop: map every organ, run the mechanisms live before anything is built) already owns this. V9 also cites `[#689]`; V11 cites `[#1450]`. Repo untouched; nothing committed.

## The lanes (all local, Sonnet 5.5 medium; checker = another vendor)

```
A lane-nv-929-a-dispatch-land       V1 dispatch, V2 land          [#929] [#689]  reads agy  checks codex gpt-6-astra
B lane-nv-929-b-ci-gates            V3 CI, V7 hooks+gates         [#929] [#689]  reads agy  checks codex gpt-6-astra
C lane-nv-929-c-handoff-transport   V4 handoff tools, V5 transport [#929] [#1450] reads agy checks codex gpt-6-astra
D lane-nv-929-d-telemetry-providers V6 telemetry, V10 providers   [#929] [#689]  reads agy  checks codex gpt-6-astra
E lane-nv-689-e-skills-engine       V8 commands+skills, V9 engine [#689] [#929] [#669] reads agy checks codex gpt-6-astra
F lane-nv-1450-f-handoff-gaps       V11 handoff/boot/process      [#1450] [#929] reads agy  attacks codex gpt-5.6-sol
integrator  Opus 5.5 low    collects only, writes DIGEST-VERIFIED-HARNESS-MAP-2026-10-15
dispatcher  Sonnet 5.5 low  queue --watch, cap = min(resource_lifecycle CEILING, 6)
```

Files: `to-cc/BATCH-NV-COMMON-2026-10-14.md`, `to-cc/INTEGRATOR-NV-2026-10-14.md`, `to-cc/DISPATCHER-NV-2026-10-14.md`, root `LANE-nv-*.md` (6).

## Before you paste

- 3 worktrees exist that this batch did not make: `green-main-2026-10-14` (locked, running), `codespace-finish-2026-10-14`, `system-map-2026-10-14`. The dispatcher's step 0 does not read them, so they do not block it. `lane-ceiling --check-worktrees` does refuse while they exist. PLAN r5 step 1 has those two sessions finish first.

## Pastes, in order (Ch8 row 3, INTERACTIVE: start `claude`, then the first message)

**1 — integrator** (new terminal, `.dev-knowledge` root):
```
claude --model claude-opus-5-5 --effort low
```
```
Read H:\My Drive\CLAUDE PROMPT DIR\to-cc\INTEGRATOR-NV-2026-10-14.md and execute it exactly.
```
See before paste 2: `no-live-integrator: PASS -- batch NV is received by integrator ...`

**2 — dispatcher** (second terminal, same root). This paste is the batch GO:
```
claude --model claude-sonnet-5-5 --effort low
```
```
Read H:\My Drive\CLAUDE PROMPT DIR\to-cc\DISPATCHER-NV-2026-10-14.md and execute it exactly.
```
See after it: six `[queue] FIRE lane-nv-...: job <id>` lines in `to-browser/SESSION-dispatcher-nv-2026-10-14.md`. Nothing else to paste. In the morning, read `to-browser/DIGEST-VERIFIED-HARNESS-MAP-2026-10-15.md`.

## Findings from the render (inputs for V1, V4, V7; nothing edited)

- `gen_lane_contract.py check` requires a bare alias (`sonnet`); `plan_lint.py` refuses a bare alias as BLOCKING (it "resolves today to claude-sonnet-5", not 5.5). The two gates cannot both pass. The versioned id was kept (the order's criterion, and the last batch's precedent).
- `seat_refusals.py dryrun-step0` refuses `templates/dispatcher-order-template.md` itself (`dryrun-absent`: it wants the retired PowerShell `-DryRun` token). Every order rendered from the template fails it. Not run as a gate here.
- The `emit` boilerplate trips `preflight_contract --freeze` in every contract: it cites closed `[#717]`, `register V-2` (no `### V-2` heading in STANDING_RULINGS), and an unwitnessed "measured".
- `plan_lint report` excludes `claude-sonnet-5-5` receipts as "[unknown-tier] ... names no model family this reader knows". The cost estimate reads UNDEFINED (n=0).
- `open-batch`: no committed manifest. That is correct tonight because nothing merges.
