# RESULT -- lane-dz-0-m1-model-probe -- PARTIAL (2026-10-18)

Base sha: `d8aa4dd73f43d1e69e633995feda80f37c8b1927`. Budget: USD 8. Summed measured USD: **0.00** (ledger: `ledger.jsonl`).

## Why PARTIAL

The 12 Claude cells and the blind grading did not run. Headless `claude -p` is **not logged in** in this session's tool
shell (`claude auth status`: `loggedIn: false`; every call returned `Not logged in · Please run /login`, USD 0).
The runner had `CLAUDE_CODE_OAUTH_TOKEN`, but it is not in the tool shell's environment, and this lane did not go looking
for it in another process. Evidence: `facts/NOTES.md`, `facts/effort-*.json`. Nothing below is estimated.

What ran: the facts check (partial), the four tasks with their keys and deterministic checks (each check validated with a
good and a bad control), the driver `probe.py`, and the one Copilot cell (task b).

## Cells (quality = blind grade 0-3; check = deterministic)

cell: task a haiku-5-5 highest accepted effort | quality: NOT RUN | check: NOT RUN | USD: NOT RUN
cell: task a haiku-5-5 default | NOT RUN
cell: task a sonnet-5-5 default | NOT RUN
cell: task b haiku-5-5 highest accepted effort | NOT RUN
cell: task b haiku-5-5 default | NOT RUN
cell: task b sonnet-5-5 default | NOT RUN
cell: task c haiku-5-5 highest accepted effort | NOT RUN
cell: task c haiku-5-5 default | NOT RUN
cell: task c sonnet-5-5 default | NOT RUN
cell: task d haiku-5-5 highest accepted effort | NOT RUN
cell: task d haiku-5-5 default | NOT RUN
cell: task d sonnet-5-5 default | NOT RUN
cell: task b Copilot CLI 1.0.98 (`copilot -p --allow-all-tools`, no `--model`) | quality: NOT GRADED (blind grader needs claude) | check: PASS (RED on the assertion `assert 5 == 0`; green under the reference fix; only the new test file added) | USD: UNVERIFIED (reports "AI Credits 17.32", not USD) | tokens: up 290.2k (237.5k cached, 52.6k written), down 1.8k (93 reasoning) | wall: 25.0 s | served model: UNVERIFIED (the CLI names none)

## Per task: cheapest cell that passed

- a READ: UNVERIFIED (no cell ran)
- b RED test: Copilot CLI passed the deterministic check; its cost is not in USD, so "cheapest" is UNVERIFIED
- c fix to green: UNVERIFIED
- d VERDICT: UNVERIFIED

## PROPOSED role -> model + effort

No proposal is made: a row without a measured cell would be an estimate.

role: read-only fan-out | model/effort: UNVERIFIED | evidence: none (task a not run)
role: RED tests | UNVERIFIED | evidence: only the Copilot cell ran (check PASS, quality ungraded, cost not in USD)
role: implement | UNVERIFIED | evidence: none (task c not run)
role: verify | UNVERIFIED | evidence: none
role: review-prep | UNVERIFIED | evidence: none (task d not run)
Haiku highest accepted effort | UNVERIFIED (see `facts/NOTES.md`)

## Contract defects found (DECIDED-BY-LANE)

- Task c premise: `[#1350]` is **already fixed at the base sha** (`a9ae5280`, in `d8aa4dd7`'s history): `_DestinationLock.__enter__`
  catches `(FileExistsError, PermissionError)`, so a test written for the stated behaviour cannot be RED on base. The task row's
  `:193` locator is also stale (the lock is at `scripts/transport.py:323-360`). Decision, by the Value line (a measured fix-to-green
  cell): the cell's clone is re-seeded with the **pre-fix** lock (`tasks/c_fix/seed.patch` = the reverse of that hunk, committed
  with the RED test as the clone's HEAD), so the cell still edits `scripts/transport.py` only. Validated: RED on the seeded
  clone; green with the original fix (5 changed lines); `tests/test_transport.py` green.
- Step 0 claim: `claim.py claim LANE-dz-0-m1-model-probe` exit 2, "CLAUDE_PROMPTS_DIR is not set"; with
  `--transport-root /workspaces/dispatch`, "to-cc does not exist; refusing to create it". Exit 2 is an environment fault,
  not contention (exit 3); this Codespace has no `to-cc` transport. No marker was written. The lane branch/worktree was created
  fresh with `git worktree add -b`, which would have failed had another session held the name.
- `to-browser/` is not a tracked path in this checkout, so the handback is `SESSION-lane-dz-0-m1-model-probe.md` in this
  directory (an owned path), plus the structured handback.

## OPERATOR-ACTION

Put a Claude login in the lane's tool environment (the runner's `CLAUDE_CODE_OAUTH_TOKEN`, or `claude /login` on the box), then from this
directory run: step 1 facts (12 one-liners, see `facts/NOTES.md` for the shape), then `python3 probe.py cell <a|b|c|d> <label> <model> <effort|default>`
for each of the 12 cells (labels `<task>-haiku-hi`, `<task>-haiku-def`, `<task>-sonnet-def`), then `python3 probe.py grade`, then fill the tables above.
`probe.py ledger` prints the running sum and the driver refuses to start a cell at USD 8.
