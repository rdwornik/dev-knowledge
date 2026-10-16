# Archive copy of transport file DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 4478da1f15adad7a. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
supersedes: none
summary: S3 (T2). UC1-UC10: 0 GREEN, 2 PARTIAL, 8 RED. Codespace spec: 0 PASS, 3 PARTIAL, 3 RED, 1 NOT RUN. Codex sol and Grok attacked; UC11 and a scoreboard file dropped; portability re-scoped to the consumer. Rows [#1551]-[#1555] + intake 112 on branch worktree-define-outcomes-2026-10-15 (69ab3bc9, pushed), landing with the next freeze.
by: CC session S3 (Claude Code bg job cae209ca, claude-opus-5-5), for Tech-Architect-45

# OUTCOME SCOREBOARD — 2026-10-15

Statuses come from existing evidence only (no double analysis): the two LANE-ENDs of 10-14, HOW-WORK-RUNS (G1-G15), VERIFIED-HARNESS-MAP, BUILD1-READY, REVIEW-SEAT-CHECKLIST-10-10, the 10-13 probes audit. No BUILD-1 lane has landed yet.

## 1. Scoreboard

| UC | Acceptance test (evidence) | Today | Carriers |
|---|---|---|---|
| UC1 ask -> row, no hand id | a file verb turns an ask into `tasks/<id>-*.md` plus its manifest node in ONE commit; the id comes from the single allocation authority ([#804] manifest); two concurrent filings get distinct ids; `gen_task_tree --check` exit 0 (row + manifest diff) | RED: "No verb files a row; ids are allocated by hand" (HOW-WORK-RUNS G11) | [#580], [#788], [#804]; BUILD-2b G-4 (after the ADR-122 ruling) |
| UC2 row starts a lane by itself | open row N -> `distill` reads `tasks/N` -> `dispatch.py queue --watch` fires it; the launch receipt's REQUESTED and SERVED model (served-id witness), vendor and substrate equal the route, any fallback recorded | PARTIAL: the queue fires a frozen contract by itself (BU L4); distill refuses a repair task (G2), one model per lane (G3), router lacks roles (G4), launch admits claude/codex only (G8), no cloud (G12) | [#1535](5), [#1536], [#804], [#669]; cloud verb (BUILD-2b) |
| UC3 isolated phases, operator reads headers | steel thread D6 on [#1430]: P1-P7 via `conductor.py lane --round r`; a PhaseReceipt per phase; the planted RED ("a redirected cp1252 run exits 0", DESIGN:115) halts at P2; a never-exiting vendor is KILLED; the row closes on main; the operator's view is `transport.py query --since` | RED: the 7-stage chain has run only BY HAND (green-main LAND r2; codespace-finish REFUSE); G3, G13, G14 | [#1535] (L1) -> steel thread (BUILD-2 slot 1), [#669], [#1539] |
| UC4 night integrates, morning green + one digest | every night handback reaches a terminal LANDED or REFUSED through `merge_path.py land`, with no seat paste; at 07:00 laptop time the newest conductor push run on main HEAD is green on both legs, and `ci_verdict` with a baseline shows 0 outside the registry; ONE digest lists every lane | RED: integration is a pasted seat with operator cycles (LEDGER v204); conductor push runs on b6161972 failed x3; 12 false reds without a baseline ([#1534]); R119 starts at BUILD-2 | R119 tiered CI (BUILD-2a), [#1534], [#1540], [#939], seat auto-start US-5 (unfiled) |
| UC5 a lane runs in a Codespace end to end | section 2: items 1-5 on 3 consecutive fresh runs (R63 e), then 6 and 7 | RED: in the 10-14 outcome test, its steps 1, 2 and 7 PASS (create, credentials, delete) and steps 3-6 FAIL (top-level `allOf` refused by the API) | [#1537] (L4), [#1366], [#1453], [#1551]-[#1553], [#1555] |
| UC6 a new seat boots and knows the process | the seat answers DIGEST-SEAT-CHECKLIST, regenerated from main; an isolated CC and a blind other-vendor grader grade it; pass = >=36/39 and every star item | RED: "VERDICT: FAIL — CC 33/39, ★ 20/25; Copilot … 28/39" (REVIEW-SEAT-CHECKLIST-2026-10-10); handoff gaps Given 0 / Partial 6 / Missing 2 | [#1450] + [#1538] (L5), the handoff generator rows (BUILD-2b) |
| UC7 removal takes its tests; tests prove outcomes | (a) night census, coverage contexts plus the graph: ORPHAN = a test whose covered lines have no non-test caller -> 0; (b) planted: a seeded module and a test that covers only it; deleting the module is refused at pre-commit; (c) separately, the mutation score on changed code is >= 70 % (R120) | RED: tests are not in the graph; mutmut 863/2077 killed (~41 %); S2 measures today | R120 build (BUILD-2a; rows owed by S1's ADR), S2 data |
| UC8 cost of every task visible | for a closed row: one line of tokens and USD per phase and vendor, plus core-hours, from receipts; a vendor with no price shows its native unit and a reason, outside the USD total | PARTIAL: Claude tokens per lane OK; 5-5 models UNPRICED (V6 BROKEN); `ordered_model`/`ran_model` empty; Copilot and Codex USD not exposed | [#1536], [#893] (amendment owed: the per-row line), [#694] |
| UC9 duplicate stopped at the front | at distill, before any id: a seeded ask duplicating an open row is refused, naming `[#id]`; a seeded duplicate ORGAN is refused ([#1535] (6)); a near-miss passes | RED: no distiller; duplicates are caught by review (REVIEW:215, "[#615]"); `reuse_gate` acts at write time only | [#1535](5)(6), [#1554], R118 admission (BUILD-2) |
| UC10 a corp-monorepo task through the loop | ADR-123 step-2 exit: corp-monorepo pins `v1`, runs `harness install` and one lane in its own codespace, "merged 3/3 with gates armed and zero hub calls"; the hub only publishes the package and reads the evidence | RED: never attempted; only P-1..P-3 PASS with a stand-in package (2026-10-13 audit) | [#1555] (step 1), then a corp-monorepo-owned row; [#670] |

**Rule** (the order's): a batch item that moves no UC toward GREEN waits. AMENDED after the adversaries: the browser applies it when planning a batch. It is not a code gate, and it does not apply to defects on main, to safety work, or to the prerequisites a UC carrier names. A row may carry `moves: UCn` for traceability only.

## 2. Codespace acceptance spec (UC5)

GREEN = items 1-5 on 3 consecutive fresh runs, no NOT-RUN leg (R63); then items 6 and 7 once. Sources: CODESPACE-PARITY-DEFINITION-2026-10-03 (cited 10-10 by TA-44; no 10-10 version exists), R63, R6 (09-25).

| # | Check (executable) | Today (LANE-END-codespace-finish) | Missing |
|---|---|---|---|
| 1 Container parity | the devcontainer declares claude, gh, codex, copilot, grok, agy, rclone and uv at COMMITTED versions (`.devcontainer-lock.json`); `uv sync --locked` exit 0; `codespace_parity.py check` -> C1-C5 PASS, C1 comparing the declared, laptop and box versions | PARTIAL: C1 FAIL (copilot 1.0.98 vs 1.0.97, laptop auto-update), C2 PASS 0/599, C3 FAIL, C4 PASS, C5 FAIL | [#1537](4); the laptop's copilot auto-update must be pinned or declared |
| 2 Credentials | a fresh box answers a read-only probe per tool (a nonce per model CLI, `gh auth status`, `rclone lsd`), no operator step except the agy link; a register of class, issuer, expiry and renewal act; no `*_API_KEY` secret (R87) | PARTIAL: claude, codex, copilot, gh seeded; agy GAP, no URL ever shown; codex refresh never witnessed; a `CODEX_API_KEY` user secret exists | [#1537](7)(8), [#1552]; deleting the secret is an operator act |
| 3 Process parity | the UC3 steel thread with `substrate: codespace`: the same phases, receipts and gates; land through `merge_path.py land` (C3 PASS) | RED: no Codespace lane has ever committed; C3 has never passed | [#1537](8), [#1535], [#1366] |
| 4 Monitoring + self-repair | a heartbeat every 60 s, read by `codespace-observe` every 60 s. Detect and recover: (a) producer killed, 2 min, re-run the phase once; (b) claude killed, 2 min, same; (c) network dropped, 5 min, back off then stop/start after 15 min; (d) credential expired, at the failing call: codex re-mirror, claude OPERATOR-ACTION (the exception); (e) box deleted, 5 min, re-provision from the last pushed commit; (f) disk full, 5 min, prune then re-provision. N values are budgets measured by the first run. RED first on sandbox fixtures; the live destructive run needs the operator's GO | RED: no phase heartbeat or timeout (GAP 2, G14); observe reads once; only "the finish gates FAIL a lane that did no work" witnessed | [#1551] |
| 5 Harvest + teardown | stop -> harvest (manifest has `handback.json`) -> manifest-gated delete; C5 PASS; `no_leftovers verify` CLEAN; ledger uptime, core-hours, USD | PARTIAL: delete PASS, 5.14 core-hours measured; no `handback.json`; C5 FAIL (scratch branch) | [#1537](5)(8) |
| 6 Concurrency | 2, then 6 lanes, each with its own heartbeat; `quota_watch.py check` before each launch; a 15 core-hour probe cap | NOT RUN. 130.62/180 left; 6 x 4-core = 24 core-h/h; GitHub documents no per-user cap for personal accounts | [#1553] |
| 7 Portability | items 1-5 for corp-monorepo, run BY the consumer from the shipped package; the hub reads evidence | PARTIAL-0: P-1..P-3 PASS in a corp-monorepo box (no lane, no `.devcontainer/`) | [#1555], then the consumer's row |

`codespace-exec` already sets `--idle-timeout 240m --retention-period 24h` (`dispatch.py:1912-1929`); 240 min is GitHub's maximum, and item 4 covers a lane that is silent longer than that.

## 3. Adversaries (Codex gpt-5.6-sol attested; Grok grok-4.20-0309-non-reasoning, from the draft text only)

Codex counts by block: 2 AGREE / 14 AMEND / 12 DISAGREE (its own tally line says 19). Grok: 17 / 1 / 10 (its line says 13/2/13).

| Item | Objection | Answer |
|---|---|---|
| UC3 | Codex: [#1430] is a cp1252 bug, not the steel thread | REJECTED: D6's payload is [#1430] (DESIGN:115); status lowered to RED (Grok) |
| UC10 B7 P6 P9 | Codex: hub landing on corp-monorepo breaks Layer 2 | ACCEPTED: consumer runs ADR-123 step 2; P6/P9 dropped; [#1555] filed |
| UC11 | both: vacuous; duplicates [#658] | ACCEPTED: dropped |
| RULE | Codex: blocks defect/safety/prerequisite work | ACCEPTED: amended. Grok's Layer-2 reading REJECTED |
| P1 | both: a second status register | ACCEPTED: dropped |
| B4 | Codex: no receipt to resume, unpushed work lost, revoked auth, DROP privileges; Grok: N arbitrary | ACCEPTED: re-run from phase start, push first, claude = OPERATOR-ACTION, N measured, sandbox then live GO |
| B1 / B5 / B6 P5 | lock records drift / stop-harvest-delete / no abort budget | ACCEPTED (B5: the manifest gate is the authorization) |
| UC7 / UC8 | orphan oracle wrong / fake zero prices | ACCEPTED: caller-defined orphan; native unit + reason |
| P3 P7 | duplicate [#1537](4), [#893], [#1536] | ACCEPTED: not filed; grok passed C1 on 10-14 (10-10 note stale) |
| UC1 UC2 UC4 UC5 UC9 B2 P2 P4 P8 | Codex AMENDs | ACCEPTED, folded in |
| UC1 B1 B2 B6 | Grok: "untestable today" | REJECTED: RED status is not an unexecutable test |

## 4. Rows filed (intake 112, branch `worktree-define-outcomes-2026-10-15` @ 69ab3bc9, pushed, all gates passed)

[#1551] P1 heartbeat + six injected failures · [#1552] P2 credential register · [#1553] P2 concurrency 2 -> 6 · [#1554] P2 duplicate ask refused at distill (T2) · [#1555] P2 ADR-123 step 1. The ids leave 1541-1550 and intake 111 free for the BU lanes and S1. They land with the next freeze, which needs a JOURNAL anchor at the merge.

## 5. Questions for the operator

1. **Live destructive injections ([#1551] item 4):** one GO per spec run, on throwaway boxes, covering deletion, token revocation, a network drop and a full disk? **Recommend YES**, counted as the "destructive acts" human point.
2. **Claude's credential:** the setup token needs a browser (about one year per third-party guides; the docs state no lifetime). Accept a dated OPERATOR-ACTION 30 days before expiry as the second standing exception beside the agy link? **Recommend YES.**
3. **The rule "moves no UC -> waits":** a browser planning rule with the three exemptions, or a code gate? **Recommend the planning rule** (both adversaries opposed a gate).

## 6. Usage, vendor defects and sources

- SUBSTITUTION: agy -> Copilot. agy said `SUCCESS`, empty, after a 14-min timeout (307k tokens). Copilot: 34.26 credits, served id UNATTESTED, 4/4 sampled quotes literal.
- Codex: `-s read-only`, stdin closed, 102 s, 196,012 in (137,600 cached) / 4,451 out.
- PREMISE-FAILED, Grok `--max-turns 2` in the repo cwd: runs 1-2 spend both turns on tools, empty ($0.089); run 3 config error, no call; run 4 (empty cwd, `plan` mode) answered in 1 turn ($0.027).
- This seat: not measurable (bg).
- Web: docs.github.com (idle timeout 5-240 min, per-user policy); containers.dev (devcontainer lockfile); developers.openai.com/codex/auth; setup-token lifetime third-party only.
