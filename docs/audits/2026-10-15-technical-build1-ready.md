# Archive copy of transport file DIGEST-BUILD1-READY-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-READY-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 2bb1f4a0866fb79f. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5)
summary: BUILD-1 (batch BU) is frozen and ready to launch; nothing launched. Step-0 CHALLENGE: 3 parts INPUT_REQUIRED (R111, R112 List A, R113 confinement), the rest AGREE/AMEND. Design re-check REJECT, absorbed. Render green. Two pastes below.

# BUILD-1 READY - 2026-10-15

## CHALLENGE

Method: /decide, two non-producer evaluators (Codex gpt-5.6-sol: 54 findings; Grok grok-4.20-0309-non-reasoning: 23), four weighted matrices (unattended 20, code 15, library-first 15, model-agnostic 15, OS-agnostic 10, tokens 10, testable 10, simplicity 5). `decide_checks`: 0 defects on all eight runs. Evidence: `DIGEST-BUILD1-CHALLENGE-{EVAL1,EVAL2,M2-R113,M3-R114,M4-RUNNER,M5-L6,RESPONSES}-2026-10-15.md`.

| idea | verdict | why (evidence) |
|---|---|---|
| R111 Linux-first CI, Windows nightly (BUILD-2 row) | **DISAGREE -> INPUT_REQUIRED** | repo PUBLIC, standard runners free (ADR-127:13-15); last 7 d $0 (linux 3,579 min, windows 3,986); ADR-127 D1/D3 make `pytest (windows-latest)` a required context; a push path filter is refused by an existing conductor test; Windows leg 26.5 min < the 40-min flip. Row NOT filed. The OS-agnostic half: AGREE (already ADR-127). |
| R112 List A deletions | **DISAGREE -> INPUT_REQUIRED** | every item is live by R112's own caller rule: one ruff hook only (`.pre-commit-config.yaml:824`); plugin `validate_backlog.py` is the ADR-78 carrier twin with a parity test; aider/llm/amp are asserted negative probes (`tests/test_provider_bench.py:433-438`); `terra` is a deliberate report-only signal pinned by `tests/test_conductor.py:709-719`. Lists B/C: AGREE (BUILD-2). |
| R113 "agy read-only, worktree/job tmp only" | **INPUT_REQUIRED** | unenforceable: agy wrote into `~/.gemini/.../scratch` (627 re-adjudication :280-300, :498-509). Accept the residual risk, or require `--sandbox` (unprobed). |
| R113 / L2 agy route | AMEND | agy 1.3.5 has `--dangerously-skip-permissions`, no `--yolo`; live probes: in-cwd reads work in every mode, an out-of-workspace read is auto-denied in plain mode and works with `--add-dir` -> V10/V11 failed on workspace, not permission. `read_gate.py:375-381` already passes bypass; registry already routes read agy -> Copilot -> Sonnet. No new route; declare the workspace. |
| R114 / L1 distiller + point tasks | AMEND | extend `gen_lane_contract distill` (reads BUILD-LIST today -> must read `tasks/`), compose existing organs (`bounded_hook.py` tree kill, read_gate, decide_checks); completion = FRESH payload (nonce, input hash, mtime after spawn), exit recorded, not required; no reviewer = INPUT_REQUIRED. |
| R115 sequence (BUILD-3 trials, then consumer) | AGREE | nothing built in BUILD-1; the import-linter trial must test ADR-124's flip condition. Codex's consumer-first objection rejected: operator's standing order. |
| Runner | AGREE (a) | conductor + doit + pydantic 3.55 vs e 3.35; V9: doit gates natively; python-statemachine stays behind the `[#669]` spike. |
| Lane split | AMEND | L5 starts after L6; L2 after L4 kept; steel thread `[#1430]` -> BUILD-2 slot 1. |
| L3 | AMEND | List A, terra, Linux-first out; concurrency already exists (`conductor.yml:87-89`) -> replaced by `[#1540]` (schedule run cancels main's push verdict); `[#863]` (incl. `billing_leak_sentinel.ps1`) and `[#912]` in full. |
| L4 agy sign-in | AMEND | official docs: CLI prints a URL, browser shows a code, operator pastes it BACK into the remote prompt -> needs a return channel; bounded file-observed wait, tree kill on timeout. |
| L5 rulings | AMEND | by id from their own files: R100 exists (RATIFICATION-2026-10-13:42; register says "no R100"), no R103 anywhere, R102/R104-R110/R112 only in superseded files; boot teaches only mechanisms on main. |
| L6 transport | AMEND | mostly exists; `_after_write` trigger fails open and INDEX is stale (writers bypass it); `query` gains `--since`; status derived from answer records; janitor `--apply` only with an operator-reviewed `--expect-manifest`. |

## Failures and defects found

- **Design re-check (step 1), Codex sol: `VERDICT: REJECT`** (verbatim: `DIGEST-BUILD1-DESIGN-RECHECK-2026-10-15.md`). Changed: O2 -> `[#1535]` is a step, `[#689]` stays open; O3/O4 -> L3 carries `[#863]`/`[#912]` in full; O5 -> `[#669]` consumer to BUILD-2 (intake 110); O6 -> L1 cites `dodo.py:330-345`; O7 -> steel thread BUILD-2. O1 rejected (R100 exists) -> `[#1538]` by id.
- lane-ceiling `--check-worktrees` REFUSED: it counts this prep worktree. Without the leg: PASS 6 <= 6. The dispatcher reruns it after the freeze lands.
- `seat_refusals file-collision` reads paths only inside `## Done-contract`; first render declared 12 paths, L6 none. Fixed (46 paths).
- `gen_lane_contract emit` only offers bare model aliases, which plan lint refuses; `emit --stdout` writes cp1252 (`[#1430]` class). Contracts post-edited to `claude-opus-5-5`.

## Rows filed (intake 110)

`[#1535]` L1 outer-loop step + ADR-130 · `[#1536]` L2 R104 routing · `[#1537]` L4 Codespace finish + agy sign-in · `[#1538]` L5 rulings by id · `[#1539]` L6 inbox/derived status/INDEX · `[#1540]` L3 concurrency group. `[#669]` -> `[#664]` waiver PROPOSED (needs your ratification). Commits on `worktree-build1-prep-2026-10-15` (pushed): `0c8b495d` rows, `8b2b2fed` manifest, `4432daaa` index, `7437920e` JOURNAL anchor.

## Render verdict: GREEN

plan lint no findings · `dispatch plan` x6 exit 0 · `queue --dry-run` exit 0 · file-collision PASS · lane-ceiling PASS (see above) · carried-by PASS · transport lint ok (18 files).

## The six lanes (all claude-opus-5-5, LOCAL)

| lane | rows | effort | Done-when (short) |
|---|---|---|---|
| L4 `lane-bu-1537-codespace-finish` | 1537 | high | schema token stripped + smoke-tested, pin before create, scratch cleanup, agy sign-in link |
| L1 `lane-bu-1535-outer-loop` | 1535 | high | `run_phase` tree kill + fresh payload, phases P1-P7 via doit, PhaseReceipt, constraints, distill, CHALLENGE, ADR-130 Proposed |
| L3 `lane-bu-863-prompts-guard` | 863 912 1540 | high | why hooks start suspended + watchdog; 45 ids green or owned, plain merge check; schedule/push in separate groups |
| L6 `lane-bu-1539-transport` | 1539 1454 1332 | medium | `query --since`, ANSWERED by answer record, INDEX fresh, `by:` lint, superseded discharged |
| L2 `lane-bu-1536-routing` | 1536 | medium | implement Copilot-first, red/qa/judge roles, 5-5 prices, one model-id source |
| L5 `lane-bu-1450-boot-v2` | 1450 1538 | medium | HANDOFF_BOOT R80 order + INDEX first read; R100-R115 by id |

**Land order:** L4 -> L2; L6 before L5; L1 and L3 as ready. L2 starts after L4 MERGED; L5 after L6 MERGED.

## Operator pastes

1. In a new terminal at `C:\Users\1028120\Documents\Dev\.dev-knowledge`: `claude --model claude-opus-5-5 --effort medium`, then paste:
   `Read and execute H:\My Drive\CLAUDE PROMPT DIR\to-cc\INTEGRATOR-BU-2026-10-15.md`
   **Wait for** `FREEZE-LANDED <sha> <time>` in `to-browser/SESSION-integrator-bu-2026-10-15.md`.
2. Then, in a second new terminal at the same folder: `claude --model claude-sonnet-5-5 --effort low`, then paste:
   `Read and execute H:\My Drive\CLAUDE PROMPT DIR\to-cc\DISPATCHER-BU-2026-10-15.md`
   **Wait for** `[queue] FIRE lane-bu-1537-codespace-finish` in `to-browser/SESSION-dispatcher-bu-2026-10-15.md`.

## Your decisions owed (none blocks the pastes)

R111 Linux-first (keep ADR-127, or rule a ruleset migration) · R112 List A (keep, or name what to delete despite its callers) · R113 agy confinement (accept, or require `--sandbox`) · `[#669]` waiver (intake 110).
