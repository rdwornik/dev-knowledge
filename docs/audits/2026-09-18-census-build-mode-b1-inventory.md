# BUILD MODE B1 — inventory census and week zero of the ratchet

- **Date:** 2026-09-18 · **Batch:** B1 (inventory only) · **Ref measured:** `1a3910b0` (main)
- **Ordered by:** `DECLARE-BUILD-MODE-2026-09-18.md` §2 and §3 (transport, `to-cc/`), executed on the operator's word
- **Writes:** `protocols/BUILD-MODE.md`, `protocols/BUILD-LIST.md`, this audit. Nothing else.
- **Evidence labels:** WITNESSED = command run by the orchestrating seat; RELAY = a subagent's report, not re-run here.

## 1. Result

- Build list created with all 25 operator-enumerated subjects; `prior-art`, `delta`, `removes` filled for every row (B1 -> B2 gate, first half). WITNESSED (file).
- Delta tally: ARM 8 · WIRE 11 · REWRITE 5 · DELETE 1 · MOVE 0 · **BUILD 0**. WITNESSED (count over the rows).
- Week zero recorded in `protocols/BUILD-LIST.md` §Ratchet (B1 -> B2 gate, second half): mechanisms 171 · doc bytes 43,228,069 · organs 66 · uncalled organs 36 (PROXY) · open rows 386. WITNESSED.

## 2. B1's own acceptance test

"Twenty BUILD rows rather than roughly seven means the model is building again." Result: **0 BUILD** — the test's failure mode (too many BUILD) did not fire. The gap to "roughly seven" is explained, not hidden: the §6 B4 candidates (merge as mechanism, admission control, retirement as an organ, contracts in the repo, provider layer in the launch verb, consumer-repo contract) are NOT among the 25 enumerated subjects, and the one that overlaps (`merge`) has prior art — `scripts/merge_receipt.py`, `/ship`, `/lane-integrate`, live `block-ff-push` — so it is WIRE, not BUILD. Admission control likewise has prior art (`scripts/offload_admission.py`, unwired by design). **Residual:** the B4 candidates have not been inventoried as rows; they should be, before B4, under the same prior-art rule.

## 3. Method — organs first

Organs used: `graph_queries.py process-list --render`, `file_purpose_graph.py why|stats`, `ecosystem/organ-index.md`, `audit.py checks`, `audit.py governance-health`, `gen_task_tree.py --rank`, `.pre-commit-config.yaml` (hook register), `.claude/generated/` rosters, PLAYBOOK TOC. The `[#727]` deny-and-point hook refused the seat's one raw directory listing and pointed at the graph; the seat re-ran through the organ. Raw scans declared by legs: none (RELAY). The synthesis leg used `ls` on registry/devcontainer paths to confirm presence (RELAY — reported as "RAW-SCANS: none", which understates this).

| leg | model | subjects | subagent tokens | outcome |
|---|---|---|---|---|
| A | Haiku | backlog … BACKLOG (9) | 74,078 | 9/9 |
| B | Haiku | LESSONS … handoff (8) | 78,378 | 8/8 |
| C | Haiku | logs … load (8) | 67,149 | 6/8 — merged `integrator` + `merge`, skipped substrates |
| W | Haiku | week-zero numbers | 53,797 | FAILED — blocked by worktree isolation (see §5) |
| S | Sonnet | synthesis + verification | 90,249 | 25/25, 25 corrections to the Haiku legs |

Concurrency: 4 legs in parallel (cap 4). All legs under the 20-minute deadline (longest 301 s). No Opus subagent. The orchestrating seat itself ran on Opus (the session model); it dispatched, measured week zero with deterministic commands, and wrote the files — it did not synthesise the rows.

## 4. Corrections the synthesis made (RELAY, spot-checked)

- Every Haiku "removes: none" replaced with a concrete removal (25 rows).
- DDD/SDD/TDD BUILD -> REWRITE (prose and skill exist); naming ARM -> REWRITE; Python standards WIRE -> REWRITE; ARCHITECTURE MOVE -> DELETE (per §5 of the order).
- Leg C claimed `scripts/actions_verdict.py` an orphan to remove; the graph shows it imported by `scripts/merge_receipt.py` — kept, WIRE. Seat spot-check: the process-list render lists `actions_verdict.py` as "no trigger; wired to lane-integrate.md", consistent with "imported, not triggered". WITNESSED.
- `efficiency and performance` REWRITE -> WIRE (`context_reclamation.py` exists with no caller).

## 5. Deviations from the order — stated, not smoothed

1. **Token budget exceeded.** Subagent total 363,651 against a 200k budget (+82%), before the seat's own orchestration. Cause: Haiku legs spent ~50–80k each reading organ output; leg W burned 54k failing. Next inventory: cap per leg, and hand legs pre-rendered organ output instead of letting each re-run it.
2. **A worktree was used.** §3 says "NO WORKTREE — nothing mutates". The inventory legs mutated nothing, but the build list, rulebook and audit are writes, and the repo forbids commits on `main`; the harness also refuses edits in the shared checkout. The writes went to `worktree-build-mode-b1`. Side effect: entering the worktree bound the still-running subagents to it, and leg W — told to measure the primary checkout — was refused by the isolation guard. Week zero was then measured by the seat with deterministic commands at `1a3910b0` (the worktree base == main), so the numbers are exact for that ref.
3. **Uncalled-organ count is a PROXY.** No organ records invocations over a 30-day window. The proxy is "graph process with no trigger" (36). This is the first thing B2's `build-b2-brakes` should replace with a real counter; until then week-over-week comparison of this number compares proxies.
4. **Doc bytes** counts every tracked `*.md` at the ref, including immutable audits and handoffs — a large, mostly append-only base. A living-doc subset (ARCHITECTURE 110,357 · PLAYBOOK 500,165 · CLAUDE 24,571 B at `1a3910b0`) is recorded here for the B3 campaign.

## 6. Caveats for B2 — read before arming

- **About ten ARM/WIRE rows remove only a `stages: [manual]` override.** That is a thin `removes`; it is honest for ARM (switching on what exists removes the switch), but those rows do not shrink documentation bytes and so do not help the B2 -> B3 net-negative gate.
- **Arming those hooks reverses the 2026-09-17 emergency move to `stages: [manual]` ([#863]).** That move was made because hooks were measured broken or slow. Re-arming each needs the operator's word and a check that the cause is gone — recorded as a one-line decision in the build list.
- Rows whose prior-art is RELAY-only and not re-verified: `logs` (the `report-only-wall.yml` claim), `load` (`context_reclamation.py` "no caller" — consistent with the process-list render, WITNESSED).
